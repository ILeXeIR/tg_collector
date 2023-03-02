from tortoise.contrib.pydantic import pydantic_model_creator

from .dao import CustomStorage


StateRp = pydantic_model_creator(CustomStorage)