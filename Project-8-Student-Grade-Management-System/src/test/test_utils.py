from src.auth.utils import get_hash_password, verify_password, create_access_token, decode_token


def test_password_hashing():
    password = "secret123"
    hashed = get_hash_password(password)

    assert hashed is not None
    assert verify_password(password, hashed)


def test_jwt_token_creation_and_decode():
    token = create_access_token(
        user_data={"email": "test@test.com", "user_id": "123", "role": "student"}
    )

    decoded = decode_token(token)
    assert decoded["user"]["email"] == "test@test.com"
