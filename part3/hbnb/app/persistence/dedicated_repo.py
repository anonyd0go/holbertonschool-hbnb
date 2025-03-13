from app.models.user import User
from app.models.place import Place
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


class PlaceRepository(SQLAlchemyRepository):
    """
    SQLAlchemy repository dedicated to the Place model.
    
    Inherits from SQLAlchemyRepository to handle CRUD operations
    for Place objects.
    """
    def __init__(self):
        """
        Initialize the PlaceRepository with the Place model.
        """
        super().__init__(Place)
