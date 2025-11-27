import jwt
import uuid
import logging

from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext

from src.config.config import config

"""
    Using Argon2 for password hashin. It is a function to hash the password
"""
password_context = CryptContext(schemes=['argon2'],
                                deprecated="auto")


ACCESS_TOKEN_EXPIRY_SECONDS = 3600      


"""
    Hashing plain-text password using argon2 algorithm 
"""
def get_hash_password(password: str) -> str:
    try:
        return password_context.hash(password)
    
    except Exception as e:
        logging.error(f"Password must be string, failed to generate hash.Error: {e}")
        

"""
    Password Verification
"""
def verify_password(password:str, password_hash:str) -> bool:
    return password_context.verify(password, password_hash)


"""
    Creating access token using JWT
"""
def create_access_token(user_data: dict, expiry: timedelta | None=None) -> bool:
    payload: dict = {}
    
    payload['jwt'] = str(uuid.uuid4())
    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY_SECONDS))
    
    token = jwt.encode(payload = payload,
                       key = config.JWT_SECRET,
                       algorithm=config.JWT_ALGORITHM)
    
    return token


"""
    Decoding JWT access tokens
"""
def decode_token(token: str) -> dict | None:
    try:
        token_data = jwt.decode(jwt=token,
                                key=config.JWT_SECRET,
                                algorithms=[config.JWT_ALGORITHM])
        
        return token_data
    
    except PyJWTError as e:
        logging.exception(e)
        return  None