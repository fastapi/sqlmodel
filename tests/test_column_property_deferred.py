from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import undefer
from sqlmodel import Field, Session, SQLModel, deferred_column_property, select


def test_deferred_column_property(clear_sqlmodel):
    """Test deferred_column_property that returns fallback value instead of raising DetachedInstanceError"""

    class DeferredModel(SQLModel, table=True):
        __tablename__ = "deferred_model"

        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        value: int = 0

        @classmethod
        def __declare_last__(cls):
            # Use deferred_column_property instead of regular column_property
            cls.computed_value = deferred_column_property(
                cls.__table__.c.value * 2,
                fallback_value=-1,
                deferred=True,
            )

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    test_record = DeferredModel(name="Test", value=5)

    with Session(engine) as session:
        session.add(test_record)
        session.commit()
        session.refresh(test_record)
        record_id = test_record.id

    # Query without loading deferred property
    with Session(engine) as session:
        record = session.get(DeferredModel, record_id)
        assert record is not None
        assert record.name == "Test"
        assert record.value == 5

        # Close session to ensure deferred property cannot be loaded
        session.close()

        # Access deferred property - should return fallback value instead of raising error
        computed = record.computed_value
        assert computed == -1  # This is the key difference from regular column_property

    # Test with explicit loading using undefer
    with Session(engine) as session:
        # Use undefer with class attribute instead of string
        statement = (
            select(DeferredModel)
            .options(undefer(DeferredModel.computed_value))
            .where(DeferredModel.id == record_id)
        )
        record = session.exec(statement).first()
        assert record is not None

        # Now the deferred property should be loaded and computed
        computed = record.computed_value
        assert computed == 10  # 5 * 2 = 10

    # Test different fallback value
    class CustomFallbackModel(SQLModel, table=True):
        __tablename__ = "custom_fallback_model"

        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        value: int = 0

        @classmethod
        def __declare_last__(cls):
            cls.computed_value = deferred_column_property(
                cls.__table__.c.value * 3,
                fallback_value=999,  # Custom fallback value
                deferred=True,
            )

    SQLModel.metadata.create_all(engine)

    custom_record = CustomFallbackModel(name="Custom", value=7)

    with Session(engine) as session:
        session.add(custom_record)
        session.commit()
        session.refresh(custom_record)
        custom_record_id = custom_record.id

    # Test custom fallback value
    with Session(engine) as session:
        record = session.get(CustomFallbackModel, custom_record_id)
        assert record is not None
        session.close()

        # Should return custom fallback value
        computed = record.computed_value
        assert computed == 999
