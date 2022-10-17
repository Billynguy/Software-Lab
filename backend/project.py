from flask import Blueprint, redirect, make_response, session

project_bp = Blueprint('project', __name__)
"""Blueprint for api requests related to projects.
"""

"""Project operations.
"""


@project_bp.get('/open-project')
def __project_open_project():
    """Receive a project open request.

    Verify that the user has access to the project.
    :return: url redirection to the corresponding project page if valid or the project selection page if invalid
    """

    # Verify that the user has access to the project
    # if request.project in project_collection and project_document.has_user(session['userid']):
    #     return redirect(f'/project/{request.project}')
    return redirect('/projects')


@project_bp.post('/create-project')
def __project_create_project():
    """Receive a project creation request.

    Verify that the project information is valid.
    :return: url redirection to the corresponding project page if valid or the project selection page if invalid
    """

    # Verify that the project information is valid.
    # if is_valid_project(request.project):
    #     project = create_project(admin=session['userid'])
    #     project_collection.add(create_project_document(project))
    #     return redirect(f'/project/{project}')
    return redirect('/projects')


@project_bp.post('/project/<uuid:projectid>/authorize-user')
def __project_authorize_user(projectid: str):
    """Receive an authorize user request.

    Verify that this request comes from the admin and that the user exists.
    :return: json response detailing success or failure of authorizing user access
    """

    # Verify that this request comes from the admin
    # project = project_collection.find(projectid)
    # if not project.is_admin(session['userid']):
    return make_response({
        'status': {
            'success': False,
            'reason': 'Authorize request not from admin.',
        }
    }, 403)

    # Verify that the user exists
    # if not user_collection.has(request.user):
    #     return make_response({
    #         'status': {
    #             'success': False,
    #             'reason': 'User does not exist.',
    #         }
    #     }, 404)

    # project.authorize_user(request.user)
    # return make_response({
    #     'status': {
    #         'success': True,
    #     }
    # }, 200)


@project_bp.post('/project/<uuid:projectid>/revoke-user')
def __project_revoke_user(projectid: str):
    """Receive a revoke user request.

    Verify that this request comes from the admin and that the user is currently authorized.
    :return: json response detailing success or failure of revoking user access
    """

    # Verify that this request comes from the admin
    # project = project_collection.find(projectid)
    # if not project.is_admin(session['userid'])
    return make_response({
        'status': {
            'success': False,
            'reason': 'Revoke request not from admin.',
        }
    }, 403)

    # Verify that the user is currently authorized
    # if not project.is_authorized(request.user):
    #     return make_response({
    #         'status': {
    #             'success': False,
    #             'reason': 'User is not authorized.',
    #         }
    #     }, 404)

    # project.revoke_user(request.user)
    # return make_response({
    #     'status': {
    #         'success': True,
    #     }
    # }, 200)


@project_bp.post('/project/<uuid:projectid>/update-resources')
def __project_update_resources(projectid: str):
    """Receive an update resources request.

    Verify that this request comes an authorized user and is valid within constraints.
    :return: json response detailing success or failure of updating resources
    """

    # Verify that this request comes from an authorized user
    # project = project_collection.find(projectid)
    # if not project.is_authorized(session['userid']):
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


@project_bp.post('/project/<uuid:projectid>/add-resource')
def __project_add_resource(projectid: str):
    """Receive an add resource request.

    Verify that this request comes from an authorized user and that this resource exists.
    :return: json response detailing success or failure of revoking user access
    """

    # Verify that this request comes from an authorized user
    # project = project_collection.find(projectid)
    # if not project.is_authorized(session['user']):
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


@project_bp.post('/project/<uuid:projectid>/remove-resource')
def __project_remove_resource(projectid: str):
    """Receive a remove resource request.

    Verify that this request comes from an authorized user and that the project is using 0 of this resource.
    :return: json response detailing success or failure of revoking user access
    """

    # Verify that this request comes from an authorized user
    # project = project_collection.find(projectid)
    # if not project.is_authorized(session['userid']):
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


"""Project information.
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
