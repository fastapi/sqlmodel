from typing import Optional

import pytest
from sqlmodel import Field, SQLModel


class FooMixin:
    pass


@pytest.mark.usefixtures("clear_sqlmodel")
def test_mixin():
    """Test SQLModel in combination with a mixin.

    https://github.com/tiangolo/sqlmodel/issues/254

    """

    class Hero(FooMixin, SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        secret_name: str
        age: Optional[int] = None
