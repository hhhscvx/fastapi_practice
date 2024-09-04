from typing import Annotated

from fastapi import APIRouter, Depends
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
