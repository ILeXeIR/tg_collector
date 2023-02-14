import datetime
from uuid import UUID

from typing import Optional
from pydantic import BaseModel, constr, EmailStr, validator


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
    password: constr(max_length=50)
    password2: str 

    class Config:
        orm_mode = True

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords don't match")
        return v

class Token(BaseModel):
    access_token: str
    token_type: str 
