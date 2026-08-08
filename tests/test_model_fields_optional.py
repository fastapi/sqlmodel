import pytest
from pydantic import ValidationError
from sqlmodel import Field, SQLModel
from sqlmodel._compat import SQLModelConfig


def test_model_fields_optional_basic(clear_sqlmodel):
    """Test that model_fields_optional='all' makes all inherited fields Optional
    with a default of None."""

    class HeroBase(SQLModel):
        name: str
        secret_name: str
        age: int | None = None

    class HeroUpdate(HeroBase, model_fields_optional="all"):
        pass

    # All fields should be optional (not required)
    for field_info in HeroUpdate.model_fields.values():
        assert not field_info.is_required()

    # Should be able to create with no arguments
    hero = HeroUpdate()
    assert hero.name is None
    assert hero.secret_name is None
    assert hero.age is None


def test_model_fields_optional_partial_data(clear_sqlmodel):
    """Test creating an instance with only some fields set."""

    class HeroBase(SQLModel):
        name: str
        secret_name: str
        age: int | None = None

    class HeroUpdate(HeroBase, model_fields_optional="all"):
        pass

    hero = HeroUpdate(name="Spider-Man")
    assert hero.name == "Spider-Man"
    assert hero.secret_name is None
    assert hero.age is None


def test_model_fields_optional_exclude_unset(clear_sqlmodel):
    """Test that model_dump(exclude_unset=True) only includes explicitly set
    fields."""

    class HeroBase(SQLModel):
        name: str
        secret_name: str
        age: int | None = None

    class HeroUpdate(HeroBase, model_fields_optional="all"):
        pass

    hero = HeroUpdate(name="Spider-Man")
    dumped = hero.model_dump(exclude_unset=True)
    assert dumped == {"name": "Spider-Man"}


def test_model_fields_optional_override_field(clear_sqlmodel):
    """Test that explicitly redefined fields in the child class are not
    overridden by model_fields_optional."""

    class HeroBase(SQLModel):
        name: str
        secret_name: str
        age: int | None = None

    class HeroUpdate(HeroBase, model_fields_optional="all"):
        name: str  # Keep name required

    # name should still be required
    assert HeroUpdate.model_fields["name"].is_required()
    # Other fields should be optional
    assert not HeroUpdate.model_fields["secret_name"].is_required()
    assert not HeroUpdate.model_fields["age"].is_required()

    with pytest.raises(ValidationError):
        HeroUpdate()  # name is required

    hero = HeroUpdate(name="Batman")
    assert hero.name == "Batman"
    assert hero.secret_name is None


def test_model_fields_optional_preserves_constraints(clear_sqlmodel):
    """Test that field constraints (min_length, ge, etc.) are preserved when
    making fields optional."""

    class HeroBase(SQLModel):
        name: str = Field(min_length=1)
        age: int | None = Field(default=None, ge=0)

    class HeroUpdate(HeroBase, model_fields_optional="all"):
        pass

    # None should be valid for all fields
    hero = HeroUpdate(name=None, age=None)
    assert hero.name is None
    assert hero.age is None

    # Non-None values should still be validated
    with pytest.raises(ValidationError):
        HeroUpdate(name="")  # min_length=1 violated

    with pytest.raises(ValidationError):
        HeroUpdate(age=-1)  # ge=0 violated

    # Valid non-None values should work
    hero = HeroUpdate(name="X", age=5)
    assert hero.name == "X"
    assert hero.age == 5


def test_model_fields_optional_multiple_inheritance(clear_sqlmodel):
    """Test model_fields_optional with multiple levels of inheritance."""

    class PersonBase(SQLModel):
        first_name: str
        last_name: str

    class EmployeeBase(PersonBase):
        employee_id: int
        department: str

    class EmployeeUpdate(EmployeeBase, model_fields_optional="all"):
        pass

    # All fields from all base classes should be optional
    for field_info in EmployeeUpdate.model_fields.values():
        assert not field_info.is_required()

    employee = EmployeeUpdate(department="Engineering")
    assert employee.department == "Engineering"
    assert employee.first_name is None
    assert employee.last_name is None
    assert employee.employee_id is None


def test_model_fields_optional_via_model_config(clear_sqlmodel):
    """Test model_fields_optional via model_config dict."""

    class HeroBase(SQLModel):
        name: str
        secret_name: str
        age: int | None = None

    class HeroUpdate(HeroBase):
        model_config = SQLModelConfig(model_fields_optional="all")

    # All fields should be optional
    for field_info in HeroUpdate.model_fields.values():
        assert not field_info.is_required()

    hero = HeroUpdate()
    assert hero.name is None
    assert hero.secret_name is None
    assert hero.age is None


def test_model_fields_optional_with_table_base(clear_sqlmodel):
    """Test that model_fields_optional works alongside table models."""

    class HeroBase(SQLModel):
        name: str
        secret_name: str
        age: int | None = None

    class Hero(HeroBase, table=True):
        id: int | None = Field(default=None, primary_key=True)

    class HeroUpdate(HeroBase, model_fields_optional="all"):
        pass

    # Table model should still work normally
    hero = Hero(name="Batman", secret_name="Bruce Wayne")
    assert hero.name == "Batman"

    # Update model should have all optional fields
    update = HeroUpdate(name="Dark Knight")
    assert update.name == "Dark Knight"
    assert update.secret_name is None


def test_model_fields_optional_already_optional_fields(clear_sqlmodel):
    """Test that already-optional fields remain optional and keep their
    defaults."""

    class HeroBase(SQLModel):
        name: str
        nickname: str | None = "Unknown"
        age: int | None = None

    class HeroUpdate(HeroBase, model_fields_optional="all"):
        pass

    hero = HeroUpdate()
    # name was required, should now be None
    assert hero.name is None
    # nickname had a default of "Unknown", should keep it
    assert hero.nickname == "Unknown"
    # age had a default of None, should stay None
    assert hero.age is None


def test_model_fields_optional_model_validate(clear_sqlmodel):
    """Test that model_validate works correctly with model_fields_optional."""

    class HeroBase(SQLModel):
        name: str
        secret_name: str
        age: int | None = None

    class HeroUpdate(HeroBase, model_fields_optional="all"):
        pass

    hero = HeroUpdate.model_validate({"name": "Spider-Man"})
    assert hero.name == "Spider-Man"
    assert hero.secret_name is None

    hero2 = HeroUpdate.model_validate({})
    assert hero2.name is None


def test_model_fields_optional_json_schema(clear_sqlmodel):
    """Test that JSON schema reflects optional fields."""

    class HeroBase(SQLModel):
        name: str
        secret_name: str

    class HeroUpdate(HeroBase, model_fields_optional="all"):
        pass

    schema = HeroUpdate.model_json_schema()
    # No fields should be required in the schema
    assert "required" not in schema or len(schema.get("required", [])) == 0
