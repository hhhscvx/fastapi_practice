from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.models import db_helper

from . import crud


async def get_product_by_id(product_id: int = Path,
                            session: AsyncSession = Depends(db_helper.scope_session_dependency),
                            ):  # Path -> параметр будет извлечен из урла
    """
    Используется через Depends(), следовательно передавать никакие аргументы не надо

    :param int product_id: берется из урла: /{product_id}/
    :param AsyncSession session: берется из Depends db_helper
    """
    product = await crud.get_product(session, product_id=product_id)
    if product is not None:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} Not Found"
    )
