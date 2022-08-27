from typing import Optional

import pytest
from sqlmodel import Field, SQLModel


def test_missing_sql_type():
    class CustomType:
        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def validate(cls, v):
            return v

    with pytest.raises(ValueError):

        class Item(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            item: CustomType
