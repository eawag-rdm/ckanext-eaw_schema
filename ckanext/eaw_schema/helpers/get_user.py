import re

import ckan.plugins.toolkit as tk

from ckanext.eaw_schema import logger


def generate_staff_profile_url(normed_name: str):
    return f"https://www.eawag.ch/en/about-us/portrait/organisation/staff/profile/{normed_name}/show/"


def generate_search_url(name: str):
    return f"https://www.eawag.ch/en/suche/?q={name}&tx_solr[filter][0]=filtertype%3A3"


def generate_staff_profile_picture_url(user_name: str):
    return f"https://www.eawag.ch/fileadmin/user_upload/tx_userprofiles/profileImages/{user_name}.jpg"


def parse_name(full_name: str):
    last, first = full_name.split(",")
    return "-".join([re.sub("\s+", "-", s.strip().lower()) for s in [first, last]])


def get_eaw_employee_homepage(full_name):
    "Returns the Eawag homepage of somebody"

    try:
        normed_name = parse_name(full_name)
        return generate_staff_profile_url(normed_name)

    except (ValueError, AttributeError):
        if not isinstance(full_name, str):
            full_name = ""

        logger.warning(
            f'User Fullname "{full_name}" does not have standard format ("lastname, firstname")'
        )

        return generate_search_url(full_name)


def eaw_helpers_geteawuser(username):
    """Returns info about Eawag user:
    + link to picture
    + link to homepage of user
    """
    try:
        userdict = tk.get_action("user_show")(
            context={"keep_email": True}, data_dict={"id": username}
        )
    except:
        return {}

    eawuser = {
        "fullname": userdict.get("fullname"),
        "email": userdict.get("email"),
        "no_of_packages": userdict.get("number_created_packages"),
        "homepage": get_eaw_employee_homepage(userdict.get("fullname")),
        "pic_url": generate_staff_profile_picture_url(username),
    }
    return eawuser
