from typing import Annotated

from fastapi import APIRouter, Path


router = APIRouter(prefix='/items', tags=["Items"])


items = [
    'Item1',
    'Item2',
    'Item3'
]


@router.get('/')
def get_items():
    return items


@router.get('/latest/')
def get_items_latest():
    return {"result": items[-1]}


@router.get('/{item_id}/')
def item_detail(item_id: Annotated[int, Path(..., gt=0, lt=1_000_000)], name: str = "NoName"):
    return {"item": {"id": item_id, "name": name}}
