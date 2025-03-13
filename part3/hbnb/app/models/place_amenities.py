"""
Association table for the many-to-many relationship between Place and Amenity.

This table links Place instances to Amenity instances via their respective primary keys.
Each row in this table represents an association between a Place (_id) and an Amenity (_id).
"""


from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db


place_amenities = db.Table(
    "place_amenities",
    Column("place_id", db.String(36), ForeignKey("places.id"), primary_key=True),
    Column("amenity_id", db.String(36), ForeignKey("amenities.id"), primary_key=True)
)
