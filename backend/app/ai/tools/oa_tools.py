from langchain_core.tools import BaseTool, tool

from db.models.employee import Employee
from db.repository.employee_repo import EmployeeRepository
from db.models.department import Department
from db.repository.department_repo import DepartmentRepository
from db.database import async_session_maker
from dataclasses import dataclass, asdict
from fastapi import Depends
from ai.rag.chromaClient import hand_book_vector_store


@tool
async def get_user_info(user_name: str) -> dict:
    """Obtain user information"""
    async with async_session_maker() as session:
        employee =  await EmployeeRepository.get_employee_by_name(session, name=user_name)
        
        if not employee:
            return {"error": "user not found"}

        return asdict(employee)

@tool
async def get_user_department(user_name: str) -> dict:
    """Obtain the information of the user department"""
   
    async with async_session_maker() as session: 
        employee = await EmployeeRepository.get_employee_by_name(session, name=user_name)
        
        if not employee:
            return {"error": "user not found"}

        department = await DepartmentRepository.get_department(session, department_id=employee.department_id)
        
        if not department:
            return {"error": "department not found"}
        
        return asdict(department)

@tool
async def search_handbook(query: str) -> str:
    """ Check the employee handbook and the internal rules and regulations of the company """
    result = hand_book_vector_store.similarity_search(query, k=10)
    
    if result.__len__ == 0:
        return "no result found"
    
    return "\n\n".join(doc.page_content for doc in result)    