from random import randint
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from items_views import router as items_router
from users.views import router as users_router
from api_v1 import router as router_v1
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield  # До yield - что-то для настройки, после yield - удаление ненужного


app = FastAPI(lifespan=lifespan)  # lifespan - настройка/запуск чего-то при запуске приложения

app.include_router(items_router)
app.include_router(users_router)
app.include_router(router_v1, prefix=settings.api_v1_prefix)


@app.get('/')
def get_number():
    return {"message": "Hello!"}


@app.get('/number/')
def get_number(max_num: int):
    return {"number": randint(1, max_num)}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
