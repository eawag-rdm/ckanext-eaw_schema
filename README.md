[![Tests](https://github.com/eawag-rdm/ckanext-eaw_schema/workflows/Tests/badge.svg?branch=eric-open)](https://github.com/eawag-rdm/ckanext-eaw_schema/actions)

# ckanext-eaw_schema

This CKAN extension provides the custom configuration for the metadata schemas using a YAML or JSON schema description used in EAWAG Open Data Portal. Custom validation and template snippets for editing and display are supported.
Relevant branches for **ERIC** are `eric` and the branch used for **ERIC Open** is `eric-open`. 

## TODO
Files that need adjusting in **eric-open** branch of **ckanext-eaw_theming** are and might need importing to scheming:

> diff --git a/ckanext/eaw_schema/templates/scheming/display_snippets/eaw_repeating_text.html b/ckanext/eaw_schema/templates/scheming/display_snippets/eaw_repeating_text.html
> ckanext/eaw_schema/templates/scheming/display_snippets/eaw_repeating_text.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/display_snippets/eaw_schema_multiple_string_display.html b/ckanext/eaw_schema/templates/scheming/display_snippets/eaw_schema_multiple_string_display.html
> ckanext/eaw_schema/templates/scheming/display_snippets/eaw_schema_multiple_string_display.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/display_snippets/eaw_select_noi8n.html b/ckanext/eaw_schema/templates/scheming/display_snippets/eaw_select_noi8n.html
> ckanext/eaw_schema/templates/scheming/display_snippets/eaw_select_noi8n.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/__diabled__organization.html b/ckanext/eaw_schema/templates/scheming/form_snippets/__diabled__organization.html
> ckanext/eaw_schema/templates/scheming/form_snippets/__diabled__organization.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/_organization_select.html b/ckanext/eaw_schema/templates/scheming/form_snippets/_organization_select.html
> ckanext/eaw_schema/templates/scheming/form_snippets/_organization_select.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/eaw_schema_date.html b/ckanext/eaw_schema/templates/scheming/form_snippets/eaw_schema_date.html
> ckanext/eaw_schema/templates/scheming/form_snippets/eaw_schema_date.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/eaw_schema_markdown.html b/ckanext/eaw_schema/templates/scheming/form_snippets/eaw_schema_markdown.html
> ckanext/eaw_schema/templates/scheming/form_snippets/eaw_schema_markdown.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/eaw_schema_organization.html b/ckanext/eaw_schema/templates/scheming/form_snippets/eaw_schema_organization.html
> ckanext/eaw_schema/templates/scheming/form_snippets/eaw_schema_organization.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_abstract_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_abstract_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_abstract_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_author_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_author_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_author_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_curator_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_curator_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_curator_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_keywords_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_keywords_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_keywords_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_long_term_archive_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_long_term_archive_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_long_term_archive_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_open_data_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_open_data_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_open_data_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_organization_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_organization_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_organization_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_publicationlink_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_publicationlink_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_publicationlink_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_res_name_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_res_name_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_res_name_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_resource_type_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_resource_type_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_resource_type_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_restricted_level_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_restricted_level_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_restricted_level_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_review_level_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_review_level_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_review_level_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_status_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_status_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_status_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_substances_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_substances_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_substances_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_timerange_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_timerange_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_timerange_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_title_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_title_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_title_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_usage_contact_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_usage_contact_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_usage_contact_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_variables_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_variables_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_variables_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_visibility_help.html b/ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_visibility_help.html
> ckanext/eaw_schema/templates/scheming/form_snippets/modalsnippets/eaw_schema_visibility_help.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/form_snippets/select_short.html b/ckanext/eaw_schema/templates/scheming/form_snippets/select_short.html
> ckanext/eaw_schema/templates/scheming/form_snippets/select_short.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/package/resource_read.html b/ckanext/eaw_schema/templates/scheming/package/resource_read.html
> ckanext/eaw_schema/templates/scheming/package/resource_read.html
> 
> diff --git a/ckanext/eaw_schema/templates/scheming/package/snippets/additional_info.html b/ckanext/eaw_schema/templates/scheming/package/snippets/additional_info.html
> ckanext/eaw_schema/templates/scheming/package/snippets/additional_info.html
> 



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
