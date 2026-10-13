from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel


def test_field_parameters() -> None:
    class Hero(SQLModel):
        name: str = Field()
        secret_name: str = Field(alias="secretName")
        age: int = Field(default=42)
        tags: list[str] = Field(default_factory=list)

    hero = Hero(name="Deadpond", secretName="Dive Wilson")
    other = Hero(name="Spider-Boy", secretName="Pedro Parqueador")

    assert hero.name == "Deadpond"
    assert hero.secret_name == "Dive Wilson"
    assert hero.age == 42
    assert hero.tags == []
    assert hero.tags is not other.tags

    if TYPE_CHECKING:
        Hero(secretName="Dive Wilson")  # ty: ignore[missing-argument]
        Hero("Deadpond", "Dive Wilson")  # ty: ignore[too-many-positional-arguments, missing-argument]
        Hero(name=123, secretName="Dive Wilson")  # ty: ignore[invalid-argument-type]
