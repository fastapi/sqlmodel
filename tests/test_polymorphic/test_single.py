"""Mirrors sqlalchemy/test/orm/inheritance/test_single.py :: SingleInheritanceTest, AbstractPolymorphicTest"""

from sqlalchemy import true
from sqlalchemy.orm import aliased, mapped_column
from sqlmodel import Field, Session, SQLModel, create_engine, select


def _employee_classes():
    class Employee(SQLModel, table=True):
        __tablename__ = "employees"
        employee_id: int | None = Field(default=None, primary_key=True)
        name: str
        manager_data: str | None = Field(
            default=None, sa_column=mapped_column(nullable=True)
        )
        engineer_info: str | None = Field(
            default=None, sa_column=mapped_column(nullable=True)
        )
        type: str = Field(default="employee")

        __mapper_args__ = {
            "polymorphic_on": "type",
            "polymorphic_identity": "employee",
        }

    class Manager(Employee):
        __mapper_args__ = {"polymorphic_identity": "manager"}

    class Engineer(Employee):
        __mapper_args__ = {"polymorphic_identity": "engineer"}

    class JuniorEngineer(Engineer):
        __mapper_args__ = {"polymorphic_identity": "juniorengineer"}

    return Employee, Manager, Engineer, JuniorEngineer


def _seed_employees(engine, Manager, Engineer, JuniorEngineer):
    with Session(engine) as db:
        db.add(Manager(name="Tom", manager_data="knows how to manage things"))
        db.add(Engineer(name="Kurt", engineer_info="knows how to hack"))
        db.add(JuniorEngineer(name="Ed", engineer_info="oh that ed"))
        db.commit()


# ---------------------------------------------------------------------------
# SingleInheritanceTest
# ---------------------------------------------------------------------------


def test_single_inheritance():
    # mirrors SingleInheritanceTest.test_single_inheritance
    Employee, Manager, Engineer, JuniorEngineer = _employee_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    _seed_employees(engine, Manager, Engineer, JuniorEngineer)

    with Session(engine) as db:
        employees = db.exec(select(Employee)).all()
        engineers = db.exec(select(Engineer)).all()
        managers = db.exec(select(Manager)).all()
        juniors = db.exec(select(JuniorEngineer)).all()

        db.expire(managers[0], ["manager_data"])
        assert managers[0].manager_data == "knows how to manage things"

    assert len(employees) == 3
    assert len(engineers) == 2  # Engineer + JuniorEngineer
    assert len(managers) == 1
    assert len(juniors) == 1
    assert {type(e) for e in employees} == {Manager, Engineer, JuniorEngineer}
    assert all(isinstance(e, Engineer) for e in engineers)


def test_column_qualification():
    # mirrors SingleInheritanceTest.test_column_qualification
    Employee, Manager, Engineer, JuniorEngineer = _employee_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    _seed_employees(engine, Manager, Engineer, JuniorEngineer)

    with Session(engine) as db:
        all_ids = db.scalars(select(Employee.employee_id)).all()
        eng_ids = db.scalars(select(Engineer.employee_id)).all()
        mgr_ids = db.scalars(select(Manager.employee_id)).all()
        jun_ids = db.scalars(select(JuniorEngineer.employee_id)).all()

    assert len(all_ids) == 3
    assert len(eng_ids) == 2
    assert len(mgr_ids) == 1
    assert len(jun_ids) == 1
    assert set(jun_ids) < set(eng_ids) < set(all_ids)


def test_multi_qualification():
    # mirrors SingleInheritanceTest.test_multi_qualification
    Employee, Manager, Engineer, JuniorEngineer = _employee_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    _seed_employees(engine, Manager, Engineer, JuniorEngineer)

    with Session(engine) as db:
        ealias = aliased(Engineer)
        rows = db.execute(select(Manager, ealias).join(ealias, true())).all()

    assert len(rows) == 2
    assert all(isinstance(r[0], Manager) for r in rows)
    assert all(isinstance(r[1], Engineer) for r in rows)


def test_type_filtering():
    # mirrors SingleInheritanceTest.test_type_filtering / test_type_joins
    Employee, Manager, Engineer, JuniorEngineer = _employee_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    _seed_employees(engine, Manager, Engineer, JuniorEngineer)

    with Session(engine) as db:
        engineers = db.exec(select(Engineer)).all()
        juniors = db.exec(select(JuniorEngineer)).all()
        managers = db.exec(select(Manager)).all()

    assert len(engineers) == 2
    assert len(juniors) == 1
    assert len(managers) == 1
    assert any(type(e) is JuniorEngineer for e in engineers)
    assert not any(isinstance(e, Manager) for e in engineers)


# ---------------------------------------------------------------------------
# AbstractPolymorphicTest
# ---------------------------------------------------------------------------


def test_abstract_intermediate():
    # mirrors AbstractPolymorphicTest.test_select_against_abstract
    class Employee(SQLModel, table=True):
        __tablename__ = "emp_abstract"
        id: int | None = Field(default=None, primary_key=True)
        type: str = Field(default="employee")
        name: str
        mgr_data: str | None = Field(
            default=None, sa_column=mapped_column(nullable=True)
        )
        tech_data: str | None = Field(
            default=None, sa_column=mapped_column(nullable=True)
        )

        __mapper_args__ = {
            "polymorphic_on": "type",
            "polymorphic_identity": "employee",
        }

    class Executive(Employee):
        __mapper_args__ = {"polymorphic_abstract": True}

    class Technologist(Employee):
        __mapper_args__ = {"polymorphic_abstract": True}

    class Manager(Executive):
        __mapper_args__ = {"polymorphic_identity": "manager"}

    class Engineer(Technologist):
        __mapper_args__ = {"polymorphic_identity": "engineer"}

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        db.add(Manager(name="Alice", mgr_data="MBA"))
        db.add(Engineer(name="Bob", tech_data="Python"))
        db.commit()

        executives = db.exec(select(Executive)).all()
        technologists = db.exec(select(Technologist)).all()
        all_emps = db.exec(select(Employee)).all()

    assert len(executives) == 1 and isinstance(executives[0], Manager)
    assert len(technologists) == 1 and isinstance(technologists[0], Engineer)
    assert len(all_emps) == 2
