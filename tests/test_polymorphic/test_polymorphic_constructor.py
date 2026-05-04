from sqlmodel import Field, Relationship, Session, SQLModel, create_engine


def _make_dept_employee_classes():
    """Department → Employee (base) → Manager (joined table inheritance subclass)."""

    class Department(SQLModel, table=True):
        __tablename__ = "department"
        id: int | None = Field(default=None, primary_key=True)
        name: str
        employees: list["Employee"] = Relationship(back_populates="department")

    class Employee(SQLModel, table=True):
        __tablename__ = "employee"
        id: int | None = Field(default=None, primary_key=True)
        type: str = Field(default="employee")
        name: str
        department_id: int | None = Field(default=None, foreign_key="department.id")
        department: Department | None = Relationship(back_populates="employees")

        __mapper_args__ = {
            "polymorphic_on": "type",
            "polymorphic_identity": "employee",
        }

    class Manager(Employee, table=True):
        __tablename__ = "manager"
        id: int | None = Field(
            default=None, primary_key=True, foreign_key="employee.id"
        )
        budget: float | None = Field(default=None)

        __mapper_args__ = {"polymorphic_identity": "manager"}

    return Department, Employee, Manager


def test_constructor_inherited_relationship_sets_fk():
    """
    Passing an inherited relationship as a constructor kwarg must propagate
    the foreign key so the row is persisted with the correct value.
    """
    Department, Employee, Manager = _make_dept_employee_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        eng = Department(name="Engineering")
        db.add(eng)
        db.commit()
        db.refresh(eng)
        dept_id = eng.id

        m = Manager(name="Alice", budget=100_000.0, department=eng)
        db.add(m)
        db.commit()
        m_id = m.id

    with Session(engine) as db:
        m = db.get(Manager, m_id)
        assert m.department_id == dept_id
        assert m.department.name == "Engineering"


def test_constructor_inherited_relationship_back_populates():
    """
    The back-populated collection on the related model reflects joined table
    inheritance subclass instances created via the constructor relationship kwarg.
    """
    Department, Employee, Manager = _make_dept_employee_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        eng = Department(name="Engineering")
        db.add(eng)
        db.flush()
        dept_id = eng.id

        db.add(Manager(name="Alice", budget=80_000.0, department=eng))
        db.add(Manager(name="Bob", budget=90_000.0, department=eng))
        db.commit()

    with Session(engine) as db:
        dept = db.get(Department, dept_id)
        employees = dept.employees
        assert len(employees) == 2
        assert all(isinstance(e, Manager) for e in employees)
        assert {e.name for e in employees} == {"Alice", "Bob"}
