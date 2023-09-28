from ckan.plugins import toolkit

HASH_TYPES = ["md5", "sha256"]
MISSING = toolkit.missing

# https://docs.ckan.org/en/2.9/contributing/string-i18n.html#internationalizing-strings-in-python-code
_ = toolkit._
