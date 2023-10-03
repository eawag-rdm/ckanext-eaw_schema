import datetime

import pytest
from ckan.plugins.toolkit import Invalid

from ckanext.eaw_schema.utils.eaw_schema_set_default import (
    eaw_schema_set_default_invalid_input,
)
from ckanext.eaw_schema.validators.other import (
    eaw_schema_embargodate,
    eaw_schema_publicationlink,
    eaw_schema_striptime,
)


def test_eaw_schema_embargodate():
    assert (
        eaw_schema_embargodate(
            key="time",
            data={"time": datetime.datetime.now()},
            errors={"time": ["some error"]},
            context={},
        )
        is None
    ), "an error is present, function should exit"

    _time = datetime.datetime.now() + datetime.timedelta(days=1)
    _data = {"time": _time}
    eaw_schema_embargodate(key="time", data=_data, errors={"time": []}, context={})
    assert _data["time"] == _time.isoformat() + "Z"

    _errors = {"time": []}
    eaw_schema_embargodate(
        key="time",
        data={"time": datetime.datetime.now() - datetime.timedelta(days=1)},
        errors=_errors,
        context={},
    )
    assert len(_errors["time"]) == 1

    _errors = {"time": []}
    eaw_schema_embargodate(
        key="time",
        data={"time": datetime.datetime.now() + datetime.timedelta(days=1000)},
        errors=_errors,
        context={},
    )
    assert len(_errors["time"]) == 1


@pytest.mark.parametrize(
    "ts",
    [
        "2000-11-05T00",
        "1605-11-05",
        "2000-11-05T13",
        "1972-05-20T17",
        "1972-05-20T17:33",
        "1972-05-20T17:33:18",
        "1972-05-20T17:33:18.772Z",
    ],
)
def test_eaw_schema_striptime_accepted(ts):
    eaw_schema_striptime(ts)


@pytest.mark.parametrize(
    "ts",
    ["2000-11", "-0009", "2000"],
)
def test_eaw_schema_striptime_invalid(ts):
    with pytest.raises(Invalid):
        eaw_schema_striptime(ts)


@pytest.mark.parametrize(
    "pattern,link",
    [
        (
            "fsfas/eawag:26241",
            "https://www.dora.lib4ri.ch/eawag/islandora/object/eawag:26241",
        ),
        (
            "sdff/eawag%3A26241",
            "https://www.dora.lib4ri.ch/eawag/islandora/object/eawag%3A26241",
        ),
        (".sfk/10.1016/j.gca.2022.12.010", "https://doi.org/10.1016/j.gca.2022.12.010"),
    ],
)
def test_eaw_schema_publication_link_valid(pattern, link):
    assert eaw_schema_publicationlink(pattern) == link


def test_eaw_schema_publication_link_invalid():
    with pytest.raises(Invalid):
        assert eaw_schema_publicationlink("incorrect-pattern")


@pytest.mark.parametrize(
    "inp",
    ["", None, [""], [None], ["", None]],
)
def test_eaw_schema_set_default_invalid_input_valid(inp):
    assert not eaw_schema_set_default_invalid_input(inp, "")


@pytest.mark.parametrize(
    "inp",
    ["2", [2], 2.3, 2, (2), (), {}, []],
)
def test_eaw_schema_set_default_invalid_input_invalid(inp):
    assert eaw_schema_set_default_invalid_input(inp, "")
