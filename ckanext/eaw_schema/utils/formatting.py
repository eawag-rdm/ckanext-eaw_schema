import json


def add_zulu_to_timestamp(ts):
    """Z means “zero hour offset” also known as “Zulu time” (UTC)"""
    if (ts.count(":") == 2) and not ts.endswith("Z"):
        ts += "Z"
    return ts


def load_datetime_strings(datetime_string) -> list:
    try:
        return json.loads(datetime_string)
    except ValueError:
        return [datetime_string]


