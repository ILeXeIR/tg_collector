from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from .depends import get_user_repository, get_current_user
from .schemas import UserSchema, UserInSchema
from .repositories import UserRepository


router = APIRouter()

@router.get("/", response_model=List[UserSchema])
async def read_users(
	users: UserRepository = Depends(get_user_repository),
	limit: int = 100, 
	skip: int = 0):
	return await users.get_all(limit=limit, skip=skip)

@router.post("/", response_model=UserSchema)
async def create_user(
	user: UserInSchema, 
	users: UserRepository = Depends(get_user_repository)):
	return await users.create(u=user)

@router.put("/", response_model=UserSchema)
async def update_user(
	id: int, 
	user: UserInSchema, 
	users: UserRepository = Depends(get_user_repository),
	current_user: User = Depends(get_current_user)):
	old_user = await users.get_by_id(id=id)
	if old_user is None or old_user.email != current_user.email:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
							detail="User not found")
	return await users.update(id=id, u=user)