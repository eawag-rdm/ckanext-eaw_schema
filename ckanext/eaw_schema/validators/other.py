import datetime
import json
import re

from ckan.plugins import toolkit

from ckanext.eaw_schema import logger
from ckanext.eaw_schema.globals import DOI_REGEXP, HASH_TYPES, MISSING, _
from ckanext.eaw_schema.helpers import eaw_schema_embargo_interval
from ckanext.eaw_schema.utils.general import (
    error_before_validation,
    format_to_list_of_strings,
)
from ckanext.scheming.validation import scheming_validator


# TODO: tests!
## If value is a string, and the string can be parsed as json,
## validate only if the encoded value is not empty or None
## Use for json-encoded "repeating"-fields, **after** "repeating_text".
def eaw_schema_json_not_empty(key, data, errors, context):
    if error_before_validation(errors, key):
        return
    value = data.get(key)
    try:
        val = json.loads(value)
    except (TypeError, ValueError):
        logger.warning(
            f"Can't parse {value} (type: {type(value)}) as json -- this should not happen"
        )
        return
    if not val and val != 0:
        errors[key].append(_("Missing value"))
        raise toolkit.StopOnError


# TODO: tests!
def eaw_schema_multiple_string_output(value):
    try:
        value = json.loads(value)
    except ValueError:
        raise toolkit.Invalid("String doesn't parse into JSON")
    return value


# TODO: tests!
def eaw_schema_list_to_commasepstring_output(value):
    l = eaw_schema_multiple_string_output(value)
    if isinstance(l, list):
        ret = ",".join(l)
        return ret
    else:
        raise toolkit.Invalid("String doesn't parse into JSON-list")


# TODO: tests!
@scheming_validator
def eaw_schema_multiple_choice(field, schema):
    """
    Accept zero or more values from a list of choices and convert
    to a json list for storage:

    1. a list of strings, eg.:

       ["choice-a", "choice-b"]

    2. a single string for single item selection in form submissions:

       "choice-a"

    #######################################################################
    HvW - 2016-06-21
    This was copied from ckanext-scheming.validators.
    Amendement:
        A value of <empty string> is ignored (no "unexpected choice"-error).
    We use this to pass (via hidden field, in eaw_multiple_select_js.html)
    an empty string, even if no field is selected, so that the field is
    included in the form data and not populated from the database
    by package.edit().
    #######################################################################
    """
    choice_values = set(c["value"] for c in field["choices"])

    def validator(key, data, errors, context):
        if error_before_validation(errors, key):
            return

        value = data[key]
        if value is not MISSING:
            if isinstance(value, str):
                value = [value]
            elif not isinstance(value, list):
                errors[key].append(_("expecting list of strings"))
                return
        else:
            value = []

        selected = set()
        for element in value:
            if element in choice_values:
                selected.add(element)
                continue
            if element == "":
                continue
            errors[key].append(_('unexpected choice "%s"') % element)

        if not error_before_validation(errors, key):
            data[key] = json.dumps(
                [c["value"] for c in field["choices"] if c["value"] in selected]
            )

            if field.get("required") and not selected:
                errors[key].append(_("Select at least one"))

    return validator


def eaw_schema_is_orga_admin(key, data, errors, context):
    """Validate whether the selected user is admin of the organization.
    Used for setting Datamanager of organizations.

    """
    if error_before_validation(errors, key):
        return
    organization_id = data[("name",)]
    try:
        orga = toolkit.get_action("organization_show")(
            data_dict={"id": organization_id}
        )

    except toolkit.ObjectNotFound:
        # New organization: Just check user exists
        all_users = toolkit.get_action("user_list")(data_dict={})

        allusers = [user.get("name", "") for user in all_users]
        if data[key] not in allusers:
            errors[key].append(_(f"Username '{data[key]}' does not exist"))
    else:
        admin_users = [
            user["name"] for user in orga["users"] if user["capacity"] == "admin"
        ]

        if data[key] not in admin_users:
            errors[key].append(_(f"Datamanger must be admin of '{organization_id}'"))


def eaw_schema_embargodate(key, data, errors, context):
    """Validate embargo is in range [tody, 2 years ahead].
    Add time to be compatible with SOLR ISO_INSTANT
    (https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html#ISO_INSTANT)
    """
    # if there was an error before calling our validator
    # don't bother with our validators
    if error_before_validation(errors, key):
        return
    value = data.get(key, "")

    if value:
        interval = eaw_schema_embargo_interval(interval_in_days=730)
        now = datetime.datetime.strptime(interval["now"], "%Y-%m-%d")
        maxdate = datetime.datetime.strptime(interval["maxdate"], "%Y-%m-%d")
        if value < now:
            errors[key].append("Time-travel not yet implemented.")
            return
        if value > maxdate:
            errors[key].append("Please choose an embargo date within the next 2 years.")
            return
        data[key] = value.isoformat() + "Z"


# eaw_schema_publication_link
def eaw_schema_publicationlink(value):
    if not value:
        return ""

    pattern_result_map = {
        r".*(eawag:\d+$|eawag%3A\d+$)": "https://www.dora.lib4ri.ch/eawag/islandora/object/{}",  # dora match
        # ".*(10.\d{4,9}\/.+$)": "https://doi.org/{}", # doi match
        r".*(10\.\d{4,9}\/.+$)": "https://doi.org/{}",  # doi match
    }

    _match = None
    for pattern, result in pattern_result_map.items():
        _match = re.match(pattern, value)

        if _match:
            return result.format(_match.group(1))

    if not _match:
        raise toolkit.Invalid(f"'{value}' is not a valid publication identifier.")


def eaw_schema_multiple_string_convert(typ):
    """
    Converts a string that represents multiple strings according to
    certain conventions to a json-list for storage. The convention has to
    be given as parameter for this validator in the schema file
    (e.g. "schema_default.json")
    Currently implemented: typ = pipe ("|" as separator),
                           typ = textbox ("\r\n" as separator)
                           typ = comma ("," as separator)
    """

    def validator(value):
        if not isinstance(value, list) and not isinstance(value, str):
            raise toolkit.Invalid("Only strings or lists allowed")

        sep = {"pipe": "|", "textbox": "\r\n", "comma": ","}[typ]

        try:
            if isinstance(json.loads(value), list):
                return value
        except:
            pass

        if isinstance(value, list):
            return json.dumps(value)

        elif isinstance(value, str):
            return json.dumps([val.strip() for val in value.split(sep) if val.strip()])

    return validator


def eaw_schema_striptime(value):
    """
    Strips time (and tz) from ISO date-time string.

    """
    pattern_date = r"^((\d{4})-(\d{2})-(\d{2}))"
    date_match = re.match(pattern_date, value)
    if date_match:
        return date_match.group(1)
    else:
        raise toolkit.Invalid(f"'{value}' is not a valid datetime format.")


# TODO: function allows empty input string; should validator raise error when field empty?
def eaw_users_exist(users_comma_sep):
    """checks whether a list of users (as comma separated string)
    contains only existing usernames.
    """
    if isinstance(users_comma_sep, str):
        users = [user.strip() for user in users_comma_sep.split(",") if user.strip()]
    else:
        raise toolkit.Invalid("{} not a string.".format(repr(users_comma_sep)))
    for user in users:
        try:
            toolkit.get_action("user_show")(data_dict={"id": user})
        except toolkit.ObjectNotFound:
            raise toolkit.Invalid('User "{}" does not exist.'.format(user))
    return users_comma_sep


# TODO: tests
# eaw_schema_cp_filename_to_name
def eaw_schema_cp_filename2name(key, flattened_data, errors, context):
    name_key = ("resources", key[1], "name")
    if flattened_data.get(name_key) is None:
        flattened_data[name_key] = flattened_data[key]


def eaw_schema_check_package_type(pkgtype):
    """Called from organization schema. Returns "dataset"
    if the submitted default package type is not implemented.
    """
    route_new = "{}_new".format(pkgtype)
    if route_new in toolkit.config["routes.named_routes"].keys():
        return pkgtype
    else:
        return "dataset"


def eaw_schema_check_hashtype(hashtype):
    if not hashtype in HASH_TYPES:
        raise toolkit.ValidationError(
            {"hashtype": [_("Hashtype must be one of {}".format(HASH_TYPES))]}
        )
    return hashtype


def eaw_schema_is_doi(value):
    if DOI_REGEXP.match(value):
        return value
    else:
        raise toolkit.Invalid("{} is not a valid DOI".format(value))


def test_before(key, flattened_data, errors, context):
    # Check
    review_level = flattened_data.get(("review_level",))
    reviewed_by = flattened_data.get(("reviewed_by",))
    if review_level != "none" and not reviewed_by:
        raise toolkit.ValidationError({"reviewed_by": [_("Missing value")]})
    elif review_level == "none" and reviewed_by:
        raise toolkit.ValidationError(
            {"reviewed_by": [_('Not empty implies Review Level not "none".')]}
        )


def output_daterange(values):
    """
    For display:
      + remove brackets from timerange.
      + remove trailing "Z"  from time-points.
    """
    # We try to output everything, even "illegal" values.
    values = format_to_list_of_strings(values)
    return [value.strip().strip("[]").replace("Z", "") for value in values]
