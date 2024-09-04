from typing import Annotated
import secrets

from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.security import (HTTPBasic,  # проверка авторизован ли request.user
                              HTTPBasicCredentials)  # Pydantic: username, password


router = APIRouter(prefix='/demo-auth', tags=["Demo Auth"])

security = HTTPBasic()


@router.get("/basic-auth/")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]  # пропускает только Authorized
):
    if credentials.username == "hhhscvx":
        return {
            "message": "Hi!",
            "username": credentials.username,
            "password": credentials.password,
        }
    return {"message": "pashol nahuy"}

# http://hhhscvx:passw@127.0.0.1:8000/api/v1/demo-auth/basic-auth/
# Первый раз логинишься - бразуер запоминает и некст тайм пробрасывает Authorization в Request (Закодированная Base64)
# echo aGhoc2N2eDpwYXNzdw== | base64 --decode


usernames_to_passwords = {
    "hhhscvx": "passw",
    "admin": "admin"
}


def get_auth_user_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> str:
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail="Invalid username or password",
                                 headers={"WWW-Authenticate": "Basic"})
    if credentials.username not in usernames_to_passwords:
        raise unauthed_exc

    correct_password = usernames_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc

    # secrets
    if not secrets.compare_digest(credentials.password.encode('utf-8'),
                                  correct_password.encode('utf-8')):
        raise unauthed_exc

    return credentials.username


@router.get('/basic-auth-username/')
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username)
):
    return {
        "message": "Hi!",
        "username": auth_username
    }


"""Token-Authorization"""

static_auth_token_to_username = {
    "XGwj645nfVNGV9wVBE": "фвьшт",
    "35vLuHVhWmtYsegHFD": "hhhscvx"
}


def get_username_by_static_auth_token(
        static_token: str = Header(alias="x-auth-token")  # В x-auth-token надо будет передать токен
) -> str:
    if username := static_auth_token_to_username.get(static_token):
        return username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token",
    )


@router.get('/some-http-header-auth/')
def demo_auth_some_http_header(
    username: str = Depends(get_username_by_static_auth_token)
):
    return {
        "message": f"Hi, {username}",
        "username": username
    }
