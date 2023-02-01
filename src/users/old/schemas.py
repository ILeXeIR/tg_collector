import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr

class UserSchema(BaseModel):
	id: Optional[int] = None
	name: str
	email: EmailStr
	hashed_password: str
	created_at: datetime.datetime
	updated_at: datetime.datetime

class UserInSchema(BaseModel):
	name: str
	email: EmailStr
	password: constr(min_length=8)
	password2: str 

	@validator("password2")
	def password_match(cls, v, values, **kwargs):
		if "password" in values and v != values["password"]:
			raise ValueError("passwords don't match")
		return v