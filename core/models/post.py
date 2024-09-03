from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .user import User


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

    user: Mapped[User] = relationship(back_populates="posts") # как в джанго related_name)
