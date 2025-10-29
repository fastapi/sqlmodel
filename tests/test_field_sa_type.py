import typing as t

import typing_extensions as te
from sqlmodel import Field, SQLModel

from tests.conftest import needs_py312


@needs_py312
def test_sa_type_typing_1() -> None:
    Type1_t = str

    class Hero1(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type1_t = "sword"


@needs_py312
def test_sa_type_typing_2() -> None:
    Type2_t = t.Annotated[str, "Just a comment"]

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type2_t = "sword"


Type3_t: t.TypeAlias = str


@needs_py312
def test_sa_type_typing_3() -> None:
    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type3_t = "sword"


Type4_t: t.TypeAlias = t.Annotated[str, "Just a comment"]


@needs_py312
def test_sa_type_typing_4() -> None:
    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type4_t = "sword"


@needs_py312
def test_sa_type_typing_5() -> None:
    type Type5_t = str

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type5_t = "sword"


@needs_py312
def test_sa_type_typing_6() -> None:
    type Type6_t = t.Annotated[str, "Just a comment"]

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type6_t = "sword"


@needs_py312
def test_sa_type_typing_extensions_1() -> None:
    Type1_te = str

    class Hero1(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type1_te = "sword"


@needs_py312
def test_sa_type_typing_extensions_2() -> None:
    Type2_te = te.Annotated[str, "Just a comment"]

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type2_te = "sword"


Type3_te: te.TypeAlias = str


@needs_py312
def test_sa_type_typing_extensions_3() -> None:
    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type3_te = "sword"


Type4_te: te.TypeAlias = te.Annotated[str, "Just a comment"]


@needs_py312
def test_sa_type_typing_extensions_4() -> None:
    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type4_te = "sword"


@needs_py312
def test_sa_type_typing_extensions_5() -> None:
    type Type5_te = str

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type5_te = "sword"


@needs_py312
def test_sa_type_typing_extensions_6() -> None:
    type Type6_te = te.Annotated[str, "Just a comment"]

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type6_te = "sword"
