from typing_extensions import Annotated

from sqlmodel import Field, SQLModel


def test_declaration_syntax_1():
    class Person1(SQLModel):
        name: str = Field(primary_key=True)

    class Person1Final(Person1, table=True):
        pass


def test_declaration_syntax_2():
    class Person2(SQLModel):
        name: Annotated[str, Field(primary_key=True)]

    class Person2Final(Person2, table=True):
        pass


def test_declaration_syntax_3():
    class Person3(SQLModel):
        name: Annotated[str, ...] = Field(primary_key=True)

    class Person3Final(Person3, table=True):
        pass
