from fastapi import HTTPException, Depends
import jwt
from config import TokenConfig
from typing import Annotated
from uuid import uuid4


def decode_token(
    token: str,
    public_key: str = TokenConfig.public_key,
    algorithm: str = TokenConfig.algorithm,
) -> dict:

    return jwt.decode(token, public_key, algorithms=[algorithm])


def access_token_check(access_token: str) -> dict:
    """If token is valid, function returns token payload"""
    try:
        payload = decode_token(access_token)
        assert payload["type"] == "access"
        return payload
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


access_token = Annotated[dict, Depends(access_token_check)]


def generate_uuid() -> str:
    return str(uuid4())

