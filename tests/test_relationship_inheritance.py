import datetime
from typing import Optional

from sqlalchemy import DateTime, func
from sqlalchemy.orm import declared_attr, relationship
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


def test_relationship_inheritance() -> None:
    def now():
        return datetime.datetime.now(tz=datetime.timezone.utc)

    class User(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str

    class CreatedUpdatedMixin(SQLModel):
        # Fields in reusable base models must be defined using `sa_type` and `sa_column_kwargs` instead of `sa_column`
        # https://github.com/tiangolo/sqlmodel/discussions/743
        #
        # created_at: datetime.datetime = Field(default_factory=now, sa_column=DateTime(default=now))
        created_at: datetime.datetime = Field(
            default_factory=now, sa_type=DateTime, sa_column_kwargs={"default": now}
        )

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

        updated_at: datetime.datetime = Field(
            default_factory=now, sa_type=DateTime, sa_column_kwargs={"default": now}
        )
        updated_by_id: Optional[int] = Field(default=None, foreign_key="user.id")
        updated_by: Optional[User] = Relationship(
            sa_relationship=declared_attr(
                lambda cls: relationship(User, foreign_keys=cls.updated_by_id)
            )
        )

    class Asset(CreatedUpdatedMixin, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str

    # Demonstrate that the mixin can be applied to more than 1 model
    class Document(CreatedUpdatedMixin, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    john = User(name="John")
    jane = User(name="Jane")
    asset = Asset(name="Test", created_by=john, updated_by=jane)
    doc = Document(name="Resume", created_by=jane, updated_by=john)

    with Session(engine) as session:
        session.add(asset)
        session.add(doc)
        session.commit()

    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(User)) == 2

        asset = session.exec(select(Asset)).one()
        assert asset.created_by.name == "John"
        assert asset.updated_by.name == "Jane"

        doc = session.exec(select(Document)).one()
        assert doc.created_by.name == "Jane"
        assert doc.updated_by.name == "John"
