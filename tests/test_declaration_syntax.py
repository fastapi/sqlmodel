from typing import Annotated

from sqlmodel import Field, SQLModel


def test_declaration_syntax_1():
    class Person1(SQLModel, table=True):
        name: str = Field(primary_key=True)


def test_declaration_syntax_2():
    class Person2(SQLModel, table=True):
        name: Annotated[str, Field(primary_key=True)]


def test_declaration_syntax_3():
    class Person3(SQLModel, table=True):
        name: Annotated[str, ...] = Field(primary_key=True)
