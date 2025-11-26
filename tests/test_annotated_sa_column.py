"""Tests for Annotated fields with sa_column and Pydantic validators.

When using Annotated[type, Field(sa_column=...), Validator(...)], Pydantic V2 may
create a new FieldInfo that doesn't preserve SQLModel-specific attributes like
sa_column. These tests ensure the sa_column is properly extracted from the
Annotated metadata.
"""

from datetime import datetime
from typing import Annotated, Optional

from pydantic import AfterValidator, BeforeValidator
from sqlalchemy import Column, DateTime, String
from sqlmodel import Field, SQLModel


def test_annotated_sa_column_with_validators() -> None:
    """Test that sa_column is preserved when using Annotated with validators."""

    def before_validate(v: datetime) -> datetime:
        return v

    def after_validate(v: datetime) -> datetime:
        return v

    class Position(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        timestamp: Annotated[
            datetime,
            Field(
                sa_column=Column(DateTime(timezone=True), nullable=False, index=True)
            ),
            BeforeValidator(before_validate),
            AfterValidator(after_validate),
        ]

    # Verify the column type has timezone=True
    assert Position.__table__.c.timestamp.type.timezone is True
    assert Position.__table__.c.timestamp.nullable is False
    assert Position.__table__.c.timestamp.index is True


def test_annotated_sa_column_with_single_validator() -> None:
    """Test sa_column with just one validator."""

    def validate_name(v: str) -> str:
        return v.strip()

    class Item(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: Annotated[
            str,
            Field(sa_column=Column(String(100), nullable=False, unique=True)),
            AfterValidator(validate_name),
        ]

    assert isinstance(Item.__table__.c.name.type, String)
    assert Item.__table__.c.name.type.length == 100
    assert Item.__table__.c.name.nullable is False
    assert Item.__table__.c.name.unique is True


def test_annotated_sa_column_without_validators() -> None:
    """Test that sa_column still works with Annotated but no validators."""

    class Record(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        created_at: Annotated[
            datetime,
            Field(sa_column=Column(DateTime(timezone=True), nullable=False)),
        ]

    assert Record.__table__.c.created_at.type.timezone is True
    assert Record.__table__.c.created_at.nullable is False


def test_annotated_sa_type_with_validators() -> None:
    """Test that sa_type is preserved when using Annotated with validators."""

    def validate_timestamp(v: datetime) -> datetime:
        return v

    class Event(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        occurred_at: Annotated[
            datetime,
            Field(sa_type=DateTime(timezone=True)),
            AfterValidator(validate_timestamp),
        ]

    # Verify the column type has timezone=True
    assert Event.__table__.c.occurred_at.type.timezone is True
