from httpx import AsyncClient
import pytest
from tortoise import Tortoise
# from tortoise.contrib.fastapi import register_tortoise, connections

from main import app
from src.users.dao import User
from src.users.security import create_access_token, hash_password


"""
@pytest.fixture(scope="session")
async def create_test_db():
    # test_db_path = tmpdir_factory.mktemp("test_dir").join("db.sqlite")
    register_tortoise(
        app,
        db_url="sqlite://database/db_test.sqlite",
        modules={"models": ["src.users.dao", "src.collector.dao",
                            "src.bot.dao"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    yield
    connections.close_all()
"""
@pytest.fixture(scope="session")
async def create_test_db():
    await Tortoise.init(
        db_url="sqlite://database/db_test.sqlite",
        modules={"models": ["src.users.dao", "src.collector.dao",
                            "src.bot.dao"]}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise._drop_databases()

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session", name="ac")
async def create_async_client():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        yield ac

@pytest.fixture()
async def db_with_users(create_test_db):
    test_users = [
        {
            "username": "user1",
            "email": "user1@example.com",
            "real_name": "User A",
            "password_hash": "qwerty123"
        },
        {
            "username": "user2",
            "email": "user2@example.com",
            "real_name": "User B",
            "password_hash": "qwerty123"
        }
    ]
    for test_user in test_users:
        test_user["password_hash"] = hash_password(test_user["password_hash"])
        await User.create(**test_user)
    yield
    await User.all().delete()

@pytest.fixture(name="token")
async def create_test_token(db_with_users):
    test_token = create_access_token({"sub": "user2"})
    bearer_token = "Bearer " + test_token
    yield bearer_token