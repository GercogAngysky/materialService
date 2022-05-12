from typing import BinaryIO, Optional
from fastapi import Depends
import csv
import re

import models
import services as s
from loggers import get_logger

logger = get_logger(__name__)


# фабрики:
MAKERS = {
    'MG': 'мебельгрупп',
    'SQ': 'квадрат'
}

# плотность кг/м3
DENSITY = {
    'лдсп': 680,
    'мдф': 750,
    'двпо': 600,
    'двп': 600,
}

class ItemFromCsv:
    '''
    парсинг и преобразование данных словаря(строка из csv),
    создает объект с атрибутами для дальнейшей записи в базу данных  
    '''

    def __init__(self):
        pass

    def read(self, row: dict):
        self._row = row
        self.maker = models.ParentBase(
            name = MAKERS['MG']
        )
        self.typedecor = models.ParentBase(
            name = row['decor'].lower()
        )
        self.format = models.FormatBase.parse_obj(
            self._get_length_width(row['name'])
        )
        self.typeplate = models.ParentBase(
            name = self._get_typeplate(row['name'])
        )
        self.brand = models.ParentBase(
            name = row['maker'].lower()
        )
        self.decor = models.DecorBase(
            name = row['name'].lower(),
            img = row['img_url']
            # typedecor_id = None
        )
        self.plate = models.PlateBase(
            thickness = row['thickness'].lower(),
            density = DENSITY[self.typeplate.name],
            # typeplate_id = None
        )
        self.material = models.MaterialBase(
            # brand_id = None,
            # format_id = None,
            # plate_id = None,
            # decor_id = None,
        )
        self.price = models.PriceBase(
            description = row['url'],
            measure = self._get_measure(row['measure']) or 'not info',
            value = self._get_price(row['price']),
            currency = '₽',
            # maker_id = None,
            # material_id = None
        )
        # self.url = row['url'],

    def _get_price(self, row: str):
        price = row.replace(" ", "").replace(",", ".")
        try:
            price = int(price)
        except Exception:
            price = 0
        return price

    def _uniformize_string(self, raw_str: str = "") -> Optional[str]:
        """ затирание лишних символов """
        result = re.sub(r"\n*|\t*|(^\W+)|(\W+$)*?", "", raw_str)
        return result.lower()

    def _get_typeplate(self, st: str) -> Optional[str]:
        result = re.search(r"лдсп|двпо|мдфо|двп|мдф", st.lower())
        return result and result.group()

    def _get_length_width(self, st: str) -> dict:
        result = re.search(r"\d+\*\d+\*\d+", st.lower())
        if result:
            result = result.group().split("*")[:2]
            return dict(zip(('length', 'width'), result))
        else:
            return {'length': 0, 'width': 0}

    def _get_measure(self, st: str) -> Optional[str]:
        result = re.search(r"лист|кв.м", st.lower())
        return result and result.group()



class WriterMaterial:

    def __init__(
        self,
        service_typedecor: s.TypeDecorsService = Depends(),
        service_format: s.FormatsService = Depends(),
        service_typeplate: s.TypePlatesService = Depends(),
        service_brand: s.BrandsService = Depends(),
        service_maker: s.MakersService = Depends(),
        service_decor: s.DecorsService = Depends(),
        service_plate: s.PlatesService = Depends(),
        service_material: s.MaterialsService = Depends(),
        service_price: s.PricesService = Depends()
    ):
        self.service_typedecor = service_typedecor
        self.service_format = service_format
        self.service_typeplate = service_typeplate
        self.service_brand = service_brand
        self.service_maker = service_maker
        self.service_decor = service_decor
        self.service_plate = service_plate
        self.service_material = service_material
        self.service_price = service_price


    def _get_or_create(self, service: s, model: models):
        row = (
            service.get_one(model)
            or 
            service.create(model)
        )
        return row


    def add_in_db(self, item):
        self.item = item

        self.typedecor = self._get_or_create(self.service_typedecor, self.item.typedecor)
        self.format = self._get_or_create(self.service_format, self.item.format)
        self.typeplate = self._get_or_create(self.service_typeplate, self.item.typeplate)
        self.brand = self._get_or_create(self.service_brand, self.item.brand)
        self.maker = self._get_or_create(self.service_maker, self.item.maker)

        self.item.decor.typedecor_id = self.typedecor.id
        self.decor = self._get_or_create(self.service_decor, self.item.decor)

        self.item.plate.typeplate_id = self.typeplate.id
        self.plate = self._get_or_create(self.service_plate, self.item.plate)

        self.item.material.brand_id = self.brand.id
        self.item.material.format_id = self.format.id
        self.item.material.plate_id = self.plate.id
        self.item.material.decor_id = self.decor.id
        self.material = self._get_or_create(self.service_material, self.item.material)

        self.item.price.maker_id = self.maker.id
        self.item.price.material_id = self.material.id
        # self.item.price.description = self.item.url
        self.price = self._get_or_create(self.service_price, self.item.price)



class ReportsService:

    def __init__(
        self,
        writer: WriterMaterial = Depends(),
        item: ItemFromCsv = Depends()
    ):
        self.item = item
        self.writer = writer
        self.field_names = (
            'maker',
            'url',
            'img_url',
            'name',
            'thickness',
            'decor',
            'price',
            'currency',
            'measure',
            'in_stock'
        )

    def import_csv(self, file: BinaryIO):
        reader = csv.DictReader(
            (line.decode() for line in file),
            fieldnames = self.field_names
        )
        next(reader, None) # skip the header
        for row in reader:
            try:
                self.item.read(row)
                self.writer.add_in_db(self.item)
            except Exception:
                continue
