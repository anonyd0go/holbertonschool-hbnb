from app.models.basecls import BaseModel
from app.extensions import bcrypt, db
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.ext.hybrid import hybrid_property


class User(BaseModel):
    """
    User model class that inherits from BaseModel.
    Represents a user with first name, last name, email, password, and admin status.
    Also handles password hashing and validation, and maintains a list of associated places.
    """
    __tablename__ = "users"

    # SQLAlchemy columns
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """
        Initialize a User instance.

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            email (str): The email of the user.
            password (str): The plaintext password of the user. Will be hashed and stored.
            is_admin (bool): The admin status of the user. Defaults to False.
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.__is_admin = is_admin
        self._places = []
        self.password = password

    @property
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
        Hash and set the password.

        Args:
            password (str): The plaintext password to hash and set.
        """
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Verify if the provided plaintext password matches the hashed password.

        Args:
            password (str): The plaintext password to verify.
        
        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.check_password_hash(self._password, password)

    def add_place(self, place):
        """
        Add a place to the user's list of places.

        Args:
            place (Place): The place to add.
        """
        self._places.append(place)

    @hybrid_property
    def places(self):
        """
        Get the list of places associated with the user.

        Returns:
            list: The list of places.
        """
        return self._places

    @places.setter
    def places(self, places):
        """
        Set the list of places associated with the user.

        Args:
            places (str or list): A place or a list of places to add.

        Raises:
            TypeError: If the places is not a string or a list of strings.
        """
        if type(places) is str:
            self.add_place(places)
            self._places = self.places
        elif type(places) is list:
            if not all(isinstance(plc, str) for plc in places):
                raise TypeError("User places must be a list of str")
            self._places = self.places + places
        else:
            raise TypeError("User places can only process str or list")

    @hybrid_property
    def first_name(self):
        """
        Get the first name of the user.

        Returns:
            str: The first name of the user.
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """
        Set the first name of the user.

        Args:
            first_name (str): The new first name of the user.

        Raises:
            TypeError: If the first name is not a string.
            ValueError: If the first name is longer than 50 characters.
        """
        if type(first_name) is not str:
            raise TypeError("User first name must be str")
        if len(first_name) > 50:
            raise ValueError("User first name max chars is 50")
        self._first_name = first_name

    @hybrid_property
    def last_name(self):
        """
        Get the last name of the user.

        Returns:
            str: The last name of the user.
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """
        Set the last name of the user.

        Args:
            last_name (str): The new last name of the user.

        Raises:
            TypeError: If the last name is not a string.
            ValueError: If the last name is longer than 50 characters.
        """
        if type(last_name) is not str:
            raise TypeError("User last name must be type str")
        if len(last_name) > 50:
            raise ValueError("User last name max chars is 50")
        self._last_name = last_name

    @hybrid_property
    def email(self):
        """
        Get the email of the user.

        Returns:
            str: The email of the user.
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Set the email of the user.

        Args:
            email (str): The new email of the user.
        """
        if not validate_email(email, check_deliverability=False):
            raise EmailNotValidError
        self._email = email

    @hybrid_property
    def is_admin(self):
        """
        Get the admin status of the user.

        Returns:
            bool: The admin status of the user.
        """
        return self.__is_admin
