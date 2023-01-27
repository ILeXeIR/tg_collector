from tortoise import Tortoise
from src import settings

async def init():
    await Tortoise.init(config=settings.DATABASE_CONFIG)
    await Tortoise.generate_schemas()