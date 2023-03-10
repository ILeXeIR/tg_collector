import pytest

from src.collector.dao import Message
from src.settings import settings


class TestGetMessages():

    @pytest.mark.anyio
    async def test_get_messages(self, db_with_messages, ac, token):
        headers = {"Authorization": token}
        response = await ac.get("/messages/", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) == 3
        assert response.json()[0]["message_id"] == 100
        assert response.json()[1]["dispatch_time"] == "01.02.2023 14:16:16"
        assert response.json()[2]["text"] == "Hello, world!"
        assert isinstance(response.json()[0]["id"], str)

    @pytest.mark.anyio
    async def test_get_messages_unauthorized(self, db_with_messages, ac):
        response = await ac.get("/messages/")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"


class TestGetListOfChats():

    @pytest.mark.anyio
    async def test_get_list_of_chats(self, db_with_messages, ac, token):
        headers = {"Authorization": token}
        response = await ac.get("/messages/chats", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert response.json() == [1, 2]

    @pytest.mark.anyio
    async def test_get_list_of_chats_unauthorized(self, db_with_messages, ac):
        response = await ac.get("/messages/chats")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"


class TestGetChatMessages():

    @pytest.mark.anyio
    async def test_get_chat_messages(self, db_with_messages, ac, token):
        headers = {"Authorization": token}
        chat_id = 1
        response = await ac.get(f"/messages/chat_objects/{chat_id}",
                                headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 2
        assert isinstance(response.json()[0], dict)
        assert response.json()[1]["message_id"] == 101

    @pytest.mark.anyio
    async def test_get_chat_messages_unauthorized(self, db_with_messages, ac):
        chat_id = 1
        response = await ac.get(f"/messages/chat_objects/{chat_id}")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @pytest.mark.anyio
    async def test_get_chat_messages_unknown_chat(self, db_with_messages,
                                                  ac, token):
        headers = {"Authorization": token}
        chat_id = 12345
        response = await ac.get(f"/messages/chat_objects/{chat_id}",
                                headers=headers)
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.anyio
    async def test_get_chat_messages_incorrect_chat_id(self, db_with_messages,
                                                       ac, token):
        headers = {"Authorization": token}
        chat_id = "text_id"
        response = await ac.get(f"/messages/chat_objects/{chat_id}",
                                headers=headers)
        assert response.status_code == 422
        error_text = "value is not a valid integer"
        assert response.json()["detail"][0]["msg"] == error_text

class TestSaveMessage():

    update = {
        "update_id": 1234,
        "message": {
            "message_id": 300,
            "chat": {"id": 3, "type": "supergroup"},
            "date": 1677837600,
            "from": {
                "username": "john",
                "id": 1002,
                "is_bot": False,
                "first_name": "John"
            },
            "content_type": "text",
            "text": "Ho Ho Ho"
        }
    }

    @pytest.mark.anyio
    async def test_save_messages(self, db_with_messages, ac):
        webhook_token = settings.WEBHOOK_TOKEN
        headers = {"X-Telegram-Bot-Api-Secret-Token": webhook_token}
        response = await ac.post("/messages/", headers=headers,
                                 json=self.update)
        assert response.status_code == 200
        message = await Message.filter(message_id=300).first()
        assert message.message_id == 300
        assert message.attachment["message"]["message_id"] ==300
        assert message.chat_id == 3
        assert message.sender == "john"
        assert message.sender_id == 1002
        assert message.text == "Ho Ho Ho"
        assert message.message_type == "message_text"

    @pytest.mark.anyio
    async def test_save_messages_incorrect_webhook_token(self, db_with_messages,
                                                         ac):
        webhook_token = "fake_token"
        headers = {"X-Telegram-Bot-Api-Secret-Token": webhook_token}
        response = await ac.post("/messages/", headers=headers,
                                 json=self.update)
        assert response.status_code == 200
        message = await Message.filter(message_id=300).first()
        assert message is None

    @pytest.mark.anyio
    async def test_save_messages_without_webhook_token(self, db_with_messages,
                                                       ac):
        response = await ac.post("/messages/", json=self.update)
        assert response.status_code == 200
        message = await Message.filter(message_id=300).first()
        assert message is None

