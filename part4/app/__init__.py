from flask import Flask
from app.extensions import bcrypt, jwt, db
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.protected import api as protected_ns
from app.api.v1.admin import api as admin_ns
from app.routes import html
from app.cli import init_app as init_cli  # REMOVE for production


def create_app(config_class="config.DevelopmentConfig"):
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    #this is for SQLite db
    init_cli(app)  #REMOVE for production
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # API namespaces for respective URIs
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(protected_ns, path='/api/v1/protected')
    api.add_namespace(admin_ns, path='/api/v1/admin')

    # Register the HTML Blueprint
    app.register_blueprint(html)

    return app
