from abc import ABC, abstractmethod
from app.extensions import db


class Repository(ABC):
    """
    Abstract base class for a repository. Defines the interface for data
    persistence operations.
    """
    @abstractmethod
    def add(self, obj):
        """
        Add an object to the repository.

        Args:
            obj: The object to add.
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Retrieve an object from the repository by its ID.

        Args:
            obj_id: The ID of the object to retrieve.

        Returns:
            The retrieved object, or None if not found.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Retrieve all objects from the repository.

        Returns:
            A list of all objects in the repository.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Update an object in the repository.

        Args:
            obj_id: The ID of the object to update.
            data: A dictionary of updated data.
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Delete an object from the repository by its ID.

        Args:
            obj_id: The ID of the object to delete.
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object from the repository by an attribute value.

        Args:
            attr_name: The name of the attribute.
            attr_value: The value of the attribute.

        Returns:
            The retrieved object, or None if not found.
        """
        pass


class SQLAlchemyRepository(Repository):
    """
    SQLAlchemy implementation of the Repository interface.
    """

    def __init__(self, model):
        """
        Initialize the SQLAlchemy repository.

        Args:
            model: The SQLAlchemy model class.
        """
        self.model = model

    def add(self, obj):
        """
        Add an object to the SQLAlchemy repository.

        Args:
            obj: The object to add.
        """
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """
        Retrieve an object from the SQLAlchemy repository by its ID.

        Args:
            obj_id: The ID of the object to retrieve.

        Returns:
            The retrieved object, or None if not found.
        """
        return self.model.query.get(obj_id)

    def get_all(self):
        """
        Retrieve all objects from the SQLAlchemy repository.

        Returns:
            A list of all objects in the repository.
        """
        return self.model.query.all()

    def update(self, obj_id, data):
        """
        Update an object in the SQLAlchemy repository.

        Args:
            obj_id: The ID of the object to update.
            data: A dictionary of updated data.
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        """
        Delete an object from the SQLAlchemy repository by its ID.

        Args:
            obj_id: The ID of the object to delete.
        """
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object from the SQLAlchemy repository by an attribute value.

        Args:
            attr_name: The name of the attribute.
            attr_value: The value of the attribute.

        Returns:
            The retrieved object, or None if not found.
        """
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()
