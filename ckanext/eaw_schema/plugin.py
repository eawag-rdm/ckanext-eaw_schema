import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins.interfaces import IPackageController
from ckanext.eaw_vocabularies.validate_solr_daterange import SolrDaterange
import pylons.config as config
from itertools import count
import json
import logging

logger = logging.getLogger(__name__)

def _json2list(value):
    if isinstance(value, list):
        val = value
    elif isinstance(value, basestring):
        val = [val.strip() for val in value.split(sep) if val.strip()]
    else:
        raise toolkit.Invalid("Only strings or lists allowed")
    val = json.dumps(val)


def vali_daterange(values):
    '''
    Initial conversion, 2 possibilities:
    1) <values> is a json representation of a list of DateRange-strings
       (output of validator repeating_text),
    2) <values> is one DateRange-string (output from ordinary text field)

    Both are initially converted to a list of DateRange strings
    
    Then add some slack to proper format of timerange before submitting
    to real validator:
      + insert trailing "Z" for points in time if necessary
      + add brackets if necessary
    '''
    def _fix_timestamp(ts):
        try:
            fixed = (ts + "Z" if len(ts.split(":")) == 3 and ts[-1] != "Z"
                     else ts)
        except:
            pass
        return fixed
    def _to_list_of_strings(valuestring):
        try:
            values = json.loads(valuestring)
        except ValueError:
            values = [valuestring]
        return(values)
            
    values = _to_list_of_strings(values)
    valid_values = []
    for value in values:
        value = value.strip()
        try:
            timestamps = value.split(" TO ")
        except ValueError:
            pass
        else:
            if len(timestamps) == 2:
                timestamps = [_fix_timestamp(ts) for ts in timestamps]
            value = " TO ".join(timestamps)
            if len(timestamps) == 2 and value[0] != "[" and value[-1] != "]":
                value = "[" + value + "]"
        valid_values.append(SolrDaterange.validate(value))
    valid_values = json.dumps(valid_values)
    return(valid_values)

def output_daterange(values):
    '''
    For display:
      + remove brackets from timerange.
      + remove trailing "Z"  from time-points.
    '''
    def _fix_timestamp(ts):
        return(ts[0:-1] if len(ts.split(":")) == 3 and ts[-1] == "Z" else ts)

    values_out = []
    for value in values:
        value = value.strip("[]")
        try:
            timestamps = value.split(" TO ")
        except ValueError:
                pass
        else:
            value = " TO ".join([_fix_timestamp(ts) for ts in timestamps])
        values_out.append(value)
    return(values_out)

def eaw_schema_multiple_string_convert(typ):
    '''
    Converts a string that represents multiple strings according to
    certain conventions to a json-list for storage. The convention has to 
    be given as parameter for this validator in the schema file
    (e.g. "schema_default.json")
    Currently implemented: typ = pipe ("|" as separator),
                           typ = textbox ("\r\n" as separator)
    '''

    def validator(value):
        sep = {"pipe": "|", "textbox": "\r\n"}[typ]
        if isinstance(value, list):
            val = value
        elif isinstance(value, basestring):
            val = [val.strip() for val in value.split(sep) if val.strip()]
        else:
            raise toolkit.Invalid("Only strings or lists allowed")
        val = json.dumps(val)
        return val
    
    return validator

## Maybe this could be replaced / merged with repeating_text_output.
def eaw_schema_multiple_string_output(value):
    try:
        value = json.loads(value)
    except ValueError:
        raise toolkit.Invalid("String doesn't parse into JSON")
    return value
                  
class Eaw_SchemaPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IPackageController, inherit=True)

    ## The fields that should be indexed as list
    ## a cludge until I figure out how to do that DRY.
    json2list_fields = [
        'substances',
        'variables',
        'systems',
        'timerange',
    ]

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        # toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'eaw_schema')
        
    # IValidators
    def get_validators(self):
        return {"vali_daterange": vali_daterange,
                "output_daterange": output_daterange,
                "eaw_schema_multiple_string_convert":
                    eaw_schema_multiple_string_convert,
                "eaw_schema_multiple_string_output":
                    eaw_schema_multiple_string_output
        }

    # IPackageController
    # 
    def before_index(self, pkg_dict):
        for field in self.json2list_fields:
            val = pkg_dict.get(field)
            if not val:
                continue
            try:
                valnew = json.loads(val)
            except:
                logger.debug("{} doesn't parse as JSON".format(val))
                val1 = json.dumps([repr(val)])
                logger.debug("replacing with {}".format(val1))
                valnew = json.loads(val1)
            if isinstance(valnew, list):
                pkg_dict[field] = valnew
            else:
                raise toolkit.Invalid("{} = {} doesn't parse into list"
                                      .format(field, val))
        return(pkg_dict)
 
