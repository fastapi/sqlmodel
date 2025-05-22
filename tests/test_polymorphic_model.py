from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

from tests.conftest import needs_pydanticv2


@needs_pydanticv2
def test_polymorphic_joined_table(clear_sqlmodel) -> None:
    class Hero(SQLModel, table=True):
        __tablename__ = "hero"
        id: Optional[int] = Field(default=None, primary_key=True)
        hero_type: str = Field(default="hero")

        __mapper_args__ = {
            "polymorphic_on": "hero_type",
            "polymorphic_identity": "normal_hero",
        }

    class DarkHero(Hero):
        __tablename__ = "dark_hero"
        id: Optional[int] = Field(
            default=None,
            sa_column=mapped_column(ForeignKey("hero.id"), primary_key=True),
        )
        dark_power: str = Field(
            default="dark",
            sa_column=mapped_column(
                nullable=False, use_existing_column=True, default="dark"
            ),
        )

        __mapper_args__ = {
            "polymorphic_identity": "dark",
        }

    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db:
        hero = Hero()
        db.add(hero)
        dark_hero = DarkHero()
        db.add(dark_hero)
        db.commit()
        statement = select(DarkHero)
        result = db.exec(statement).all()
    assert len(result) == 1
    assert isinstance(result[0].dark_power, str)


@needs_pydanticv2
def test_polymorphic_joined_table_with_sqlmodel_field(clear_sqlmodel) -> None:
    class Hero(SQLModel, table=True):
        __tablename__ = "hero"
        id: Optional[int] = Field(default=None, primary_key=True)
        hero_type: str = Field(default="hero")

        __mapper_args__ = {
            "polymorphic_on": "hero_type",
            "polymorphic_identity": "normal_hero",
        }

    class DarkHero(Hero):
        __tablename__ = "dark_hero"
        id: Optional[int] = Field(
            default=None,
            primary_key=True,
            foreign_key="hero.id",
        )
        dark_power: str = Field(
            default="dark",
            sa_column=mapped_column(
                nullable=False, use_existing_column=True, default="dark"
            ),
        )

        __mapper_args__ = {
            "polymorphic_identity": "dark",
        }

    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db:
        hero = Hero()
        db.add(hero)
        dark_hero = DarkHero()
        db.add(dark_hero)
        db.commit()
        statement = select(DarkHero)
        result = db.exec(statement).all()
    assert len(result) == 1
    assert isinstance(result[0].dark_power, str)


@needs_pydanticv2
def test_polymorphic_single_table(clear_sqlmodel) -> None:
    class Hero(SQLModel, table=True):
        __tablename__ = "hero"
        id: Optional[int] = Field(default=None, primary_key=True)
        hero_type: str = Field(default="hero")

        __mapper_args__ = {
            "polymorphic_on": "hero_type",
            "polymorphic_identity": "normal_hero",
        }

    class DarkHero(Hero):
        dark_power: str = Field(
            default="dark",
            sa_column=mapped_column(
                nullable=False, use_existing_column=True, default="dark"
            ),
        )

        __mapper_args__ = {
            "polymorphic_identity": "dark",
        }

    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db:
        hero = Hero()
        db.add(hero)
        dark_hero = DarkHero(dark_power="pokey")
        db.add(dark_hero)
        db.commit()
        statement = select(DarkHero)
        result = db.exec(statement).all()
    assert len(result) == 1
    assert isinstance(result[0].dark_power, str)


@needs_pydanticv2
def test_polymorphic_relationship(clear_sqlmodel) -> None:
    class Tool(SQLModel, table=True):
        __tablename__ = "tool_table"

        id: int = Field(primary_key=True)

        name: str

    class Person(SQLModel, table=True):
        __tablename__ = "person_table"

        id: int = Field(primary_key=True)

        discriminator: str
        name: str

        tool_id: int = Field(foreign_key="tool_table.id")
        tool: Tool = Relationship()

        __mapper_args__ = {
            "polymorphic_on": "discriminator",
            "polymorphic_identity": "simple_person",
        }

    class Worker(Person):
        __mapper_args__ = {
            "polymorphic_identity": "worker",
        }

    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db:
        tool = Tool(id=1, name="Hammer")
        db.add(tool)
        worker = Worker(id=2, name="Bob", tool_id=1)
        db.add(worker)
        db.commit()

        statement = select(Worker).where(Worker.tool_id == 1)
        result = db.exec(statement).all()
        assert len(result) == 1
        assert isinstance(result[0].tool, Tool)
