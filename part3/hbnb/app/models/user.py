from app.models.basecls import BaseModel
from app.extensions import bcrypt, db
from email_validator import validate_email
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates


class User(BaseModel):
    """
    User model class that inherits from BaseModel.

    Represents a user with first name, last name, email, password, and admin status.
    Handles password hashing and validation, and maintains a relationship with Place instances.
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
        """
        Get the hashed password.

        Returns:
            str: The hashed password.
        """
        return self._password

    @password.setter
    def password(self, password):
        """
        Set the password by hashing the plaintext password.

        Args:
            password (str): The plaintext password to hash.
        """
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Verify a plaintext password against the stored hashed password.

        Args:
            password (str): The plaintext password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.check_password_hash(self._password, password)

    @hybrid_property
    def first_name(self):
        """
        Get the user's first name.

        Returns:
            str: The first name.
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """
        Set the user's first name.

        Args:
            first_name (str): The first name.
        """
        self._first_name = first_name

    @validates('_first_name')
    def validate_first_name(self, key, first_name):
        """
        Validate the first name ensuring it is a string and within allowed length.

        Args:
            key (str): The attribute key.
            first_name (str): The first name to validate.

        Returns:
            str: The validated first name.

        Raises:
            TypeError: If first name is not a string.
            ValueError: If first name exceeds 50 characters.
        """
        if not isinstance(first_name, str):
            raise TypeError("User first name must be str")
        if len(first_name) > 50:
            raise ValueError("User first name max chars is 50")
        return first_name

    @hybrid_property
    def last_name(self):
        """
        Get the user's last name.

        Returns:
            str: The last name.
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """
        Set the user's last name.

        Args:
            last_name (str): The last name.
        """
        self._last_name = last_name
    
    @validates("_last_name")
    def validate_last_name(self, key, last_name):
        """
        Validate the last name ensuring it is a string and within allowed length.

        Args:
            key (str): The attribute key.
            last_name (str): The last name to validate.

        Returns:
            str: The validated last name.

        Raises:
            TypeError: If last name is not a string.
            ValueError: If last name exceeds 50 characters.
        """
        if not isinstance(last_name, str):
            raise TypeError("User last name must be type str")
        if len(last_name) > 50:
            raise ValueError("User last name max chars is 50")
        return last_name

    @hybrid_property
    def email(self):
        """
        Get the user's email address.

        Returns:
            str: The email address.
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Set the user's email address.

        Args:
            email (str): The email address.
        """
        self._email = email
    
    @validates("_email")
    def validate_user_email(self, key, email):
        """
        Validate and normalize the user's email address.

        Args:
            key (str): The attribute key.
            email (str): The email address to validate.

        Returns:
            str: The normalized email if valid.

        Raises:
            EmailNotValidError: If the email is not valid.
        """
        validated = validate_email(email, check_deliverability=False)
        return validated["email"]

    @hybrid_property
    def is_admin(self):
        """
        Get the admin status of the user.

        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        return self._is_admin
