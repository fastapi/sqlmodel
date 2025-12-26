"""Test that Python type annotations map to correct SQLAlchemy column types"""

from typing import Dict, Optional

from sqlalchemy import JSON, Boolean, Date, DateTime, Float, Integer
from sqlalchemy.sql.sqltypes import LargeBinary
from sqlmodel import Field, SQLModel
from sqlmodel.sql.sqltypes import AutoString
from typing_extensions import TypedDict

from .conftest import needs_pydanticv2


def test_type_mappings(clear_sqlmodel):
    from datetime import date, datetime

    class Model(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        count: int
        price: float
        active: bool
        created: datetime
        birth_date: date
        data_bytes: bytes

    # Verify the type mappings
    assert isinstance(Model.name.type, AutoString)  # type: ignore
    assert isinstance(Model.count.type, Integer)  # type: ignore
    assert isinstance(Model.price.type, Float)  # type: ignore
    assert isinstance(Model.active.type, Boolean)  # type: ignore
    assert isinstance(Model.created.type, DateTime)  # type: ignore
    assert isinstance(Model.birth_date.type, Date)  # type: ignore
    assert isinstance(Model.data_bytes.type, LargeBinary)  # type: ignore


@needs_pydanticv2
def test_dict_maps_to_json(clear_sqlmodel):
    """Test that plain dict annotation maps to JSON column type"""

    class Model(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        data: dict

    assert isinstance(Model.data.type, JSON)  # type: ignore


@needs_pydanticv2
def test_typing_dict_maps_to_json(clear_sqlmodel):
    class Model(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        data: Dict[str, int]

    assert isinstance(Model.data.type, JSON)  # type: ignore


@needs_pydanticv2
def test_typeddict_maps_to_json(clear_sqlmodel):
    class MyDict(TypedDict):
        name: str
        count: int

    class Model(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        data: MyDict

    assert isinstance(Model.data.type, JSON)  # type: ignore
