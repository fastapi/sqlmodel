"""Mirrors sqlalchemy/test/orm/inheritance/test_poly_persistence.py :: InsertOrderTest, RoundTripTest"""

from types import SimpleNamespace
from typing import Optional

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapped_column, with_polymorphic
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


def _make_classes():
    class Company(SQLModel, table=True):
        __tablename__ = "companies"
        company_id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        employees: list["Person"] = Relationship(back_populates="company")

    class Person(SQLModel, table=True):
        __tablename__ = "people"
        person_id: Optional[int] = Field(default=None, primary_key=True)
        company_id: Optional[int] = Field(
            default=None, foreign_key="companies.company_id"
        )
        name: str
        type: str = Field(default="person")
        company: Optional[Company] = Relationship(back_populates="employees")

        __mapper_args__ = {
            "polymorphic_on": "type",
            "polymorphic_identity": "person",
        }

    class Engineer(Person):
        __tablename__ = "engineers"
        person_id: Optional[int] = Field(
            default=None, primary_key=True, foreign_key="people.person_id"
        )
        status: Optional[str] = Field(default=None, sa_column=mapped_column(nullable=True))
        engineer_name: Optional[str] = Field(default=None, sa_column=mapped_column(nullable=True))
        primary_language: Optional[str] = Field(default=None, sa_column=mapped_column(nullable=True))

        __mapper_args__ = {"polymorphic_identity": "engineer"}

    class Manager(Person):
        __tablename__ = "managers"
        person_id: Optional[int] = Field(
            default=None, primary_key=True, foreign_key="people.person_id"
        )
        status: Optional[str] = Field(default=None, sa_column=mapped_column(nullable=True))
        manager_name: Optional[str] = Field(default=None, sa_column=mapped_column(nullable=True))

        __mapper_args__ = {"polymorphic_identity": "manager"}

    class Boss(Manager):
        __tablename__ = "boss"
        person_id: Optional[int] = Field(
            default=None, primary_key=True, foreign_key="managers.person_id"
        )
        golf_swing: Optional[str] = Field(default=None, sa_column=mapped_column(nullable=True))

        __mapper_args__ = {"polymorphic_identity": "boss"}

    return Company, Person, Engineer, Manager, Boss


def _seed(engine, Company, Engineer, Manager):
    with Session(engine) as db:
        c = Company(name="company1")
        db.add(c)
        db.flush()
        cid = c.company_id
        db.add(Manager(name="pointy haired boss", status="AAB", manager_name="manager1", company_id=cid))
        db.add(Engineer(name="dilbert", status="BBA", engineer_name="engineer1", primary_language="java", company_id=cid))
        db.add(Engineer(name="wally", status="CGG", engineer_name="engineer2", primary_language="python", company_id=cid))
        db.add(Manager(name="jsmith", status="ABA", manager_name="manager2", company_id=cid))
        db.commit()
    return SimpleNamespace(company_id=cid)


def test_insert_order():
    # mirrors InsertOrderTest.test_insert_order
    Company, Person, Engineer, Manager, Boss = _make_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        c = Company(name="company1")
        db.add(c)
        db.flush()
        cid = c.company_id
        db.add(Manager(name="pointy haired boss", status="AAB", manager_name="manager1", company_id=cid))
        db.add(Engineer(name="dilbert", status="BBA", engineer_name="engineer1", primary_language="java", company_id=cid))
        db.add(Engineer(name="wally", status="CGG", engineer_name="engineer2", primary_language="python", company_id=cid))
        db.add(Manager(name="jsmith", status="ABA", manager_name="manager2", company_id=cid))
        db.commit()

    with Session(engine) as db:
        employees = db.exec(select(Person)).all()

    assert len(employees) == 4
    assert sum(isinstance(e, Manager) for e in employees) == 2
    assert sum(isinstance(e, Engineer) for e in employees) == 2


def test_lazy_load():
    # mirrors RoundTripTest.test_lazy_load
    Company, Person, Engineer, Manager, Boss = _make_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    c = _seed(engine, Company, Engineer, Manager)

    with Session(engine) as db:
        company = db.get(Company, c.company_id)
        employees = company.employees

    assert len(employees) == 4
    assert {type(e) for e in employees} == {Engineer, Manager}


def test_with_polymorphic_eager_load():
    # mirrors RoundTripTest with with_polymorphic='auto' configuration
    Company, Person, Engineer, Manager, Boss = _make_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    _seed(engine, Company, Engineer, Manager)

    with Session(engine) as db:
        poly = with_polymorphic(Person, [Engineer, Manager])
        results = db.exec(select(poly)).all()

    assert len(results) == 4
    engineers = [r for r in results if isinstance(r, Engineer)]
    managers = [r for r in results if isinstance(r, Manager)]
    assert len(engineers) == 2
    assert len(managers) == 2
    assert engineers[0].primary_language in {"java", "python"}
    assert managers[0].manager_name in {"manager1", "manager2"}


def test_standalone_orphans():
    # mirrors RoundTripTest.test_standalone_orphans
    class Company2(SQLModel, table=True):
        __tablename__ = "companies2"
        company_id: Optional[int] = Field(default=None, primary_key=True)
        name: str

    class Person2(SQLModel, table=True):
        __tablename__ = "people2"
        person_id: Optional[int] = Field(default=None, primary_key=True)
        company_id: Optional[int] = Field(
            default=None, sa_column=mapped_column(nullable=False)
        )
        name: str
        type: str = Field(default="person")

        __mapper_args__ = {
            "polymorphic_on": "type",
            "polymorphic_identity": "person",
        }

    class Manager2(Person2):
        __tablename__ = "managers2"
        person_id: Optional[int] = Field(
            default=None, primary_key=True, foreign_key="people2.person_id"
        )
        manager_name: Optional[str] = Field(default=None, sa_column=mapped_column(nullable=True))

        __mapper_args__ = {"polymorphic_identity": "manager"}

    class Boss2(Manager2):
        __tablename__ = "boss2"
        person_id: Optional[int] = Field(
            default=None, primary_key=True, foreign_key="managers2.person_id"
        )
        golf_swing: Optional[str] = Field(default=None, sa_column=mapped_column(nullable=True))

        __mapper_args__ = {"polymorphic_identity": "boss"}

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with pytest.raises(IntegrityError):
        with Session(engine) as db:
            daboss = Boss2(name="daboss", manager_name="boss", golf_swing="fore")
            db.add(daboss)
            db.flush()


def test_multi_level_three_tables():
    # mirrors RoundTripTest — select(Person) returns all levels; select(Manager) includes Boss
    Company, Person, Engineer, Manager, Boss = _make_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        c = Company(name="corp")
        db.add(c)
        db.flush()
        cid = c.company_id
        db.add(Manager(name="mgr", manager_name="middle mgr", company_id=cid))
        db.add(Boss(name="boss", manager_name="top boss", golf_swing="fore", company_id=cid))
        db.commit()

    with Session(engine) as db:
        people = db.exec(select(Person)).all()
        managers = db.exec(select(Manager)).all()
        bosses = db.exec(select(Boss)).all()

    assert len(people) == 2
    assert len(managers) == 2  # Manager + Boss
    assert len(bosses) == 1
    assert isinstance(bosses[0], Boss)
    assert {type(p) for p in people} == {Manager, Boss}
