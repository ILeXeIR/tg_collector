from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import parse_obj_as
from tortoise.exceptions import IntegrityError
from typing import List

from .security import hash_password, verify_password, create_access_token
from .dao import User
from .deps import users_router
from .services import get_current_user
from .models import UserRp, UserRq, Token


@users_router.get("/")
async def get_users(
        current_user: UserRp = Depends(get_current_user)) -> List[UserRp]:
    users = await User.all()
    return parse_obj_as(List[UserRp], users)


@users_router.get("/id/{id}")
async def get_user_by_id(
        id: str,
        current_user: UserRp = Depends(get_current_user)
) -> UserRp:
    user_obj = await User.get_or_none(id=id)
    if not user_obj:
        raise HTTPException(400, detail="User not found")
    return UserRp.from_orm(user_obj)


@users_router.get("/email/{email}")
async def get_user_by_email(
        email: str,
        current_user: UserRp = Depends(get_current_user)
) -> UserRp:
    user_obj = await User.get_or_none(email=email)
    if not user_obj:
        raise HTTPException(400, detail="User not found")
    return UserRp.from_orm(user_obj)


@users_router.post("/")
async def create_user(user: UserRq) -> UserRp:
    password_hash = hash_password(user.password)
    try:
        user_obj = await User.create(**user.dict(exclude_unset=True),
                                     password_hash=password_hash)
    except IntegrityError as e:
        detail = ""
        if str(e).endswith("username"):
            detail = "Username must be unique"
        elif str(e).endswith("email"):
            detail = "Email must be unique"
        raise HTTPException(400, detail=detail)
    else:
        return UserRp.from_orm(user_obj)


@users_router.put("/")
async def update_user(
        user: UserRq,
        current_user: UserRp = Depends(get_current_user)
) -> UserRp:
    user_obj = await User.get(id=current_user.id)
    user_obj.password_hash = hash_password(user.password)
    user_obj.update_from_dict(user.dict())
    try:
        await user_obj.save()
    except IntegrityError as e:
        detail = ""
        if str(e).endswith("username"):
            detail = "Username must be unique"
        elif str(e).endswith("email"):
            detail = "Email must be unique"
        raise HTTPException(400, detail=detail)
    else:
        return UserRp.from_orm(user_obj)


@users_router.post("/login")
async def login(login: OAuth2PasswordRequestForm = Depends()) -> Token:
    user_obj = await User.get_or_none(username=login.username)
    if user_obj is None or not verify_password(login.password,
                                               user_obj.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Incorrect username or password")
    return Token(
        access_token=create_access_token({"sub": user_obj.username}),
        token_type="bearer"
    )


@users_router.get("/me")
async def get_my_user(
        current_user: UserRp = Depends(get_current_user)) -> UserRp:
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="User is not authenticated")
    return current_user
