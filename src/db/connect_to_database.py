from tortoise import Tortoise
from src import settings

async def connect_to_database():
    await Tortoise.init(
        db_url=get_db_uri(
            user=settings.POSTGRESQL_USERNAME,
            passwd=settings.POSTGRESQL_PASSWORD,
            host=settings.POSTGRESQL_HOSTNAME,
            db=settings.POSTGRESQL_DATABASE
        ),
        modules={"models": ["src.users.models", "aerich.models"]}   
    )