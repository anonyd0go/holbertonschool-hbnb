from app.models.basecls import BaseModel


class Amenity(BaseModel):
    """
    Amenity model class that inherits from BaseModel.
    Represents an amenity with a name.
    """

    def __init__(self, name):
        """
        Initialize an Amenity instance.

        Args:
            name (str): The name of the amenity.
        """
        super().__init__()
        self.name = name

    @property
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
            name (str): The new name of the amenity.

        Raises:
            ValueError: If the name is longer than 50 characters.
        """
        if not name.strip():
            raise ValueError("Amenity must have a name")
        if len(name) > 50:
            raise ValueError("Amenity name is too long")
        self._name = name
