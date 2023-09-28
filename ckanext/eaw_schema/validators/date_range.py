import json

from ckanext.eaw_schema.utils.formatting import (
    add_zulu_to_timestamp,
    load_datetime_strings,
)
from ckanext.eaw_schema.validators.date_range_solr import SolrDaterange


def vali_daterange(values):
    """
    Initial conversion, 2 possibilities:
    1) <values> is a json representation of a list of DateRange-strings
       (output of validator repeating_text),
    2) <values> is one DateRange-string (output from ordinary text field)

    Both are initially converted to a list of DateRange strings

    Then add some slack to proper format of timerange before submitting
    to real validator:
      + insert trailing "Z" for points in time if necessary
      + add brackets if necessary
    """
    values = load_datetime_strings(values)
    valid_values = []
    for value in values:
        value = value.strip()
        # datetime range
        if "TO" in value:
            start, end = value.strip("[]").split("TO")
            value = f"[{add_zulu_to_timestamp(start.strip())} TO {add_zulu_to_timestamp(end.strip())}]"
        else:
            value = add_zulu_to_timestamp(value)

        valid_values.append(SolrDaterange.validate(value))
    return json.dumps(valid_values)
