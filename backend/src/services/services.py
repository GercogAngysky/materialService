import models
import tables

from .base_services import BaseService


'''
сервисы по работе с отдельными таблицами базы данных,
методы позволяют получать, записывать, обновлять
и удалять записи
'''

class MakersService(BaseService):

    table = tables.Maker
    model = models.Maker
    basemodel = models.ParentBase


class BrandsService(BaseService):

    table = tables.Brand
    model = models.Brand
    basemodel = models.ParentBase


class TypeDecorsService(BaseService):

    table = tables.TypeDecor
    model = models.TypeDecor
    basemodel = models.ParentBase


class TypePlatesService(BaseService):

    table = tables.TypePlate
    model = models.TypePlate
    basemodel = models.ParentBase


class FormatsService(BaseService):

    table = tables.Format
    model = models.Format
    basemodel = models.FormatBase


class DecorsService(BaseService):

    table = tables.Decor
    model = models.Decor
    basemodel = models.DecorBase


class PlatesService(BaseService):

    table = tables.Plate
    model = models.Plate
    basemodel = models.PlateBase


class PricesService(BaseService):

    table = tables.Price
    model = models.Price
    basemodel = models.PriceBase


class MaterialsService(BaseService):

    table = tables.Material
    model = models.Material
    basemodel = models.MaterialBase

    def get_all(
        self,
        brand_id: int = None,
        format_id: int = None,
        typedecor_id: int = None,
        typeplate_id: int = None
    ) -> list[tables.Material]:
        materials  = (
            self.session.query(tables.Material)
        )
        if brand_id:
             materials = (
                materials.filter_by(brand_id=brand_id)
            )
        if format_id:
             materials = (
                materials.filter_by(format_id=format_id)
            )
        if typedecor_id:
            materials = (
                materials.join(tables.Decor)
                .filter(tables.Decor.typedecor_id==typedecor_id)
            )
        if typeplate_id:
             materials = (
                materials.join(tables.Plate)
                .filter_(tables.Plate.typeplate_id==typeplate_id)
            )
        return materials.all()
