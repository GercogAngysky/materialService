from pydantic import BaseModel
from typing import Optional

from .parents import TypeDecor


class DecorBase(BaseModel):

    name: Optional[str] = None
    img: Optional[str] = None
    description: Optional[str] = None
    typedecor_id: Optional[int] = None

    class Config:
        orm_mode = True
        underscore_attrs_are_private = True


class Decor(DecorBase):

    id: int
    typedecor: Optional[TypeDecor]
