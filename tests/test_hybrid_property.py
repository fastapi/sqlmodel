"""Tests for SQLAlchemy descriptor compatibility with SQLModel metaclass.

Regression tests for https://github.com/fastapi/sqlmodel/issues/299:

  Declaring a ``sqlalchemy.ext.hybrid.hybrid_property`` (or ``hybrid_method``)
  directly on a ``SQLModel`` class with ``table=True`` raises
  ``pydantic.errors.PydanticUserError: A non-annotated attribute was detected``
  because Pydantic v2 inspects every non-dunder attribute on the class body and
  expects an annotation.  ``hybrid_property`` is a SQLAlchemy descriptor, not a
  Pydantic field, so the SQLModel metaclass must tell Pydantic to skip it via
  ``model_config["ignored_types"]``.
"""

from datetime import datetime

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlmodel import Field, Session, SQLModel, create_engine


def _make_engine():
    return create_engine("sqlite:///:memory:")


def test_table_model_allows_hybrid_property(clear_sqlmodel):
    """A ``hybrid_property`` defined on a ``table=True`` model must not crash
    class construction and must be callable at the instance level."""

    class Span(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        start: datetime
        end: datetime

        @hybrid_property
        def duration_seconds(self) -> float:
            return (self.end - self.start).total_seconds()

    engine = _make_engine()
    SQLModel.metadata.create_all(engine)
    # The hybrid attribute must not be turned into a SQL column.
    assert "duration_seconds" not in Span.__table__.columns

    with Session(engine) as session:
        span = Span(start=datetime(2024, 1, 1), end=datetime(2024, 1, 2))
        session.add(span)
        session.commit()
        session.refresh(span)
        assert span.duration_seconds == 86400.0


def test_table_model_allows_hybrid_method(clear_sqlmodel):
    """A ``hybrid_method`` must not raise during class construction."""

    class Box(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        width: int
        height: int

        @hybrid_method
        def area_at_least(self, threshold: int) -> bool:
            return (self.width * self.height) >= threshold

    engine = _make_engine()
    SQLModel.metadata.create_all(engine)
    assert "area_at_least" not in Box.__table__.columns

    with Session(engine) as session:
        box = Box(width=4, height=5)
        session.add(box)
        session.commit()
        session.refresh(box)
        assert box.area_at_least(10) is True
        assert box.area_at_least(100) is False


def test_table_model_allows_association_proxy(clear_sqlmodel):
    """An ``association_proxy`` declared without an annotation must not raise.

    The proxy itself does not need to be functional for this regression test;
    its presence used to crash the metaclass in Pydantic v2 because
    ``AssociationProxy`` has no type annotation.
    """

    class Item(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        label: str
        # ``association_proxy`` is also a non-annotated SQLAlchemy descriptor.
        # We do not need a working relationship to assert the metaclass does
        # not blow up at class-body time -- that is the regression.
        legacy_alias = association_proxy("label", "label")

    engine = _make_engine()
    SQLModel.metadata.create_all(engine)
    assert "legacy_alias" not in Item.__table__.columns


def test_non_table_model_allows_hybrid_property(clear_sqlmodel):
    """The fix must also work for ``table=False`` (plain Pydantic) models so
    that mix-ins shared between table and non-table classes do not break."""

    class HasArea(SQLModel):
        width: int = 0
        height: int = 0

        @hybrid_property
        def area(self) -> int:
            return self.width * self.height

    instance = HasArea(width=3, height=4)
    assert instance.area == 12
