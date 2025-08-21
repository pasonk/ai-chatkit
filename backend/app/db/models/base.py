from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlmodel import SQLModel
from sqlmodel import Field


class DBBaseModel(SQLModel):
    """
    DB base model
    """
    create_time: datetime | None = Field(default=datetime.now, title="创建时间")
    edit_time: datetime | None = Field(default=datetime.now, title="更新时间")
    # create_by: str | None = Field(default="", title="创建者")
    # update_by: str | None = Field(default="", title="更新者")
