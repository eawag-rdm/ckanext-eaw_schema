import pytest
from ckan.tests.factories import User

from ckanext.eaw_schema.helpers.general import eaw_username_fullname_email


@pytest.mark.usefixtures("with_plugins")
@pytest.mark.usefixtures("clean_db", "with_request_context")
def test_eaw_username_fullname_email_known_users():
    users = [User() for _ in range(3)]
    expected = [f"{u['display_name']} <{u['email']}>" for u in users]

    for pattern in [", ", " , ", ",", " ,", ",, "]:
        users_string = pattern.join(user["id"] for user in users)
        assert expected == eaw_username_fullname_email(users_string)


@pytest.mark.usefixtures("with_plugins")
@pytest.mark.usefixtures("clean_db", "with_request_context")
def test_eaw_username_fullname_email_unknown_users():
    users = [User() for _ in range(3)]
    invalid_ids = ["43sdd", "s4gs333"]
    expected = [f"{iid} <unknown>" for iid in invalid_ids]

    for pattern in [", ", " , ", ",", " ,", ",, "]:
        users_string = pattern.join(invalid_ids)
        assert expected == eaw_username_fullname_email(users_string)


@pytest.mark.usefixtures("with_plugins")
@pytest.mark.usefixtures("clean_db", "with_request_context")
@pytest.mark.parametrize("inp", [None, 2, 2.0, [], {}, (), True])
def test_eaw_username_fullname_email_invalid_inputs(inp):
    with pytest.raises(AttributeError):
        eaw_username_fullname_email(inp)
