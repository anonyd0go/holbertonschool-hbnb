from basecls import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if len(title) > 100:
            raise ValueError("Place title is longer than 100 chars")
        self._title = title

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if type(price) is not float:
            raise TypeError("Place price is not type float")
        if price < 0:
            raise ValueError("Place price must be positive")
        self._price = price

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        if type(latitude) is not float:
            raise TypeError("Place latitude must be type float")
        if latitude not in range(-90.0, 90.1):
            return ValueError("Place latitude must be in range -90.0 to 90.0")
        self._latitude = latitude

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        if type(longitude) is not float:
            raise TypeError("Place longitude must be type float")
        if longitude not in range(-180.0, 180.1):
            raise ValueError("Place longitude must be range -180.0 to 180.0")
        self._longitude = longitude

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        self._owner = owner
