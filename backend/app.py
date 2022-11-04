from flask import Flask
from dotenv import load_dotenv
import os
import atexit


# Entry point
def create_app():
    app = Flask(__name__)

    load_dotenv()
    app.secret_key = os.environ["FLASK_SECRET_KEY"]

    # Example routing
    @app.route('/')
    def index():
        return 'Hello, World!'

    # Apply api blueprint, accessed through '/api' prefix
    from api_routes import api_bp
    app.register_blueprint(api_bp)

    return app


@atexit.register
def destroy_app() -> None:
    # Close singleton instance
    from db_manager import DBManager
    DBManager.get_instance().close()
