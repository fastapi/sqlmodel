"""
Test edge cases that might cause our fallback to fail
"""

from typing import Optional

from sqlalchemy import create_engine
from sqlmodel import Field, SQLModel, deferred_column_property, Session


def test_attribute_preloading_scenario():
    """Test what happens if attribute gets preloaded somehow"""

    class Employee(SQLModel, table=True):
        __tablename__ = "employee_preload"

        id: Optional[int] = Field(default=None, primary_key=True)
        user_id: Optional[int] = None
        company_id: int

        @classmethod
        def __declare_last__(cls):
            cls.is_owner = deferred_column_property(
                cls.__table__.c.user_id == cls.__table__.c.company_id,
                fallback_value=-777,
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

    # Scenario: Access attribute BEFORE closing session (preloads it)
    with Session(engine) as session:
        employee = session.get(Employee, employee_id)

        # Access the attribute while session is still open - this loads it
        print(f"Accessing is_owner while session open...")
        is_owner_loaded = employee.is_owner
        print(f"Loaded value: {is_owner_loaded}")

        # Check state after loading
        state = employee._sa_instance_state
        print(f"Unloaded after access: {list(state.unloaded)}")
        print(f"is_owner in __dict__: {'is_owner' in employee.__dict__}")
        print(
            f"Value in __dict__: {getattr(employee, '__dict__', {}).get('is_owner', 'NOT_FOUND')}"
        )

        # NOW close session
        session.close()
        print(f"Session after close: {state.session}")

        # Try to access again - will it use cached value or fallback?
        try:
            is_owner_after_close = employee.is_owner
            print(f"✅ Value after session close: {is_owner_after_close}")

            if is_owner_after_close == is_owner_loaded:
                print("⚠️  Using CACHED value (no fallback)")
            elif is_owner_after_close == -777:
                print("✅ Using FALLBACK value")
            else:
                print(f"❓ Unexpected value: {is_owner_after_close}")

        except Exception as e:
            print(f"❌ Error: {e}")
            raise


def test_session_detach_scenario():
    """Test what happens with session.expunge()"""

    class Employee(SQLModel, table=True):
        __tablename__ = "employee_detach"

        id: Optional[int] = Field(default=None, primary_key=True)
        user_id: Optional[int] = None

        @classmethod
        def __declare_last__(cls):
            cls.is_owner = deferred_column_property(
                cls.__table__.c.user_id * 100,
                fallback_value=-555,
                deferred=True,
            )

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        employee = Employee(user_id=3)
        session.add(employee)
        session.commit()
        session.refresh(employee)

        # Detach from session using expunge
        session.expunge(employee)

        state = employee._sa_instance_state
        print(f"Session after expunge: {state.session}")
        print(f"Unloaded after expunge: {list(state.unloaded)}")

        # Try to access deferred property
        try:
            is_owner = employee.is_owner
            print(f"✅ Value after expunge: {is_owner}")
            assert is_owner == -555, f"Expected -555, got {is_owner}"

        except Exception as e:
            print(f"❌ Error: {e}")
            raise


if __name__ == "__main__":
    print("=== Testing attribute preloading scenario ===")
    test_attribute_preloading_scenario()
    print("\n=== Testing session detach scenario ===")
    test_session_detach_scenario()
    print("\n✅ All edge case tests completed!")
