from fastapi.testclient import TestClient
import pytest
# from starlette.websockets import WebSocketDisconnect

from main import app
from src.collector.dao import Message
import src.websocket.api
from src.websocket.deps import manager
from testcases.conftest import stub_send_from_bot


class TestWebsocketChat():

    @pytest.mark.anyio
    async def test_websocket_active_connections(self, token):
        assert manager.active_connections == []
        chat_id = 1
        headers = {"Authorization": token}
        client = TestClient(app)
        with client.websocket_connect(f"/ws/{chat_id}", headers=headers):
            assert len(manager.active_connections) == 1
            assert manager.active_connections[0]["chat_id"] == 1

    @pytest.mark.anyio
    async def test_websocket_get_messages(self, db_with_messages, token):
        chat_id = 1
        headers = {"Authorization": token}
        client = TestClient(app)
        with client.websocket_connect(f"/ws/{chat_id}", headers=headers) as ws:
            data = ws.receive_json()
            assert data["text"] == "Hi, Bob"
            data = ws.receive_json()
            assert data["text"] == "Hi, Alice"

    @pytest.mark.anyio
    async def test_websocket_send_message(self, token, mocker):
        chat_id = 1
        text = "my test"
        headers = {"Authorization": token}
        mocker.patch.object(src.websocket.api, "send_from_bot",
                            new=stub_send_from_bot)
        client = TestClient(app)
        with client.websocket_connect(f"/ws/{chat_id}", headers=headers) as ws:
            ws.send_text(text)
            data = ws.receive_text()
            assert data == f"Your message was sent:\n'{text}'"

    @pytest.mark.anyio
    async def test_websocket_send_empty_message(self, token, mocker):
        chat_id = 1
        text = ""
        headers = {"Authorization": token}
        mocker.patch.object(src.websocket.api, "send_from_bot",
                            new=stub_send_from_bot)
        client = TestClient(app)
        with client.websocket_connect(f"/ws/{chat_id}", headers=headers) as ws:
            ws.send_text(text)
            data = ws.receive_text()
            assert data == "Error:\nMessage can't be empty."

    @pytest.mark.anyio
    async def test_websocket_receive_new_message(self, db_with_messages, token):
        chat_id = 3
        text = "New message test"
        headers = {"Authorization": token}
        new_message = Message(
            message_id=110,
            chat_id=chat_id,
            dispatch_time="02.02.2023 14:15:16",
            sender="alice",
            sender_id=1000,
            message_type="message_text",
            text=text,
            attachment=str({})
        )
        client = TestClient(app)
        with client.websocket_connect(f"/ws/{chat_id}", headers=headers) as ws:
            await manager.broadcast(message=new_message, chat_id=chat_id)
            data = ws.receive_json()
            assert data["message_id"] == new_message.message_id
            assert data["text"] == text


"""
    @pytest.mark.anyio
    async def test_websocket_unauthorized(self):
        chat_id = 1
        client = TestClient(app)
        with client.websocket_connect(f"/ws/{chat_id}") as ws:
            pass
"""
