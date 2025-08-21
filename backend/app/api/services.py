"""
API business logic processing
"""

from sqlalchemy.orm import Session
from . import schemas
from ..db import models

def create_user(db: Session, user: schemas.UserCreate):
    """ create a new user"""
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=user.password + "_hashed" 
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user