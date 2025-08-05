"""
Демонстрация нового поля __sqlalchemy_hybrid_property_setters__
"""

from typing import Optional
from sqlalchemy.ext.hybrid import hybrid_property
from sqlmodel import Field, SQLModel


def test_hybrid_property_setters_field(clear_sqlmodel):
    """Тест нового поля __sqlalchemy_hybrid_property_setters__"""

    class User(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        computed_value: Optional[str] = Field(default=None)

        @hybrid_property
        def display_name(self) -> str:
            """Hybrid property с setter"""
            return self.computed_value or self.name

        @display_name.inplace.setter
        def _display_name_setter(self, value: str) -> None:
            """Setter для display_name"""
            self.computed_value = f"User: {value}"

        @hybrid_property
        def read_only_name(self) -> str:
            """Hybrid property БЕЗ setter"""
            return f"ReadOnly: {self.name}"

    # Проверяем что поле создалось и содержит только hybrid properties с setters
    assert hasattr(User, "__sqlalchemy_hybrid_property_setters__")

    # display_name имеет setter - должен быть в списке
    assert "display_name" in User.__sqlalchemy_hybrid_property_setters__

    # read_only_name НЕ имеет setter - НЕ должен быть в списке
    assert "read_only_name" not in User.__sqlalchemy_hybrid_property_setters__

    # _display_name_setter - функция setter - НЕ должна быть в списке
    assert "_display_name_setter" not in User.__sqlalchemy_hybrid_property_setters__

    print("✅ Поле __sqlalchemy_hybrid_property_setters__ работает корректно!")
    print(f"   Содержит: {list(User.__sqlalchemy_hybrid_property_setters__.keys())}")


def test_hybrid_property_setter_functionality(clear_sqlmodel):
    """Тест функциональности hybrid property setter через новое поле"""

    class User(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        computed_value: Optional[str] = Field(default=None)

        @hybrid_property
        def display_name(self) -> str:
            return self.computed_value or self.name

        @display_name.inplace.setter
        def _display_name_setter(self, value: str) -> None:
            self.computed_value = f"User: {value}"

    # Тест прямого присваивания
    user = User(name="John Doe")
    user.display_name = "Custom Name"
    assert user.computed_value == "User: Custom Name"
    assert user.display_name == "User: Custom Name"

    # Тест model_validate
    test_data = {"id": 1, "name": "Jane Doe", "display_name": "Validated Name"}
    validated_user = User.model_validate(test_data)
    assert validated_user.computed_value == "User: Validated Name"
    assert validated_user.display_name == "User: Validated Name"

    print("✅ Функциональность hybrid property setter работает через новое поле!")


if __name__ == "__main__":
    test_hybrid_property_setters_field()
    test_hybrid_property_setter_functionality()
    print("\n🎉 Все тесты прошли успешно!")
