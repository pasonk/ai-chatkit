from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List, Optional

from db.database import db_session
from db.models.employee import Employee
from db.models.base import DBBaseModel

class EmployeeRepository:
    
    @classmethod
    async def create_employee(cls, session: AsyncSession, employee: Employee) -> Employee:
        session.add(employee)
        await session.commit()
        await session.refresh(employee)
        return employee

    @classmethod
    async def get_employee(cls, session: AsyncSession, employee_id: int) -> Optional[Employee]:
        result = await session.execute(
            select(Employee).where(Employee.id == employee_id)
        )
        return result.scalars().first()

    ##通过员工名称获取员工信息
    @classmethod
    async def get_employee_by_name(cls, session: AsyncSession, name: str) -> Employee:
        result = await session.execute(
            select(Employee).where(Employee.name == name)
        )
        return result.scalars().first()
    
    @classmethod
    async def get_all_employees(cls, session: AsyncSession) -> List[Employee]:
        result = await session.execute(select(Employee))
        return result.scalars().all()

    @classmethod
    async def update_employee(cls, session: AsyncSession, employee_id: int, employee_data: dict) -> Optional[Employee]:
        employee = await cls.get_employee(session, employee_id)
        if employee:
            for key, value in employee_data.items():
                setattr(employee, key, value)
            await session.commit()
            await session.refresh(employee)
        return employee

    @classmethod
    async def delete_employee(cls, session: AsyncSession, employee_id: int) -> bool:
        employee = await cls.get_employee(session, employee_id)
        if employee:
            await session.delete(employee)
            await session.commit()
            return True
        return False