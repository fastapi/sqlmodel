from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.hybrid import hybrid_property
from sqlmodel import Field, Session, SQLModel


def test_hybrid_property_setter_direct(clear_sqlmodel):
    """Test direct assignment through hybrid property setter"""

    class User(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        # Simple field to store computed value
        computed_value: Optional[str] = Field(default=None)

        @hybrid_property
        def display_name(self) -> str:
            """Getter for display name"""
            return self.computed_value or self.name

        @display_name.inplace.setter
        def _display_name_setter(self, value: str) -> None:
            """Setter for display name - stores in computed_value"""
            self.computed_value = f"User: {value}"

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Create user
        user = User(name="John Doe")
        session.add(user)
        session.commit()
        session.refresh(user)

        # Test direct assignment (should trigger setter)
        user.display_name = "Jane Smith"

        # Verify the setter was triggered
        assert user.computed_value == "User: Jane Smith"
        assert user.display_name == "User: Jane Smith"


def test_hybrid_property_setter_with_model_validate(clear_sqlmodel):
    """Test hybrid property setter through model_validate"""

    class User(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        computed_value: Optional[str] = Field(default=None)

        @hybrid_property
        def display_name(self) -> str:
            """Getter for display name"""
            return self.computed_value or self.name

        @display_name.inplace.setter
        def _display_name_setter(self, value: str) -> None:
            """Setter for display name"""
            self.computed_value = f"User: {value}"

    # Test model_validate with hybrid property
    test_data = {
        "id": 1,
        "name": "Jane Doe",
        "display_name": "Custom Display Name",  # Through hybrid property
    }

    validated_user = User.model_validate(test_data)

    # Verify the hybrid property setter was triggered
    assert validated_user.name == "Jane Doe"
    assert validated_user.computed_value == "User: Custom Display Name"
    assert validated_user.display_name == "User: Custom Display Name"


def test_hybrid_property_setter_detection(clear_sqlmodel):
    """Test detection of hybrid property with setter"""

    class TestModel(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        stored_value: str = Field(default="")

        @hybrid_property
        def computed_value(self) -> str:
            return self.stored_value.upper()

        @computed_value.inplace.setter
        def _computed_value_setter(self, value: str) -> None:
            self.stored_value = value.lower()

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        model = TestModel(name="test")
        session.add(model)
        session.commit()
        session.refresh(model)

        # Test that hybrid property setter works
        model.computed_value = "HELLO WORLD"

        # Verify the setter logic was executed
        assert model.stored_value == "hello world"
        assert model.computed_value == "HELLO WORLD"


def test_hybrid_property_without_setter(clear_sqlmodel):
    """Test hybrid property without setter (should not interfere)"""

    class TestModel(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        value: int = 0

        @hybrid_property
        def doubled_value(self) -> int:
            return self.value * 2

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        model = TestModel(name="test", value=5)
        session.add(model)
        session.commit()
        session.refresh(model)

        # Regular attribute assignment should work normally
        model.value = 10
        assert model.value == 10
        assert model.doubled_value == 20

        # Hybrid property without setter should be read-only
        # (attempting to set it should fall through to normal Pydantic behavior)
        model.name = "updated"
        assert model.name == "updated"
