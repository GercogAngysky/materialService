from decimal import Decimal
from enum import Enum
from pydantic import BaseModel
from typing import Optional

from .materials import Material
from .parents import Maker


# class Measure(Enum):

#     PLATE = "лист"
#     AREA = "кв.м"
#     AMOUNT = "шт."


class PriceBase(BaseModel):

    description: Optional[str] = None
    measure: Optional[str] = None           # Measure = None
    value: Optional[Decimal] = None
    currency: Optional[str] = "₽"
    maker_id: Optional[int] = None
    material_id: Optional[int] = None

    class Config:
        orm_mode = True
        underscore_attrs_are_private = True


class Price(PriceBase):

    id: int
    maker: Optional[Maker]
    material: Optional[Material]
