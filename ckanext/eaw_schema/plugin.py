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
    eaw_schema_get_citationurl,
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
    vali_daterange,
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

    def before_index(self, data_dict):
        data_dict["variables"] = json.loads(data_dict.get("variables", "[]"))
        data_dict["systems"] = json.loads(data_dict.get("systems", "[]"))
        data_dict["substances"] = json.loads(data_dict.get("substances", "[]"))
        data_dict["taxa"] = json.loads(data_dict.get("taxa", "[]"))
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
            "eaw_schema_choices_label_noi8n": eaw_schema_choices_label_noi8n,
            "eaw_schema_get_citationurl": eaw_schema_get_citationurl,
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
        }

    # IActions
    def get_actions(self):
        return {"eaw_schema_datamanger_show": eaw_schema_datamanger_show}
