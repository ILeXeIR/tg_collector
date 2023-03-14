import pytest

import src.bot.api
from testcases.conftest import stub_send_from_bot


class TestGetActiveChats():

    @pytest.mark.anyio
    async def test_get_active_chats(self, db_with_chats, ac, token):
        headers = {"Authorization": token}
        response = await ac.get("/bot/active_chats", headers=headers)
        assert response.status_code == 200
        assert response.json() == [1, 2]

    @pytest.mark.anyio
    async def test_get_active_chats_unauthorized(self, db_with_chats, ac):
        response = await ac.get("/bot/active_chats")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"


class TestGetAllStates():

    @pytest.mark.anyio
    async def test_get_all_states(self, db_with_states, ac, token):
        headers = {"Authorization": token}
        response = await ac.get("/bot/all_states", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert isinstance(response.json()[0]["id"], str)
        assert response.json()[0]["chat_id"] == 1
        assert response.json()[1]["user_id"] == 1001
        assert response.json()[1]["state"] == "RateTheBot:confirm"

    @pytest.mark.anyio
    async def test_get_all_states_unauthorized(self, db_with_states, ac):
        response = await ac.get("/bot/all_states")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"


class TestGetChatStates():

    @pytest.mark.anyio
    async def test_get_chat_states(self, db_with_states, ac, token):
        headers = {"Authorization": token}
        chat_id = 1
        response = await ac.get(f"/bot/chat_states/{chat_id}", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert isinstance(response.json()[0]["id"], str)
        assert response.json()[0]["chat_id"] == 1
        assert response.json()[1]["user_id"] == 1001
        assert response.json()[1]["state"] == "RateTheBot:confirm"

    @pytest.mark.anyio
    async def test_get_chat_states_unauthorized(self, db_with_states, ac):
        chat_id = 1
        response = await ac.get(f"/bot/chat_states/{chat_id}")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @pytest.mark.anyio
    async def test_get_chat_states_empty(self, db_with_states, ac, token):
        headers = {"Authorization": token}
        chat_id = 123
        response = await ac.get(f"/bot/chat_states/{chat_id}", headers=headers)
        assert response.status_code == 200
        assert response.json() == []


class TestSendInChat():

    @pytest.mark.anyio
    async def test_send_in_chat(self, ac, token, mocker):
        headers = {"Authorization": token}
        chat_id = 1
        text = "test text"
        mocker.patch.object(src.bot.api, "send_from_bot",
                            new=stub_send_from_bot)
        response = await ac.post(f"/bot/chat/{chat_id}", headers=headers,
                                     params={"text": text})
        assert response.status_code == 200
        assert response.json() == "Done!"

    @pytest.mark.anyio
    async def test_send_in_chat_unauthorized(self, ac):
        chat_id = 1
        text = "test text"
        response = await ac.post(f"/bot/chat/{chat_id}", params={"text": text})
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @pytest.mark.anyio
    async def test_send_empty_message(self, ac, token, mocker):
        headers = {"Authorization": token}
        chat_id = 1
        text = ""
        mocker.patch.object(src.bot.api, "send_from_bot",
                            new=stub_send_from_bot)
        response = await ac.post(f"/bot/chat/{chat_id}", headers=headers,
                                 params={"text": text})
        assert response.status_code == 200
        assert response.json() == "Message can't be empty."