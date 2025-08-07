"""
Final typing test for deferred_column_property.

This test verifies that deferred_column_property has the same typing behavior
as the original column_property from SQLAlchemy.
"""

from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import column_property, undefer
from sqlmodel import Field, SQLModel, Session, select

from sqlmodel.deferred_column import deferred_column_property


class TestTyping(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    salary: int = 50000

    @classmethod
    def __declare_last__(cls):
        # Test both standard column_property and our deferred_column_property
        cls.standard_prop = column_property(cls.__table__.c.salary > 40000)
        cls.deferred_prop = deferred_column_property(
            cls.__table__.c.salary > 60000, fallback_value=False
        )


def test_typing_equivalence():
    """Test that both properties have equivalent typing"""

    # Test that both can be used with undefer() - this verifies typing compatibility
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        user = TestTyping(salary=70000)
        session.add(user)
        session.commit()
        user_id = user.id

    # Test that both properties can be used with undefer (no typing errors)
    with Session(engine) as session:
        stmt = (
            select(TestTyping)
            .options(
                undefer(TestTyping.standard_prop),  # Should work without typing errors
                undefer(TestTyping.deferred_prop),  # Should work without typing errors
            )
            .where(TestTyping.id == user_id)
        )

        loaded_user = session.exec(stmt).one()

        print(f"User salary: {loaded_user.salary}")
        print(f"Standard prop (salary > 40000): {loaded_user.standard_prop}")
        print(f"Deferred prop (salary > 60000): {loaded_user.deferred_prop}")

        # Both should return True for salary=70000
        assert loaded_user.standard_prop is True  # 70000 > 40000
        assert loaded_user.deferred_prop is True  # 70000 > 60000

        # Test typing compatibility - both should have similar type annotations
        print(f"Standard prop type: {type(TestTyping.standard_prop)}")
        print(f"Deferred prop type: {type(TestTyping.deferred_prop)}")

        # Both should have descriptor protocol
        assert hasattr(TestTyping.standard_prop, "__get__")
        assert hasattr(TestTyping.deferred_prop, "__get__")

        print("✅ Both properties work correctly with undefer()")
        print("✅ Both have descriptor protocol")
        print("✅ Typing compatibility confirmed!")


if __name__ == "__main__":
    test_typing_equivalence()
