# TODO: REMOVE! Function seems unused
def format_to_list_of_strings(values):
    if not isinstance(values, list):
        return [str(values)]

    output = []
    for value in values:
        if isinstance(value, str):
            output.append(value)
        else:
            output.append(repr(value))
    return output


def error_before_validation(errors, key):
    """Check if error occured so that validators can exit early"""
    if errors.get(key, False):
        return True
    return False
