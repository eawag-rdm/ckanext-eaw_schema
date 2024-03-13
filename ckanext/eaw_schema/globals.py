import re
from ckan.plugins import toolkit

HASH_TYPES = ["md5", "sha256"]
MISSING = toolkit.missing

# https://docs.ckan.org/en/2.9/contributing/string-i18n.html#internationalizing-strings-in-python-code
_ = toolkit._


DOI_REGEXP = re.compile("10\.\d+(.\d+)*/.+$", flags=re.I)

