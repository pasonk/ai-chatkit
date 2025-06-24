
from dataclasses import dataclass
from sqlmodel import Field, SQLModel
from db.models.base import DBBaseModel

@dataclass
class Department(DBBaseModel, table=True):
    """
    部门表
    """
    __tablename__ = "department"
    id: int = Field(primary_key=True, index=True, description="部门id")
    name: str = Field(max_length=50, description="部门名称")
    parent_id: int = Field(default=0, description="父部门id")
    manager_id: int = Field(default=0, description="部门负责人id")