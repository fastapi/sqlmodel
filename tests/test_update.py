from pytest import raises
from sqlmodel import Field, SQLModel


def test_sqlmodel_update():
    class Organization(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        city: str
        headquarters: str

    class OrganizationUpdate(SQLModel):
        name: str
        city: str | None = None

    org = Organization(name="Example Org", city="New York", headquarters="NYC HQ")
    org_in = OrganizationUpdate(name="Updated org")
    org.sqlmodel_update(
        org_in,
        update={
            "headquarters": "-",  # This field is in Organization, but not in OrganizationUpdate
        },
        exclude_unset=True,
    )
    # fields that should stay the same
    assert org.city == "New York"
    # fields that should be updated
    assert org.name == "Updated org"
    assert org.headquarters == "-"
    # test raise value error when passing in updates other than dict or BaseModel
    with raises(ValueError):
        org.sqlmodel_update(["Boston"])
