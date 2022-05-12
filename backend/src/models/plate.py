from pydantic import BaseModel
from typing import Optional

from . parents import TypePlate


class PlateBase(BaseModel):

    description: Optional[str] = None
    typeplate_id: Optional[int] = None
    thickness: int
    density: int

    class Config:
        orm_mode = True
        underscore_attrs_are_private = True


class Plate(PlateBase):

    id: int
    typeplate: TypePlate
