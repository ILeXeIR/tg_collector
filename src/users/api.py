from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from .dao import Users, User_Pydantic, UserIn_Pydantic
#from .models import User_Pydantic, UserIn_Pydantic

users_router = APIRouter()

@users_router.get("/", response_model=List[User_Pydantic])
async def get_users():
	return await User_Pydantic.from_queryset(Users.all())

@users_router.get("/{id}", response_model=User_Pydantic)
async def get_user_by_id(id: str):
	user_obj = await Users.get_or_none(id=id)
	if not user_obj:
		raise HTTPException(400, detail="User not found")
	return await User_Pydantic.from_tortoise_orm(user_obj)

@users_router.get("/email/{email}", response_model=User_Pydantic)
async def get_user_by_email(email: str):
	user_obj = await Users.get_or_none(email=email)
	if not user_obj:
		raise HTTPException(400, detail="User not found")
	return await User_Pydantic.from_tortoise_orm(user_obj)

@users_router.post("/", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)

@users_router.put("/{id}", response_model=User_Pydantic)
async def update_user(id: str, user: UserIn_Pydantic):
	user_obj = await Users.get_or_none(id=id)
	if not user_obj:
		raise HTTPException(400, detail="User not found")
	await user_obj.update(**user.dict(exclude_unset=True))
	#for field_name in user.dict(exclude_unset=True):
	#	setattr(user_obj, field_name, user[field_name])
	#await user_obj.save(update_fields=user.keys())
	return await User_Pydantic.from_tortoise_orm(user_obj)