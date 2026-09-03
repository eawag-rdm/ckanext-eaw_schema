import json

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.eaw_schema.actions.general import eaw_schema_datamanger_show
from ckanext.eaw_schema.helpers import (
    eaw_helpers_geteawuser,
    eaw_schema_embargo_interval,
    eaw_schema_get_values,
    eaw_schema_human_filesize,
    eaw_schema_set_default,
    eaw_username_fullname_email,
)
from ckanext.eaw_schema.helpers.general import (
    eaw_schema_choices_label_noi8n,
    eaw_schema_clean_citation,
    eaw_schema_get_citationurl,
    eaw_schema_get_paper_citationurl,
)
from ckanext.eaw_schema.validators import (
    eaw_schema_check_hashtype,
    eaw_schema_check_package_type,
    eaw_schema_cp_filename2name,
    eaw_schema_embargodate,
    eaw_schema_is_orga_admin,
    eaw_schema_json_not_empty,
    eaw_schema_list_to_commasepstring_output,
    eaw_schema_multiple_choice,
    eaw_schema_multiple_string_convert,
    eaw_schema_multiple_string_output,
    eaw_schema_publicationlink,
    eaw_schema_striptime,
    eaw_users_exist,
    output_daterange,
    test_before,
    test_before_resources,
    vali_daterange,
    eaw_schema_is_doi,
    eaw_schema_is_doi_optional,
    get_citation_from_doi,
)


class EawSchemaPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IActions)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "eaw_schema")
        # TODO: check if this is this necessary?
        toolkit.add_resource("assets/vendor/bootstrap-switch", "bootstrap-switch")

    def before_dataset_index(self, data_dict):
        for key in ["variables", "systems", "substances", "taxa"]:
            data_dict[key] = json.loads(data_dict.get(key, "[]"))

        return data_dict

    # IValidators
    def get_validators(self):
        return {
            "vali_daterange": vali_daterange,
            "output_daterange": output_daterange,
            "eaw_schema_multiple_string_convert": eaw_schema_multiple_string_convert,
            "eaw_schema_multiple_string_output": eaw_schema_multiple_string_output,
            "eaw_schema_multiple_choice": eaw_schema_multiple_choice,
            "eaw_schema_json_not_empty": eaw_schema_json_not_empty,
            "eaw_schema_is_orga_admin": eaw_schema_is_orga_admin,
            "eaw_schema_embargodate": eaw_schema_embargodate,
            "eaw_schema_publicationlink": eaw_schema_publicationlink,
            "eaw_schema_striptime": eaw_schema_striptime,
            "eaw_schema_list_to_commasepstring_output": eaw_schema_list_to_commasepstring_output,
            "eaw_users_exist": eaw_users_exist,
            "test_before": test_before,
            "eaw_schema_cp_filename2name": eaw_schema_cp_filename2name,
            "eaw_schema_check_package_type": eaw_schema_check_package_type,
            "eaw_schema_check_hashtype": eaw_schema_check_hashtype,
            "eaw_schema_is_doi": eaw_schema_is_doi,
            "eaw_schema_is_doi_optional": eaw_schema_is_doi_optional,
        }

    # ITemplateHelpers
    def get_helpers(self):
        return {
            "eaw_schema_set_default": eaw_schema_set_default,
            "eaw_schema_get_values": eaw_schema_get_values,
            "eaw_schema_geteawuser": eaw_helpers_geteawuser,
            "eaw_schema_embargo_interval": eaw_schema_embargo_interval,
            "eaw_username_fullname_email": eaw_username_fullname_email,
            "eaw_schema_human_filesize": eaw_schema_human_filesize,
            "eaw_schema_get_citationurl": eaw_schema_get_citationurl,
            "eaw_schema_choices_label_noi8n": eaw_schema_choices_label_noi8n,
            "eaw_schema_get_paper_citationurl": eaw_schema_get_paper_citationurl,
            "eaw_schema_clean_citation": eaw_schema_clean_citation,
        }

    # IActions
    def get_actions(self):
        return {"eaw_schema_datamanger_show": eaw_schema_datamanger_show}

    # IPackageController
    def after_dataset_create(self, context, pkg_dict):
        """Generate citations after dataset creation"""
        self._generate_citations_if_needed(pkg_dict)

    def after_dataset_update(self, context, pkg_dict):
        """Generate citations after dataset update"""
        self._generate_citations_if_needed(pkg_dict)

    def _generate_citations_if_needed(self, pkg_dict):
        """Generate citations for DOIs if citation fields are empty"""
        updated = False
        
        # Generate dataset citation from DOI
        doi = pkg_dict.get('doi')
        citation = pkg_dict.get('citation')
        
        if doi and (not citation or citation.strip() == ""):
            generated_citation = get_citation_from_doi(doi)
            if generated_citation:
                pkg_dict['citation'] = generated_citation
                updated = True
        
        # Generate publication citation from paper DOI
        paper_doi = pkg_dict.get('paper_doi')
        citation_publication = pkg_dict.get('citation_publication')
        
        if paper_doi and (not citation_publication or citation_publication.strip() == ""):
            generated_citation = get_citation_from_doi(paper_doi)
            if generated_citation:
                pkg_dict['citation_publication'] = generated_citation
                updated = True
        
        # If we updated citations, save the package
        if updated:
            try:
                toolkit.get_action('package_patch')(
                    {'ignore_auth': True},
                    {
                        'id': pkg_dict['id'],
                        'citation': pkg_dict.get('citation'),
                        'citation_publication': pkg_dict.get('citation_publication')
                    }
                )
            except Exception:
                pass
