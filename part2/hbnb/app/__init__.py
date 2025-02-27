from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/vi/'
    )

    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for places, reviews, and amenities will be added
    api.add_namespace(users_ns, path='/api/v1/users')

    return app
