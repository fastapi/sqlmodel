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


@needs_pydanticv2
def test_polymorphic_deeper(clear_sqlmodel) -> None:
    class Employee(SQLModel, table=True):
        __tablename__ = "employee"

        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        type: str = Field(default="employee")

        __mapper_args__ = {
            "polymorphic_identity": "employee",
            "polymorphic_on": "type",
        }

    class Executive(Employee):
        """An executive of the company"""

        executive_background: Optional[str] = Field(
            sa_column=mapped_column(nullable=True), default=None
        )

        __mapper_args__ = {"polymorphic_abstract": True}

    class Technologist(Employee):
        """An employee who works with technology"""

        competencies: Optional[str] = Field(
            sa_column=mapped_column(nullable=True), default=None
        )

        __mapper_args__ = {"polymorphic_abstract": True}

    class Manager(Executive):
        """A manager"""

        __mapper_args__ = {"polymorphic_identity": "manager"}

    class Principal(Executive):
        """A principal of the company"""

        __mapper_args__ = {"polymorphic_identity": "principal"}

    class Engineer(Technologist):
        """An engineer"""

        __mapper_args__ = {"polymorphic_identity": "engineer"}

    class SysAdmin(Technologist):
        """A systems administrator"""

        __mapper_args__ = {"polymorphic_identity": "sysadmin"}

    # Create database and session
    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        # Add different employee types
        manager = Manager(name="Alice", executive_background="MBA")
        principal = Principal(name="Bob", executive_background="Founder")
        engineer = Engineer(name="Charlie", competencies="Python, SQL")
        sysadmin = SysAdmin(name="Diana", competencies="Linux, Networking")

        db.add(manager)
        db.add(principal)
        db.add(engineer)
        db.add(sysadmin)
        db.commit()

        # Query each type to verify they persist correctly
        managers = db.exec(select(Manager)).all()
        principals = db.exec(select(Principal)).all()
        engineers = db.exec(select(Engineer)).all()
        sysadmins = db.exec(select(SysAdmin)).all()

        # Query abstract classes to verify they return appropriate concrete classes
        executives = db.exec(select(Executive)).all()
        technologists = db.exec(select(Technologist)).all()

        # All employees
        all_employees = db.exec(select(Employee)).all()

    # Assert individual type counts
    assert len(managers) == 1
    assert len(principals) == 1
    assert len(engineers) == 1
    assert len(sysadmins) == 1

    # Check that abstract classes can't be instantiated directly
    # but their subclasses are correctly returned when querying
    assert len(executives) == 2
    assert len(technologists) == 2
    assert len(all_employees) == 4

    # Check that properties of abstract classes are accessible from concrete instances
    assert managers[0].executive_background == "MBA"
    assert principals[0].executive_background == "Founder"
    assert engineers[0].competencies == "Python, SQL"
    assert sysadmins[0].competencies == "Linux, Networking"

    # Check polymorphic identities
    assert managers[0].type == "manager"
    assert principals[0].type == "principal"
    assert engineers[0].type == "engineer"
    assert sysadmins[0].type == "sysadmin"
