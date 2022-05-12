from decimal import Decimal
from pydantic import BaseModel, ValidationError
from typing import Optional


from utils import get_enum
from models.formats import Format



class ParentBase(BaseModel):

    name: Optional[str] = None
    description: Optional[str]

    class Config:
        orm_mode = True
        underscore_attrs_are_private = True


class Base(ParentBase):

    id: int



class TypeDecor(Base):

    _names = get_enum("typedecor_names", "TypeDecor")


class TypePlate(Base):

    _names = get_enum("typeplate_names", "TypePlate")


class Brand(Base):

    _names = get_enum("brand_names", "Brand")


class Maker(Base):

    _names = get_enum("brand_names", "Brand")
