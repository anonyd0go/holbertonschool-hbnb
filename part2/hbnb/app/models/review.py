from app.models.basecls import BaseModel


class Review(BaseModel):
    """
    Review model class that inherits from BaseModel.
    Represents a review with text, rating, place, and user.
    """

    def __init__(self, text, rating, place, user):
        """
        Initialize a Review instance.

        Args:
            text (str): The text of the review.
            rating (int): The rating of the review (1-5).
            place (Place): The place being reviewed.
            user (User): The user who wrote the review.
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        """
        Get the text of the review.

        Returns:
            str: The text of the review.
        """
        return self._text

    @text.setter
    def text(self, text):
        """
        Set the text of the review.

        Args:
            text (str): The new text of the review.

        Raises:
            TypeError: If the text is not a string.
        """
        if type(text) is not str:
            raise TypeError("Review text must be a str")
        self._text = text

    @property
    def rating(self):
        """
        Get the rating of the review.

        Returns:
            int: The rating of the review.
        """
        return self._rating

    @rating.setter
    def rating(self, rating):
        """
        Set the rating of the review.

        Args:
            rating (int): The new rating of the review (1-5).

        Raises:
            TypeError: If the rating is not an integer.
            ValueError: If the rating is not in the range 1-5.
        """
        if type(rating) is not int:
            raise TypeError("Rating must be an int")
        if rating not in range(1, 6):
            raise ValueError("Rating outside of range (1-5)")
        self._rating = rating

    @property
    def place(self):
        """
        Get the place being reviewed.

        Returns:
            Place: The place being reviewed.
        """
        return self._place

    @place.setter
    def place(self, place):
        """
        Set the place being reviewed.

        Args:
            place (Place): The new place being reviewed.
        """
        self._place = place

    @property
    def user(self):
        """
        Get the user who wrote the review.

        Returns:
            User: The user who wrote the review.
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Set the user who wrote the review.

        Args:
            user (User): The new user who wrote the review.
        """
        self._user = user
