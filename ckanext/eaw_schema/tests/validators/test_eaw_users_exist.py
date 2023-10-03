import pytest
from ckan.plugins.toolkit import Invalid
from ckan.tests.factories import User

from ckanext.eaw_schema.validators.other import eaw_users_exist


@pytest.mark.usefixtures("with_plugins")
@pytest.mark.usefixtures("clean_db", "with_request_context")
def test_eaw_users_exist_valid():
    users = [User() for i in range(3)]
    for pattern in [", ", " , ", ",", " ,", ",, "]:
        user_str = pattern.join([u["id"] for u in users])
        assert user_str == eaw_users_exist(user_str)

    assert "" == eaw_users_exist("")  # TODO: is this a valid input?


@pytest.mark.usefixtures("with_plugins")
@pytest.mark.usefixtures("clean_db", "with_request_context")
def test_eaw_users_exist_invalid():
    users = [User() for i in range(3)]
    for value in [2, users, [], None, 3.4, max]:
        with pytest.raises(Invalid):
            eaw_users_exist(value)


@pytest.mark.usefixtures("with_plugins")
@pytest.mark.usefixtures("clean_db", "with_request_context")
def test_eaw_users_exist_valid_but_no_users():
    with pytest.raises(Invalid):
        eaw_users_exist("no_users_defined")
