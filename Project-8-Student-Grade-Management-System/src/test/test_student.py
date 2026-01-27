import pytest


@pytest.mark.asyncio
async def test_admin_create_student(client):
    # Admin login (auto-created in lifespan)
    login = await client.post(
        "/auth/login",
        json={
            "email": "admin@example.com",
            "password": "admin123",
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post(
        "/students/add",
        json={"name": "Rahul Sharma"},
        headers=headers,
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Rahul Sharma"
