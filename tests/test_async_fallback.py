"""
Test async behavior of deferred_column_property
"""

from typing import Optional

from sqlalchemy import create_engine
from sqlmodel import Field, SQLModel, deferred_column_property


def test_async_fallback_value():
    """Test that deferred_column_property returns fallback value in async context without greenlet"""

    class AsyncTestModel(SQLModel, table=True):
        __tablename__ = "async_test_model"

        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        value: int = 0

        @classmethod
        def __declare_last__(cls):
            cls.computed_value = deferred_column_property(
                cls.__table__.c.value * 2,
                fallback_value=-999,
                deferred=True,
            )

    # Create regular engine first to set up data
    sync_engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(sync_engine)

    from sqlmodel import Session

    with Session(sync_engine) as session:
        test_record = AsyncTestModel(name="AsyncTest", value=5)
        session.add(test_record)
        session.commit()
        session.refresh(test_record)
        record_id = test_record.id

    # Now test with async session context (simulating MissingGreenlet scenario)
    with Session(sync_engine) as session:
        record = session.get(AsyncTestModel, record_id)
        assert record is not None

        # Close session to simulate detached state that might cause async issues
        session.close()

        # This should return fallback value without raising MissingGreenlet
        computed = record.computed_value
        assert computed == -999


if __name__ == "__main__":
    test_async_fallback_value()
    print("✅ Async fallback test passed!")
