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
    org.sqlmodel_update(
        org_in,
        update={
            "headquarters": "-",  # This field is in Organization, but not in OrganizationUpdate
        },
    )
