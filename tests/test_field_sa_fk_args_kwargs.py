from sqlalchemy import ForeignKey, create_engine
from sqlmodel import Field, SQLModel


def test_base_model_fk(clear_sqlmodel, caplog) -> None:
    class User(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)

    class Base(SQLModel):
        owner_id: int | None = Field(
            default=None, sa_column_args=(ForeignKey("user.id", ondelete="SET NULL"),)
        )

    class Asset(Base, table=True):
        id: int | None = Field(default=None, primary_key=True)

    class Document(Base, table=True):
        id: int | None = Field(default=None, primary_key=True)

    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)

    assert (
        "FOREIGN KEY(owner_id) REFERENCES user (id) ON DELETE SET NULL" in caplog.text
    )


def test_base_model_fk_args(clear_sqlmodel, caplog) -> None:
    class User(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)

    class Base(SQLModel):
        owner_id: int | None = Field(
            default=None,
            foreign_key=ForeignKey("user.id", ondelete="SET NULL"),
        )

    class Asset(Base, table=True):
        id: int | None = Field(default=None, primary_key=True)

    class Document(Base, table=True):
        id: int | None = Field(default=None, primary_key=True)

    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)

    assert (
        "FOREIGN KEY(owner_id) REFERENCES user (id) ON DELETE SET NULL" in caplog.text
    )
