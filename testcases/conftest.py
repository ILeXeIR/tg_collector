from httpx import AsyncClient
import pytest
from tortoise import Tortoise
# from tortoise.contrib.fastapi import register_tortoise, connections

from main import app
from src.bot.dao import ActiveChat, CustomStorage
from src.collector.dao import Message
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


@pytest.fixture()
async def db_with_messages(create_test_db):
    test_messages = [
        {
            "message_id": 100,
            "chat_id": 1,
            "dispatch_time": "01.02.2023 14:15:16",
            "sender": "alice",
            "sender_id": 1000,
            "message_type": "message_text",
            "text": "Hi, Bob",
            "attachment": str({})
        },
        {
            "message_id": 101,
            "chat_id": 1,
            "dispatch_time": "01.02.2023 14:16:16",
            "sender": "bob",
            "sender_id": 1001,
            "message_type": "message_text",
            "text": "Hi, Alice",
            "attachment": str({})
        },
        {
            "message_id": 200,
            "chat_id": 2,
            "dispatch_time": "01.02.2023 14:17:16",
            "sender": "alice",
            "sender_id": 1000,
            "message_type": "message_text",
            "text": "Hello, world!",
            "attachment": str({})
        }
    ]
    for message in test_messages:
        await Message.create(**message)
    yield
    await Message.all().delete()


@pytest.fixture()
async def db_with_chats(create_test_db):
    test_chat_ids = [1, 2]
    for chat_id in test_chat_ids:
        await ActiveChat.create(chat_id=chat_id)
    yield
    await ActiveChat.all().delete()


@pytest.fixture()
async def db_with_states(create_test_db):
    test_states = [
        {
            "chat_id": 1,
            "user_id": 1000,
            "state": "RateTheBot:rate"
        },
        {
            "chat_id": 1,
            "user_id": 1001,
            "state": "RateTheBot:confirm"
        }
    ]
    for state in test_states:
        await CustomStorage.create(**state)
    yield
    await CustomStorage.all().delete()


async def stub_send_from_bot(chat_id: int, text: str):
    active_chats = [1, 2, 3]
    if not text.strip():
        return "Message can't be empty."
    if chat_id in active_chats:
        return "Done!"
