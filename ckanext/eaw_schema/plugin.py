import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.eaw_vocabularies.validate_solr_daterange import SolrDaterange
import pylons.config as config
from itertools import count
import json

def vali_daterange(value):
    '''
    Add some slack to proper format of timerange:
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
    return SolrDaterange.validate(value)

def output_daterange(value):
    '''
    For display:
      + remove brackets from timerange.
      + remove trailing "Z"  from time-points.
    '''
    def _fix_timestamp(ts):
        return(ts[0:-1] if len(ts.split(":")) == 3 and ts[-1] == "Z" else ts)

    value = value.strip("[]")
    try:
        timestamps = value.split(" TO ")
    except ValueError:
            pass
    else:
        value = " TO ".join([_fix_timestamp(ts) for ts in timestamps])
    return(value)

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
        print repr("VALIDATOR: GOT {} ({})".format(value, type(value)))

        sep = {"pipe": "|", "textbox": "\r\n"}[typ]
        print "SEP: {}".format(sep)
        

        ## if pipe-separated string, parse into list first
        if isinstance(value, list):
            val = value
        elif isinstance(value, basestring):
            val = [val.strip() for val in value.split(sep) if val.strip()]
        else:
            raise toolkit.Invalid("Only strings or lists allowed")
        val = json.dumps(val)
        print "VALIDATOR: RET {} ({})".format(val, type(value))
        return val
    
    return validator
    
def eaw_schema_multiple_string_output(value):
    try:
        value = json.loads(value)
    except ValueError:
        raise toolkit.Invalid("String doesn't parse into JSON")
    return value
                  
class Eaw_SchemaPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IValidators)

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

 
