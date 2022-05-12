from enum import Enum
from urllib.parse import parse_qsl

import tables
from database import get_session as s


def get_enum(value, tablename):
    return Enum(
        value=value,
        names=[
            (str(row.id), row.name) for row in
            next(s()).query(getattr(tables, tablename)).all()
        ]
    )


def get_data_from_query(query: str) -> dict:
    """
    "name=lamarty&id=2" --> {"name": "lamarty", "id": "2"}
    """
    data = dict(
        parse_qsl(query)
    )
    return data
