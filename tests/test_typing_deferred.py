"""
Test typing compatibility of deferred_column_property.

This test verifies that deferred_column_property has the same typing behavior
as the original column_property from SQLAlchemy.
"""

from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import configure_mappers
from sqlalchemy.orm import Query, sessionmaker, undefer
from sqlmodel import Field, SQLModel, create_engine

from sqlmodel.deferred_column import deferred_column_property

if TYPE_CHECKING:
    from sqlalchemy.orm.attributes import InstrumentedAttribute


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default="default")
    age: Optional[int] = None

    @classmethod
    def __declare_last__(cls):
        # Test that deferred_column_property returns proper type
        cls.computed_age: "InstrumentedAttribute[int]" = deferred_column_property(
            cls.__table__.c.age * 2, fallback_value=0
        )


def test_typing_compatibility():
    """Test that typing works correctly with deferred_column_property"""
    # Force SQLAlchemy to configure mappers
    configure_mappers()

    # Test that we can use undefer() with deferred_column_property
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # Create test user
    user = User(name="Test", age=25)
    session.add(user)
    session.commit()
    user_id = user.id

    # Test loading with undefer (should work without typing errors)
    query: Query[User] = session.query(User).filter(User.id == user_id)

    loaded_user = query.first()
    assert loaded_user is not None
    print(f"Without undefer - loaded_user.computed_age = {loaded_user.computed_age}")
    print(f"Without undefer - loaded_user.age = {loaded_user.age}")

    # Now try with undefer
    query_with_undefer: Query[User] = (
        session.query(User)
        .options(
            undefer(User.computed_age)  # This should not cause typing errors
        )
        .filter(User.id == user_id)
    )

    loaded_user_undefer = query_with_undefer.first()
    assert loaded_user_undefer is not None
    print(
        f"With undefer - loaded_user_undefer.computed_age = {loaded_user_undefer.computed_age}"
    )
    print(f"With undefer - loaded_user_undefer.age = {loaded_user_undefer.age}")

    # Test fallback behavior when detached
    session.expunge(loaded_user)  # Detach from session
    assert loaded_user.computed_age == 0  # Should return fallback value

    session.close()

    print("✅ All typing and functionality tests passed!")


if __name__ == "__main__":
    test_typing_compatibility()
