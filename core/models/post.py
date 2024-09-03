from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class Post(UserRelationMixin, Base):
    _user_back_populates = "posts"

    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(
        type_=Text,
        default="",  # дефолт значение, если создаем через алхимию
        server_default=""  # дефолт значение, даже если создадим через базу
    )
