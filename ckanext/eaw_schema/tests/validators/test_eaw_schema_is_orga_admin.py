import pytest
from ckan.tests.factories import Organization, User

from ckanext.eaw_schema.validators.other import eaw_schema_is_orga_admin


@pytest.mark.usefixtures("with_plugins")
@pytest.mark.usefixtures("clean_db", "with_request_context")
def test_eaw_schema_is_orga_admin_no_organization():
    user = User()
    key = "some-keyword"
    data = {("name",): "some-non-existant-id", key: user["name"]}
    errors = {key: []}

    eaw_schema_is_orga_admin(key, data, errors, context={})
    assert len(errors[key]) == 0  # No error should be raised


@pytest.mark.usefixtures("with_plugins")
@pytest.mark.usefixtures("clean_db", "with_request_context")
def test_eaw_schema_is_orga_admin_no_user():
    user = User()
    key = "some-keyword"
    data = {("name",): "some-non-existant-id", key: "kevin"}
    errors = {key: []}

    eaw_schema_is_orga_admin(key, data, errors, context={})
    assert len(errors[key]) == 1  # User does not exist
    assert errors[key][0] == f"Username '{data[key]}' does not exist"


@pytest.mark.usefixtures("with_plugins")
@pytest.mark.usefixtures("clean_db", "with_request_context")
def test_eaw_schema_is_orga_admin_with_organization_not_adm():
    user = User()
    key = "some-keyword"
    errors = {key: []}

    orga = Organization(users=[{"name": user["name"], "capacity": "member"}])
    organization_id = orga["id"]
    data = {("name",): organization_id, key: user["name"]}

    eaw_schema_is_orga_admin(key, data, errors, context={})
    assert len(errors[key]) == 1  # User is not an admin of the organization
    assert errors[key][0] == f"Datamanger must be admin of '{organization_id}'"


@pytest.mark.usefixtures("with_plugins")
@pytest.mark.usefixtures("clean_db", "with_request_context")
def test_eaw_schema_is_orga_admin_with_organization_adm():
    user = User()
    key = "some-keyword"
    errors = {key: []}

    orga = Organization(users=[{"name": user["name"], "capacity": "admin"}])
    organization_id = orga["id"]
    data = {("name",): organization_id, key: user["name"]}

    eaw_schema_is_orga_admin(key, data, errors, context={})
    assert len(errors[key]) == 0  # User is an admin of the organization
