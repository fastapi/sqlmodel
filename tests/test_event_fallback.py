"""
Test that deferred_column_property returns fallback values correctly
even after refresh operations.
"""

from typing import Optional

from sqlalchemy import create_engine
from sqlmodel import Field, SQLModel, Session, select
from sqlmodel import deferred_column_property


def test_fallback_after_refresh():
    """Test that fallback value is returned even after refresh"""

    class Employee(SQLModel, table=True):
        __tablename__ = "employee_refresh_test"

        id: Optional[int] = Field(default=None, primary_key=True)
        user_id: Optional[int] = None
        company_id: int = 1

        @classmethod
        def __declare_last__(cls):
            cls.is_owner = deferred_column_property(
                cls.__table__.c.user_id == cls.__table__.c.company_id,
                fallback_value=False,  # Should always return False
                deferred=True,
            )

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        employee = Employee(user_id=1, company_id=1)
        session.add(employee)
        session.commit()
        session.refresh(employee)
        employee_id = employee.id

        # Check that fallback is set automatically
        print(f"is_owner after refresh: {employee.is_owner}")
        print(f"is_owner in __dict__: {'is_owner' in employee.__dict__}")

        assert employee.is_owner == False, (
            f"Expected False (fallback), got {employee.is_owner}"
        )

    # Test loading in new session
    with Session(engine) as session:
        employee = session.get(Employee, employee_id)

        # Should have fallback value immediately
        print(f"is_owner in new session: {employee.is_owner}")
        assert employee.is_owner == False, (
            f"Expected False (fallback), got {employee.is_owner}"
        )

        # Refresh again
        session.refresh(employee)
        print(f"is_owner after second refresh: {employee.is_owner}")
        assert employee.is_owner == False, (
            f"Expected False (fallback), got {employee.is_owner}"
        )

    print("✅ Fallback after refresh test passed!")


def test_no_actual_load():
    """Test that deferred property never actually loads from database"""

    class TestModel(SQLModel, table=True):
        __tablename__ = "test_no_load"

        id: Optional[int] = Field(default=None, primary_key=True)
        value: int = 10

        @classmethod
        def __declare_last__(cls):
            cls.computed = deferred_column_property(
                cls.__table__.c.value * 100,  # Would be 1000 if loaded from DB
                fallback_value=-999,  # Should always return this instead
                deferred=True,
            )

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        obj = TestModel(value=10)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        obj_id = obj.id

    # Load in new session - should get fallback, NOT computed value from DB
    with Session(engine) as session:
        obj = session.get(TestModel, obj_id)

        print(f"Value from DB: {obj.value}")  # Should be 10
        print(
            f"Computed (should be fallback): {obj.computed}"
        )  # Should be -999, NOT 1000

        # The key test: we should NEVER get 1000 (the computed value)
        assert obj.computed == -999, (
            f"Expected -999 (fallback), got {obj.computed} - deferred property was incorrectly loaded!"
        )

        # Even multiple accesses should return fallback
        assert obj.computed == -999, f"Second access should still return fallback"

    print("✅ No actual load test passed!")


if __name__ == "__main__":
    test_fallback_after_refresh()
    test_no_actual_load()
    print("\\n✅ All event-based fallback tests passed!")
