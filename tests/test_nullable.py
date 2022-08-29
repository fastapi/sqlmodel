from typing import Optional

import pytest
from sqlalchemy.exc import InterfaceError
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel, create_engine


def test_nullable_fields_set_properly(clear_sqlmodel, caplog):
    class Hero(SQLModel, table=True):
        nullable_integer_primary_key: Optional[int] = Field(
            default=None, primary_key=True
        )
        nullable_optional_string: Optional[str] = Field(default=None, nullable=True)
        nullable_integer: Optional[int] = None
        not_null_string: str = Field(default=..., nullable=False)
        not_null_integer: int

    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)

    create_table_log = [
        message for message in caplog.messages if "CREATE TABLE hero" in message
    ][0]
    assert "\n\tnullable_integer_primary_key INTEGER NOT NULL," in create_table_log
    assert "\n\tnot_null_string VARCHAR NOT NULL," in create_table_log
    assert "\n\tnullable_optional_string VARCHAR," in create_table_log
    assert "\n\tnullable_integer INTEGER," in create_table_log
    assert "\n\tnot_null_integer INTEGER NOT NULL," in create_table_log

    # Ensure we cannot create a hero with `None` set for not-nullable-fields:
    hero = Hero(not_null_integer=None, not_null_string=None)
    with Session(engine) as session:
        session.add(hero)
        with pytest.raises(InterfaceError):
            session.commit()
