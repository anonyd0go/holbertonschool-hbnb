from app.persistence.dedicated_repo import UserRepository, PlaceRepository
from app.persistence.dedicated_repo import AmenityRepository, ReviewRepository
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.user import User


class HBnBFacade:
    """
    Facade class to manage interactions between different layers of the application.
    
    This class aggregates dedicated repositories for User, Place, Amenity, and Review models,
    and exposes high-level methods that encapsulate common CRUD and query operations.
    """
    def __init__(self):
        """
        Initialize the HBnBFacade with SQLAlchemy repositories for users,
        places, reviews, and amenities.
        """
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

#--------------User facade CRUD ops--------------#
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
        return self.user_repo.get_user_by_email(email)
    
    def get_users_all(self):
        """
        Retrieve all users.

        Returns:
            list: A list of all user instances.
        """
        return self.user_repo.get_all()
    
    def get_all_admins(self):
        """
        Retrieves all admin users

        Returns:
            list: A lists of all admin user instances
        """
        return self.user_repo.get_admin_users()

    def get_non_admin_users(self):
        """
        Retrieve all non-admin users.

        Returns:
            list: A list of non-admin user instances.
        """
        return self.user_repo.get_non_admin_users()

    def search_users_by_name(self, name_substring):
        """
        Search for users whose first or last name contains a given substring (case-insensitive).

        Args:
            name_substring (str): The substring to search for.

        Returns:
            list: A list of user objects that match the search criteria.
        """
        return self.user_repo.search_users_by_name(name_substring)
    
    def update_user(self, user_id, user_data):
        """
        Update a user's information.

        Args:
            user_id (str): The ID of the user to update.
            user_data (dict): A dictionary of updated user data.
        """
        self.user_repo.update(user_id, user_data)

    def authenticate_user(self, email, password):
        """
        Authenticate a user using their email and password.

        Args:
            email (str): The user's email.
            password (str): The plaintext password to verify.

        Returns:
            User: The authenticated user if credentials are valid, otherwise None.
        """
        return self.user_repo.authenticate_user(email, password)
    
    def delete_user(self, user_id):
        """
        Delete a user by its ID.

        Args:
            user_id (str): The ID of the user to delete.
        """
        self.user_repo.delete(user_id)

#--------------Amenity facade CRUD ops--------------#
    def create_amenity(self, amenity_data):
        """
        Create an amenity and add it to the repository.

        Args:
            amenity_data (dict): A dictionary containing amenity data.

        Returns:
            Amenity: The created amenity instance.
        """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by its ID.

        Args:
            amenity_id (str): The ID of the amenity to retrieve.

        Returns:
            Amenity: The retrieved amenity instance, or None if not found.
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Retrieve all amenities.

        Returns:
            list: A list of all amenity instances.
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an amenity's information.

        Args:
            amenity_id (str): The ID of the amenity to update.
            amenity_data (dict): A dictionary of updated amenity data.
        """
        self.amenity_repo.update(amenity_id, amenity_data)

    def search_amenity_by_name(self, name):
        """
        Retrieve an amenity by its name.

        Args:
            name (str): The name of the amenity to search for.

        Returns:
            Amenity: The matching amenity instance, or None if not found.
        """
        return self.amenity_repo.get_amenity_by_name(name)
    
    def delete_amenity(self, amenity_id):
        """
        Delete an amenity by its ID.

        Args:
            amenity_id (str): The ID of the amenity to delete.
        """
        self.amenity_repo.delete(amenity_id)

#--------------Place facade CRUD ops--------------#
    def create_place(self, place_data):
        """
        Create a place and add it to the repository.

        Args:
            place_data (dict): A dictionary containing place data.

        Returns:
            Place: The created place instance.
        """
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """
        Retrieve a place by its ID.

        Args:
            place_id (str): The ID of the place to retrieve.

        Returns:
            Place: The retrieved place instance, or None if not found.
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Retrieve all places.

        Returns:
            list: A list of all place instances.
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Update a place's information.

        Args:
            place_id (str): The ID of the place to update.
            place_data (dict): A dictionary of updated place data.
        """
        self.place_repo.update(place_id, place_data)

    def get_places_by_owner(self, owner_id):
        """
        Retrieve all places belonging to a specific owner.

        Args:
            owner_id (str): The owner's unique identifier.

        Returns:
            list: A list of Place objects for the specified owner.
        """
        return self.place_repo.get_places_by_owner(owner_id)

    def get_places_by_price_range(self, min_price, max_price):
        """
        Retrieve the places within a specified price range.

        Args:
            min_price (float): The minimum price.
            max_price (float): The maximum price.

        Returns:
            list: A list of Place objects whose price falls within the range.
        """
        return self.place_repo.get_places_by_price_range(min_price, max_price)

    def search_places_by_title(self, title_substring):
        """
        Search for places by a partial title match (case-insensitive).

        Args:
            title_substring (str): The substring to search for in place titles.

        Returns:
            list: A list of Place objects that match the search criteria.
        """
        return self.place_repo.search_places_by_title(title_substring)

    def get_average_rating_for_place(self, place_id):
        """
        Calculate the average rating for a given place based on its reviews.

        Args:
            place_id (str): The ID of the place.

        Returns:
            float: The average rating, or None if the place has no reviews.
        """
        place = self.get_place(place_id)
        if not place or not place.reviews:
            return None
        ratings = [self.review_repo.get(review)._rating for review in place.reviews]
        return sum(ratings) / len(ratings) if ratings else None
    
    def delete_place(self, place_id):
        """
        Delete a place by its ID.

        Args:
            place_id (str): The ID of the place to delete.
        """
        self.place_repo.delete(place_id)

#--------------Review facade CRUD ops--------------#
    def create_review(self, review_data):
        """
        Create a review and add it to the repository.

        Args:
            review_data (dict): A dictionary containing review data.

        Returns:
            Review: The created review instance.
        """
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """
        Retrieve a review by its ID.

        Args:
            review_id (str): The ID of the review to retrieve.

        Returns:
            Review: The retrieved review instance, or None if not found.
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Retrieve all reviews.

        Returns:
            list: A list of all review instances.
        """
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        """
        Update a review's information.

        Args:
            review_id (str): The ID of the review to update.
            review_data (dict): A dictionary of updated review data.
        """
        self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """
        Delete a review by its ID.

        Args:
            review_id (str): The ID of the review to delete.
        """
        self.review_repo.delete(review_id)

    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews for a specified place.

        Args:
            place_id (str): The ID of the place.

        Returns:
            list: A list of Review objects associated with the place.
        """
        return self.review_repo.get_reviews_by_place_id(place_id)

    def get_reviews_by_user(self, user_id):
        """
        Retrieve all reviews written by a specified user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            list: A list of Review objects authored by the user.
        """
        return self.review_repo.get_reviews_by_user_id(user_id)
