from flask import Blueprint, request, make_response

project_page_bp = Blueprint('project-page', __name__)
"""Blueprint for api requests related to a project's page.
"""


@project_page_bp.post('/project/<uuid:projectid>/authorize-user')
def __authorize_user(projectid: str):
    """Receive an authorize user request.

    Verify that this request comes from the admin and that the user exists.
    :return: json response detailing success or failure of authorizing user access
    """

    # Verify that this request comes from the admin
    # project = project_collection.find(projectid)
    # if not project.is_admin(request.authorizer):
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


@project_page_bp.post('/project/<uuid:projectid>/revoke-user')
def __revoke_user(projectid: str):
    """Receive a revoke user request.

    Verify that this request comes from the admin and that the user is currently authorized.
    :return: json response detailing success or failure of revoking user access
    """

    # Verify that this request comes from the admin
    # project = project_collection.find(projectid)
    # if not project.is_admin(request.authorizer):
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
