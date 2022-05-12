from fastapi import Depends

from .base_routers import BaseRouter
from services import *


class MakersRouter(BaseRouter):

    # tablename = "maker"
    services = MakersService


class BrandsRouter(BaseRouter):

    # tablename = "brand"
    services = BrandsService


class TypeDecorsRouter(BaseRouter):

    # tablename = "typedecor"
    services = TypeDecorsService


class TypePlatesRouter(BaseRouter):

    # tablename = "typeplate"
    services = TypePlatesService


class FormatsRouter(BaseRouter):

    # tablename = "format"
    services = FormatsService


class DecorsRouter(BaseRouter):

    # tablename = "decor"
    services = DecorsService


class PlatesRouter(BaseRouter):

    # tablename = "plate"
    services = PlatesService


class PricesRouter(BaseRouter):

    # tablename = "price"
    services = PricesService


class MaterialsRouter(BaseRouter):

    # tablename="materials"
    services=MaterialsService

    def __init__(self):
        super().__init__()
        @self.get(
            path="/filter/",
            response_model=list[self.model],
        )
        def get_all(
            brand_id: int = None,
            format_id: int = None,
            typedecor_id: int = None,
            typeplate_id: int = None,
            service: self.services = Depends()
        ):
            return service.get_all(brand_id, format_id, typedecor_id, typeplate_id)
