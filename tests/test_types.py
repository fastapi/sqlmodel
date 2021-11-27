import ipaddress
import uuid
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum, auto
from pathlib import Path
from typing import Optional

import pytest
from pydantic import BaseModel

from sqlmodel import Field, Session, SQLModel, create_engine


class HeroEnum(Enum):
    SPIDER_MAN = auto()
    BAT_MAN = auto()


types_values = [
    str("Hero"),
    float(0.5),
    int(5),
    datetime(year=2020, month=2, day=2, hour=2, minute=2, second=2, microsecond=2),
    date(year=2020, month=2, day=2),
    timedelta(days=2, seconds=2, microseconds=2, milliseconds=2, minutes=2, hours=2, weeks=2),
    time(hour=2, minute=2, second=2, microsecond=2),
    HeroEnum.SPIDER_MAN, HeroEnum.BAT_MAN,
    bytes(b'2020-hero'),
    Decimal(2),
    ipaddress.IPv4Address('192.168.0.1'),
    ipaddress.IPv4Network('192.0.2.0/28'),
    ipaddress.IPv6Address('2001:db8::'),
    ipaddress.IPv6Network('2001:db8::1000/124'),
    Path('/etc'),
    uuid.UUID(bytes=b'hero' * 4),
]


def skip_conditions(object_value):
    object_type = type(object_value)
    if issubclass(object_type, BaseModel) and object_type.__custom_root_type__:
        object_type_checks = object_type.__fields__['__root__'].type_
    else:
        object_type_checks = object_type

    if issubclass(object_type_checks, Enum):
        pytest.skip("Enums require changing sa_column, it will be tested in "
                    "https://github.com/tiangolo/sqlmodel/pull/165 for now they will be skipped")

    if any(issubclass(object_type_checks, cls) for cls in [ipaddress.IPv4Address, ipaddress.IPv4Network,
                                                           ipaddress.IPv6Address, ipaddress.IPv6Network]):
        pytest.skip("ip addressees are not natively supported types in sqlite")

    if issubclass(object_type_checks, Path):
        pytest.skip("Path is not supported in sqlite")


def table_creation_and_selection_with_types(object_value):
    skip_conditions(object_value)

    class Item(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        object: type(object_value)

    item = Item(object=object_value)
    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)

    with Session(engine) as session:
        query_hero = session.query(Item).first()
        assert type(query_hero.object) is type(item.object)
        assert query_hero.object == item.object

    SQLModel.metadata.clear()


@pytest.mark.parametrize("object_value", types_values)
def test_non_basemodel_types(object_value):
    table_creation_and_selection_with_types(object_value)


@pytest.mark.parametrize("object_value", types_values)
def test_basemodel_types(object_value):
    class ItemModel(BaseModel):
        __root__: type(object_value)

    table_creation_and_selection_with_types(ItemModel.parse_obj(object_value))
