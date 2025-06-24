"""
API业务逻辑处理
"""

from sqlalchemy.orm import Session
from . import schemas
from ..db import models

def create_user(db: Session, user: schemas.UserCreate):
    """创建用户"""
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=user.password + "_hashed"  # 示例哈希处理
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user