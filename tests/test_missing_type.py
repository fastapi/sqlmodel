from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


def test_custom_type_works(clear_sqlmodel):
    """Test that custom Pydantic types are now supported in SQLModel table classes."""

    class CustomType(BaseModel):
        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def validate(cls, v):  # pragma: no cover
            return v

    # Should not raise an error and should create a table column
    class Item(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        item: CustomType

    assert "item" in Item.__table__.columns

    # Can create an instance
    custom_data = CustomType()
    item = Item(item=custom_data)
    assert isinstance(item.item, CustomType)
