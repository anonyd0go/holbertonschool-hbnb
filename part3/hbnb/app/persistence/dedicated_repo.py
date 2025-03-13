from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app import db
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """
    SQLAlchemy repository dedicated to the User model.
    
    Inherits from SQLAlchemyRepository and provides additional functionality
    specific to users, such as retrieving a user by email.
    """
    def __init__(self):
        """
        Initialize the UserRepository with the User model.
        """
        super().__init__(User)

    def get_user_by_email(self, email):
        """
        Retrieve a user by their email.
        
        Args:
            email (str): The email address of the user.
            
        Returns:
            User: The user object if found, otherwise None.
        """
        return self.model.query.filter_by(email=email).first()

    def authenticate_user(self, email, password):
        """
        Retrieve a user by email and verify the plaintext password.
        
        Args:
            email (str): The user's email.
            password (str): The plaintext password to verify.
        
        Returns:
            User: The authenticated user if the credentials match, else None.
        """
        user = self.get_user_by_email(email)
        if user and user.verify_password(password):
            return user
        return None
    
    def get_admin_users(self):
        """
        Retrieve all admin users.
        
        Returns:
            list: A list of User objects that have is_admin set to True.
        """
        return self.model.query.filter_by(is_admin=True).all()

    def get_non_admin_users(self):
        """
        Retrieve all non-admin users.
        
        Returns:
            list: A list of User objects that have is_admin set to False.
        """
        return self.model.query.filter_by(_is_admin=False).all()

    def search_users_by_name(self, name_substring):
        """
        Search for users whose first or last name contains the provided substring (case-insensitive).
        
        Args:
            name_substring (str): The substring to search for.
        
        Returns:
            list: A list of User objects matching the search criteria.
        """
        return self.model.query.filter(
            db.or_(
                self.model._first_name.ilike(f"%{name_substring}%"),
                self.model._last_name.ilike(f"%{name_substring}%")
            )
        ).all()


class PlaceRepository(SQLAlchemyRepository):
    """
    SQLAlchemy repository dedicated to the Place model.
    
    Inherits from SQLAlchemyRepository to handle CRUD operations
    for Place objects and provides additional queries specific to Place.
    """
    def __init__(self):
        """
        Initialize the PlaceRepository with the Place model.
        """
        super().__init__(Place)

    def get_places_by_owner(self, owner_id):
        """
        Retrieve all places owned by a specific user.
        
        Args:
            owner_id (str): The unique identifier of the owner.
            
        Returns:
            list: A list of Place objects owned by the specified user.
        """
        return self.model.query.filter_by(owner_id=owner_id).all()

    def get_places_by_price_range(self, min_price, max_price):
        """
        Retrieve all places with a price within the specified range.
        
        Args:
            min_price (float): The minimum price.
            max_price (float): The maximum price.
            
        Returns:
            list: A list of Place objects whose price is between min_price and max_price.
        """
        return self.model.query.filter(
            self.model.price >= min_price,
            self.model.price <= max_price
        ).all()

    def search_places_by_title(self, title_substring):
        """
        Search for places with a title containing a given substring (case-insensitive).
        
        Args:
            title_substring (str): The substring to search for in the place title.
            
        Returns:
            list: A list of Place objects whose title matches the search criteria.
        """
        return self.model.query.filter(
            self.model.title.ilike(f"%{title_substring}%")
        ).all()


class AmenityRepository(SQLAlchemyRepository):
    """
    SQLAlchemy repository dedicated to the Amenity model.
    
    Inherits from SQLAlchemyRepository and provides additional functionality
    specific to Amenity objects.
    """
    def __init__(self):
        """
        Initialize the AmenityRepository with the Amenity model.
        """
        super().__init__(Amenity)
    
    def get_amenity_by_name(self, name):
        """
        Retrieve an amenity by its name.
        
        Args:
            name (str): The name of the amenity.
            
        Returns:
            Amenity: The amenity object if found, otherwise None.
        """
        return self.model.query.filter_by(_name=name).first()
    
    def get_all_amenities(self):
        """
        Retrieve all amenity objects.
        
        Returns:
            list: A list of Amenity objects.
        """
        return self.model.query.all()


class ReviewRepository(SQLAlchemyRepository):
    """
    SQLAlchemy repository dedicated to the Review model.
    
    Inherits from SQLAlchemyRepository and provides additional functionality
    specific to Review objects.
    """
    def __init__(self):
        """
        Initialize the ReviewRepository with the Review model.
        """
        super().__init__(Review)
    
    def get_reviews_by_place_id(self, place_id):
        """
        Retrieve all reviews associated with a given place.
        
        Args:
            place_id (str): The unique identifier of the place.
            
        Returns:
            list: A list of Review objects for the specified place.
        """
        return self.model.query.filter_by(place_id=place_id).all()
    
    def get_reviews_by_user_id(self, user_id):
        """
        Retrieve all reviews written by a specified user.
        
        Args:
            user_id (str): The unique identifier of the user.
            
        Returns:
            list: A list of Review objects associated with the specified user.
        """
        return self.model.query.filter_by(user_id=user_id).all()
