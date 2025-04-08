from app.models.basecls import BaseModel
from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates


class Review(BaseModel):
    """
    Review model class that inherits from BaseModel.

    Represents a review for a place written by a user. Contains text and a numeric rating.
    Also stores foreign keys to link a review to a specific Place and User.
    
    Attributes:
        _text (Text): The text content of the review.
        _rating (Integer): The numeric rating for the review (between 1 and 5).
        place_id (str): Foreign key linking the review to a Place.
        user_id (str): Foreign key linking the review to a User.
    """
    __tablename__ = "reviews"

    _text = db.Column("text", db.Text, nullable=False)
    _rating = db.Column("rating", db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    @hybrid_property
    def text(self):
        """
        Get the text of the review.

        Returns:
            str: The text content of the review.
        """
        return self._text

    @text.setter
    def text(self, text):
        """
        Set the text of the review.

        Args:
            text (str): The new text content for the review.
        """
        self._text = text
    
    @validates("_text")
    def validate_review_text(self, key, text):
        """
        Validate the review text ensuring it is a non-empty string.

        Args:
            key (str): The attribute key.
            text (str): The review text to validate.

        Returns:
            str: The validated review text.

        Raises:
            TypeError: If the text is not a string.
            ValueError: If the text is empty.
        """
        if not isinstance(text, str):
            raise TypeError("Review text must be a str")
        if not text.strip():
            raise ValueError("Review text cannot be empty")
        return text

    @hybrid_property
    def rating(self):
        """
        Get the rating of the review.

        Returns:
            int: The numeric rating.
        """
        return self._rating

    @rating.setter
    def rating(self, rating):
        """
        Set the rating for the review.

        Args:
            rating (int): The new rating value.
        """
        self._rating = rating
    
    @validates("_rating")
    def validate_review_rating(self, key, rating):
        """
        Validate the review rating ensuring it is an integer within the range 1 to 5.

        Args:
            key (str): The attribute key.
            rating (int): The rating to validate.

        Returns:
            int: The validated rating.

        Raises:
            TypeError: If the rating is not an integer.
            ValueError: If the rating is not in the range 1 to 5.
        """
        if not isinstance(rating, int):
            raise TypeError("Rating must be an int")
        if rating not in range(1, 6):
            raise ValueError("Rating outside of range (1-5)")
        return rating
