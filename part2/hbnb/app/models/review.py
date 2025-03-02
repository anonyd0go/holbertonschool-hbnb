from app.models.basecls import BaseModel


class Review(BaseModel):
    """
    Review model class that inherits from BaseModel.
    Represents a review with text, rating, place, and user.
    """

    def __init__(self, text, rating, place_id, user_id):
        """
        Initialize a Review instance.

        Args:
            text (str): The text of the review.
            rating (int): The rating of the review (1-5).
            place_id (str): The ID of the place being reviewed.
            user_id (str): The ID of the user who wrote the review.
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

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
        if not text.strip():
            raise ValueError("Review text cannot be empty")
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
    def place_id(self):
        """
        Get the ID of the place being reviewed.

        Returns:
            str: The ID of the place being reviewed.
        """
        return self._place_id

    @place_id.setter
    def place_id(self, place_id):
        """
        Set the ID of the place being reviewed.

        Args:
            place_id (str): The new ID of the place being reviewed.

        Raises:
            TypeError: If the place_id is not a string.
        """
        if not isinstance(place_id, str):
            raise TypeError("Review place_id must be a str")
        self._place_id = place_id

    @property
    def user_id(self):
        """
        Get the ID of the user who wrote the review.

        Returns:
            str: The ID of the user who wrote the review.
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Set the ID of the user who wrote the review.

        Args:
            user_id (str): The new ID of the user who wrote the review.

        Raises:
            TypeError: If the user_id is not a string.
        """
        if not isinstance(user_id, str):
            raise TypeError("Review user_id must be a str")
        self._user_id = user_id
