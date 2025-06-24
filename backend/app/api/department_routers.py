
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Annotated

from db.models.department import Department
from db.repository.department_repo import DepartmentRepository
from db.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import SessionDep


department_router = APIRouter(
    prefix="/department",
    tags=["department"],
)

@department_router.post("/add", response_model=Department, status_code=status.HTTP_201_CREATED)
async def create_department(
    department: Department,
    session: SessionDep
):
    return await DepartmentRepository.create_department(session, department)


@department_router.get("/{department_id}", response_model=Department)
async def get_department(
    department_id: int,
     session: SessionDep
):
    department = await DepartmentRepository.get_department(session, department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    return department

@department_router.get("/get_by_name/{department_name}", response_model=Department)
async def get_department_by_name(
    department_id: int,
     session: SessionDep
):
    department = await DepartmentRepository.get_department(session, department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    return department

@department_router.get("/", response_model=List[Department])
async def get_all_departments( session: SessionDep):
    return await DepartmentRepository.get_all_departments(session)


@department_router.put("/update/{department_id}", response_model=Department)
async def update_department(
    department_id: int,
    department_data: dict,
    session: SessionDep
):
    department = await DepartmentRepository.update_department(session, department_id, department_data)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    return department


@department_router.delete("/del/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_id: int,
    session: SessionDep
):
    success = await DepartmentRepository.delete_department(session, department_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
