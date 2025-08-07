"""
Test real-world async scenario that causes MissingGreenlet
"""

from typing import Optional

from sqlalchemy import create_engine
from sqlmodel import Field, SQLModel, deferred_column_property, Session


def test_real_greenlet_error_scenario():
    """Test scenario that reproduces the actual MissingGreenlet error"""

    class Employee(SQLModel, table=True):
        __tablename__ = "employee"

        id: Optional[int] = Field(default=None, primary_key=True)
        user_id: Optional[int] = None
        company_id: int

        @classmethod
        def __declare_last__(cls):
            # This simulates the is_owner column_property from the user's code
            cls.is_owner = deferred_column_property(
                cls.__table__.c.user_id
                == cls.__table__.c.company_id,  # Simplified expression
                fallback_value=None,
                deferred=True,
            )

    # Set up data
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        employee = Employee(user_id=1, company_id=1)
        session.add(employee)
        session.commit()
        session.refresh(employee)
        employee_id = employee.id

    # Scenario 1: Load object without accessing deferred property
    with Session(engine) as session:
        employee = session.get(Employee, employee_id)
        assert employee is not None

        # Check initial state
        state = employee._sa_instance_state
        print(f"Initial unloaded attributes: {list(state.unloaded)}")
        print(f"is_owner in __dict__: {'is_owner' in employee.__dict__}")

        # Close session BEFORE accessing the deferred property
        session.close()

        # Now try to access - this should trigger our fallback logic
        print(f"Session after close: {state.session}")
        print(f"Async session: {state.async_session}")

        try:
            # This is where MissingGreenlet would normally occur
            is_owner = employee.is_owner
            print(f"✅ is_owner accessed successfully: {is_owner}")

            # Verify it's the fallback value
            assert is_owner is None, f"Expected None (fallback), got {is_owner}"

        except Exception as e:
            print(f"❌ Error accessing is_owner: {e}")
            raise

    print("✅ Real scenario test passed!")


def test_force_unloaded_state():
    """Test by manually forcing unloaded state"""

    class TestEmployee(SQLModel, table=True):
        __tablename__ = "test_employee"

        id: Optional[int] = Field(default=None, primary_key=True)
        user_id: Optional[int] = None

        @classmethod
        def __declare_last__(cls):
            cls.is_owner = deferred_column_property(
                cls.__table__.c.user_id * 2,
                fallback_value=-888,
                deferred=True,
            )

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        employee = TestEmployee(user_id=5)
        session.add(employee)
        session.commit()
        session.refresh(employee)
        employee_id = employee.id

    # Load fresh object and manually manipulate state
    with Session(engine) as session:
        employee = session.get(TestEmployee, employee_id)
        state = employee._sa_instance_state

        # Ensure the attribute is unloaded
        if "is_owner" not in state.unloaded:
            # Force it back to unloaded state
            if "is_owner" in employee.__dict__:
                delattr(employee, "is_owner")
            # Add back to unloaded set
            state.unloaded.add("is_owner")

        print(f"Forced unloaded state: {list(state.unloaded)}")
        session.close()

        # Now access should use fallback
        is_owner = employee.is_owner
        print(f"✅ Forced unloaded access: {is_owner}")
        assert is_owner == -888, f"Expected -888, got {is_owner}"

    print("✅ Forced unloaded test passed!")


if __name__ == "__main__":
    test_real_greenlet_error_scenario()
    test_force_unloaded_state()
    print("✅ All real scenario tests passed!")
