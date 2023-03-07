import pytest


@pytest.mark.anyio
async def test_read_root(ac):
    response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"Connection": "Success"}
