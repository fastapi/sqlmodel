import copy
import datetime
import ipaddress
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import sqlalchemy as sa
import sqlmodel.main
from pydantic import BaseModel
from sqlalchemy.engine.mock import MockConnection
from sqlmodel import AutoString, Field, SQLModel
from sqlmodel.sql.sqltypes import PydanticJSONType


def get_engine(url: str) -> MockConnection:
    engine = sa.create_mock_engine(
        url, lambda sql, *args, **kwargs: print(sql.compile(dialect=engine.dialect))
    )

    return engine


def test_string_length_constraint(clear_sqlmodel, capsys):
    class StrTest(SQLModel, table=True):
        id: str = Field(default=None, primary_key=True, max_length=10)

    SQLModel.metadata.create_all(get_engine("sqlite://"))
    captured = capsys.readouterr()

    assert "id VARCHAR(10) NOT NULL," in captured.out


def test_native_uuid_column_mapping(clear_sqlmodel, capsys):
    class UuidTest(SQLModel, table=True):
        id: UUID = Field(default=None, primary_key=True)

    assert isinstance(UuidTest.id.type, sa.Uuid)

    SQLModel.metadata.create_all(get_engine("sqlite://"))
    captured = capsys.readouterr()

    assert "id CHAR(32) NOT NULL" in captured.out

    SQLModel.metadata.create_all(get_engine("postgresql://"))
    captured = capsys.readouterr()

    assert "id UUID NOT NULL" in captured.out

    SQLModel.metadata.create_all(get_engine("mssql://"))
    captured = capsys.readouterr()

    assert "id UNIQUEIDENTIFIER NOT NULL" in captured.out

    SQLModel.metadata.create_all(get_engine("mysql://"))
    captured = capsys.readouterr()

    assert "id CHAR(32) NOT NULL" in captured.out


def test_default_sa_types_to_python_mapping_is_correct(clear_sqlmodel, capsys):
    class Parent(BaseModel):
        name: str
        sex: str
        birth_date: datetime.date

    class Hero(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        global_hero_id: UUID
        name: str
        birth_date: datetime.date
        birth_time: datetime.time
        created_at: datetime.datetime
        last_seen_delta: datetime.timedelta
        salary: Decimal
        speed: float
        is_on_vacation: bool
        dna_marker_data: bytes
        headquarter_ip_v4: ipaddress.IPv4Address
        headquarter_ip_v6: ipaddress.IPv6Address
        shared_folder_path: Path
        mother: Parent
        father: Parent

    SQLModel.metadata.create_all(get_engine("sqlite://"))
    captured = capsys.readouterr()

    assert isinstance(Hero.id.type, sa.Integer)
    assert "id INTEGER NOT NULL" in captured.out

    assert isinstance(Hero.global_hero_id.type, sa.Uuid)
    assert "global_hero_id CHAR(32) NOT NULL" in captured.out

    assert isinstance(Hero.name.type, AutoString)
    assert "name VARCHAR NOT NULL" in captured.out

    assert isinstance(Hero.birth_date.type, sa.Date)
    assert "birth_date DATE NOT NULL" in captured.out

    assert isinstance(Hero.birth_time.type, sa.Time)
    assert "birth_time TIME NOT NULL" in captured.out

    assert isinstance(Hero.created_at.type, sa.DateTime)
    assert "created_at DATETIME NOT NULL" in captured.out

    assert isinstance(Hero.last_seen_delta.type, sa.Interval)
    assert "created_at DATETIME NOT NULL" in captured.out

    assert isinstance(Hero.salary.type, sa.Numeric)
    assert "salary NUMERIC NOT NULL" in captured.out

    assert isinstance(Hero.speed.type, sa.Float)
    assert "speed FLOAT NOT NULL" in captured.out

    assert isinstance(Hero.is_on_vacation.type, sa.Boolean)
    assert "is_on_vacation BOOLEAN NOT NULL" in captured.out

    assert isinstance(Hero.dna_marker_data.type, sa.LargeBinary)
    assert "dna_marker_data BLOB NOT NULL" in captured.out

    assert isinstance(Hero.headquarter_ip_v4.type, AutoString)
    assert "headquarter_ip_v4 VARCHAR NOT NULL" in captured.out

    assert isinstance(Hero.headquarter_ip_v6.type, AutoString)
    assert "headquarter_ip_v6 VARCHAR NOT NULL" in captured.out

    assert isinstance(Hero.shared_folder_path.type, AutoString)
    assert "shared_folder_path VARCHAR NOT NULL" in captured.out

    assert isinstance(Hero.mother.type, PydanticJSONType)
    assert "mother JSON NOT NULL" in captured.out

    assert isinstance(Hero.father.type, PydanticJSONType)
    assert "father JSON NOT NULL" in captured.out


def test_default_sa_type_mapping_change(clear_sqlmodel, capsys):
    base_map = copy.deepcopy(sqlmodel.main.sa_types_map)
    sqlmodel.main.sa_types_map[str] = lambda type_, meta, annotation: sa.Unicode(
        length=getattr(meta, "max_length", None)
    )

    class Hero(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str = Field(max_length=255)
        history: str

    assert str(Hero.name.type) == str(sa.Unicode(255))
    assert str(Hero.history.type) == str(sa.Unicode())

    SQLModel.metadata.create_all(get_engine("mssql://"))
    captured = capsys.readouterr()

    assert "name NVARCHAR(255) NOT NULL" in captured.out
    assert "history NVARCHAR(max) NOT NULL" in captured.out

    SQLModel.metadata.create_all(get_engine("sqlite://"))
    captured = capsys.readouterr()

    assert "name VARCHAR(255) NOT NULL" in captured.out
    assert "history VARCHAR NOT NULL" in captured.out

    sqlmodel.main.sa_types_map = base_map
