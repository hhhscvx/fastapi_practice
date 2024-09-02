
from fastapi import APIRouter

from .schemas import CreateUser


router = APIRouter(prefix='/users', tags=["Users"])


@router.post('/')
def create_user(user: CreateUser):
    return {
        "message": "success",
        "user": {
            "username": user.username,
            "email": user.email,
            "age": user.age
        }
    }
