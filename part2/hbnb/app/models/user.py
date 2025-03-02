from app.models.basecls import BaseModel
from email_validator import validate_email, EmailNotValidError

class User(BaseModel):
    """
    User model class that inherits from BaseModel.
    Represents a user with first name, last name, email, and admin status.
    """

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize a User instance.

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            email (str): The email of the user.
            is_admin (bool): The admin status of the user. Defaults to False.
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.__is_admin = is_admin
        self._places = []

    def add_place(self, place):
        """
        Add a place to the user's list of places.

        Args:
            place (Place): The place to add.
        """
        self._places.append(place)

    @property
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

    @property
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

    @property
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

    @property
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

    @property
    def is_admin(self):
        """
        Get the admin status of the user.

        Returns:
            bool: The admin status of the user.
        """
        return self.__is_admin
