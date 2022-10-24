from flask import Blueprint, make_response, session, redirect, request
from user import User

user_bp = Blueprint('user', __name__)
"""Blueprint for api requests related to users.
"""

"""User operations.
"""


@user_bp.post('/sign-in')
def __user_sign_in():
    """Sign in the user.

    Verify that the sign-in information is valid.
    In this implementation, the front-end has to handle redirection by using, for example: `window.location = ...`.
    :return: json response for front-end to handle
    """

    # # Verify that the sign-in information is valid
    user = User.load_user_by_name(request.form['username'])
    if user is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Could not sign in.',
            }
        }, 404)

    if not user.matches_password(request.form['password']):
        return make_response({
            'status': {
                'success': False,
                'reason': 'Could not sign in.',
            }
        }, 404)

    session.clear()
    session['userid'] = user.get_userid()

    return make_response({
        'status': {
            'success': True,
        },
        'data': {
            'userid': user.get_userid(),
        }
    }, 200)


@user_bp.post('/sign-up')
def __user_sign_up():
    """Sign up a new account.

    Verify that the sign-up information is valid.
    In this implementation, the front-end has to handle redirection by using, for example: `window.location = ...`.
    :return: json response for front-end to handle
    """

    # Verify that the sign-up information is valid
    if User.load_user_by_name(request.form['username']) is not None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Could not sign up.',
            }
        }, 405)

    # Note: Inserts new document into database
    user = User.new_user(request.form['username'], request.form['password'])

    session.clear()
    session['userid'] = user.get_userid()
    return make_response({
        'status': {
            'success': True,
        },
        'data': {
            'userid': user.get_userid(),
        }
    }, 201)


@user_bp.get('/sign-out')
def __user_sign_out():
    """Sign out the user.

    Clear the session user.
    :return: url redirection to login page
    """

    session.clear()
    return redirect('/login')


"""User information.
"""


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

    user = User.load_user_by_id(userid)
    if user is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Unable to get user information.',
            }
        }, 404)

    return make_response({
        'status': {
            'success': True,
        },
        'data': {
            'username': user.get_username(),
            'userid': user.get_userid(),
        }
    }, 200)


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

    user = User.load_user_by_id(userid)
    if user is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Unable to get user information.',
            }
        }, 404)

    return make_response({
        'status': {
            'success': True,
        },
        'data': {
            'projects': user.get_projects()
        }
    }, 200)
