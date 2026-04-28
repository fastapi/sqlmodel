"""
Tests the polymorphic query operators that operate above SQLModel's layer
(selectin_polymorphic, with_polymorphic, of_type) to confirm that SQLModel's
metaclass produces a mapper config compatible with them.
"""

from typing import Optional

import pytest
from sqlalchemy import or_
from sqlalchemy.orm import selectin_polymorphic, selectinload, with_polymorphic
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


def _make_classes():
    class Company(SQLModel, table=True):
        __tablename__ = "qg_company"
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        employees: list["Employee"] = Relationship(back_populates="company")

    class Employee(SQLModel, table=True):
        __tablename__ = "qg_employee"
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        type: str = Field(default="employee")
        company_id: Optional[int] = Field(default=None, foreign_key="qg_company.id")
        company: Optional[Company] = Relationship(back_populates="employees")

        __mapper_args__ = {
            "polymorphic_on": "type",
            "polymorphic_identity": "employee",
        }

    class Manager(Employee, table=True):
        __tablename__ = "qg_manager"
        id: Optional[int] = Field(
            default=None, primary_key=True, foreign_key="qg_employee.id"
        )
        manager_name: Optional[str] = None
        paperwork: list["Paperwork"] = Relationship(back_populates="manager")

        __mapper_args__ = {"polymorphic_identity": "manager"}

    class Engineer(Employee, table=True):
        __tablename__ = "qg_engineer"
        id: Optional[int] = Field(
            default=None, primary_key=True, foreign_key="qg_employee.id"
        )
        engineer_info: Optional[str] = None

        __mapper_args__ = {"polymorphic_identity": "engineer"}

    class Paperwork(SQLModel, table=True):
        __tablename__ = "qg_paperwork"
        id: Optional[int] = Field(default=None, primary_key=True)
        manager_id: Optional[int] = Field(
            default=None, foreign_key="qg_manager.id"
        )
        document_name: str
        manager: Optional[Manager] = Relationship(back_populates="paperwork")

    return Company, Employee, Manager, Engineer, Paperwork


def _make_deep_classes():
    Company, Employee, Manager, Engineer, Paperwork = _make_classes()

    class SeniorEngineer(Engineer, table=True):
        __tablename__ = "qg_senior_engineer"
        id: Optional[int] = Field(
            default=None, primary_key=True, foreign_key="qg_engineer.id"
        )
        years_experience: Optional[int] = None

        __mapper_args__ = {"polymorphic_identity": "senior_engineer"}

    return Company, Employee, Manager, Engineer, SeniorEngineer, Paperwork


def _seed(engine, Company, Manager, Engineer, Paperwork):
    with Session(engine) as db:
        db.add(
            Company(
                name="Krusty Krab",
                employees=[
                    Manager(
                        name="Mr. Krabs",
                        manager_name="Eugene H. Krabs",
                        paperwork=[
                            Paperwork(document_name="Secret Recipes"),
                            Paperwork(document_name="Krabby Patty Orders"),
                        ],
                    ),
                    Engineer(name="SpongeBob", engineer_info="Krabby Patty Master"),
                    Engineer(
                        name="Squidward",
                        engineer_info="Senior Customer Engagement Engineer",
                    ),
                ],
            )
        )
        db.commit()


# test selectin_polymorphic
def test_selectin_polymorphic_eager_loads_subclass_attrs():
    """selectin_polymorphic fires extra SELECTs so subclass attrs are already
    loaded when accessed — no additional lazy load per object."""
    Company, Employee, Manager, Engineer, Paperwork = _make_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    _seed(engine, Company, Manager, Engineer, Paperwork)

    with Session(engine) as db:
        stmt = (
            select(Employee)
            .order_by(Employee.id)
            .options(selectin_polymorphic(Employee, [Manager, Engineer]))
        )
        employees = db.exec(stmt).all()
        assert len(employees) == 3
        mgr = employees[0]
        assert isinstance(mgr, Manager)
        assert mgr.manager_name == "Eugene H. Krabs"
        eng = employees[1]
        assert isinstance(eng, Engineer)
        assert eng.engineer_info == "Krabby Patty Master"


def test_selectin_polymorphic_via_relationship():
    """selectin_polymorphic chained on selectinload eager-loads subclass attrs
    through a relationship (mirrors the Company.employees example in the docs)."""
    Company, Employee, Manager, Engineer, Paperwork = _make_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    _seed(engine, Company, Manager, Engineer, Paperwork)

    with Session(engine) as db:
        stmt = select(Company).options(
            selectinload(Company.employees).selectin_polymorphic([Manager, Engineer])
        )
        companies = db.exec(stmt).all()
        assert len(companies) == 1
        employees = companies[0].employees
        assert len(employees) == 3
        mgr = next(e for e in employees if isinstance(e, Manager))
        assert mgr.manager_name == "Eugene H. Krabs"


# test with_polymorphic


def test_with_polymorphic_filter_by_subclass_attr():
    """with_polymorphic exposes subclass namespaces so WHERE clauses can
    reference columns from multiple sub-tables at once."""
    Company, Employee, Manager, Engineer, Paperwork = _make_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    _seed(engine, Company, Manager, Engineer, Paperwork)

    with Session(engine) as db:
        poly = with_polymorphic(Employee, [Manager, Engineer])
        stmt = select(poly).where(
            or_(
                poly.Manager.manager_name == "Eugene H. Krabs",
                poly.Engineer.engineer_info == "Senior Customer Engagement Engineer",
            )
        )
        results = db.exec(stmt).all()
        assert len(results) == 2
        names = {r.name for r in results}
        assert names == {"Mr. Krabs", "Squidward"}


# test of_type — joining to specific sub-types
def test_of_type_join_filters_to_subclass():
    """Company.employees.of_type(Engineer) inner-joins only the engineer
    sub-table, allowing WHERE on engineer-specific columns."""
    Company, Employee, Manager, Engineer, Paperwork = _make_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    _seed(engine, Company, Manager, Engineer, Paperwork)

    with Session(engine) as db:
        stmt = (
            select(Company.name, Engineer.name)
            .join(Company.employees.of_type(Engineer))
            .where(
                or_(
                    Engineer.name == "SpongeBob",
                    Engineer.engineer_info == "Senior Customer Engagement Engineer",
                )
            )
        )
        rows = db.exec(stmt).all()
        assert len(rows) == 2
        emp_names = {r[1] for r in rows}
        assert emp_names == {"SpongeBob", "Squidward"}


def test_of_type_eager_load_with_polymorphic():
    """selectinload(Company.employees.of_type(with_polymorphic('*')))
    eagerly loads all employees with all subclass columns in one shot."""
    Company, Employee, Manager, Engineer, Paperwork = _make_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    _seed(engine, Company, Manager, Engineer, Paperwork)

    with Session(engine) as db:
        all_employees = with_polymorphic(Employee, "*")
        stmt = select(Company).options(
            selectinload(Company.employees.of_type(all_employees))
        )
        companies = db.exec(stmt).all()
        employees = companies[0].employees
        assert len(employees) == 3
        mgr = next(e for e in employees if isinstance(e, Manager))
        assert mgr.manager_name == "Eugene H. Krabs"


# test selectin_polymorphic combined with selectinload on subclass relationship
def test_selectin_polymorphic_with_sibling_selectinload():
    """selectin_polymorphic and selectinload(Manager.paperwork) as sibling
    options both fire; Manager instances have paperwork eagerly loaded."""
    Company, Employee, Manager, Engineer, Paperwork = _make_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    _seed(engine, Company, Manager, Engineer, Paperwork)

    with Session(engine) as db:
        stmt = (
            select(Employee)
            .order_by(Employee.id)
            .options(
                selectin_polymorphic(Employee, [Manager, Engineer]),
                selectinload(Manager.paperwork),
            )
        )
        employees = db.exec(stmt).all()
        mgr = next(e for e in employees if isinstance(e, Manager))
        assert isinstance(mgr, Manager)
        assert {p.document_name for p in mgr.paperwork} == {
            "Secret Recipes",
            "Krabby Patty Orders",
        }


def _seed_deep(engine, Company, Manager, Engineer, SeniorEngineer, Paperwork):
    with Session(engine) as db:
        db.add(
            Company(
                name="Krusty Krab",
                employees=[
                    Manager(
                        name="Mr. Krabs",
                        manager_name="Eugene H. Krabs",
                        paperwork=[Paperwork(document_name="Secret Recipes")],
                    ),
                    Engineer(name="SpongeBob", engineer_info="Krabby Patty Master"),
                    SeniorEngineer(
                        name="Sandy",
                        engineer_info="Aquatic Research",
                        years_experience=10,
                    ),
                ],
            )
        )
        db.commit()


# three-level joined-table inheritance query tests

def test_three_level_selectin_polymorphic_loads_deepest_subclass():
    """selectin_polymorphic on a 3-level hierarchy eagerly loads the deepest
    subclass attrs without an extra lazy load."""
    Company, Employee, Manager, Engineer, SeniorEngineer, Paperwork = _make_deep_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    _seed_deep(engine, Company, Manager, Engineer, SeniorEngineer, Paperwork)

    with Session(engine) as db:
        stmt = (
            select(Employee)
            .order_by(Employee.id)
            .options(selectin_polymorphic(Employee, [Manager, Engineer, SeniorEngineer]))
        )
        employees = db.exec(stmt).all()
        assert len(employees) == 3
        senior = next(e for e in employees if isinstance(e, SeniorEngineer))
        assert senior.name == "Sandy"
        assert senior.engineer_info == "Aquatic Research"
        assert senior.years_experience == 10


def test_three_level_with_polymorphic_filters_on_deepest_column():
    """with_polymorphic exposes the third-level sub-table so a WHERE clause
    can reference years_experience without a separate join step."""
    Company, Employee, Manager, Engineer, SeniorEngineer, Paperwork = _make_deep_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    _seed_deep(engine, Company, Manager, Engineer, SeniorEngineer, Paperwork)

    with Session(engine) as db:
        poly = with_polymorphic(Employee, [Manager, Engineer, SeniorEngineer])
        stmt = select(poly).where(poly.SeniorEngineer.years_experience > 5)
        results = db.exec(stmt).all()
        assert len(results) == 1
        assert results[0].name == "Sandy"


def test_three_level_of_type_joins_through_all_tables():
    """of_type(SeniorEngineer) on a base relationship joins through both
    intermediate tables and returns only the deepest subclass rows."""
    Company, Employee, Manager, Engineer, SeniorEngineer, Paperwork = _make_deep_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    _seed_deep(engine, Company, Manager, Engineer, SeniorEngineer, Paperwork)

    with Session(engine) as db:
        stmt = (
            select(Company.name, SeniorEngineer.name)
            .join(Company.employees.of_type(SeniorEngineer))
        )
        rows = db.exec(stmt).all()
        assert len(rows) == 1
        assert rows[0][1] == "Sandy"
