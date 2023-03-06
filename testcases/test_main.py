import pytest


@pytest.mark.anyio
async def test_read_root(ac):
    response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"Connection": "Success"}


@pytest.mark.anyio
async def test_get_users(db_with_users, ac):
    response = await ac.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["username"] == "user1"
    assert response.json()[1]["real_name"] == "User B"

"""
def test_login(db_with_users):
    response = client.post(
        "/users/login/",
        json={"username": "user1", "password": "qwerty123"}
    )
    assert response.status_code == 200
    assert response.json().token_type == "bearer"
"""