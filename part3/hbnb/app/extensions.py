from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
"""This file contains all the extensions to run the Flask app"""


bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()
