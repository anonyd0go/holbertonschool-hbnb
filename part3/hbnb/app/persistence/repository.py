from abc import ABC, abstractmethod


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


class InMemoryRepository(Repository):
    """
    In-memory implementation of the Repository interface.
    """

    def __init__(self):
        """
        Initialize the in-memory repository.
        """
        self._storage = {}

    def add(self, obj):
        """
        Add an object to the in-memory repository.

        Args:
            obj: The object to add.
        """
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """
        Retrieve an object from the in-memory repository by its ID.

        Args:
            obj_id: The ID of the object to retrieve.

        Returns:
            The retrieved object, or None if not found.
        """
        return self._storage.get(obj_id)

    def get_all(self):
        """
        Retrieve all objects from the in-memory repository.

        Returns:
            A list of all objects in the repository.
        """
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Update an object in the in-memory repository.

        Args:
            obj_id: The ID of the object to update.
            data: A dictionary of updated data.
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """
        Delete an object from the in-memory repository by its ID.

        Args:
            obj_id: The ID of the object to delete.
        """
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object from the in-memory repository by an attribute value.

        Args:
            attr_name: The name of the attribute.
            attr_value: The value of the attribute.

        Returns:
            The retrieved object, or None if not found.
        """
        return next(
            (obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value),
            None
        )
