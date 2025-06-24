from fastapi import APIRouter, Depends, HTTPException, status
from db.models.employee import Employee
from db.repository.employee_repo import EmployeeRepository
from db.database import SessionDep
from typing import List
from ai.tools.oa_tools import get_user_info, get_user_department

employee_router = APIRouter(prefix="/employee", tags=["employee"])

# 新增员工
@employee_router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_employee(employee: Employee, session: SessionDep):
    try:
        await EmployeeRepository.create_employee(session, employee)
        return {"message": "Employee added successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    
# 获取员工信息
@employee_router.get("/get/{employee_id}", response_model=Employee)    
async def get_employee(employee_id: int, session: SessionDep):
    employee = await EmployeeRepository.get_employee(session, employee_id)  
    if employee:
        return employee
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

# 获取所有员工信息
@employee_router.get("/get_all", response_model=List[Employee])
async def get_all_employees(session: SessionDep):
    return await EmployeeRepository.get_all_employees(session)


# 更新员工信息
@employee_router.put("/update/{employee_id}", response_model=Employee)
async def update_employee(employee_id: int, employee_data: Employee, session: SessionDep):
    employee = await EmployeeRepository.update_employee(session, employee_id, employee_data)
    if employee:
        return employee
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
# 删除员工信息
@employee_router.delete("/delete/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_id: int, session: SessionDep):
    success = await EmployeeRepository.delete_employee(session, employee_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    
# 获取员工信息通过姓名
@employee_router.get("/get_by_name/{name}", response_model=dict)
async def get_employee_by_name(name: str):
    # employee = await EmployeeRepository.get_employee_by_name(session, name)
    employee = await get_user_info(name)
    if employee:
        return employee
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")