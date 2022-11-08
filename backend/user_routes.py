from flask import Blueprint, make_response, session, redirect, request
from user import User

user_bp = Blueprint('user', __name__)
"""Blueprint for api requests related to users.
"""

"""User operations.
"""


@user_bp.post('/sign-in')
def user_sign_in():
    """Sign in the user.

    Verify that the sign-in information is valid.
    In this implementation, the front-end has to handle redirection by using, for example: `window.location = ...`.
    :return: json response for front-end to handle
    """

    # # Verify that the sign-in information is valid
    user = User.load_user(request.form['userid'])
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
def user_sign_up():
    """Sign up a new account.

    Verify that the sign-up information is valid.
    In this implementation, the front-end has to handle redirection by using, for example: `window.location = ...`.
    :return: json response for front-end to handle
    """

    # Verify that the sign-up information is valid
    if User.load_user(request.form['userid']) is not None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Could not sign up.',
            }
        }, 405)

    # TODO: Encrypt password
    # Note: Inserts new document into database
    User.new_user(request.form['username'], request.form['userid'], request.form['password'])

    session.clear()
    session['userid'] = request.form['userid']
    return make_response({
        'status': {
            'success': True,
        },
        'data': {
            'userid': request.form['userid'],
        }
    }, 201)


@user_bp.get('/sign-out')
def user_sign_out():
    """Sign out the user.

    Clear the session user.
    :return: url redirection to login page
    """

    session.clear()
    return redirect('/login')


"""User information.
"""


@user_bp.get('/user/<string:userid>/user-info')
def user_get_user_info(userid: str):
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

    user = User.load_user(userid)
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


@user_bp.get('/user/<string:userid>/project-list')
def user_get_projects(userid: str):
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

    user = User.load_user(userid)
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


@user_bp.get('/user/session-user-info')
def user_get_session_user_info():
    """Get the session user's username and userid.

    We make all types of errors look identical to make it harder to reverse engineer.
    :return: json response with data containing username and userid or 404 error
    """

    user = User.load_user(session['userid'])
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


@user_bp.get('/user/session-project-list')
def user_get_session_projects():
    """Get the session user's list of projects.

    We make all types of errors look identical to make it harder to reverse engineer.
    :return: json response with data containing projectid or 404 error
    """

    user = User.load_user(session['userid'])
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
