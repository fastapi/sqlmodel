from typing import Optional

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, Session, SQLModel, create_engine


def test_nullable_fields_set_properly(clear_sqlmodel, caplog):
    class Hero(SQLModel, table=True):
        # Uses Field
        nullable_integer_primary_key: Optional[int] = Field(
            default=None,
            primary_key=True,
        )
        non_nullable_integer_with_field: int = Field(default=..., nullable=False)

        # Does not use Field
        nullable_integer: Optional[int] = None
        non_nullable_integer: int

        # Uses Field
        non_nullable_optional_string_with_field: Optional[str] = Field(
            default=..., nullable=False
        )
        non_nullable_optional_string_with_field_no_default_set: Optional[str] = Field(
            nullable=False
        )
        non_nullable_optional_string_with_field_with_default: Optional[str] = Field(
            default=None, nullable=False
        )
        non_nullable_string_with_field: str = Field(default=..., nullable=False)

        # Does not use Field
        nullable_optional_string: Optional[str] = Field(default=None, nullable=True)
        non_nullable_string: str

    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)

    create_table_log = [
        message for message in caplog.messages if "CREATE TABLE hero" in message
    ][0]
    assert "\n\tnullable_integer_primary_key INTEGER NOT NULL," in create_table_log
    assert "\n\tnullable_integer INTEGER," in create_table_log
    assert "\n\tnon_nullable_integer INTEGER NOT NULL," in create_table_log
    assert "\n\tnon_nullable_integer_with_field INTEGER NOT NULL," in create_table_log

    assert "\n\tnullable_optional_string VARCHAR," in create_table_log
    assert (
        "\n\tnon_nullable_optional_string_with_field VARCHAR NOT NULL,"
        in create_table_log
    )
    assert (
        "\n\tnon_nullable_optional_string_with_field_no_default_set VARCHAR NOT NULL,"
        in create_table_log
    )
    assert (
        "\n\tnon_nullable_optional_string_with_field_with_default VARCHAR NOT NULL,"
        in create_table_log
    )
    assert "\n\tnon_nullable_string VARCHAR NOT NULL," in create_table_log
    assert "\n\tnon_nullable_string_with_field VARCHAR NOT NULL," in create_table_log


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

    # We can create a hero with `None` set for the optional non-nullable field,
    # but we cannot commit it.
    hero = Hero(nullable_integer_primary_key=123, optional_non_nullable_no_default=None)
    with Session(engine) as session:
        session.add(hero)
        with pytest.raises(IntegrityError):
            session.commit()
