from typing import Annotated, AsyncGenerator

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, SQLModel, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str = Field()


sqlite_file_name = "../../app/resource/database.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"
mysql_url = "mysql+aiomysql://root:root@localhost/ai-chatkit"

# connect_args = {"check_same_thread": False}
engine = create_async_engine(sqlite_url)

async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# async def get_session():
#     async with AsyncSession(engine) as session:
#         yield session


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

app = FastAPI()

    
@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()