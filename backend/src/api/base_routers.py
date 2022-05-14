from urllib import response
from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse

from models import *
from services import allow_create_items, allow_get_items, allow_delete_items, allow_update_items

class BaseRouter(APIRouter):

    # tablename = None
    services = None

    def __init__(self):
        super().__init__(
            prefix = f"/{self.services.table.__tablename__}",
            tags = [self.services.table.__tablename__,],
            # default_response_class=JSONResponse
        )
        self.basemodel = self.services.basemodel
        self.model = self.services.model
        self.fields = self.services.model.__fields__.keys()


        @self.get(
            path="/",
            response_model=list[self.model]
        )
        def get(
            query: str = None,
            service: self.services = Depends(),
            allowed: allow_get_items = Depends()
        ):
            """
            метод принимает в "query" сроку типа:
            "name%3Dlamarty%26id%3D2" <--(name=lamarty&id=2)
            с параметрами для фильтрации, при отсутствии
            параметров - возвращает список всех записей из таблицы
            """
            return service.get(query)


        @self.post(
            path="/",
            response_model=self.model,
            status_code=status.HTTP_201_CREATED
        )
        def create(
            data: self.basemodel,
            service: self.services = Depends(),
            allowed: allow_create_items = Depends()
        ):
            return service.create(data)


        @self.put(
            path="/{id}",
            response_model=self.model
        )
        def update(
            id: int,
            data: self.basemodel,
            service: self.services = Depends(),
            allowed: allow_update_items = Depends()
        ):
            return service.update(id, data)


        @self.delete(
            path="/{id}",
            status_code=status.HTTP_204_NO_CONTENT
        )
        def delete(
            id: int,
            service: self.services = Depends(),
            allowed: allow_delete_items = Depends()
        ):
            service.delete(id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
