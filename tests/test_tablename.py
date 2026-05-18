from sqlalchemy import inspect
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool


def _engine():
    return create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )


def test_default_tablename() -> None:
    """table=True models get __tablename__ = classname.lower() by default."""

    class Gadget(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)

    assert Gadget.__tablename__ == "gadget"

    engine = _engine()
    SQLModel.metadata.create_all(engine)
    assert inspect(engine).has_table("gadget")


def test_explicit_tablename() -> None:
    """An explicit __tablename__ overrides the default."""

    class Widget(SQLModel, table=True):
        __tablename__ = "custom_widgets"
        id: int | None = Field(default=None, primary_key=True)
        name: str

    assert Widget.__tablename__ == "custom_widgets"

    engine = _engine()
    SQLModel.metadata.create_all(engine)
    assert inspect(engine).has_table("custom_widgets")
    assert not inspect(engine).has_table("widget")

    with Session(engine) as session:
        session.add(Widget(name="sprocket"))
        session.commit()

    with Session(engine) as session:
        row = session.exec(select(Widget)).first()
        assert row is not None
        assert row.name == "sprocket"


def test_tablename_inheritance_default() -> None:
    """A subclass that is also a table gets its own default __tablename__."""

    class BaseThing(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        kind: str = "base"

    class SubThing(BaseThing, table=True):
        extra: str | None = None

    assert BaseThing.__tablename__ == "basething"
    assert SubThing.__tablename__ == "subthing"


def test_tablename_inheritance_explicit_child() -> None:
    """A subclass can set its own __tablename__, visible on the class."""

    class Vehicle(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        kind: str = ""

    class Truck(Vehicle, table=True):
        __tablename__ = "trucks"
        payload: int | None = None

    assert Vehicle.__tablename__ == "vehicle"
    assert Truck.__tablename__ == "trucks"


def test_tablename_default_on_plain_model() -> None:
    """Non-table models also get a default __tablename__."""

    class Schema(SQLModel):
        name: str

    assert Schema.__tablename__ == "schema"
