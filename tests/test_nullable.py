from typing import Optional

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, Session, SQLModel, create_engine


def test_nullable_fields_set_properly(clear_sqlmodel, caplog):
    class Hero(SQLModel, table=True):
        primary_key: Optional[int] = Field(
            default=None,
            primary_key=True,
        )
        required_value: str
        optional_non_nullable: Optional[str] = Field(
            nullable=False,
        )
        optional_default_ellipses_non_nullable: Optional[str] = Field(
            default=...,
            nullable=False,
        )
        optional_default_none_non_nullable: Optional[str] = Field(
            default=None,
            nullable=False,
        )
        default_ellipses_non_nullable: str = Field(default=..., nullable=False)
        optional_default_none_nullable: Optional[str] = Field(
            default=None,
            nullable=True,
        )

    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)

    create_table_log = [
        message for message in caplog.messages if "CREATE TABLE hero" in message
    ][0]
    assert "\n\tprimary_key INTEGER NOT NULL," in create_table_log
    assert "\n\trequired_value VARCHAR NOT NULL," in create_table_log
    assert (
        "\n\toptional_default_ellipses_non_nullable VARCHAR NOT NULL,"
        in create_table_log
    )
    assert (
        "\n\toptional_default_none_non_nullable VARCHAR NOT NULL," in create_table_log
    )
    assert "\n\tdefault_ellipses_non_nullable VARCHAR NOT NULL," in create_table_log
    assert "\n\toptional_default_none_nullable VARCHAR," in create_table_log


# Test for regression in https://github.com/tiangolo/sqlmodel/issues/420
def test_non_nullable_optional_field_with_no_default_set(clear_sqlmodel, caplog):
    class Hero(SQLModel, table=True):
        nullable_integer_primary_key: Optional[int] = Field(
            default=None,
            primary_key=True,
        )

        optional_non_nullable_no_default: Optional[str] = Field(nullable=False)

    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)

    create_table_log = [
        message for message in caplog.messages if "CREATE TABLE hero" in message
    ][0]
    assert "\n\tnullable_integer_primary_key INTEGER NOT NULL," in create_table_log
    assert "\n\toptional_non_nullable_no_default VARCHAR NOT NULL," in create_table_log

    # We can create a hero with `None` set for the optional non-nullable field
    hero = Hero(nullable_integer_primary_key=123, optional_non_nullable_no_default=None)
    # But we cannot commit it.
    with Session(engine) as session:
        session.add(hero)
        with pytest.raises(IntegrityError):
            session.commit()
