import typing as t
from textwrap import dedent

import pytest
import typing_extensions as te
from sqlmodel import Field, SQLModel

from tests.conftest import needs_py312


def test_sa_type_typing_1() -> None:
    Type1_t = str

    class Hero1(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type1_t = "sword"


def test_sa_type_typing_2() -> None:
    Type2_t = t.Annotated[str, "Just a comment"]

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type2_t = "sword"


Type3_t: t.TypeAlias = str


def test_sa_type_typing_3() -> None:
    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type3_t = "sword"


Type4_t: t.TypeAlias = t.Annotated[str, "Just a comment"]


def test_sa_type_typing_4() -> None:
    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type4_t = "sword"


@needs_py312
def test_sa_type_typing_5() -> None:
    test_code = dedent("""
    type Type5_t = str

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type5_t = "sword"
    """)
    exec(test_code, globals())


@needs_py312
def test_sa_type_typing_6() -> None:
    test_code = dedent("""
    type Type6_t = t.Annotated[str, "Just a comment"]

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type6_t = "sword"
    """)
    exec(test_code, globals())


def test_sa_type_typing_7() -> None:
    Type7_t = t.NewType("Type7_t", str)

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type7_t = "sword"


def test_sa_type_typing_8() -> None:
    Type8_t = t.TypeVar("Type8_t", bound=str)

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type8_t = "sword"


def test_sa_type_typing_9() -> None:
    Type9_t = t.TypeVar("Type9_t", str, bytes)

    with pytest.raises(ValueError):

        class Hero(SQLModel, table=True):
            pk: int = Field(primary_key=True)
            weapon: Type9_t = "sword"


def test_sa_type_typing_extensions_1() -> None:
    Type1_te = str

    class Hero1(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type1_te = "sword"


def test_sa_type_typing_extensions_2() -> None:
    Type2_te = te.Annotated[str, "Just a comment"]

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type2_te = "sword"


Type3_te: te.TypeAlias = str


def test_sa_type_typing_extensions_3() -> None:
    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type3_te = "sword"


Type4_te: te.TypeAlias = te.Annotated[str, "Just a comment"]


def test_sa_type_typing_extensions_4() -> None:
    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type4_te = "sword"


@needs_py312
def test_sa_type_typing_extensions_5() -> None:
    test_code = dedent("""
    type Type5_te = str

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type5_te = "sword"
    """)
    exec(test_code, globals())


@needs_py312
def test_sa_type_typing_extensions_6() -> None:
    test_code = dedent("""
    type Type6_te = te.Annotated[str, "Just a comment"]

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type6_te = "sword"
    """)
    exec(test_code, globals())


def test_sa_type_typing_extensions_7() -> None:
    Type7_te = te.NewType("Type7_te", str)

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type7_te = "sword"


def test_sa_type_typing_extensions_8() -> None:
    Type8_te = te.TypeVar("Type8_te", bound=str)

    class Hero(SQLModel, table=True):
        pk: int = Field(primary_key=True)
        weapon: Type8_te = "sword"


def test_sa_type_typing_extensions_9() -> None:
    Type9_te = te.TypeVar("Type9_te", str, bytes)

    with pytest.raises(ValueError):

        class Hero(SQLModel, table=True):
            pk: int = Field(primary_key=True)
            weapon: Type9_te = "sword"
