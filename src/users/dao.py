from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(models.Model):
    #The User model
    
    id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=30, unique=True)
    email = fields.CharField(max_length=80, unique=True)
    real_name = fields.CharField(max_length=50, null=True)
    password_hash = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.username

    #class PydanticMeta:
    #    exclude = ["password_hash"]


User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)