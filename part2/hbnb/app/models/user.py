from basecls import BaseModel


class User(BaseModel):
    """
    Set the user who wrote the review.

    Args:
        user (User): The new user who wrote the review.
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
        self.places = []

    def add_place(self, place):
        """
        Add a place to the user's list of places.

        Args:
            place (Place): The place to add.
        """
        self.places.append(place)

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

    # TODO email validation
    @email.setter
    def email(self, email):
        """
        Set the email of the user.

        Args:
            email (str): The new email of the user.
        """
        self._email = email
    
    @property
    def is_admin(self):
        """
        Get the admin status of the user.

        Returns:
            bool: The admin status of the user.
        """
        return self.__is_admin
