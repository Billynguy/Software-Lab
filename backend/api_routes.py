from flask import Blueprint, request
from user_routes import user_bp
from project_routes import project_bp
from resource_routes import resource_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')
"""Blueprint for all api-related routes.

All valid api routes are prefixed by the '/api' url prefix
"""


# Apply other modular blueprints within the api blueprint
api_bp.register_blueprint(user_bp)
api_bp.register_blueprint(project_bp)
api_bp.register_blueprint(resource_bp)
