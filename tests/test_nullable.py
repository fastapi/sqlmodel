import pytest
from sqlalchemy import Engine, inspect
from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, Session, SQLModel, create_engine


def test_nullable_fields(database_engine: Engine):
    class Hero(SQLModel, table=True):
        primary_key: int | None = Field(
            default=None,
            primary_key=True,
        )
        required_value: str
        optional_default_ellipsis: str | None = Field(default=...)
        optional_default_none: str | None = Field(default=None)
        optional_non_nullable: str | None = Field(
            nullable=False,
        )
        optional_nullable: str | None = Field(
            nullable=True,
        )
        optional_default_ellipses_non_nullable: str | None = Field(
            default=...,
            nullable=False,
        )
        optional_default_ellipses_nullable: str | None = Field(
            default=...,
            nullable=True,
        )
        optional_default_none_non_nullable: str | None = Field(
            default=None,
            nullable=False,
        )
        optional_default_none_nullable: str | None = Field(
            default=None,
            nullable=True,
        )
        default_ellipses_non_nullable: str = Field(default=..., nullable=False)
        optional_default_str: str | None = "default"
        optional_default_str_non_nullable: str | None = Field(
            default="default", nullable=False
        )
        optional_default_str_nullable: str | None = Field(
            default="default", nullable=True
        )
        str_default_str: str = "default"
        str_default_str_non_nullable: str = Field(default="default", nullable=False)
        str_default_str_nullable: str = Field(default="default", nullable=True)
        str_default_ellipsis_non_nullable: str = Field(default=..., nullable=False)
        str_default_ellipsis_nullable: str = Field(default=..., nullable=True)

    engine = database_engine
    SQLModel.metadata.create_all(engine)

    nullable = {
        column["name"]: column["nullable"]
        for column in inspect(engine).get_columns("hero")
    }
    assert nullable == {
        "primary_key": False,
        "required_value": False,
        "optional_default_ellipsis": True,
        "optional_default_none": True,
        "optional_non_nullable": False,
        "optional_nullable": True,
        "optional_default_ellipses_non_nullable": False,
        "optional_default_ellipses_nullable": True,
        "optional_default_none_non_nullable": False,
        "optional_default_none_nullable": True,
        "default_ellipses_non_nullable": False,
        "optional_default_str": True,
        "optional_default_str_non_nullable": False,
        "optional_default_str_nullable": True,
        "str_default_str": False,
        "str_default_str_non_nullable": False,
        "str_default_str_nullable": True,
        "str_default_ellipsis_non_nullable": False,
        "str_default_ellipsis_nullable": True,
    }


# Test for regression in https://github.com/tiangolo/sqlmodel/issues/420
def test_non_nullable_optional_field_with_no_default_set(database_engine: Engine):
    class Hero(SQLModel, table=True):
        primary_key: int | None = Field(
            default=None,
            primary_key=True,
        )

        optional_non_nullable_no_default: str | None = Field(nullable=False)

    engine = database_engine
    SQLModel.metadata.create_all(engine)

    nullable = {
        column["name"]: column["nullable"]
        for column in inspect(engine).get_columns("hero")
    }
    assert nullable == {
        "primary_key": False,
        "optional_non_nullable_no_default": False,
    }

    # We can create a hero with `None` set for the optional non-nullable field
    hero = Hero(primary_key=123, optional_non_nullable_no_default=None)
    # But we cannot commit it.
    with Session(engine) as session:
        session.add(hero)
        with pytest.raises(IntegrityError):
            session.commit()


def test_sqlite_nullable_primary_key(clear_sqlmodel, caplog):
    # Probably the weirdest corner case, it shouldn't happen anywhere, but let's test it
    class Hero(SQLModel, table=True):
        nullable_integer_primary_key: int | None = Field(
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
