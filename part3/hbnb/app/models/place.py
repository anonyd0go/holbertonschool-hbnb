from app.models.basecls import BaseModel
from app.models.place_amenities import place_amenities
from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates


class Place(BaseModel):
    """
    Place model class that inherits from BaseModel.

    Represents a place with various attributes including title, description,
    price, latitude, and longitude. It is related to a User (owner) via a foreign key,
    may have multiple Reviews (one-to-many relationship), and is associated with multiple
    Amenity instances via a many-to-many relationship (through the place_amenities association table).

    Attributes:
        _title (str): Title of the place.
        _description (str): Detailed description of the place.
        _price (float): Price of the place.
        _latitude (float): Latitude coordinate of the place.
        _longitude (float): Longitude coordinate of the place.
        owner_id (str): Foreign key referencing the owner (User) of the place.
        reviews (list[Review]): One-to-many relationship; list of reviews for the place.
        amenities (list[Amenity]): Many-to-many relationship; list of amenity objects associated with the place.
    """
    __tablename__ = "places"

    _title = db.Column("title", db.String(100), nullable=False)
    _description = db.Column("description", db.Text, nullable=False)
    _price = db.Column("price", db.Float, nullable=False)
    _latitude = db.Column("latitude", db.Float, nullable=False)
    _longitude = db.Column("longitude", db.Float, nullable=False)
    owner_id = db.Column("owner_id", db.String(36), db.ForeignKey('users.id'), nullable=False)

    # One-to-many relationship with Review: each place can have multiple reviews.
    reviews = db.relationship("Review", backref="place", lazy=True)

    # Many-to-many relationship with Amenity via the association table.
    amenities = db.relationship(
        "Amenity",
        secondary=place_amenities,
        lazy="subquery",
        backref=db.backref("places", lazy=True)
    )

    @hybrid_property
    def title(self):
        """
        Get the title of the place.

        Returns:
            str: The title of the place.
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Set the title of the place.

        Args:
            title (str): The new title for the place.
        """
        self._title = title
    
    @validates("_title")
    def validate_place_title(self, key, title):
        """
        Validate the title of the place.

        Args:
            key (str): The attribute key.
            title (str): The title to validate.

        Returns:
            str: The validated title.

        Raises:
            TypeError: If title is not a str.
            ValueError: If title is empty or exceeds 100 characters.
        """
        if not isinstance(title, str):
            raise TypeError("Place title must be a str")
        if not title.strip():
            raise ValueError("Place title cannot be empty")
        if len(title) > 100:
            raise ValueError("Place title is longer than 100 chars")
        return title

    @hybrid_property
    def description(self):
        """
        Get the description of the place.

        Returns:
            str: The description of the place.
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Set the description of the place.

        Args:
            description (str): The new description.
        """
        self._description = description
    
    @validates("_description")
    def validate_place_description(self, key, description):
        """
        Validate the description of the place.

        Args:
            key (str): The attribute key.
            description (str): The description to validate.

        Returns:
            str: The validated description.

        Raises:
            TypeError: If description is not a string.
            ValueError: If description is empty.
        """
        if not isinstance(description, str):
            raise TypeError("Place description must be a str")
        if not description.strip():
            raise ValueError("Place description cannot be empty")
        return description

    @hybrid_property
    def price(self):
        """
        Get the price of the place.

        Returns:
            float: The price of the place.
        """
        return self._price

    @price.setter
    def price(self, price):
        """
        Set the price of the place.

        Args:
            price (float|int): The new price.
        """
        self._price = price
    
    @validates("_price")
    def validate_place_price(self, key, price):
        """
        Validate the price of the place.

        Args:
            key (str): The attribute key.
            price (int|float): The price to validate.

        Returns:
            float: The validated price.

        Raises:
            TypeError: If price is not numeric.
            ValueError: If price is negative.
        """
        if not isinstance(price, (int, float)):
            raise TypeError("Place price is not type float")
        if price < 0:
            raise ValueError("Place price must be positive")
        return float(price)

    @hybrid_property
    def latitude(self):
        """
        Get the latitude of the place.

        Returns:
            float: The latitude coordinate.
        """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        """
        Set the latitude of the place.

        Args:
            latitude (float|int): The new latitude.
        """
        self._latitude = latitude
    
    @validates("_latitude")
    def validate_place_latitude(self, key, latitude):
        """
        Validate the latitude of the place.

        Args:
            key (str): The attribute key.
            latitude (float|int): The latitude to validate.

        Returns:
            float: The validated latitude.

        Raises:
            TypeError: If latitude is not numeric.
            ValueError: If latitude is not between -90.0 and 90.0.
        """
        if not isinstance(latitude, (int, float)):
            raise TypeError("Place latitude must be type float")
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("Place latitude must be in range -90.0 to 90.0")
        return float(latitude)

    @hybrid_property
    def longitude(self):
        """
        Get the longitude of the place.

        Returns:
            float: The longitude coordinate.
        """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        """
        Set the longitude of the place.

        Args:
            longitude (float|int): The new longitude.
        """
        self._longitude = longitude
    
    @validates("_longitude")
    def validate_place_longitude(self, key, longitude):
        """
        Validate the longitude of the place.

        Args:
            key (str): The attribute key.
            longitude (float|int): The longitude to validate.

        Returns:
            float: The validated longitude.

        Raises:
            TypeError: If longitude is not numeric.
            ValueError: If longitude is not between -180.0 and 180.0.
        """
        if not isinstance(longitude, (int, float)):
            raise TypeError("Place longitude must be type float")
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("Place longitude must be range -180.0 to 180.0")
        return float(longitude)
