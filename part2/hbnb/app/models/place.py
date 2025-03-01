from app.models.basecls import BaseModel


class Place(BaseModel):
    """
    Place model class that inherits from BaseModel.
    Represents a place with various attributes and related
    reviews and amenities.
    """
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        """
        Initialize a Place instance.

        Args:
            title (str): The title of the place.
            description (str): The description of the place.
            price (float): The price of the place.
            latitude (float): The latitude of the place.
            longitude (float): The longitude of the place.
            owner (str): The owner of the place.
        """
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self._reviews = []  # List to store related reviews
        self._amenities = []  # List to store related amenities

    def add_review(self, review):
        """
        Add a review to the place.

        Args:
            review: The review to add.
        """
        self._reviews.append(review)

    @property
    def reviews(self):
        """
        Get the list of reviews associated with the place.

        Returns:
            list: The list of reviews.
        """
        return self._reviews

    @reviews.setter
    def reviews(self, reviews):
        """
        Set the list of reviews associated with the place.

        Args:
            reviews (str or list): A review or a list of reviews to add.

        Raises:
            TypeError: If the reviews is not a string or a list of strings.
        """
        if type(reviews) is str:
            self.add_review(reviews)
            self._reviews = self.reviews
        elif type(reviews) is list:
            if not all(isinstance(rev, str) for rev in reviews):
                raise TypeError("Place reviews must be a list of str")
            self._reviews = self.reviews + reviews
        else:
            raise TypeError("Place reviews can only be list or str")

    def add_amenity(self, amenity):
        """
        Add an amenity to the place.

        Args:
            amenity: The amenity to add.
        """
        self._amenities.append(amenity)

    @property
    def amenities(self):
        """
        Get the list of amenities associated with the place.

        Returns:
            list: The list of amenities.
        """
        return self._amenities

    @amenities.setter
    def amenities(self, amenities):
        """
        Set the list of amenities associated with the place.

        Args:
            amenities (str or list): An amenity or a list of amenities to add.

        Raises:
            TypeError: If the amenities is not a string or a list of strings.
        """
        if type(amenities) is str:
            self.add_amenity(amenities)
            self._amenities = self.amenities
        elif type(amenities) is list:
            if not all(isinstance(ame, str) for ame in amenities):
                raise TypeError("Place amenities must be a list of str")
            self._amenities = self.amenities + amenities
        else:
            raise TypeError("Place amenities can only be str or list")

    @property
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
            title (str): The new title of the place.

        Raises:
            TypeError: If the title is not a string.
            ValueError: If the title is longer than 100 characters.
        """
        if type(title) is not str:
            raise TypeError("Place title must be a str")
        if len(title) > 100:
            raise ValueError("Place title is longer than 100 chars")
        self._title = title

    @property
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
            description (str): The new description of the place.

        Raises:
            TypeError: If the description is not a string.
        """
        if type(description) is not str:
            raise TypeError("Place description must be a str")
        self._description = description

    @property
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
            price (float): The new price of the place.

        Raises:
            TypeError: If the price is not a float.
            ValueError: If the price is negative.
        """
        if type(price) is not float:
            raise TypeError("Place price is not type float")
        if price < 0:
            raise ValueError("Place price must be positive")
        self._price = price

    @property
    def latitude(self):
        """
        Get the latitude of the place.

        Returns:
            float: The latitude of the place.
        """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        """
        Set the latitude of the place.

        Args:
            latitude (float): The new latitude of the place.

        Raises:
            TypeError: If the latitude is not a float.
            ValueError: If the latitude is not in the range -90.0 to 90.0.
        """
        if type(latitude) is not float:
            raise TypeError("Place latitude must be type float")
        if latitude < -90.0 or latitude > 90.0:
            return ValueError("Place latitude must be in range -90.0 to 90.0")
        self._latitude = latitude

    @property
    def longitude(self):
        """
        Get the longitude of the place.

        Returns:
            float: The longitude of the place.
        """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        """
        Set the longitude of the place.

        Args:
            longitude (float): The new longitude of the place.

        Raises:
            TypeError: If the longitude is not a float.
            ValueError: If the longitude is not in the range -180.0 to 180.0.
        """
        if type(longitude) is not float:
            raise TypeError("Place longitude must be type float")
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("Place longitude must be range -180.0 to 180.0")
        self._longitude = longitude

    @property
    def owner_id(self):
        """
        Get the owner of the place.

        Returns:
            str: The owner of the place.
        """
        return self._owner_id

    @owner_id.setter
    def owner_id(self, owner_id):
        """
        Set the owner of the place.

        Args:
            owner (str): The new owner of the place.

        Raises:
            TypeError: If the owner_id is not a str.
        """
        if not isinstance(owner_id, str):
            raise TypeError("Place owner_id must be a str")
        self._owner_id = owner_id
