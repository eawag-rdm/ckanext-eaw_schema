import datetime
import json

import pytest
from ckan.plugins.toolkit import Invalid

from ckanext.eaw_schema.utils.eaw_schema_set_default import (
    eaw_schema_set_default_invalid_input,
)
from ckanext.eaw_schema.validators.other import (
    eaw_schema_embargodate,
    eaw_schema_publicationlink,
    eaw_schema_striptime,
    eaw_schema_validate_author_format,
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


# --- eaw_schema_validate_author_format tests ---


class TestValidateAuthorFormat:
    def test_valid_first_author_with_email(self):
        value = json.dumps(["Bach, Johann <joe@eawag.ch>"])
        assert eaw_schema_validate_author_format(value) == value

    def test_invalid_first_author_without_email(self):
        value = json.dumps(["Bach, Johann"])
        with pytest.raises(Invalid, match="First author must include email"):
            eaw_schema_validate_author_format(value)

    def test_valid_subsequent_author_without_email(self):
        value = json.dumps(["Bach, Johann <joe@eawag.ch>", "Mozart, Wolfgang"])
        assert eaw_schema_validate_author_format(value) == value

    def test_valid_subsequent_author_with_email(self):
        value = json.dumps(
            ["Bach, Johann <joe@eawag.ch>", "Mozart, Wolfgang <wolf@eawag.ch>"]
        )
        assert eaw_schema_validate_author_format(value) == value

    def test_invalid_subsequent_author_bad_email(self):
        value = json.dumps(
            ["Bach, Johann <joe@eawag.ch>", "Mozart, Wolfgang <bademail>"]
        )
        with pytest.raises(Invalid, match="Author email format invalid"):
            eaw_schema_validate_author_format(value)

    def test_invalid_format_no_comma(self):
        value = json.dumps(["Johann Bach <joe@eawag.ch>"])
        with pytest.raises(Invalid, match="First author must include email"):
            eaw_schema_validate_author_format(value)

    def test_empty_entries_skipped(self):
        value = json.dumps(
            ["Bach, Johann <joe@eawag.ch>", "", "Mozart, Wolfgang"]
        )
        assert eaw_schema_validate_author_format(value) == value

    def test_single_author_with_email(self):
        value = json.dumps(["Bach, Johann <joe@eawag.ch>"])
        assert eaw_schema_validate_author_format(value) == value

    def test_empty_value_returns_early(self):
        assert eaw_schema_validate_author_format("") == ""
        assert eaw_schema_validate_author_format("   ") == "   "

    def test_subsequent_author_no_comma_fails(self):
        value = json.dumps(
            ["Bach, Johann <joe@eawag.ch>", "Wolfgang Mozart"]
        )
        with pytest.raises(Invalid, match="Author format must be"):
            eaw_schema_validate_author_format(value)

    def test_invalid_first_author_email_missing_at(self):
        value = json.dumps(["Bach, Johann <joeeawag.ch>"])
        with pytest.raises(Invalid, match="First author must include email"):
            eaw_schema_validate_author_format(value)

    def test_invalid_first_author_email_missing_closing_bracket(self):
        value = json.dumps(["Bach, Johann <joe@eawag.ch"])
        with pytest.raises(Invalid, match="First author must include email"):
            eaw_schema_validate_author_format(value)

    def test_invalid_first_author_email_empty_brackets(self):
        value = json.dumps(["Bach, Johann <>"])
        with pytest.raises(Invalid, match="First author must include email"):
            eaw_schema_validate_author_format(value)

    def test_invalid_subsequent_author_email_missing_at(self):
        value = json.dumps(
            ["Bach, Johann <joe@eawag.ch>", "Mozart, Wolfgang <wolfeawag.ch>"]
        )
        with pytest.raises(Invalid, match="Author email format invalid"):
            eaw_schema_validate_author_format(value)

    def test_invalid_subsequent_author_email_missing_closing_bracket(self):
        value = json.dumps(
            ["Bach, Johann <joe@eawag.ch>", "Mozart, Wolfgang <wolf@eawag.ch"]
        )
        with pytest.raises(Invalid, match="Author email format invalid"):
            eaw_schema_validate_author_format(value)

    def test_invalid_first_author_email_no_domain(self):
        value = json.dumps(["Bach, Johann <joe@>"])
        with pytest.raises(Invalid, match="First author must include email"):
            eaw_schema_validate_author_format(value)
