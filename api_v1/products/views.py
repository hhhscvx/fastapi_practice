from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial
from core.models import db_helper
from .dependencies import get_product_by_id

router = APIRouter(tags=['Products'])


@router.get('/', response_model=list[Product])
async def get_products(
    session: AsyncSession = Depends(db_helper.scope_session_dependency)
):  # сессию получаем из db_helper
    return await crud.get_products(session=session)


# [response_model]: FastAPI сверит, что возвращаемое значение соответствует данной Pydantic-модели
@router.post('/', response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.scope_session_dependency)
):
    return await crud.create_product(session, product_in)


@router.get('/{product_id}/', response_model=Product)
async def get_product(product: Product = Depends(get_product_by_id)):
    return product


@router.put('/{product_id}/', response_model=Product)
async def update_product(product_update: ProductUpdate,
                         product: Product = Depends(get_product_by_id),  # product_id передастся из Path (гениально)
                         session: AsyncSession = Depends(db_helper.scope_session_dependency)):
    return await crud.update_product(session, product=product, product_update=product_update)


@router.patch('/{product_id}/', response_model=Product)
async def update_product_partial(product_update: ProductUpdatePartial,
                                 # product_id передастся из Path (гениально)
                                 product: Product = Depends(get_product_by_id),
                                 session: AsyncSession = Depends(db_helper.scope_session_dependency)):
    return await crud.update_product(session,
                                     product=product,
                                     product_update=product_update,
                                     partial=True)


@router.delete('/{product_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product: Product = Depends(get_product_by_id),
                         session: AsyncSession = Depends(db_helper.scope_session_dependency)
                         ) -> None:
    await crud.delete_product(session, product=product)
