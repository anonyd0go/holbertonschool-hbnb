from app.extensions import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    """
    Base model class that provides common attributes and methods for other models.
    
    Attributes:
        id (str): Primary key, a UUID string.
        created_at (datetime): Timestamp when the instance was created.
        updated_at (datetime): Timestamp when the instance was last updated.
    """
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        """
        Initialize a new BaseModel instance with keyword arguments.
        
        This sets any provided attributes (such as first_name, email, etc.),
        thereby triggering any associated validations.
        
        Args:
            **kwargs: Arbitrary keyword arguments corresponding to column names.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        """
        Update the updated_at timestamp to the current time.
        
        This method should be called before committing the instance to the database
        if you want to update the modification timestamp.
        """
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """
        Update the instance attributes based on the provided dictionary.
        
        Each key/value pair in the data dictionary is set as an attribute on the instance.
        This method also calls the save() method to refresh the updated_at timestamp.
        
        Args:
            data (dict): A dictionary of attributes to update.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp
