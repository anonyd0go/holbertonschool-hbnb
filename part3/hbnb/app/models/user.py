from app.models.basecls import BaseModel
from app.extensions import bcrypt, db
from email_validator import validate_email
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates


class User(BaseModel):
    """
    User model class that inherits from BaseModel.
    Represents a user with first name, last name, email, password, and admin status.
    Also handles password hashing and validation, and maintains a list of associated places.
    """
    __tablename__ = "users"

    _first_name = db.Column("first_name", db.String(50), nullable=False)
    _last_name = db.Column("last_name", db.String(50), nullable=False)
    _email = db.Column("email", db.String(120), nullable=False, unique=True)
    _password = db.Column("password", db.String(128), nullable=False)
    places = db.relationship('Place', backref='owner', lazy=True)
    _is_admin = db.Column(db.Boolean, default=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password, password)

    @hybrid_property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        self._first_name = first_name

    @validates('_first_name')
    def validate_first_name(self, key, first_name):
        if not isinstance(first_name, str):
            raise TypeError("User first name must be str")
        if len(first_name) > 50:
            raise ValueError("User first name max chars is 50")
        return first_name

    @hybrid_property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        self._last_name = last_name
    
    @validates("_last_name")
    def validate_last_name(self, key, last_name):
        if not isinstance(last_name, str):
            raise TypeError("User last name must be type str")
        if len(last_name) > 50:
            raise ValueError("User last name max chars is 50")
        return last_name

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email
    
    @validates("_email")
    def validate_user_email(self, key, email):
        validated = validate_email(email, check_deliverability=False)
        return validated["email"]

    @hybrid_property
    def is_admin(self):
        return self._is_admin
