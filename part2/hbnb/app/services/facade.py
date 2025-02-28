from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity

class HBnBFacade:
    """
    Facade class to manage interactions between different layers of the
    application.
    """
    def __init__(self):
        """
        Initialize the HBnBFacade with in-memory repositories for users,
        places, reviews, and amenities.
        """
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

#--------------User facade CURD ops--------------#

    def create_user(self, user_data):
        """
        Create a user and add it to the repository.

        Args:
            user_data (dict): A dictionary containing user data.

        Returns:
            User: The created user instance.
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieve a user by their ID.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            User: The retrieved user instance, or None if not found.
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Retrieve a user by their email.

        Args:
            email (str): The email of the user to retrieve.

        Returns:
            User: The retrieved user instance, or None if not found.
        """
        return self.user_repo.get_by_attribute('email', email)
    
    def get_users_all(self):
        """
        Retrieve all users.

        Returns:
            list: A list of all user instances.
        """
        return self.user_repo.get_all()
    
    def update_user(self, user_id, user_data):
        """
        Update a user's information.

        Args:
            user_id (str): The ID of the user to update.
            data (dict): A dictionary of updated user data.
        """
        self.user_repo.update(user_id, user_data)

#--------------Amenity facade CURD ops--------------#

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)

#--------------Place facade CURD ops--------------#
    def get_place(self, place_id):
        """
        Placeholder method for fetching a place by ID.

        Args:
            place_id: The ID of the place to fetch.
        """
        # Logic will be implemented in later tasks
        pass