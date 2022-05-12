from pydantic import BaseModel, ValidationError
from typing import Optional

from .parents import Brand, Format
from .plate import Plate
from .decor import Decor



class MaterialBase(BaseModel):

    description: Optional[str] = None
    brand_id: Optional[int] = None
    format_id: Optional[int] = None
    plate_id: Optional[int] = None
    decor_id: Optional[int] = None

    class Config:
        orm_mode = True
        underscore_attrs_are_private = True


class Material(MaterialBase):

    id: int
    brand: Optional[Brand]
    format: Optional[Format]
    plate: Optional[Plate]
    decor: Optional[Decor]
