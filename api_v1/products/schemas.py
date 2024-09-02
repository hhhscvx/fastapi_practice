from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    desciption: str
    price: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductCreate):
    pass


class ProductUpdatePartial(ProductCreate):
    name: str | None = None
    desciption: str | None = None
    price: int | None = None


class Product(ProductBase):
    # преобразование объектов SQLAlchemy в Pydantic
    model_config = ConfigDict(from_attributes=True)

    id: int
