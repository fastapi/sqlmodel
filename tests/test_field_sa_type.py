import sys
from typing import Annotated, TypeAlias

from sqlmodel import Field, SQLModel

from tests.conftest import needs_py312


@needs_py312
def test_sa_type_1() -> None:
    Type1 = str

    class Hero1(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type1 = "sword"


@needs_py312
def test_sa_type_2() -> None:
    Type2 = Annotated[str, "Just a comment"]

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type2 = "sword"


Type3: TypeAlias = str


@needs_py312
def test_sa_type_3() -> None:
    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type3 = "sword"


Type4: TypeAlias = Annotated[str, "Just a comment"]


@needs_py312
def test_sa_type_4() -> None:
    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type4 = "sword"


if sys.version_info >= (3, 12):

    @needs_py312
    def test_sa_type_5() -> None:
        type Type5 = str

        class Hero(SQLModel, table=True):
            pk: int = Field(primary_key=True)
            weapon: Type5 = "sword"

    @needs_py312
    def test_sa_type_6() -> None:
        type Type6 = Annotated[str, "Just a comment"]

        class Hero(SQLModel, table=True):
            pk: int = Field(primary_key=True)
            weapon: Type6 = "sword"
