from db.models.base import DBBaseModel
from sqlmodel import Field, SQLModel
from datetime import date
from dataclasses import dataclass

@dataclass
class Employee(DBBaseModel, table=True):
    """
    employee model
    """
    __tablename__ = "employee"
    id: int = Field(primary_key=True, index=True, description="employee id")
    employee_no: str = Field(max_length=50, description="employee no")
    name: str = Field(max_length=50, index=True, description="employee name")
    gender: int = Field(max_length=10, description="gender: 0-unknown 1-male 2-female")
    department_id: int = Field(default=0, description="department id")
    position: str = Field(max_length=50, description="position")
    phone: str = Field(max_length=11, description="phone")
    email: str = Field(max_length=50, description="email")
    status: int = Field(default=0, description="status: 1-trial 2-active 3-terminated")
    entry_date: str = Field(max_length=50, description="entry date")
