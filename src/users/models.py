from tortoise.models import Model
from tortoise import fields


class User(Model):
    #id = fields.IntField(pk=True) Automaticly created with generated=True
    name = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.name