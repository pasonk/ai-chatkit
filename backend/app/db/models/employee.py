from db.models.base import DBBaseModel
from sqlmodel import Field, SQLModel
from datetime import date
from dataclasses import dataclass

@dataclass
class Employee(DBBaseModel, table=True):
    """
    员工表
    """
    __tablename__ = "employee"
    id: int = Field(primary_key=True, index=True, description="员工id")
    employee_no: str = Field(max_length=50, description="员工编号")
    name: str = Field(max_length=50, index=True, description="员工名称")
    gender: int = Field(max_length=10, description=":0-未知 1-男 2-女")
    department_id: int = Field(default=0, description="部门id")
    position: str = Field(max_length=50, description="职位")
    phone: str = Field(max_length=11, description="手机号")
    email: str = Field(max_length=50, description="邮箱")
    status: int = Field(default=0, description="1-试用 2-在职 3-离职")
    entry_date: str = Field(max_length=50, description="入职日期")