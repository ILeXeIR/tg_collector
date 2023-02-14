import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

from src.security import hash_password, verify_password, create_access_token
from .dao import Users
from .depends import get_current_user
from .models import User_Pydantic, UserIn_Pydantic, Token


users_router = APIRouter()

@users_router.get("/", response_model=List[User_Pydantic])
async def get_users():
    return await Users.all()

@users_router.get("/id/{id}", response_model=User_Pydantic)
async def get_user_by_id(id: str):
    user_obj = await Users.get_or_none(id=id)
    if not user_obj:
        raise HTTPException(400, detail="User not found")
    return user_obj

@users_router.get("/email/{email}", response_model=User_Pydantic)
async def get_user_by_email(email: str):
    user_obj = await Users.get_or_none(email=email)
    if not user_obj:
        raise HTTPException(400, detail="User not found")
    return user_obj

@users_router.post("/", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    password_hash = hash_password(user.password)
    user_obj = await Users.create(password_hash=password_hash,
                                **user.dict(exclude_unset=True))
    return user_obj

@users_router.put("/{id}", response_model=User_Pydantic)
async def update_user(id: str, user: UserIn_Pydantic):
    user_obj = await Users.get_or_none(id=id)
    if not user_obj:
        raise HTTPException(400, detail="User not found")
    user_obj.password_hash = hash_password(user.password)
    for field_name, field_value in user.dict(exclude_unset=True).items():
        setattr(user_obj, field_name, field_value)
    await user_obj.save()
    return user_obj

@users_router.post("/login", response_model=Token)
async def login(login: OAuth2PasswordRequestForm = Depends()):
    user_obj = await Users.get_or_none(username=login.username)
    if user_obj is None or not verify_password(login.password, 
                                                user_obj.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Incorrect username or password")
    return Token(
        access_token=create_access_token({"sub": user_obj.username}),
        token_type="bearer"
    )

@users_router.get("/me", response_model=User_Pydantic)
async def get_my_user(current_user: User_Pydantic = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="User is not authenticated")
    return current_user