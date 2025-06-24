from fastapi import FastAPI
from api.department_routers import department_router
from api.chat_routes import chat_router
from api.employee_routers import employee_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# Cross-domain is allowed. For production environments, 
# please change * to a specific domain name
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(department_router)
app.include_router(chat_router)
app.include_router(employee_router)






