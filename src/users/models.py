import datetime
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel, constr, EmailStr, validator
from typing import Optional


class UserRp(BaseModel):
    id: Optional[UUID]
    username: constr(max_length=30)
    email: EmailStr
    real_name: Optional[constr(max_length=50)]
    password_hash: constr(max_length=128)
    created_at: datetime.datetime
    modified_at: datetime.datetime

    class Config:
        orm_mode = True


class UserRq(BaseModel):
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
            raise HTTPException(400, detail="passwords don't match")
        return v


class Token(BaseModel):
    access_token: str
    token_type: str 
