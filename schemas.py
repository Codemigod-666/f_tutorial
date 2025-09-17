from pydantic import BaseModel

class ProductBase(BaseModel):
    # id: str
    name: str
    description: str
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode =True