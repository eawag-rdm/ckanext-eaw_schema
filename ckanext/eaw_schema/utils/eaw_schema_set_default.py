from ckan.plugins import toolkit


def eaw_schema_set_default_invalid_input(values, default_value):
    """
    ## Only set default value if current value is empty string or None
    ## or a list containing only '' or None.
    """
    if isinstance(values, str) or values is None:
        if values not in ["", None]:
            return True
    elif isinstance(values, list):
        if not all([x in ["", None] for x in values]):
            return True
        elif not values:
            return True
    else:
        return True

    return False


def eaw_schema_set_default_choose_default(default_value):
    # special default value resulting in "Full Name <email>"
    default_val_map = {
        "context_fullname_email": f"{toolkit.g.userobj.fullname} <{toolkit.g.userobj.email}>",
        "context_username": toolkit.g.userobj.name,
    }
    return default_val_map.get(default_value, default_value)


def eaw_schema_set_default_set_values(values, val):
    """
    # deal with list/string - duality
    """
    if isinstance(values, list):
        values[0] = val
    else:
        values = val
    return values
