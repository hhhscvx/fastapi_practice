from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True  # не сохраняем в БД

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Автогенерация __tablename__ для таблиц"""
        return f'{cls.__name__.lower()}s'

    id: Mapped[int] = mapped_column(primary_key=True)
