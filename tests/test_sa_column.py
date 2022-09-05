"""These test cases should become obsolete once `sa_column`-parameters are dropped from `Field`."""

import pytest
from pydantic.config import BaseConfig
from pydantic.fields import ModelField
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlmodel.main import Field, FieldInfo, get_column_from_field


def test_sa_column_params_raise_warnings():
    with pytest.warns(DeprecationWarning):
        Field(sa_column=Column())
    with pytest.warns(DeprecationWarning):
        Field(sa_column_args=[ForeignKey("foo.id"), CheckConstraint(">1")])
    with pytest.warns(DeprecationWarning):
        Field(sa_column_kwargs={"name": "foo"})


def test_sa_column_overrides_other_params():
    col = Column()
    field = ModelField(
        name="foo",
        type_=str,
        class_validators=None,
        model_config=BaseConfig,
        field_info=FieldInfo(
            index=True,  # should be ignored
            sa_column=col,
        ),
    )
    output = get_column_from_field(field)
    assert output is col
    assert output.index is None
