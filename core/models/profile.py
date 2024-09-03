from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class Profile(UserRelationMixin, Base):
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    bio: Mapped[str | None]

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(first_name={self.first_name}, last_name={self.last_name}, bio={self.bio})'

    def __repr__(self) -> str:
        return str(self)
