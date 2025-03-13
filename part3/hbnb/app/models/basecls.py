from app.extensions import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    """
    Base model class that provides common attributes and methods for other models.
    """
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        """
        Initialize a new BaseModel instance with keyword arguments.
        This passes any provided attributes (such as first_name, email, etc.)
        to the instance, thereby triggering any associated validations.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        """
        Update the updated_at timestamp whenever the object is modified.
        """
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """
        Update the attributes of the object based on the provided dictionary.

        Args:
            data (dict): A dictionary of attributes to update.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp