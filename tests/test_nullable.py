from typing import Optional

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, Session, SQLModel, create_engine


def test_nullable_fields(clear_sqlmodel, caplog):
    class Hero(SQLModel, table=True):
        primary_key: Optional[int] = Field(
            default=None,
            primary_key=True,
        )
        required_value: str
        optional_default_ellipsis: Optional[str] = Field(default=...)
        optional_default_none: Optional[str] = Field(default=None)
        optional_non_nullable: Optional[str] = Field(
            nullable=False,
        )
        optional_nullable: Optional[str] = Field(
            nullable=True,
        )
        optional_default_ellipses_non_nullable: Optional[str] = Field(
            default=...,
            nullable=False,
        )
        optional_default_ellipses_nullable: Optional[str] = Field(
            default=...,
            nullable=True,
        )
        optional_default_none_non_nullable: Optional[str] = Field(
            default=None,
            nullable=False,
        )
        optional_default_none_nullable: Optional[str] = Field(
            default=None,
            nullable=True,
        )
        default_ellipses_non_nullable: str = Field(default=..., nullable=False)
        optional_default_str: Optional[str] = "default"
        optional_default_str_non_nullable: Optional[str] = Field(
            default="default", nullable=False
        )
        optional_default_str_nullable: Optional[str] = Field(
            default="default", nullable=True
        )
        str_default_str: str = "default"
        str_default_str_non_nullable: str = Field(default="default", nullable=False)
        str_default_str_nullable: str = Field(default="default", nullable=True)
        str_default_ellipsis_non_nullable: str = Field(default=..., nullable=False)
        str_default_ellipsis_nullable: str = Field(default=..., nullable=True)

    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)

    create_table_log = [
        message for message in caplog.messages if "CREATE TABLE hero" in message
    ][0]
    assert "primary_key INTEGER NOT NULL," in create_table_log
    assert "required_value VARCHAR NOT NULL," in create_table_log
    assert "optional_default_ellipsis VARCHAR," in create_table_log
    assert "optional_default_none VARCHAR," in create_table_log
    assert "optional_non_nullable VARCHAR NOT NULL," in create_table_log
    assert "optional_nullable VARCHAR," in create_table_log
    assert (
        "optional_default_ellipses_non_nullable VARCHAR NOT NULL," in create_table_log
    )
    assert "optional_default_ellipses_nullable VARCHAR," in create_table_log
    assert "optional_default_none_non_nullable VARCHAR NOT NULL," in create_table_log
    assert "optional_default_none_nullable VARCHAR," in create_table_log
    assert "default_ellipses_non_nullable VARCHAR NOT NULL," in create_table_log
    assert "optional_default_str VARCHAR," in create_table_log
    assert "optional_default_str_non_nullable VARCHAR NOT NULL," in create_table_log
    assert "optional_default_str_nullable VARCHAR," in create_table_log
    assert "str_default_str VARCHAR NOT NULL," in create_table_log
    assert "str_default_str_non_nullable VARCHAR NOT NULL," in create_table_log
    assert "str_default_str_nullable VARCHAR," in create_table_log
    assert "str_default_ellipsis_non_nullable VARCHAR NOT NULL," in create_table_log
    assert "str_default_ellipsis_nullable VARCHAR," in create_table_log


# Test for regression in https://github.com/tiangolo/sqlmodel/issues/420
def test_non_nullable_optional_field_with_no_default_set(clear_sqlmodel, caplog):
    class Hero(SQLModel, table=True):
        primary_key: Optional[int] = Field(
            default=None,
            primary_key=True,
        )

        optional_non_nullable_no_default: Optional[str] = Field(nullable=False)

    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)

    create_table_log = [
        message for message in caplog.messages if "CREATE TABLE hero" in message
    ][0]
    assert "primary_key INTEGER NOT NULL," in create_table_log
    assert "optional_non_nullable_no_default VARCHAR NOT NULL," in create_table_log

    # We can create a hero with `None` set for the optional non-nullable field
    hero = Hero(primary_key=123, optional_non_nullable_no_default=None)
    # But we cannot commit it.
    with Session(engine) as session:
        session.add(hero)
        with pytest.raises(IntegrityError):
            session.commit()


def test_nullable_primary_key(clear_sqlmodel, caplog):
    # Probably the weirdest corner case, it shouldn't happen anywhere, but let's test it
    class Hero(SQLModel, table=True):
        nullable_integer_primary_key: Optional[int] = Field(
            default=None,
            primary_key=True,
            nullable=True,
        )

    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)

    create_table_log = [
        message for message in caplog.messages if "CREATE TABLE hero" in message
    ][0]
    assert "nullable_integer_primary_key INTEGER," in create_table_log
