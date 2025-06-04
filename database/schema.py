from datetime import datetime

from pydantic import BaseModel, Field, validator
from typing import Union, Optional, List


class Task(BaseModel):
    id: int
    user_id: int

    task_name: Union[str] = Field(default=None, title="Имя задачи")
    task_body: Union[str] = Field(default=None, title="Задача")

    class Config:
        from_attributes = True


class User(BaseModel):
    id: int
    tg_id: int

    name: Union[str] = Field(default=None, title="Имя пользователя")

    tasks: List[Task]

    class Config:
        from_attributes = True


class AddUser(BaseModel):
    tg_id: int

    name: Union[str] = Field(default=None, title="Имя пользователя")

    class Config:
        from_attributes = True


class ClosedTask(BaseModel):
    id: int
    user_id: int

    task_name: Union[str] = Field(default=None, title="Имя задачи")
    task_body: Union[str] = Field(default=None, title="Задача")

    class Config:
        from_attributes = True
