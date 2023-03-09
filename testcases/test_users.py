from fastapi import HTTPException
import pytest

from src.users.dao import User
from src.users.security import hash_password, verify_password


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
        assert response.json()["detail"] == "Not authenticated"


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

"""
    @pytest.mark.anyio
    async def test_login_wrong_password2(self, db_with_users, ac):
        with pytest.raises(HTTPException) as e:
            await ac.post(
                "/users/login",
                data={"username": "user1", "password": "qwerty"}
            )
        assert isinstance(e.value, HTTPException)
        assert e.value.status_code == 401
        assert e.value.detail == "Incorrect username or password"
"""

class TestGetUserByID():

    @pytest.mark.anyio
    async def test_get_user_by_id(self, db_with_users, ac, token):
        headers = {"Authorization": token}
        new_user = {
            "username": "user3",
            "email": "user3@example.com",
            "real_name": "User C",
            "password_hash": hash_password("qwerty123")
        }
        test_user = await User.create(**new_user)
        response = await ac.get(f"/users/id/{test_user.id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["username"] == new_user["username"]
        assert response.json()["email"] == new_user["email"]
        assert response.json()["real_name"] == new_user["real_name"]
        assert response.json()["password_hash"] == new_user["password_hash"]

    @pytest.mark.anyio
    async def test_get_user_by_id_unauthorized(self, db_with_users, ac):
        new_user = {
            "username": "user3",
            "email": "user3@example.com",
            "real_name": "User C",
            "password_hash": hash_password("qwerty123")
        }
        test_user = await User.create(**new_user)
        response = await ac.get(f"/users/id/{test_user.id}")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @pytest.mark.anyio
    async def test_get_user_by_id_with_fake_id(self, db_with_users, ac, token):
        headers = {"Authorization": token}
        fake_id = "fakeid"
        response = await ac.get(f"/users/id/{fake_id}", headers=headers)
        assert response.status_code == 400
        assert response.json()["detail"] == "User not found"

    @pytest.mark.anyio
    async def test_get_user_by_id_with_fake_id_unauthorized(self, db_with_users, ac):
        fake_id = "fakeid"
        response = await ac.get(f"/users/id/{fake_id}")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"


class TestGetUserByEmail():

    @pytest.mark.anyio
    async def test_get_user_by_email(self, db_with_users, ac, token):
        headers = {"Authorization": token}
        test_email = "user1@example.com"
        response = await ac.get(f"/users/email/{test_email}", headers=headers)
        assert response.status_code == 200
        assert response.json()["username"] == "user1"
        assert response.json()["email"] == "user1@example.com"
        assert response.json()["real_name"] == "User A"
        assert verify_password("qwerty123", response.json()["password_hash"])

    @pytest.mark.anyio
    async def test_get_user_by_id_unauthorized(self, db_with_users, ac):
        test_email = "user1@example.com"
        response = await ac.get(f"/users/email/{test_email}")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @pytest.mark.anyio
    async def test_get_user_by_id_with_fake_email(self, db_with_users, ac, token):
        headers = {"Authorization": token}
        fake_email = "fakeemail@example.com"
        response = await ac.get(f"/users/id/{fake_email}", headers=headers)
        assert response.status_code == 400
        assert response.json()["detail"] == "User not found"


class TestGetMyUser():
    @pytest.mark.anyio
    async def test_get_my_user(self, db_with_users, ac, token):
        headers = {"Authorization": token}
        response = await ac.get("/users/me", headers=headers)
        assert response.status_code == 200
        assert response.json()["username"] == "user2"
        assert response.json()["email"] == "user2@example.com"
        assert response.json()["real_name"] == "User B"
        assert verify_password("qwerty123", response.json()["password_hash"])

    @pytest.mark.anyio
    async def test_get_my_user_unauthorized(self, db_with_users, ac):
        response = await ac.get("/users/me")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @pytest.mark.anyio
    async def test_get_my_user_fake_token(self, db_with_users, ac):
        fake_token = "Bearer faketoken"
        headers = {"Authorization": fake_token}
        response = await ac.get("/users/me", headers=headers)
        print(response.headers)
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid authentication credentials"
