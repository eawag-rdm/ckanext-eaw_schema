import pytest
from ckan.plugins.toolkit import Invalid

from ckanext.eaw_schema.validators.date_range_solr import SolrDaterange


@pytest.mark.parametrize(
    "date_string",
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
def test_solr_date_range_validation(date_string):
    sdrv = SolrDaterange()
    sdrv.validate(date_string)


def test_solr_data_range_validation_invalid():
    sdrv = SolrDaterange()
    with pytest.raises(Invalid):
        sdrv.validate("2000-11-05T24")
