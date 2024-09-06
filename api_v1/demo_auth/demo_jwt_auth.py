from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from users.schemas import UserSchema
from auth import utils_jwt as auth_utils

http_bearer = HTTPBearer()


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="/jwt", tags=["JWT"])


john = UserSchema(
    username="John",
    password=auth_utils.hash_password('qwerty'),
    email="john@example.com")

hhhscvx = UserSchema(
    username="John",
    password=auth_utils.hash_password('y3ahnothack'),
    email="hhhscvx@yandex.ru")

users_db: dict[str, UserSchema] = {
    'john': john,
    'hhhscvx': hhhscvx
}


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
) -> UserSchema:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password"
    )
    if (user_db := users_db.get(username)) is None:
        raise unauthed_exc
    if not auth_utils.validate_password(password, user_db.password):
        raise unauthed_exc
    if not user_db.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive"
        )

    return user_db


def get_current_active_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> UserSchema:
    print('++++ 2')
    jwt_token = credentials.credentials
    print(jwt_token)


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_active_user)
):
    print('++++ 1')
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive"
    )


@router.post('/login/')
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user)
):
    jwt_payload = {
        # subject - определитель, про что это поле (если есть id юзается id)
        'sub': user.username,
        'username': user.username,
        'email': user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )


@router.get('/users/me/')
def auth_user_get_me(
    user: UserSchema = Depends(get_current_active_auth_user)
):
    return {
        "username": user.username,
        "email": user.email,
    }
