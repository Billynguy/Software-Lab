from flask import Blueprint, redirect, make_response, session

user_bp = Blueprint('user', __name__)
"""Blueprint for api requests related to user information.
"""


@user_bp.get('/sign-out')
def __user_sign_out():
    """Sign out the user.

    Clear the session user.
    :return: url redirection to login page
    """

    session.clear()
    return redirect('/login')


@user_bp.get('/user/<uuid:userid>/user-info')
def __user_get_user_info(userid: str):
    """Get the user's username and userid.

    Session user must have permission.
    We make all types of errors look identical to make it harder to reverse engineer.
    :return: json response with data containing username and userid if session user has permission or 404 error if not
    """

    # Verify that the session user has permission (session user must be the same user)
    if session['userid'] != userid:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Unable to get user information.',
            }
        }, 404)

    # user = get_user_collection().get_user(userid)
    # if user is None:
    #     return make_response({
    #         'status': {
    #             'success': False,
    #             'reason': 'Unable to get user information.',
    #         }
    #     }, 404)

    # return make_response({
    #     'status': {
    #         'success': True,
    #     },
    #     'data': {
    #         'username': user.get_username(),
    #         'userid': user.get_userid(),
    #     }
    # }, 200)


@user_bp.get('/user/<uuid:userid>/project-list')
def __user_get_projects(userid: str):
    """Get the user's list of projects.

    Session user must have permission.
    We make all types of errors look identical to make it harder to reverse engineer.
    :return: json response with data containing projectid if session user has permission or 404 error if not
    """

    # Verify that the session user has permission (session user must be the same user)
    if session['userid'] != userid:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Unable to get user information.',
            }
        }, 404)

    # user = get_user_collection().get_user(userid)
    # if user is None:
    #     return make_response({
    #         'status': {
    #             'success': False,
    #             'reason': 'Unable to get user information.',
    #         }
    #     }, 404)

    # return make_response({
    #     'status': {
    #         'success': True,
    #     },
    #     'data': {
    #         'projects': user.get_project_list()
    #     }
    # }, 200)
