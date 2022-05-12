from typing import Optional, Union
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException, Request
from sqlalchemy import exc

from loggers import get_logger
from utils import get_data_from_query
from database import get_session


logger = get_logger(__name__)


class BaseService:
    '''
    базовый метакласс по работе с таблицами базы данных,
    методы позволяют получать, записывать, обновлять
    и удалять записи
    '''

    table = None
    model = None
    basemodel = None

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session


    def get_one(
        self,
        query: Union[str, basemodel] = None
    ) -> Optional[table]:
        logger.info(
            f"get: {query}"
        )
        if query :
            try:
                if isinstance(query, str):
                    rows = (
                        self.session.query(self.table)
                        .filter_by(**get_data_from_query(query))
                    )
                else:
                    rows = (
                        self.session.query(self.table)
                        .filter_by(**query.dict())
                    )
            except exc.SQLAlchemyError as error:
                logger.error(
                    f"get: {error.__repr__()}, data: {query}"
                )
                raise HTTPException(
                    status
                    .HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=error.__repr__()
                )
        return rows.first()


    def get(
        self,
        query: str = None
    ) -> list[table]:
        logger.info(
            f"get: {query}"
        )
        rows = self.session.query(self.table)
        if query:
            try:
                rows = rows.filter_by(
                    **get_data_from_query(query)
                )
            except exc.SQLAlchemyError as error:
                logger.error(
                    f"get: {error.__repr__()}, data: {query}"
                )
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=error.__repr__()
                )
        return rows.all()


    def create(
        self,
        data: basemodel
    ) -> table:
        row = self.table(
            **data.dict()
        )
        self.session.add(row)
        logger.info(
            f"create: {data}"
        )
        self._commit(data=data)
        return row


    def update(
        self,
        id: int,
        data: basemodel
    ) -> table:
        row = self._get_by_id(id)
        for field, value in data:
            if value:
                setattr(row, field, value)
        logger.info(
            f"update: {data}"
        )
        self._commit(data=data)
        return row


    def delete(
        self,
        id: int,
    ):
        row = self._get_by_id(id)
        self.session.delete(row)
        self._commit(data=row)
        logger.info(
            f"delete: {row}"
        )
        return row


    def _get_by_id(
        self,
        id: int
    ) -> table:
        row = (
            self.session.query(self.table)
            .filter_by(id=id)
            .first()
        )
        if not row:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="Not found id"
            )
        return row


    def _commit(self, data=None):
        try:
            self.session.commit()
        except exc.SQLAlchemyError as error:
            logger.error(
                f"_commit: {error.__repr__()}, data: {data}"
            )
            self.session.rollback()
            raise HTTPException(
                status
                .HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error.__repr__()
            )
