from ckanext.eaw_schema.helpers.get_user import (
    generate_search_url,
    generate_staff_profile_picture_url,
    generate_staff_profile_url,
    get_eaw_employee_homepage,
    parse_name,
)

EAWAG_PROFILE_NAME_NORMED = "Christian-Foerster"
EAWAG_ACCOUNT_NAME = "foerstch"


# @pytest.mark.skip(reason="Hardcoded Eawag user name!")
def test_generate_staff_profile_url(request_code):
    assert request_code(generate_staff_profile_url(EAWAG_PROFILE_NAME_NORMED)) == 200


def test_generate_search_url(request_code):
    assert request_code(generate_search_url("Christian Foerster")) == 200


# @pytest.mark.skip(reason="Hardcoded Eawag account name!")
def test_generate_staff_profile_picture_url(request_code):
    assert request_code(generate_staff_profile_picture_url(EAWAG_ACCOUNT_NAME)) == 200


def test_parse_name():
    assert "first-last" == parse_name("Last, First")
    assert "first-last" == parse_name("Last,First")
    assert "first-last1-last2" == parse_name("Last1 Last2, First")
    assert "first-last1-last2" == parse_name("  Last1   Last2,    First  ")


def test_get_eaw_employee_homepage():
    assert generate_search_url("") == get_eaw_employee_homepage(2)

    assert generate_staff_profile_url(
        parse_name("Last, First")
    ) == get_eaw_employee_homepage("Last, First")
