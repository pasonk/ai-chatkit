from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List, Optional
from db.models.department import Department


class DepartmentRepository:
    
    @classmethod
    async def create_department(cls, session: AsyncSession, department: Department) -> Department:
        session.add(departmnt)
        await session.commit()
        await session.refresh(department)
        return department

    
    @classmethod
    async def get_department(cls, session: AsyncSession, department_id: int) -> Department:
        result = await session.execute(
            select(Department).where(Department.id == department_id)
        )
        return result.scalars().first()

    @classmethod
    async def get_all_departments(cls, session: AsyncSession) -> List[Department]:
        result = await session.execute(select(Department))
        return result.scalars().all()

    @classmethod
    async def update_department(cls, session: AsyncSession, department_id: int, department_data: dict) -> Optional[Department]:
        department = await cls.get_department(department_id)
        if department:
            for key, value in department_data.items():
                setattr(department, key, value)
            await session.commit()
            await session.refresh(department)
        return department
    @classmethod
    async def delete_department(cls, session: AsyncSession, department_id: int) -> bool:
        department = await cls.get_department(department_id)
        if department:
            await session.delete(department)
            await session.commit()
            return True
        return False