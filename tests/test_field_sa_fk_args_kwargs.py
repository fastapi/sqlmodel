import re
from typing import Optional

from sqlalchemy import ForeignKey, create_engine
from sqlmodel import Field, SQLModel


def test_base_model_fk(clear_sqlmodel, caplog) -> None:
    class User(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)

    class Base(SQLModel):
        owner_id: Optional[int] = Field(
            default=None, sa_column_args=(ForeignKey("user.id", ondelete="SET NULL"),)
        )

    class Asset(Base, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)

    class Document(Base, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)

    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)

    fk_log = [
        message
        for message in caplog.messages
        if re.search(
            r"FOREIGN KEY\s*\(owner_id\)\s*REFERENCES\s*user\s*\(id\)", message
        )
    ][0]
    assert "ON DELETE SET NULL" in fk_log


def test_base_model_fk_args(clear_sqlmodel, caplog) -> None:
    class User(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)

    class Base(SQLModel):
        owner_id: Optional[int] = Field(
            default=None,
            foreign_key=ForeignKey("user.id", ondelete="SET NULL"),
        )

    class Asset(Base, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)

    class Document(Base, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)

    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)

    fk_log = [
        message
        for message in caplog.messages
        if re.search(
            r"FOREIGN KEY\s*\(owner_id\)\s*REFERENCES\s*user\s*\(id\)", message
        )
    ][0]
    assert "ON DELETE SET NULL" in fk_log
