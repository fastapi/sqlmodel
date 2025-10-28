from sys import version_info
from typing import Annotated, TypeAlias

import pytest
from sqlmodel import Field, SQLModel

Type5: TypeAlias = str
Type6: TypeAlias = Annotated[str, "Just a comment"]


@pytest.mark.skipif(version_info[1] < 12, reason="Language feature of Python 3.12+")
def test_sa_type_1() -> None:
    Type1 = str

    class Hero1(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type1 = 'sword'

@pytest.mark.skipif(version_info[1] < 12, reason="Language feature of Python 3.12+")
def test_sa_type_2() -> None:
    Type2 = Annotated[str, "Just a comment"]

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type2 = 'sword'

@pytest.mark.skipif(version_info[1] < 12, reason="Language feature of Python 3.12+")
def test_sa_type_3() -> None:
    type Type3 = str

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type3 = 'sword'

@pytest.mark.skipif(version_info[1] < 12, reason="Language feature of Python 3.12+")
def test_sa_type_4() -> None:
    type Type4 = Annotated[str, "Just a comment"]

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type4 = 'sword'

@pytest.mark.skipif(version_info[1] < 12, reason="Language feature of Python 3.12+")
def test_sa_type_5() -> None:

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type5 = 'sword'

@pytest.mark.skipif(version_info[1] < 12, reason="Language feature of Python 3.12+")
def test_sa_type_6() -> None:
    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type6 = 'sword'
