from typing import Dict, Optional

from sqlmodel import Field, Session, SQLModel, create_engine
from typing_extensions import TypedDict

from .conftest import needs_pydanticv2

pytestmark = needs_pydanticv2


def test_dict_maps_to_json(clear_sqlmodel):
    class Resource(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        data: dict

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    resource = Resource(name="test", data={"key": "value", "num": 42})

    with Session(engine) as session:
        session.add(resource)
        session.commit()
        session.refresh(resource)

        assert resource.data["key"] == "value"
        assert resource.data["num"] == 42


def test_typing_dict_maps_to_json(clear_sqlmodel):
    """Test if typing.Dict type annotation works without explicit sa_type"""

    class Resource(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        data: Dict[str, int]

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    resource = Resource(name="test", data={"count": 100})

    with Session(engine) as session:
        session.add(resource)
        session.commit()
        session.refresh(resource)

        assert resource.data["count"] == 100


class Metadata(TypedDict):
    name: str
    email: str


def test_typeddict_automatic_json_mapping(clear_sqlmodel):
    """
    Test that TypedDict fields automatically map to JSON type.

    This fixes the original error:
    ValueError: <class 'app.models.NeonMetadata'> has no matching SQLAlchemy type
    """

    class ConnectedResource(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        neon_metadata: Metadata

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    resource = ConnectedResource(
        name="my-resource",
        neon_metadata={"name": "John Doe", "email": "john.doe@example.com"},
    )

    with Session(engine) as session:
        session.add(resource)
        session.commit()
        session.refresh(resource)

        assert resource.neon_metadata["name"] == "John Doe"
        assert resource.neon_metadata["email"] == "john.doe@example.com"
