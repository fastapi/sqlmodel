from pydantic import PrivateAttr
from sqlmodel import Field, Session, SQLModel, create_engine, select


def test_private_attr_default_preserved_after_db_load(clear_sqlmodel):
    """PrivateAttr defaults should be available on instances loaded from DB (#149)."""

    class Item(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        _secret: str = PrivateAttr(default="default_secret")

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        item = Item(name="test")
        assert item._secret == "default_secret"
        db.add(item)
        db.commit()

    with Session(engine) as db:
        loaded_item = db.exec(select(Item)).one()
        # Previously raised AttributeError because __pydantic_private__ was None.
        assert loaded_item._secret == "default_secret"

    SQLModel.metadata.clear()


def test_private_attr_default_factory_preserved_after_db_load(clear_sqlmodel):
    """PrivateAttr with default_factory should work on DB-loaded instances (#149)."""

    class Item(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        _tags: list[str] = PrivateAttr(default_factory=list)

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        item = Item(name="test")
        item._tags.append("hello")
        db.add(item)
        db.commit()

    with Session(engine) as db:
        loaded_item = db.exec(select(Item)).one()
        # Should get a fresh empty list from default_factory, not AttributeError.
        assert loaded_item._tags == []

    SQLModel.metadata.clear()
