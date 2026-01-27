import pytest


@pytest.mark.asyncio
async def test_signup_and_login(client):
    signup_response = await client.post(
        "/auth/signup",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@gmail.com",
            "password": "StrongPass123",
        },
    )

    assert signup_response.status_code == 201

    login_response = await client.post(
        "/auth/login",
        json={
            "email": "testuser@gmail.com",
            "password": "StrongPass123",
        },
    )

    # User not approved yet
    assert login_response.status_code == 403
    