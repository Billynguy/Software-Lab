from flask import Blueprint, request
from login import login_bp
from project_selection import project_selection_bp
from project_page import project_page_bp
from resource_page import resource_page_bp
from user import user_bp
from project import project_bp
from resource import resource_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')
"""Blueprint for all api-related routes.

All valid api routes are prefixed by the '/api' url prefix
"""


# Example get and post routes

@api_bp.get('/get-test')
def _get_test():
    # Send a response to front-end
    return {'string': 'This is a string from the api.'}


@api_bp.get('/post-test')
@api_bp.post('/post-test')
def _post_test():
    if request.method == 'POST':
        # Return a response from a post request
        string = request.form.get('string')

        if string is None:
            return {'response': 'No string was sent.'}
        else:
            return {'response': f'This is your string: "{string}"'}
    else:
        # Create a form to test the post route
        return '''
        <form method="post">
            <input type="text" name="string" />
            <button type="submit">Post form with string</button>
        </form>
        '''


# Apply other modular blueprints within the api blueprint
api_bp.register_blueprint(login_bp)
api_bp.register_blueprint(project_selection_bp)
api_bp.register_blueprint(project_page_bp)
api_bp.register_blueprint(resource_page_bp)
api_bp.register_blueprint(user_bp)
api_bp.register_blueprint(project_bp)
api_bp.register_blueprint(resource_bp)
