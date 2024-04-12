from typing import Optional

from sqlalchemy.orm import declared_attr, relationship
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


def test_relationship_inheritance() -> None:
    class User(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str

    class CreatedUpdatedMixin(SQLModel):
        # With Pydantic V2, it is also possible to define `created_by` like this:
        #
        #   ```python
        #   @declared_attr
        #   def _created_by(cls):
        #       return relationship(User, foreign_keys=cls.created_by_id)
        #
        #   created_by: Optional[User] = Relationship(sa_relationship=_created_by))
        #   ```
        #
        # The difference from Pydantic V1 is that Pydantic V2 plucks attributes with names starting with '_' (but not '__')
        # from class attributes and stores them separately as instances of `pydantic.ModelPrivateAttr` somewhere in depths of
        # Pydantic internals.  Under Pydantic V1 this doesn't happen, so SQLAlchemy ends up having two class attributes
        # (`_created_by` and `created_by`) corresponding to one database attribute, causing a conflict and unreliable behavior.
        # The approach with a lambda always works because it doesn't produce the second class attribute and thus eliminates
        # the possibility of a conflict entirely.
        #
        created_by_id: Optional[int] = Field(default=None, foreign_key="user.id")
        created_by: Optional[User] = Relationship(
            sa_relationship=declared_attr(
                lambda cls: relationship(User, foreign_keys=cls.created_by_id)
            )
        )

        updated_by_id: Optional[int] = Field(default=None, foreign_key="user.id")
        updated_by: Optional[User] = Relationship(
            sa_relationship=declared_attr(
                lambda cls: relationship(User, foreign_keys=cls.updated_by_id)
            )
        )

    class Asset(CreatedUpdatedMixin, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    john = User(name="John")
    jane = User(name="Jane")
    asset = Asset(created_by=john, updated_by=jane)

    with Session(engine) as session:
        session.add(asset)
        session.commit()

    with Session(engine) as session:
        asset = session.exec(select(Asset)).one()
        assert asset.created_by.name == "John"
        assert asset.updated_by.name == "Jane"
