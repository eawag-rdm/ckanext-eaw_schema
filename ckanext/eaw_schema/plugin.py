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

def eaw_schema_multiple_string_convert(key, data, errors, context):
    '''Takes a list of values that is a "|"-separated string (in data[key])
    and parses values. These are added to the data dict, enumerated. They
    are also validated.'''

    if isinstance(data[key], basestring):
        val = [val.strip() for val in data[key].split('|') if val.strip()]
    else:
        val = data[key]

    # current_index = max( [int(k[1]) for k in data.keys() if len(k) == 3 and k[0] == 'tags'] + [-1] )

    print("eaw_schema_multiple_string_convert: keys:\n{}".format(data.keys()))
    # print("eaw_schema_multiple_string_convert: current tag-index:\n{}".format(current_index))

    print("val = {}".format(val))
    for num, name in zip(count(0), val):
        print("SUBSTANCE NR: {}".format(num))
        print("SUBSTANCE NAME: {}".format(name))
        data[('substances', num, 'name')] = name
        
    print("eaw_schema_multiple_string_convert: keys CHANGED:\n{}".format(data.keys()))

    


    # for num, val in zip(count(current_index+1), tags):
    #     data[('tags', num, 'name')] = tag

    # for tag in tags:
    #     tag_length_validator(tag, context)
    #     tag_name_validator(tag, context)


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
                "eaw_schema_multiple_string_convert":
                    eaw_schema_multiple_string_convert
        }
