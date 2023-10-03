import pytest
from ckan.plugins.toolkit import Invalid

from ckanext.eaw_schema.helpers.general import eaw_schema_human_filesize
from ckanext.eaw_schema.utils.formatting import (
    add_zulu_to_timestamp,
    load_datetime_strings,
)
from ckanext.eaw_schema.validators import output_daterange
from ckanext.eaw_schema.utils.general import (
    error_before_validation,
    format_to_list_of_strings,
)
from ckanext.eaw_schema.validators.date_range import vali_daterange
from ckanext.eaw_schema.validators.other import eaw_schema_multiple_string_convert


def test_error_before_validation():
    assert error_before_validation({}, "abs") == False
    assert error_before_validation({"abc": 222}, "abc")


def test_everything_to_stinglist():
    assert format_to_list_of_strings("abc") == ["abc"]
    assert format_to_list_of_strings((2, "a", ["a"])) == ["(2, 'a', ['a'])"]
    assert format_to_list_of_strings(["adbf", "efdfds", 2]) == ["adbf", "efdfds", "2"]


@pytest.mark.parametrize(
    "ts",
    [
        "2000-11-05T00",
        "2000-11",
        "1605-11-05",
        "2000-11-05T13",
        "-0009",
        "1972-05-20T17",
        "1972-05-20T17:33",
        "1972-05-20T17:33:18.772Z",
    ],
)
def test_fix_timestamp_no_change(ts):
    assert ts == add_zulu_to_timestamp(ts)


@pytest.mark.parametrize("ts", ["1972-05-20T17:33:18", "1972-05-20T17:33:18.772"])
def test_fix_timestamp_change(ts):
    assert ts + "Z" == add_zulu_to_timestamp(ts)


def test_to_list_of_strings():
    assert load_datetime_strings('[2,3,"a"]') == [2, 3, "a"]

    assert load_datetime_strings("a") == ["a"]


@pytest.mark.parametrize(
    "datetime",
    [
        "2000-11-05T00",
        "2000-11",
        "1605-11-05",
        "2000-11-05T13",
        "-0009",
        "[2000-11-01 TO 2014-12-01]",
        "[2014 TO 2014-12-01]",
        "[* TO 2014-12-01]",
        "1972-05-20T17:33:18.772Z",
        "[1972-05-20T17:33:18.772Z TO *]",
    ],
)
def test_vali_daterange(datetime):
    # this test is simply checking no error occurs
    vali_daterange(datetime)


@pytest.mark.parametrize(
    "datetime",
    [
        "2000-11-05T00",
        "2000-11",
        "1605-11-05",
        "2000-11-05T13",
        "-0009",
        "[2000-11-01 TO 2014-12-01]",
        "[2014 TO 2014-12-01]",
        "[* TO 2014-12-01]",
        "1972-05-20T17:33:18.772Z",
        "[1972-05-20T17:33:18.772Z TO *]",
    ],
)
def test_output_daterange(datetime):
    _fomatted = output_daterange(datetime)
    assert "Z" not in _fomatted
    assert "[" not in _fomatted
    assert "[" not in _fomatted


def test_eaw_schema_multiple_string_convert():
    with pytest.raises(KeyError):
        validator = eaw_schema_multiple_string_convert(2)
        validator("")

    with pytest.raises(Invalid):
        validator = eaw_schema_multiple_string_convert("comma")
        validator(2)

    # empty strings allowed why?
    validator = eaw_schema_multiple_string_convert("comma")
    assert validator("") == "[]"

    validator = eaw_schema_multiple_string_convert("comma")

    # TODO: clean formatting only with strings, needs fixing?
    # json input
    assert validator('["a  ", " b"]') == '["a  ", " b"]'  # beahviour unexpected
    # str input
    assert validator("a  ,  b   ") == '["a", "b"]'
    # list input
    assert validator(["a  ,  b   "]) == '["a  ,  b   "]'  # beahviour unexpected


@pytest.mark.parametrize(
    "inp, outp",
    [
        ("", "unknown"),
        ("3", "unknown"),
        ([3], "unknown"),
        (5, "5.0 B"),
        (5 * 10**3, "5.0 KB"),
        (5 * 10**6, "5.0 MB"),
        (5 * 10**9, "5.0 GB"),
        (5 * 10**12, "5.0 TB"),
        (5 * 10**15, "5.0 PB"),
        (5 * 10**18, "5.0 EB"),
        (5 * 10**21, "5.0 ZB"),
        (5 * 10**24, "5.0 YB"),
        (5 * 10**27, "this file is off the scale huge"),
    ],
)
def test_eaw_schema_human_filesize(inp, outp):
    assert eaw_schema_human_filesize(inp) == outp
