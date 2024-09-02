from random import randint

from fastapi import FastAPI
from pydantic import EmailStr, BaseModel
import uvicorn


app = FastAPI()


class CreateUser(BaseModel):
    name: str
    email: str
    age: int


@app.get('/')
def get_number():
    return {"message": "Hello!"}


@app.get('/number/')
def get_number():
    return {"number": randint(1, 10)}


items = [
    'Item1',
    'Item2',
    'Item3'
]


@app.get('/items/')
def get_items():
    return items


@app.get('/items/latest/')
def get_items_latest():
    return {"result": items[-1]}


@app.get('/items/{item_id}/')
def item_detail(item_id: int, title: str = "Untitled"):
    return {"item": {"id": item_id, "title": title}}


@app.post('/users/')
def create_user(user: CreateUser):
    return {
        "message": "success",
        "user": {
            "name": user.name,
            "email": user.email,
            "age": user.age
        }
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
