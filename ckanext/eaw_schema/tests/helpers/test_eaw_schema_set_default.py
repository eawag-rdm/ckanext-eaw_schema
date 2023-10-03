from unittest import mock

import pytest
from ckan.plugins.toolkit import Invalid
from ckan.tests.factories import User

from ckanext.eaw_schema.helpers import eaw_schema_set_default


@pytest.mark.usefixtures("with_plugins")
@pytest.mark.usefixtures("clean_db", "with_request_context")
@pytest.mark.parametrize(
    "val, def_val",
    [("2", ""), ([2], ""), (2.3, ""), (2, ""), ((2), ""), ((), ""), ({}, ""), ([], "")],
)
def test_eaw_schema_set_default_invalid_input(val, def_val):
    assert val == eaw_schema_set_default(val, def_val)


def g_mock():
    _g_mock = mock.Mock()
    _g_mock.userobj.fullname = "fullname"
    _g_mock.userobj.email = "email"
    _g_mock.userobj.name = "name"
    return _g_mock


@pytest.mark.usefixtures("with_plugins")
@pytest.mark.usefixtures("clean_db", "with_request_context")
@pytest.mark.parametrize(
    "val, def_val",
    [
        ("", "a"),
        ([""], "a"),
        (["", None], "a"),
        ([None, ""], "a"),
    ],
)
def test_eaw_schema_set_default_valid_input(monkeypatch, val, def_val):
    monkeypatch.setattr("ckan.plugins.toolkit.g", g_mock())
    result = eaw_schema_set_default(val, def_val)
    if isinstance(result, list):
        assert result[0] == def_val
    else:
        assert result == def_val


@pytest.mark.usefixtures("with_plugins")
@pytest.mark.usefixtures("clean_db", "with_request_context")
@pytest.mark.parametrize(
    "val, def_val, res",
    [
        (
            "",
            "context_fullname_email",
            f"{g_mock().userobj.fullname} <{g_mock().userobj.email}>",
        ),
        (None, "context_username", f"{g_mock().userobj.name}"),
    ],
)
def test_eaw_schema_set_default_valid_input(monkeypatch, val, def_val, res):
    """
    Make sure 'toolkit' module is imported at 'eaw_schema_set_default' function location via:
    import ckan.plugins.toolkit as toolkit
    """
    monkeypatch.setattr("ckan.plugins.toolkit.g", g_mock())
    assert res == eaw_schema_set_default(val, def_val)
