from pydantic import BaseModel
from typing import Optional


class FormatBase(BaseModel):

    length: Optional[int]
    width: Optional[int]

    class Config:
        orm_mode = True
        underscore_attrs_are_private = True


class Format(FormatBase):

    id: int = None
    