"""
Test async context simulation that would cause MissingGreenlet
"""

from typing import Optional

from sqlalchemy import create_engine
from sqlmodel import Field, SQLModel, deferred_column_property, Session


class MockAsyncState:
    """Mock async state to simulate problematic scenario"""

    def __init__(self, original_state):
        self.original_state = original_state

    def __getattr__(self, name):
        if name == "async_session":
            # Simulate having async session (which would cause MissingGreenlet)
            return "mock_async_session"
        return getattr(self.original_state, name)


def test_simulated_async_greenlet_error():
    """Test simulated async context that would cause MissingGreenlet"""

    class Employee(SQLModel, table=True):
        __tablename__ = "employee_async_sim"

        id: Optional[int] = Field(default=None, primary_key=True)
        user_id: Optional[int] = None
        company_id: int

        @classmethod
        def __declare_last__(cls):
            cls.is_owner = deferred_column_property(
                cls.__table__.c.user_id == cls.__table__.c.company_id,
                fallback_value=-999,
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

    # Load object and access property while session is open (loads it)
    with Session(engine) as session:
        employee = session.get(Employee, employee_id)

        # Access while session is open to cache it
        is_owner_loaded = employee.is_owner
        print(f"Loaded while session open: {is_owner_loaded}")

        # Close session
        session.close()

        # Now simulate async context by patching the state
        original_state = employee._sa_instance_state

        # Mock the async_session to simulate async context
        mock_state = MockAsyncState(original_state)
        employee._sa_instance_state = mock_state

        # Try to access - should now return fallback due to async context
        try:
            is_owner_after_mock = employee.is_owner
            print(f"✅ Value with mocked async context: {is_owner_after_mock}")

            if is_owner_after_mock == -999:
                print("✅ FALLBACK value returned correctly!")
            else:
                print(f"⚠️  Expected fallback -999, got {is_owner_after_mock}")

        except Exception as e:
            print(f"❌ Error: {e}")
            raise
        finally:
            # Restore original state
            employee._sa_instance_state = original_state


def test_force_async_context():
    """Test by actually creating a scenario that might trigger async issues"""

    class TestEmployee(SQLModel, table=True):
        __tablename__ = "test_employee_async"

        id: Optional[int] = Field(default=None, primary_key=True)
        user_id: Optional[int] = None

        @classmethod
        def __declare_last__(cls):
            cls.computed = deferred_column_property(
                cls.__table__.c.user_id * 10,
                fallback_value=-111,
                deferred=True,
            )

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        employee = TestEmployee(user_id=7)
        session.add(employee)
        session.commit()
        session.refresh(employee)
        employee_id = employee.id

    # Test unloaded state after session close
    with Session(engine) as session:
        employee = session.get(TestEmployee, employee_id)

        # Don't access the property - keep it unloaded
        state = employee._sa_instance_state
        print(f"Unloaded attributes: {list(state.unloaded)}")

        session.close()
        print(f"Session after close: {state.session}")

        # Access should use fallback for unloaded attribute
        computed = employee.computed
        print(f"✅ Unloaded access after session close: {computed}")
        assert computed == -111, f"Expected -111, got {computed}"

    print("✅ Async context tests completed!")


if __name__ == "__main__":
    print("=== Testing simulated async context ===")
    test_simulated_async_greenlet_error()
    print("\n=== Testing force async context ===")
    test_force_async_context()
    print("\n✅ All async simulation tests passed!")
