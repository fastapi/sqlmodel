import json
from datetime import date
from typing import Optional
from uuid import UUID

import pytest
from pydantic.error_wrappers import ValidationError
from sqlmodel import SQLModel

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
def test_validation_strict_mode(clear_sqlmodel):
    """Test validation of fields in strict mode from python and json."""
    from pydantic import TypeAdapter

    class Hero(SQLModel):
        id: Optional[int] = None
        birth_date: Optional[date] = None
        uuid: Optional[UUID] = None

        model_config = {"strict": True}

    date_obj = date(1970, 1, 1)
    date_str = date_obj.isoformat()
    uuid_obj = UUID("0ffef15c-c04f-4e61-b586-904ffe76c9b1")
    uuid_str = str(uuid_obj)

    Hero.model_validate({"id": 1, "birth_date": date_obj, "uuid": uuid_obj})
    TypeAdapter(Hero).validate_python(
        {"id": 1, "birth_date": date_obj, "uuid": uuid_obj}
    )
    # Check that python validation requires strict types
    with pytest.raises(ValidationError):
        Hero.model_validate({"id": "1"})
    with pytest.raises(ValidationError):
        Hero.model_validate({"birth_date": date_str})
    with pytest.raises(ValidationError):
        Hero.model_validate({"uuid": uuid_str})

    # Check that json is a bit more lax, but still refuses to "cast" values when not necessary
    Hero.model_validate_json(
        json.dumps({"id": 1, "birth_date": date_str, "uuid": uuid_str})
    )
    TypeAdapter(Hero).validate_json(
        json.dumps({"id": 1, "birth_date": date_str, "uuid": uuid_str})
    )
    with pytest.raises(ValidationError):
        Hero.model_validate_json(json.dumps({"id": "1"}))
