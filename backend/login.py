from flask import Blueprint, request, url_for

login_bp = Blueprint('login', __name__)
"""Blueprint for api requests related to the login page.
"""


@login_bp.post('/sign-in')
def __sign_in():
    """Receive a sign-in request.

    Verify that the sign-in information is valid.
    :return: url redirection to the project selection page if valid or the sign-in page if invalid
    """

    # Verify that the sign-in information is valid
    # if request.info in user_collection and user_document.matches(request.info):
    #     return url_for('/projects')
    return url_for('/login')


@login_bp.post('/sign-up')
def __sign_up():
    """Receive a sign-up request.

    Verify that the sign-up information is valid.
    :return: url redirection to the project selection page if valid or the sign-up page if invalid
    """

    # Verify that the sign-up information is valid
    # if request.info not in user_collection:
    #     user_collection.add(create_user_document(request.info))
    #     return url_for('/projects')
    return url_for('/login')
