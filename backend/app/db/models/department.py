
from dataclasses import dataclass
from sqlmodel import Field, SQLModel
from db.models.base import DBBaseModel

@dataclass
class Department(DBBaseModel, table=True):
    """
    department model
    """
    __tablename__ = "department"
    id: int = Field(primary_key=True, index=True, description="department id")
    name: str = Field(max_length=50, description="department name")
    parent_id: int = Field(default=0, description="parent department id")
    manager_id: int = Field(default=0, description="department manager id")
