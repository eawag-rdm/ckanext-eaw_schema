from ckanext.eaw_schema.helpers.get_user import eaw_helpers_geteawuser
from ckan.plugins.toolkit import side_effect_free

@side_effect_free
def eaw_schema_datamanger_show(context, data_dict):
    organization = data_dict.get("organization")
    orga = toolkit.get_action("organization_list")(
        data_dict={
            "organizations": [organization],
            "all_fields": True,
            "include_users": True,
            "include_extras": True,
        }
    )[0]
    datamanager = orga.get("datamanager")
    dmrec = eaw_helpers_geteawuser(datamanager)
    return dmrec
