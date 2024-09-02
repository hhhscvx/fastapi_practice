from random import randint
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from core.models import Base, db_helper
from items_views import router as items_router
from users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # создание таблиц, дочерних от Base

    yield  # До yield - что-то для настройки, после yield - удаление ненужного


app = FastAPI(lifespan=lifespan)  # lifespan - настройка/запуск чего-то при запуске приложения

app.include_router(items_router)
app.include_router(users_router)


@app.get('/')
def get_number():
    return {"message": "Hello!"}


@app.get('/number/')
def get_number():
    return {"number": randint(1, 10)}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
