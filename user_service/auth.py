import jwt
from datetime import timedelta, datetime
from config import TokenConfig


def generate_token(
    payload: dict,
    exp: timedelta,
    private_key: str = TokenConfig.private_key,
    algorithm: str = TokenConfig.algorithm,
) -> str:
    to_encode = payload.copy()
    to_encode["exp"] = datetime.utcnow() + exp

    token = jwt.encode(to_encode, private_key, algorithm)
    return token


def decode_token(
    token: str,
    public_key: str = TokenConfig.public_key,
    algorithm: str = TokenConfig.algorithm,
) -> dict:
    return jwt.decode(token, public_key, algorithms=[algorithm])


def generate_access_token(
    payload: dict,
    exp: timedelta = TokenConfig.AccessToken.expire_min,
    private_key: str = TokenConfig.private_key,
    algorithm: str = TokenConfig.algorithm,
):
    to_encode = payload.copy()
    to_encode["type"] = "access"

    return generate_token(
        payload=to_encode, exp=exp, private_key=private_key, algorithm=algorithm
    )


def generate_refresh_token(
    payload: dict,
    exp: timedelta = TokenConfig.RefreshToken.expire_min,
    private_key: str = TokenConfig.private_key,
    algorithm: str = TokenConfig.algorithm,
):
    to_encode = payload.copy()
    to_encode["type"] = "refresh"
    return generate_token(
        payload=to_encode, exp=exp, private_key=private_key, algorithm=algorithm
    )

