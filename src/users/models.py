import datetime

from typing import Optional
from pydantic import BaseModel, constr, EmailStr
from tortoise.contrib.pydantic.base import PydanticModel
from uuid import UUID

"""
class User_Pydantic(BaseModel):
    id: Optional[UUID]
    username: constr(max_length=30)
    email: EmailStr
    real_name: Optional[constr(max_length=50)]
    password_hash : constr(max_length=128)
    created_at : datetime.datetime
    modified_at : datetime.datetime

    class Config:
        orm_mode = True

class UserIn_Pydantic(BaseModel):
    username: constr(max_length=30)
    email: EmailStr
    real_name: Optional[constr(max_length=50)]
    password: constr(min_length=8, max_length=50)

    class Config:
        orm_mode = True
"""
class User_Pydantic(PydanticModel):
    id: Optional[UUID]
    username: str
    email: str
    real_name: Optional[str]
    password_hash : str
    created_at : datetime.datetime
    modified_at : datetime.datetime

    class Config:
        orm_mode = True

class UserIn_Pydantic(PydanticModel):
    username: str
    email: str
    real_name: Optional[str]
    password: str

    class Config:
        orm_mode = True