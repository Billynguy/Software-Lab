from flask import Flask, send_from_directory
import os
import atexit


# Entry point
def create_app():
    app = Flask(__name__, static_url_path='', static_folder='frontend/build/')

    @app.route('/', defaults={'path': ''})
    @app.route('/<string:path>')
    @app.route('/<path:path>')
    def catch_all(path):
        return send_from_directory('frontend/build/', 'index.html')

    @app.route('/projects/<string:path>')
    @app.route('/projects/<path:path>')
    def catch_allb(path):
        return send_from_directory('frontend/build/', 'index.html')

    app.secret_key = os.environ["FLASK_SECRET_KEY"]

    # Apply api blueprint, accessed through '/api' prefix
    from api_routes import api_bp
    app.register_blueprint(api_bp)

    return app


@atexit.register
def destroy_app() -> None:
    # Close singleton instance
    from db_manager import DBManager
    DBManager.get_instance().close()
