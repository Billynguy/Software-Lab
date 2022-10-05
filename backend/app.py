from flask import Flask


# Entry point
def create_app():
    app = Flask(__name__)

    # Example routing
    @app.route('/')
    def index():
        return 'Hello, World!'

    return app
