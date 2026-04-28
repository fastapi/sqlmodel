"""
Regression test for issue #530:
Relationship type annotations disappear after class definition is evaluated.

Before the fix, `__init_subclass__` hooks could not see Relationship annotations
in `cls.__annotations__`, making it impossible to inspect relationship types
at class creation time.
"""

from typing import Optional

from sqlmodel import Field, Relationship, SQLModel, Session, create_engine, select


# Track what annotations were visible during class creation
_seen_annotations: dict[str, set] = {}


class AnnotationInspector(SQLModel):
    """Mixin that records which annotations are visible in __init_subclass__."""

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        _seen_annotations[cls.__name__] = set(cls.__annotations__.keys())


def test_relationship_annotations_visible_in_init_subclass() -> None:
    """
    Verifies that Relationship fields appear in __annotations__ when
    __init_subclass__ is called, fixing issue #530.
    """
    _seen_annotations.clear()

    class TeamA(AnnotationInspector, SQLModel, table=True):
        __tablename__ = "teama_530"
        id: Optional[int] = Field(default=None, primary_key=True)
        members: list["MemberA"] = Relationship(back_populates="team")

    class MemberA(AnnotationInspector, SQLModel, table=True):
        __tablename__ = "membera_530"
        id: Optional[int] = Field(default=None, primary_key=True)
        team_id: Optional[int] = Field(default=None, foreign_key="teama_530.id")
        team: Optional[TeamA] = Relationship(back_populates="members")

    # The key assertion: relationship fields must be visible in __annotations__
    # at the time __init_subclass__ is called.
    assert "members" in _seen_annotations["TeamA"], (
        "Relationship 'members' was not visible in TeamA.__annotations__ "
        "during __init_subclass__ (issue #530)"
    )
    assert "team" in _seen_annotations["MemberA"], (
        "Relationship 'team' was not visible in MemberA.__annotations__ "
        "during __init_subclass__ (issue #530)"
    )


def test_relationship_annotations_not_in_model_fields() -> None:
    """
    Verifies that Relationship fields do NOT appear in model_fields (Pydantic),
    which would cause validation overhead and incorrect behavior.
    """

    class TeamB(SQLModel, table=True):
        __tablename__ = "teamb_530"
        id: Optional[int] = Field(default=None, primary_key=True)
        members: list["MemberB"] = Relationship(back_populates="team")

    class MemberB(SQLModel, table=True):
        __tablename__ = "memberb_530"
        id: Optional[int] = Field(default=None, primary_key=True)
        team_id: Optional[int] = Field(default=None, foreign_key="teamb_530.id")
        team: Optional[TeamB] = Relationship(back_populates="members")

    # Relationship fields should NOT appear in pydantic model_fields
    assert "members" not in TeamB.model_fields, (
        "Relationship 'members' incorrectly appeared in TeamB.model_fields"
    )
    assert "team" not in MemberB.model_fields, (
        "Relationship 'team' incorrectly appeared in MemberB.model_fields"
    )

    # But they should appear in sqlmodel_relationships
    assert "members" in TeamB.__sqlmodel_relationships__
    assert "team" in MemberB.__sqlmodel_relationships__


def test_relationship_functional_after_fix() -> None:
    """
    End-to-end test: Verify that relationships still work correctly after the fix.
    """

    class Department(SQLModel, table=True):
        __tablename__ = "department_530"
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        employees: list["Employee"] = Relationship(back_populates="department")

    class Employee(SQLModel, table=True):
        __tablename__ = "employee_530"
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        department_id: Optional[int] = Field(
            default=None, foreign_key="department_530.id"
        )
        department: Optional[Department] = Relationship(back_populates="employees")

    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        dept = Department(name="Engineering")
        session.add(dept)
        session.commit()
        session.refresh(dept)

        emp = Employee(name="Alice", department_id=dept.id)
        session.add(emp)
        session.commit()
        session.refresh(emp)

        # Verify relationship loading
        statement = select(Employee).where(Employee.name == "Alice")
        loaded_emp = session.exec(statement).first()
        assert loaded_emp is not None
        assert loaded_emp.department_id == dept.id
