import pytest

from ckanext.eaw_schema.helpers.general import eaw_schema_clean_citation

DATACITE_404 = (
    '{"errors":[{"status":"404","title":"The resource you are looking for '
    "doesn't exist.\"}]}"
)
CROSSREF_404 = '{"status":"error","message-type":"route-not-found"}'
CITATION = (
    "Förster, C., &amp; Eawag RDM (2026). <i>Lake Greifensee nutrient "
    "monitoring 2019&ndash;2025</i> (Version 1.0) [Data set]. Eawag. "
    "https://doi.org/10.25678/000HD2"
)


@pytest.mark.parametrize(
    "value",
    [None, "", " ", "   ", "\t", "\n", "  \n\t ", 2, 2.0, True, [], {}, ()],
)
def test_eaw_schema_clean_citation_empty_inputs(value):
    assert eaw_schema_clean_citation(value) is None


@pytest.mark.parametrize(
    "value",
    [
        DATACITE_404,
        CROSSREF_404,
        "  " + DATACITE_404 + "\n",
        '{"errors": [{"status": "404", "title": "Reworded by DataCite"}]}',
        "{}",
        "[]",
        '["not a citation"]',
    ],
)
def test_eaw_schema_clean_citation_json_payloads(value):
    """Any parseable JSON object or array in a citation field is an API
    payload, not a citation -- matching on the error text would break the
    moment DataCite rewords it."""
    assert eaw_schema_clean_citation(value) is None


@pytest.mark.parametrize(
    "value,expected",
    [
        (CITATION, CITATION),
        ("  " + CITATION + "  ", CITATION),
        # numbered styles start with "[" but are not JSON
        (
            "[1] Doe, J. (2026). A paper. Water Research, 251, 121043.",
            "[1] Doe, J. (2026). A paper. Water Research, 251, 121043.",
        ),
        # a citation may legitimately open with a brace-quoted title
        ("{Anon}. (2026). Untitled dataset.", "{Anon}. (2026). Untitled dataset."),
    ],
)
def test_eaw_schema_clean_citation_keeps_real_citations(value, expected):
    assert eaw_schema_clean_citation(value) == expected


def test_eaw_schema_clean_citation_preserves_markup():
    """The template renders the result with |safe, so the markup a real
    citation carries must survive byte-identically."""
    assert "<i>" in eaw_schema_clean_citation(CITATION)
