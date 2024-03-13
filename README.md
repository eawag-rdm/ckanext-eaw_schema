[![Tests](https://github.com/eawag-rdm/ckanext-eaw_schema/workflows/Tests/badge.svg?branch=eric-open)](https://github.com/eawag-rdm/ckanext-eaw_schema/actions)

# ckanext-eaw_schema

This CKAN extension provides the custom configuration for the metadata schemas using a YAML or JSON schema description used in EAWAG Open Data Portal. Custom validation and template snippets for editing and display are supported.
Relevant branches for **ERIC** are `eric` and the branch used for **ERIC Open** is `eric-open`. 

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | not tested    |
| 2.7             | not tested    |
| 2.8             | not tested    |
| 2.9             | Yes           |
| 2.10            | partially tested |



## Installation

To install ckanext-eaw_schema:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/eawag-rdm/ckanext-eaw_schema.git
    cd ckanext-eaw_schema
    pip install -e .
	pip install -r requirements.txt

3. Add `eaw_schema` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

The following configurations, also valid for ckanext-scheming, must be present in the production.ini file:


	# For dataset schemas
	scheming.dataset_schemas = ckanext.eaw_schema:eaw_schema_dataset.json
    
    # For group and organization schemas
    scheming.organization_schemas = ckanext.eaw_schema:eaw_schema_organization.json

    # Preset files
    scheming.presets = ckanext.scheming:presets.json ckanext.eaw_schema:presets.json


## Developer installation

To install ckanext-eaw_schema for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/eawag-rdm/ckanext-eaw_schema.git
    cd ckanext-eaw_schema
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-eaw_schema

If ckanext-eaw_schema should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
