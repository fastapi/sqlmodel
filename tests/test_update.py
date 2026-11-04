import pytest
from sqlmodel import Field, SQLModel


def test_sqlmodel_update():
    class Organization(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        headquarters: str

    class OrganizationUpdate(SQLModel):
        name: str

    org = Organization(name="Example Org", city="New York", headquarters="NYC HQ")
    org_in = OrganizationUpdate(name="Updated org")
    result = org.sqlmodel_update(
        org_in,
        update={
            "headquarters": "-",  # This field is in Organization, but not in OrganizationUpdate
        },
    )
    assert result is org
    assert org.name == "Updated org"
    assert org.headquarters == "-"
    assert org.id is None


def test_sqlmodel_update_dict():
    class Organization(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        headquarters: str

    org = Organization(name="Example Org", headquarters="NYC HQ")
    result = org.sqlmodel_update(
        {"name": "New Name", "extra_field": "val"},
        update={"headquarters": "Berlin", "other_extra": "val2"},
    )
    assert result is org
    assert org.name == "New Name"
    assert org.headquarters == "Berlin"
    assert not hasattr(org, "extra_field")
    assert not hasattr(org, "other_extra")


def test_sqlmodel_update_base_model_extra_update_keys():
    class Organization(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        headquarters: str

    class OrganizationUpdate(SQLModel):
        name: str

    org = Organization(name="Example Org", headquarters="NYC HQ")
    org_in = OrganizationUpdate(name="Updated org")
    result = org.sqlmodel_update(
        org_in,
        update={
            "headquarters": "Berlin",
            "non_model_field": "ignored",
        },
    )
    assert result is org
    assert org.name == "Updated org"
    assert org.headquarters == "Berlin"
    assert not hasattr(org, "non_model_field")


def test_sqlmodel_update_invalid_type_raises_value_error():
    class Organization(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str

    org = Organization(name="Example Org")
    with pytest.raises(ValueError, match="Can't use sqlmodel_update"):
        org.sqlmodel_update(42)  # type: ignore
