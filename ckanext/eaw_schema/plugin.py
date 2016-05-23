import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.eaw_vocabularies.validate_solr_daterange import SolrDaterange
import pylons.config as config
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

def eaw_schema_multiple_string(value):
    """
    Accept zero or more values and convert
    to a json list for storage:
    1. a list of strings, eg.:
       ["choice-a", "choice-b"]
    2. a single string for single item selection in form submissions:
       "choice-a"
    """
    print("INPUT VALIDATOR: got {}".format(value))
    value = json.dumps(value.split(","))
    print("INPUT VALIDATOR: returned {}".format(value))
    
    return value

def eaw_schema_multiple_string_output(value):
    
    print("Output validator: got {}".format(value))
    value = json.loads(value)
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
                "eaw_schema_multiple_string": eaw_schema_multiple_string,
                "eaw_schema_multiple_string_output":
                    eaw_schema_multiple_string_output
        }
