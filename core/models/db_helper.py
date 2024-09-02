from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from core.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,  # подготовка к коммиту
            autocommit=False,
            expire_on_commit=False
        )


db_helper = DatabaseHelper(url=settings.db_url, echo=settings.db_echo)

# 24:20 остановился фокуса нет
