from app.models.basecls import BaseModel
from app.models.place_amenities import place_amenities
from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates


class Amenity(BaseModel):
    """
    Amenity model class that inherits from BaseModel.

    Represents an amenity that a place can offer.
    Each amenity has a name and is connected to Place instances through a 
    many-to-many relationship established via the place_amenities association table.

    Attributes:
        _name (str): The name of the amenity.
    """
    __tablename__ = "amenities"

    _name = db.Column("name", db.String(50), nullable=False)

    @hybrid_property
    def name(self):
        """
        Get the name of the amenity.

        Returns:
            str: The name of the amenity.
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Set the name of the amenity.

        Args:
            name (str): The new name for the amenity.
        """
        self._name = name
    
    @validates("_name")
    def validate_amenity_name(self, key, name):
        """
        Validate and normalize the amenity name.

        Args:
            key (str): The attribute key.
            name (str): The name of the amenity to validate.

        Returns:
            str: The validated amenity name.

        Raises:
            ValueError: If the name is not a str, empty, or exceeds 50 characters.
        """
        if not isinstance(name, str):
            raise ValueError("Amenity name must be a str")
        if not name.strip():
            raise ValueError("Amenity must have a name")
        if len(name) > 50:
            raise ValueError("Amenity name is too long")
        return name
