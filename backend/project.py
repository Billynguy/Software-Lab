from flask import Blueprint, make_response, session

project_bp = Blueprint('project', __name__)
"""Blueprint for api requests related to project information.
"""


@project_bp.get('/project/<uuid:projectid>/project-info')
def __project_get_project_info(projectid: str):
    """Get the project's name, projectid, and description.

    Session user must have permission.
    We make all types of errors look identical to make it harder to reverse engineer.
    :return: json response with data containing project name, projectid, and description if session user has permission or 404 error if not
    """

    # project = get_project_collection(projectid)
    # if project is None:
    return make_response({
        'status': {
            'success': False,
            'reason': 'Unable to get project information.',
        }
    }, 404)

    # Verify that the session user has permission (session user must be the same user)
    # if not project.has_user(session['userid']):
    #     return make_response({
    #         'status': {
    #             'success': False,
    #             'reason': 'Unable to get project information.',
    #         }
    #     }, 404)

    # return make_response({
    #     'status': {
    #         'success': True,
    #     },
    #     'data': {
    #         'name': project.get_name(),
    #         'projectid': project.get_projectid(),
    #         'description': project.get_description(),
    #     }
    # }, 200)


@project_bp.get('/project/<uuid:projectid>/user-list')
def __project_get_users(projectid: str):
    """Get the project's list of users.

    Session user must have permission.
    We make all types of errors look identical to make it harder to reverse engineer.
    :return: json response with data containing userid if session user has permission or 404 error if not
    """

    # project = get_project_collection(projectid)
    # if project is None:
    return make_response({
        'status': {
            'success': False,
            'reason': 'Unable to get project information.',
        }
    }, 404)

    # Verify that the session user has permission (session user must be the same user)
    # if not project.has_user(session['userid']):
    #     return make_response({
    #         'status': {
    #             'success': False,
    #             'reason': 'Unable to get project information.',
    #         }
    #     }, 404)

    # return make_response({
    #     'status': {
    #         'success': True,
    #     },
    #     'data': {
    #         'users': project.get_user_list()
    #     }
    # }, 200)


@project_bp.get('/project/<uuid:projectid>/is-session-admin')
def __project_is_admin(projectid: str):
    """Get whether the session user is admin.

    Session user must have permission.
    We make all types of errors look identical to make it harder to reverse engineer.
    :return: json response with data containing whether if session user is admin or 403 error if not
    """

    # project = get_project_collection(projectid)
    # if project is None:
    return make_response({
        'status': {
            'success': False,
            'reason': 'User is not admin of project.',
        }
    }, 403)

    # Verify that the session user is admin
    # if not project.is_admin(session['userid']):
    #     return make_response({
    #         'status': {
    #             'success': False,
    #             'reason': 'User is not admin of project.',
    #         }
    #     }, 403)

    # return make_response({
    #     'status': {
    #         'success': True,
    #     }
    # }, 200)


@project_bp.get('/project/<uuid:projectid>/resources')
def __project_get_resources(projectid: str):
    """Get the project's list of resources corresponding usage information.

    Session user must have permission.
    We make all types of errors look identical to make it harder to reverse engineer.
    :return: json response with data containing resource information if session user has permission or 404 error if not
    """

    # project = get_project_collection(projectid)
    # if project is None:
    return make_response({
        'status': {
            'success': False,
            'reason': 'Unable to get project information.',
        }
    }, 404)

    # Verify that the session user has permission (session user must be the same user)
    # if not project.has_user(session['userid']):
    #     return make_response({
    #         'status': {
    #             'success': False,
    #             'reason': 'Unable to get project information.',
    #         }
    #     }, 404)

    # resources = []
    # for resource in get_hwset_collection():
    #     if resource.has_project(project):
    #         resources.append({
    #             'name': resource.get_name(),
    #             'checkedOut': resource.get_checked_out_by(project),
    #             'availability': resource.get_availability(),
    #         })
    # return make_response({
    #     'status': {
    #         'success': True,
    #     },
    #     'data': {
    #         'resources': resources,
    #     }
    # }, 200)
