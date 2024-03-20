import datetime
import json
import re

import ckan.plugins.toolkit as toolkit
from ckan.lib.helpers import linked_user

from ckanext.eaw_schema import logger
from ckanext.eaw_schema.helpers.get_user import eaw_helpers_geteawuser
from ckanext.eaw_schema.utils.eaw_schema_set_default import (
    eaw_schema_set_default_choose_default,
    eaw_schema_set_default_invalid_input,
    eaw_schema_set_default_set_values,
)


# TODO: tests
def eaw_schema_get_values(field_name, form_blanks, data):
    """
    Get data from repeating_text-field from either field_name (if the
    field comes from the database) or construct from several field-N -
    entries in case data wasn't saved yet, i.e. a validators error occurred.
    In the first case, show additional <form_blanks> empty fields. In the
    latter, don't change the form.

    """

    fields = [re.match(field_name + r"-\d+", key) for key in list(data.keys())]
    if all(f is None for f in fields):
        # not coming from form submit -> get value from DB
        value = data.get(field_name)
        value = value if isinstance(value, list) else [value]
        value = value + [""] * max(form_blanks - len(value), 1)
    else:
        # using form data
        fields = sorted([r.string for r in fields if r])
        value = [data[f] for f in fields if data[f]]
        value = value + [""] * max(form_blanks - len(value), 0)
    return value


def eaw_username_fullname_email(s_users: str):
    """Returns list ["Displayname1 <email1>", "Displayname1 <email1>", ..]
    from string of comma-separated usernames "user1,user2,user3,..."
    """

    def mkfull(user_id):
        try:
            userdict = toolkit.get_action("user_show")(
                context={"keep_email": True}, data_dict={"id": user_id}
            )
        except toolkit.ObjectNotFound:
            userdict = {"display_name": user_id, "email": "unknown"}
        return "{} <{}>".format(
            userdict.get("display_name", "unknown"), userdict.get("email", "unknown")
        )

    l_users = [mkfull(u.strip()) for u in s_users.split(",") if u.strip()]
    return l_users


def eaw_schema_choices_label_noi8n(choices, value):
    """
    This is a modification of h.scheming_choices_label that doesn't
    translate the value. Used in display_snippet eaw_select_noi8n.html.

    :param choices: choices list of {"label": .., "value": ..} dicts
    :param value: value selected
    Return the label from choices with a matching value, or
    the value passed when not found. Result is passed through
    scheming_language_text before being returned.

    """
    for c in choices:
        if c["value"] == value:
            return c.get("label", value)
    return value


def eaw_schema_get_citationurl(typ, doi):
    types = {
        "ris": "application/x-research-info-systems",
        "bibtex": "application/x-bibtex",
        "datacitexml": "application/vnd.datacite.datacite+xml",
        "citeproc": "application/vnd.citationstyles.csl+json",
    }
    if not types.get(typ):
        return "#"
    doi = re.sub("^https?://(dx\.)?doi\.org/", "", doi)
    url = "https://data.datacite.org/{}/{}".format(types[typ], doi)
    return url


def eaw_schema_human_filesize(size, suffix="B"):
    "Returns human-friendly string for filesize (bytes -> decmal prefix)"
    if not size or not (isinstance(size, float) or isinstance(size, int)):
        return "unknown"
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z", "Y"]:
        if abs(size) < 1000.0:
            return "{:3.1f} {}{}".format(size, unit, suffix)
        size /= 1000.0
    return "this file is off the scale huge"


## TODO: tests!
def eaw_theme_get_spatial_query_default_extent():
    extent_s = toolkit.config.get("ckanext.eaw_theme.spatial_query_default_extent")
    try:
        return json.loads(extent_s)
    except:
        logger.warning(
            "The variable 'ckanext.eaw_theme.spatial_query_default_extent' is not defined correctly. This is a valid form: [[-40.0, -20.], [60.0, 20.]]"
        )
        return [[-40.0, -20.0], [60.0, 20.0]]


## TODO: tests!
def eaw_theme_get_default_dataset_type(organization_id):
    """Returns the [default] dataset type of an organization"""
    default_pkg_type = toolkit.get_action("organization_show")(
        data_dict={
            "id": organization_id,
            "include_extras": True,
            "include_users": False,
            "include_groups": False,
            "include_tags": False,
            "include_followers": False,
        }
    ).get("default_package_type", "dataset")
    return default_pkg_type


## TODO: tests!
def eaw_theme_patch_activity_actor(actor):
    """Patches an activity_item actor string to replace the
    image source at gravatar.com with the Eawag picture.
    """
    new_user_name = re.search(r'<a\s*href="/user/(.*?)"\s*>', actor, flags=re.S)

    if new_user_name is None:
        new_user_name = "unknown user"
        logger.warning("faild to extract username")
    else:
        new_user_name = new_user_name.group(1)

    eaw_user_data = eaw_helpers_geteawuser(new_user_name)
    eaw_user_pic = eaw_user_data.get("pic_url", "")

    if not eaw_user_pic:
        logger.warning("Could not find Eawag user picture")

    return re.sub(
        r"<\s*img\s*.*?/\s*>",
        f'<img src="{eaw_user_pic}" width="30px height="30px"/>',
        actor,
        flags=re.S,
    ).unescape()


## TODO: tests!
def eaw_theme_patch_linked_user(user, maxlength=0, avatar=20):
    res = linked_user(user, maxlength=0, avatar=20)
    # Get the username in case <user> is the id
    user_name = toolkit.get_action("user_show")(data_dict={"id": user})["name"]
    eaw_user_data = eaw_helpers_geteawuser(user_name)
    eaw_user_pic = eaw_user_data.get("pic_url", "")

    if not eaw_user_pic:
        logger.warning("Could not find Eawag user picture")

    res = toolkit.literal(
        re.sub('src="[^"]*?"', f'src="{eaw_user_pic}"', res, flags=re.S)
    )

    return toolkit.literal(res)


# TODO: check if empty list is an invalid or valid input, for now set to invalid
def eaw_schema_set_default(values, default_value, field=""):
    ## Only set default value if current value is empty string or None
    ## or a list containing only '' or None.
    if eaw_schema_set_default_invalid_input(values, default_value):
        return values

    val = eaw_schema_set_default_choose_default(default_value)

    # deal with list/string - duality
    values = eaw_schema_set_default_set_values(values, val)

    return values


def eaw_schema_embargo_interval(interval_in_days):
    """Returns current date and max-date
    according to <interval> in format YYYY-MM-DD.
    """
    now = datetime.date.today()
    maxdate = now + datetime.timedelta(days=interval_in_days)
    return {"now": now.isoformat(), "maxdate": maxdate.isoformat()}
