from flask import Blueprint, request, make_response

resource_page_bp = Blueprint('resource-page', __name__)
"""Blueprint for api requests related to a project's resource management page.
"""


@resource_page_bp.post('/project/<uuid:projectid>/update-resources')
def __update_resources(projectid: str):
    """Receive an update resources request.

    Verify that this request comes an authorized user and is valid within constraints.
    :return: json response detailing success or failure of updating resources
    """

    # Verify that this request comes from an authorized user
    # project = project_collection.find(projectid)
    # if not project.is_authorized(request.user):
    return make_response({
        'status': {
            'success': False,
            'reason': 'Update request not from authorized user.',
        }
    }, 403)

    # Verify that the request is valid within constraints
    # for resource in project.get_resources():
    #     old_checked_out = project.get_checked_out(resource)
    #     new_checked_out = request.resource.checkout

    #     if new_checked_out < 0 or new_checked_out - old_checked_out > hwset_collection.get_hwset(resource).get_availability():
    #         return make_response({
    #             'status': {
    #                 'success': False,
    #                 'reason': 'Invalid resource request.'
    #             }
    #         }, 400)

    # for resource in project.get_resources():
    #     old_checked_out = project.get_checked_out(resource)
    #     new_checked_out = request.resource.checkout
    #     hwset = hwset_collection.get_hwset(resource)

    #     if new_checked_out > old_checked_out:
    #         hwset.check_out(new_checked_out - old_checked_out)
    #     elif new_checked_out < old_checked_out:
    #         hwset.check_in(old_checked_out - new_checked_out)

    # return make_response({
    #     'status': {
    #         'success': True,
    #     }
    # }, 200)


@resource_page_bp.post('/project/<uuid:projectid>/add-resource')
def __add_resource(projectid: str):
    """Receive an add resource request.

    Verify that this request comes from an authorized user and that this resource exists.
    :return: json response detailing success or failure of revoking user access
    """

    # Verify that this request comes from an authorized user
    # project = project_collection.find(projectid)
    # if not project.is_authorized(request.user):
    return make_response({
        'status': {
            'success': False,
            'reason': 'Add resource request not from authorized user.',
        }
    }, 403)

    # Verify that the resource exists
    # if not hwset_collection.has(request.resource):
    #     return make_response({
    #         'status': {
    #             'success': False,
    #             'reason': 'Resource does not exist.',
    #         }
    #     }, 404)

    # hwset = hwset_collection.get(request.resource)
    # project.add_resource(hwset)
    # return make_response({
    #     'status': {
    #         'success': True,
    #     }
    # }, 200)


@resource_page_bp.post('/project/<uuid:projectid>/remove-resource')
def __remove_resource(projectid: str):
    """Receive a remove resource request.

    Verify that this request comes from an authorized user and that the project is using 0 of this resource.
    :return: json response detailing success or failure of revoking user access
    """

    # Verify that this request comes from an authorized user
    # project = project_collection.find(projectid)
    # if not project.is_authorized(request.user):
    return make_response({
        'status': {
            'success': False,
            'reason': 'Add resource request not from authorized user.',
        }
    }, 403)

    # Verify that the project is using this resource
    # hwset = hwset_collection.find(request.resource)
    # if not hwset.is_used_by(project):
    #     return make_response({
    #         'status': {
    #             'success': False,
    #             'reason': 'Resource is not used by the project.',
    #         }
    #     }, 404)

    # Verify that the project is using 0 of this resource
    # if hwset.get_checked_out_by(project) != 0:
    #     return make_response({
    #         'status': {
    #             'success': False,
    #             'reason': 'Project is currently using this resource.',
    #         }
    #     }, 400)

    # project.remove_resource(hwset)
    # return make_response({
    #     'status': {
    #         'success': True,
    #     }
    # }, 200)
