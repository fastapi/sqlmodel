from typing import Optional

import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel

from .conftest import needs_pydanticv1, needs_pydanticv2


@needs_pydanticv1
def test_allow_instantiation_without_arguments_pydantic_v1(clear_sqlmodel):
    class Item(SQLModel):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        description: Optional[str] = None

        class Config:
            table = True

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db:
        item = Item()
        item.name = "Rick"
        db.add(item)
        db.commit()
        result = db.execute(select(Item)).scalars().all()
    assert len(result) == 1
    assert isinstance(item.id, int)
    SQLModel.metadata.clear()


def test_not_allow_instantiation_without_arguments_if_not_table():
    class Item(SQLModel):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        description: Optional[str] = None

    with pytest.raises(ValidationError):
        Item()


@needs_pydanticv2
def test_allow_instantiation_without_arguments_pydnatic_v2(clear_sqlmodel):
    class Item(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        description: Optional[str] = None

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db:
        item = Item()
        item.name = "Rick"
        db.add(item)
        db.commit()
        result = db.execute(select(Item)).scalars().all()
    assert len(result) == 1
    assert isinstance(item.id, int)
    SQLModel.metadata.clear()
