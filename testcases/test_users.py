# from fastapi import HTTPException
import pytest

from src.users.dao import User
from src.users.models import UserRq
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
    async def test_get_user_by_id_with_fake_id_unauthorized(self, db_with_users,
                                                            ac):
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
    async def test_get_user_by_id_with_fake_email(self, db_with_users, ac,
                                                  token):
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
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid authentication credentials"


class TestCreateUser():

    @pytest.mark.anyio
    async def test_create_user(self, db_with_users, ac, token):
        new_user = UserRq(
            username="user3",
            email="user3@example.com",
            real_name="User C",
            password="qwerty123",
            password2="qwerty123"
        )
        headers = {"Authorization": token}
        response = await ac.post("/users/", headers=headers,
                                 json=new_user.dict())
        assert response.status_code == 200
        assert response.json()["username"] == "user3"
        assert verify_password("qwerty123", response.json()["password_hash"])

    @pytest.mark.anyio
    async def test_create_user_unauthorized(self, db_with_users, ac):
        new_user = UserRq(
            username="user3",
            email="user3@example.com",
            real_name="User C",
            password="qwerty123",
            password2="qwerty123"
        )
        response = await ac.post("/users/", json=new_user.dict())
        assert response.status_code == 200
        assert response.json()["username"] == "user3"
        assert verify_password("qwerty123", response.json()["password_hash"])

    @pytest.mark.anyio
    async def test_create_user_without_real_name(self, db_with_users, ac):
        new_user = UserRq(
            username="user3",
            email="user3@example.com",
            password="qwerty123",
            password2="qwerty123"
        )
        response = await ac.post("/users/", json=new_user.dict())
        assert response.status_code == 200
        assert response.json()["username"] == "user3"
        assert response.json()["real_name"] is None

    @pytest.mark.anyio
    async def test_create_user_with_wrong_password2(self, db_with_users, ac):
        new_user = {
            "username": "user3",
            "email": "user3@example.com",
            "real_name": "User C",
            "password": "qwerty123",
            "password2": "qwerty1234"
        }
        response = await ac.post("/users/", json=new_user)
        assert response.status_code == 400
        assert response.json()["detail"] == "passwords don't match"

    @pytest.mark.anyio
    async def test_create_user_duplicate_username(self, db_with_users, ac):
        new_user = UserRq(
            username="user1",
            email="user3@example.com",
            real_name="User C",
            password="qwerty123",
            password2="qwerty123"
        )
        response = await ac.post("/users/", json=new_user.dict())
        assert response.status_code == 400
        assert response.json()["detail"] == "Username and Email must be unique"

    @pytest.mark.anyio
    async def test_create_user_duplicate_email(self, db_with_users, ac):
        new_user = UserRq(
            username="user3",
            email="user1@example.com",
            real_name="User C",
            password="qwerty123",
            password2="qwerty123"
        )
        response = await ac.post("/users/", json=new_user.dict())
        assert response.status_code == 400
        assert response.json()["detail"] == "Username and Email must be unique"


class TestUpdateUser():

    @pytest.mark.anyio
    async def test_update_user(self, db_with_users, ac, token):
        user_update = UserRq(
            username="user2_new",
            email="user2_new@example.com",
            real_name="User Bbbb",
            password="qwerty456",
            password2="qwerty456"
        )
        headers = {"Authorization": token}
        response = await ac.put("/users/", headers=headers,
                                json=user_update.dict())
        assert response.status_code == 200
        assert response.json()["username"] == "user2_new"
        assert response.json()["email"] == "user2_new@example.com"
        assert response.json()["real_name"] == "User Bbbb"
        assert verify_password("qwerty456", response.json()["password_hash"])

    @pytest.mark.anyio
    async def test_update_user_unauthorized(self, db_with_users, ac):
        user_update = UserRq(
            username="user2_new",
            email="user2_new@example.com",
            real_name="User Bbbb",
            password="qwerty456",
            password2="qwerty456"
        )
        response = await ac.put("/users/", json=user_update.dict())
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @pytest.mark.anyio
    async def test_update_user_without_real_name(self, db_with_users,
                                                 ac, token):
        user_update = UserRq(
            username="user2_new",
            email="user2_new@example.com",
            password="qwerty456",
            password2="qwerty456"
        )
        headers = {"Authorization": token}
        response = await ac.put("/users/", headers=headers,
                                json=user_update.dict())
        assert response.status_code == 200
        assert response.json()["username"] == "user2_new"
        assert response.json()["real_name"] is None

    @pytest.mark.anyio
    async def test_update_user_with_wrong_password2(self, db_with_users,
                                                    ac, token):
        user_update = {
            "username": "user2_new",
            "email": "user2_new@example.com",
            "password": "qwerty456",
            "password2": "qwerty1234"
        }
        headers = {"Authorization": token}
        response = await ac.put("/users/", headers=headers,
                                json=user_update)
        assert response.status_code == 400
        assert response.json()["detail"] == "passwords don't match"

    @pytest.mark.anyio
    async def test_update_user_duplicate_username(self, db_with_users,
                                                  ac, token):
        user_update = UserRq(
            username="user1",
            email="user2_new@example.com",
            real_name="User Bbbb",
            password="qwerty456",
            password2="qwerty456"
        )
        headers = {"Authorization": token}
        response = await ac.put("/users/", headers=headers,
                                json=user_update.dict())
        assert response.status_code == 400
        assert response.json()["detail"] == "Username and Email must be unique"

    @pytest.mark.anyio
    async def test_update_user_duplicate_email(self, db_with_users,
                                               ac, token):
        user_update = UserRq(
            username="user2_new",
            email="user1@example.com",
            real_name="User Bbbb",
            password="qwerty456",
            password2="qwerty456"
        )
        headers = {"Authorization": token}
        response = await ac.put("/users/", headers=headers,
                                json=user_update.dict())
        assert response.status_code == 400
        assert response.json()["detail"] == "Username and Email must be unique"

    @pytest.mark.anyio
    async def test_update_user_without_changes(self, db_with_users, ac, token):
        user_update = UserRq(
            username="user2",
            email="user2@example.com",
            real_name="User B",
            password="qwerty123",
            password2="qwerty123"
        )
        headers = {"Authorization": token}
        response = await ac.put("/users/", headers=headers,
                                json=user_update.dict())
        assert response.status_code == 200
        assert response.json()["username"] == "user2"
        assert response.json()["email"] == "user2@example.com"
        assert response.json()["real_name"] == "User B"
        assert verify_password("qwerty123", response.json()["password_hash"])