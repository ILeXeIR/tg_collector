from fastapi import HTTPException
import pytest


class TestGetUsers():

    @pytest.mark.anyio
    async def test_get_users(self, db_with_users, ac, token):
        headers = {"Authorization": token}
        response = await ac.get("/users/", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["username"] == "user1"
        assert response.json()[1]["real_name"] == "User B"

    @pytest.mark.anyio
    async def test_get_users_unauthorized(self, db_with_users, ac):
        response = await ac.get("/users/")
        assert response.status_code == 401


class TestLogin():

    @pytest.mark.anyio
    async def test_login(self, db_with_users, ac):
        response = await ac.post(
            "/users/login",
            data={"username": "user1", "password": "qwerty123"}
        )
        assert response.status_code == 200
        assert response.json()["token_type"] == "bearer"
        assert isinstance(response.json()["access_token"], str)

    @pytest.mark.anyio
    async def test_login_unknown_user(self, db_with_users, ac):
        response = await ac.post(
                "/users/login",
                data={"username": "user100", "password": "qwerty123"}
            )
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect username or password"

    @pytest.mark.anyio
    async def test_login_wrong_password(self, db_with_users, ac):
        response = await ac.post(
            "/users/login",
            data={"username": "user1", "password": "qwerty"}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect username or password"

    @pytest.mark.anyio
    async def test_login_wrong_password2(self, db_with_users, ac):
        with pytest.raises(HTTPException) as e:
            await ac.post(
                "/users/login",
                data={"username": "user1", "password": "qwerty"}
            )
        assert isinstance(e.value, HTTPException)
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Incorrect username or password"