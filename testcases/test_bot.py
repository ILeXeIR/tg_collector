import pytest


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
