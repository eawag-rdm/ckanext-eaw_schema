from json import loads
from logging import getLogger

import ckan.authz as authz
import ckan.logic
import ckan.logic.auth as logic_auth

# toolkit only worked when imported twice :/
import ckan.plugins.toolkit as tk
from ckan.logic import check_access, side_effect_free
from ckan.logic.action.get import (
    package_search,
    package_show,
    resource_search,
    resource_show,
    resource_view_list,
)

log = getLogger(__name__)

NotFound = ckan.logic.NotFound
_get_or_bust = ckan.logic.get_or_bust


def restricted_get_user_id():
    return tk.c.user


def restricted_check_user_resource_access(user, resource_dict, package_dict):
    """Checks whether user can access resource. Considers 3 levels:
          + public
          + same_organization
          + only_allowed_users
    The latter two are additive: You can give permision to your orga and then
    some more.

    """

    restricted_level = resource_dict.get("restricted_level", "public")
    try:
        # are the allowwed_users in a json-list?
        allowed_users = loads(resource_dict.get("allowed_users", "[]"))
        if not isinstance(allowed_users, list):
            raise
    except:
        # then they better be a comma separated string.
        allowed_users = resource_dict.get("allowed_users", "").split(",")

    # Public resources (DEFAULT)
    if restricted_level == "public":
        return {"success": True}

    # Anonymous can't have access to restricted resources
    if not user:
        return {"success": False, "msg": "No access for anonymous users"}

    if user in allowed_users:
        # User explicitly allowed
        return {"success": True}

    if restricted_level == "only_allowed_users":
        return {"success": False, "msg": "Access restricted to allowed users only"}

    elif restricted_level == "same_organization":
        orga_id = package_dict.get("owner_org")
        data_dict = {"permission": "read", "id": user}
        user_orgs = tk.get_action("organization_list_for_user")(None, data_dict)
        user_orgs = [x.get("id") for x in user_orgs if x.get("id")]

        if orga_id in user_orgs:
            return {"success": True}
        else:
            return {
                "success": False,
                "msg": (
                    "Access restricted to same organization"
                    " ({}) members".format(orga_id)
                ),
            }
    else:
        msg = 'Unknown restriction level: "{}" for resource {}'.format(
            restricted_level, resource_dict.get("id")
        )
        log.error(msg)
        return {"success": False, "msg": msg}


@tk.auth_allow_anonymous_access
def restricted_resource_show(context, data_dict=None):
    # Ensure user who can edit the package can see the resource
    resource = data_dict.get("resource", context.get("resource", {}))
    if not resource:
        resource = logic_auth.get_resource_object(context, data_dict)
    if type(resource) is not dict:
        resource = resource.as_dict()
    if authz.is_authorized(
        "package_update", context, {"id": resource.get("package_id")}
    ).get("success"):
        return {"success": True}

    # custom restricted check
    auth_user_obj = context.get("auth_user_obj", None)
    user_name = ""
    if auth_user_obj:
        user_name = auth_user_obj.as_dict().get("name", "")
    else:
        if authz.get_user_id_for_username(context.get("user"), allow_none=True):
            user_name = context.get("user", "")

    package = data_dict.get("package", {})
    if not package:
        model = context["model"]
        package = model.Package.get(resource.get("package_id"))
        package = package.as_dict()

    return restricted_check_user_resource_access(user_name, resource, package)


@side_effect_free
def restricted_resource_view_list(context, data_dict):
    model = context["model"]
    id = _get_or_bust(data_dict, "id")
    resource = model.Resource.get(id)
    if not resource:
        raise NotFound
    authorized = restricted_resource_show(
        context, {"id": resource.get("id"), "resource": resource}
    ).get("success", False)
    if not authorized:
        return []
    else:
        return resource_view_list(context, data_dict)


@side_effect_free
def restricted_package_show(context, data_dict):
    package_metadata = package_show(context, data_dict)
    # Ensure user who can edit can see the resource
    if authz.is_authorized("package_update", context, package_metadata).get(
        "success", False
    ):
        return package_metadata

    # Custom authorization
    restricted_package_metadata = package_metadata
    restricted_package_metadata["resources"] = _restricted_resource_list_url(
        context, restricted_package_metadata.get("resources", [])
    )

    return restricted_package_metadata


@side_effect_free
def restricted_resource_search(context, data_dict):
    resource_search_result = resource_search(context, data_dict)

    restricted_resource_search_result = {}

    for key, value in list(resource_search_result.items()):
        if key == "results":
            restricted_resource_search_result[key] = _restricted_resource_list_url(
                context, value
            )
        else:
            restricted_resource_search_result[key] = value

    return restricted_resource_search_result


@side_effect_free
def restricted_package_search(context, data_dict):
    package_search_result = package_search(context, data_dict)

    restricted_package_search_result = {}

    for key, value in list(package_search_result.items()):
        if key == "results":
            restricted_package_search_result_list = []
            for package in value:
                restricted_package_search_result_list += [
                    restricted_package_show(context, {"id": package.get("id")})
                ]
            restricted_package_search_result[key] = (
                restricted_package_search_result_list
            )
        else:
            restricted_package_search_result[key] = value

    return restricted_package_search_result


def _restricted_resource_list_url(context, resource_list):
    restricted_resources_list = []
    for resource in resource_list:
        restres = restricted_resource_show(
            context, {"id": resource.get("id"), "resource": resource}
        )
        authorized = restres.get("success", False)
        restricted_resource = dict(resource)
        if not authorized:
            restricted_resource["url"] = "Not Authorized"
        restricted_resources_list += [restricted_resource]
    return restricted_resources_list
