from flask import Blueprint, request, url_for

project_selection_bp = Blueprint('project-selection', __name__)
"""Blueprint for api requests related to the project selection page.
"""


@project_selection_bp.get('/open-project')
def __open_project():
    """Receive a project open request.

    Verify that the user has access to the project.
    :return: url redirection to the corresponding project page if valid or the project selection page if invalid
    """

    # Verify that the user has access to the project
    # if request.project in project_collection and project_document.has_user(request.user):
    #     return url_for(f'/project/{request.project}')
    return url_for('/projects')


@project_selection_bp.post('/create-project')
def __create_project():
    """Receive a project creation request.

    Verify that the project information is valid.
    :return: url redirection to the corresponding project page if valid or the project selection page if invalid
    """

    # Verify that the project information is valid.
    # if is_valid_project(request.project):
    #     project = create_project(admin=request.user)
    #     project_collection.add(create_project_document(project))
    #     return url_for(f'/project/{project}')
    return url_for('/projects')
