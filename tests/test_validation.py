from typing import Optional

import pytest
from pydantic.error_wrappers import ValidationError
from sqlmodel import Field, SQLModel

from .conftest import needs_pydanticv1, needs_pydanticv2


@needs_pydanticv1
def test_validation_pydantic_v1(clear_sqlmodel):
    """Test validation of implicit and explicit None values.

    # For consistency with pydantic, validators are not to be called on
    # arguments that are not explicitly provided.

    https://github.com/tiangolo/sqlmodel/issues/230
    https://github.com/samuelcolvin/pydantic/issues/1223

    """
    from pydantic import validator

    class Hero(SQLModel):
        name: Optional[str] = None
        secret_name: Optional[str] = None
        age: Optional[int] = None

        @validator("name", "secret_name", "age")
        def reject_none(cls, v):
            assert v is not None
            return v

    Hero.validate({"age": 25})

    with pytest.raises(ValidationError):
        Hero.validate({"name": None, "age": 25})


@needs_pydanticv2
def test_validation_pydantic_v2(clear_sqlmodel):
    """Test validation of implicit and explicit None values.

    # For consistency with pydantic, validators are not to be called on
    # arguments that are not explicitly provided.

    https://github.com/tiangolo/sqlmodel/issues/230
    https://github.com/samuelcolvin/pydantic/issues/1223

    """
    from pydantic import field_validator

    class Hero(SQLModel):
        name: Optional[str] = None
        secret_name: Optional[str] = None
        age: Optional[int] = None

        @field_validator("name", "secret_name", "age")
        def reject_none(cls, v):
            assert v is not None
            return v

    Hero.model_validate({"age": 25})

    with pytest.raises(ValidationError):
        Hero.model_validate({"name": None, "age": 25})


@needs_pydanticv2
def test_validation_with_table_true():
    """Test validation with table=True."""
    from pydantic import field_validator

    class Hero(SQLModel, table=True):
        name: Optional[str] = Field(default=None, primary_key=True)
        secret_name: Optional[str] = None
        age: Optional[int] = None

        @field_validator("age", mode="after")
        @classmethod
        def double_age(cls, v):
            if v is not None:
                return v * 2
            return v

    Hero(name="Deadpond", age=25)
    Hero.model_validate({"name": "Deadpond", "age": 25})
    with pytest.raises(ValidationError):
        Hero(name="Deadpond", secret_name="Dive Wilson", age="test")
    with pytest.raises(ValidationError):
        Hero.model_validate({"name": "Deadpond", "age": "test"})

    double_age_hero = Hero(name="Deadpond", age=25)
    assert double_age_hero.age == 50

    double_age_hero = Hero.model_validate({"name": "Deadpond", "age": 25})
    assert double_age_hero.age == 50
