from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Post(Base):
    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(
        type_=Text,
        default="",  # дефолт значение, если создаем через алхимию
        server_default=""  # дефолт значение, даже если создадим через базу
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        # nullable=False
    )
