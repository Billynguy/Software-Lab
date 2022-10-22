from flask import Blueprint, make_response, session, request
from projects import Projects
from user import User
from hardwareSet import HWSet

project_bp = Blueprint('project', __name__)
"""Blueprint for api requests related to projects.
"""

"""Project operations.
"""


@project_bp.get('/open-project')
def __project_open_project():
    """Receive a project open request.

    Verify that the user has access to the project.
    In this implementation, the front-end has to handle redirection by using, for example: `window.location = ...`.
    :return: json response for front-end to handle
    """

    # Verify that the user has access to the project
    project = Projects.load_project(request.form['projectid'])
    if project is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Could not open project.',
            },
        }, 404)

    if not project.has_user(session['userid']):
        return make_response({
            'status': {
                'success': False,
                'reason': 'Could not open project.',
            },
        }, 404)

    return make_response({
        'status': {
            'success': True,
        },
    }, 200)


@project_bp.post('/create-project')
def __project_create_project():
    """Receive a project creation request.

    Verify that the project information is valid.
    In this implementation, the front-end has to handle redirection by using, for example: `window.location = ...`.
    :return: json response for front-end to handle
    """

    # Verify that the project information is valid.
    # TODO: Generate a projectid (e.g. by uuid)
    projectid = request.form['projectname']
    project = Projects.new_project(projectid, request.form['name'], request.form['description'], session['userid'])
    if project is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Could not create project.',
            },
        }, 405)

    return make_response({
        'status': {
            'success': True,
        },
        'data': {
            'projectid': projectid,
        }
    }, 201)


@project_bp.post('/project/<uuid:projectid>/authorize-user')
def __project_authorize_user(projectid: str):
    """Receive an authorize user request.

    Verify that this request comes from the admin and that the user exists.
    :return: json response detailing success or failure of authorizing user access
    """

    project = Projects.load_project(projectid)
    if project is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Project does not exist.',
            }
        }, 404)

    # Verify that this request comes from the admin
    if project.get_admin() != session['userid']:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Authorize request not from admin.',
            }
        }, 403)

    # Verify that the user exists
    user = User.load_user_by_id(request['userid'])
    if user is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'User does not exist.',
            }
        }, 404)

    # Note: Calls user.add_project()
    project.add_user(user.get_userid())

    return make_response({
        'status': {
            'success': True,
        }
    }, 200)


@project_bp.post('/project/<uuid:projectid>/revoke-user')
def __project_revoke_user(projectid: str):
    """Receive a revoke user request.

    Verify that this request comes from the admin and that the user is currently authorized.
    :return: json response detailing success or failure of revoking user access
    """

    project = Projects.load_project(projectid)
    if project is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Project does not exist.',
            }
        }, 404)

    # Verify that this request comes from the admin
    if project.get_admin() != session['userid']:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Revoke request not from admin.',
            }
        }, 403)

    # Verify that the is currently authorized
    if not project.has_user(request.form['userid']):
        return make_response({
            'status': {
                'success': False,
                'reason': 'User is not authorized.',
            }
        }, 405)

    # Note: Calls user.remove_project()
    project.remove_user(request.form['userid'])

    return make_response({
        'status': {
            'success': True,
        }
    }, 200)


@project_bp.post('/project/<uuid:projectid>/update-resources')
def __project_update_resources(projectid: str):
    """Receive an update resources request.

    Verify that this request comes an authorized user and is valid within constraints.
    :return: json response detailing success or failure of updating resources
    """

    project = Projects.load_project(projectid)
    if project is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Project does not exist.',
            }
        }, 404)

    # Verify that this request comes from an authorized user
    if not project.has_user(session['userid']):
        return make_response({
            'status': {
                'success': False,
                'reason': 'Update request not from authorized user.',
            }
        }, 403)

    # Verify that the request is valid within constraints
    hwsets = project.get_hwsets()
    for hwset_name, hwset_qty in hwsets.items():
        hwset = HWSet.load_hwset(hwset_name)
        old_checked_out = hwset_qty
        new_checked_out = int(request.form[f'{hwset_name}-checkout'])

        if new_checked_out < 0 or new_checked_out - old_checked_out > hwset.get_availability():
            return make_response({
                'status': {
                    'success': False,
                    'reason': 'Invalid resource request.'
                }
            }, 405)

    # Request is ok
    for hwset_name, hwset_qty in hwsets.items():
        hwset = HWSet.load_hwset(hwset_name)
        old_checked_out = hwset_qty
        new_checked_out = int(request.form[f'{hwset_name}-checkout'])

        if new_checked_out > old_checked_out:
            hwset.check_out(projectid, new_checked_out - old_checked_out)
        elif old_checked_out < new_checked_out:
            hwset.check_in(projectid, old_checked_out - new_checked_out)

    return make_response({
        'status': {
            'success': True,
        }
    }, 200)


@project_bp.post('/project/<uuid:projectid>/add-resource')
def __project_add_resource(projectid: str):
    """Receive an add resource request.

    Verify that this request comes from an authorized user and that this resource exists.
    :return: json response detailing success or failure of revoking user access
    """

    project = Projects.load_project(projectid)
    if project is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Project does not exist.'
            }
        }, 404)

    # Verify that this request comes from an authorized user
    if not project.has_user(session['userid']):
        return make_response({
            'status': {
                'success': False,
                'reason': 'Add resource request not from authorized user.',
            }
        }, 403)

    # Verify that the resource exists
    hwset = HWSet.load_hwset(request.form['name'])
    if hwset is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Resource does not exist.',
            }
        }, 404)

    hwset.check_out(projectid, 0)
    return make_response({
        'status': {
            'success': True,
        }
    }, 200)


@project_bp.post('/project/<uuid:projectid>/remove-resource')
def __project_remove_resource(projectid: str):
    """Receive a remove resource request.

    Verify that this request comes from an authorized user and that the project is using 0 of this resource.
    :return: json response detailing success or failure of revoking user access
    """

    # Verify that this request comes from an authorized user


    # project.remove_resource(hwset)
    # return make_response({
    #     'status': {
    #         'success': True,
    #     }
    # }, 200)

    project = Projects.load_project(projectid)
    if project is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Project does not exist.'
            }
        }, 404)

    # Verify that this request comes from an authorized user
    if not project.has_user(session['userid']):
        return make_response({
            'status': {
                'success': False,
                'reason': 'Remove resource request not from authorized user.',
            }
        }, 403)

    # Verify that the resource exists
    hwset = HWSet.load_hwset(request.form['name'])
    if hwset is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Resource does not exist.',
            }
        }, 404)

    # Verify that the project is using this resource
    if not hwset.has_project(projectid):
        return make_response({
            'status': {
                'success': False,
                'reason': 'Resource is not used by the project.',
            }
        }, 404)

    # Verify that the project is using 0 of this resource
    if hwset.get_checked_out(projectid) != 0:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Project is currently using this resource.',
            }
        }, 405)

    hwset.check_out(projectid, 0)
    return make_response({
        'status': {
            'success': True,
        }
    }, 200)


"""Project information.
"""


@project_bp.get('/project/<uuid:projectid>/project-info')
def __project_get_project_info(projectid: str):
    """Get the project's name, projectid, and description.

    Session user must have permission.
    We make all types of errors look identical to make it harder to reverse engineer.
    :return: json response with data containing project name, projectid, and description if session user has permission or 404 error if not
    """

    project = Projects.load_project(projectid)
    if project is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Unable to get project information.',
            }
        }, 404)

    # Verify that the session user has permission (session user must be the same user)
    if not project.has_user(session['userid']):
        return make_response({
            'status': {
                'success': False,
                'reason': 'Unable to get project information.',
            }
        }, 404)

    return make_response({
        'status': {
            'success': True,
        },
        'data': {
            'name': project.get_name(),
            'projectid': project.get_projectid(),
            'description': project.get_description(),
        }
    }, 200)


@project_bp.get('/project/<uuid:projectid>/user-list')
def __project_get_users(projectid: str):
    """Get the project's list of users.

    Session user must have permission.
    We make all types of errors look identical to make it harder to reverse engineer.
    :return: json response with data containing userid if session user has permission or 404 error if not
    """

    project = Projects.load_project(projectid)
    if project is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Unable to get project information.',
            }
        }, 404)

    # Verify that the session user has permission (session user must be the same user)
    if not project.has_user(session['userid']):
        return make_response({
            'status': {
                'success': False,
                'reason': 'Unable to get project information.',
            }
        }, 404)

    return make_response({
        'status': {
            'success': True,
        },
        'data': {
            'users': project.get_users()
        }
    }, 200)


@project_bp.get('/project/<uuid:projectid>/is-session-admin')
def __project_is_admin(projectid: str):
    """Get whether the session user is admin.

    Session user must have permission.
    We make all types of errors look identical to make it harder to reverse engineer.
    :return: json response with data containing whether if session user is admin or 403 error if not
    """

    project = Projects.load_project(projectid)
    if project is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'User is not admin of project.',
            }
        }, 403)

    # Verify that the session user is admin
    if project.get_admin() != session['userid']:
        return make_response({
            'status': {
                'success': False,
                'reason': 'User is not admin of project.',
            }
        }, 403)

    return make_response({
        'status': {
            'success': True,
        },
        'data': {
            'isAdmin': True,
        }
    }, 200)


@project_bp.get('/project/<uuid:projectid>/resources')
def __project_get_resources(projectid: str):
    """Get the project's list of resources corresponding usage information.

    Session user must have permission.
    We make all types of errors look identical to make it harder to reverse engineer.
    :return: json response with data containing resource information if session user has permission or 404 error if not
    """

    project = Projects.load_project(projectid)
    if project is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Unable to get project information.',
            }
        }, 404)

    # Verify that the session user has permission (session user must be the same user)
    if not project.has_user(session['userid']):
        return make_response({
            'status': {
                'success': False,
                'reason': 'Unable to get project information.',
            }
        }, 404)

    hwsets = project.get_hwsets()
    resources = []
    for hwset_name, hwset_qty in hwsets.items():
        resource_info = {
            'name': hwset_name,
        }
        hwset = HWSet.load_hwset(hwset_name)

        if hwset is not None:
            resource_info['availability'] = hwset.get_availability()

            if hwset.has_project(projectid):
                resource_info['checkedOut'] = hwset.get_checked_out(projectid)
            else:
                resource_info['checkedOut'] = 0
                resource_info['unused'] = True

            resources.append(resource_info)
        else:
            resource_info['noSuchObject'] = True

        resources.append(resource_info)

    return make_response({
        'status': {
            'success': True,
        },
        'data': {
            'resources': resources,
        }
    }, 200)
