from typing import Annotated
from annotated_types import MaxLen, MinLen

from pydantic import BaseModel, ConfigDict, EmailStr


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(32)]
    email: EmailStr
    age: int


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)  # строгие аннотации
    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True
