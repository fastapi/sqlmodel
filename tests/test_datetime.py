from datetime import date, datetime, time, timedelta, timezone, tzinfo
from io import StringIO
from typing import Annotated, Any

import pytest
from alembic.autogenerate import compare_metadata, render_python_code
from alembic.migration import MigrationContext
from alembic.operations import Operations, ops
from pydantic import AwareDatetime, NaiveDatetime, ValidationError
from sqlalchemy import Column, Date, DateTime, Interval, Time
from sqlalchemy.dialects import mysql, postgresql, sqlite
from sqlalchemy.exc import StatementError
from sqlalchemy.schema import CreateTable
from sqlmodel import (
    Field,
    Session,
    SQLModel,
    UTCDateTime,
    create_engine,
    select,
    update,
)


@pytest.mark.parametrize("nullable", [False, True])
@pytest.mark.parametrize(
    "annotation, timezone_enabled, error_type",
    [
        (datetime, True, None),
        (AwareDatetime, True, "timezone_aware"),
        (NaiveDatetime, False, "timezone_naive"),
        (Annotated[datetime, AwareDatetime], True, "timezone_aware"),
        (Annotated[datetime, NaiveDatetime], False, "timezone_naive"),
        (Annotated[datetime, AwareDatetime()], True, "timezone_aware"),
        (Annotated[datetime, NaiveDatetime()], False, "timezone_naive"),
        (Annotated[NaiveDatetime, AwareDatetime], True, "timezone_aware"),
        (Annotated[AwareDatetime, NaiveDatetime], False, "timezone_naive"),
        (Annotated[datetime, NaiveDatetime, AwareDatetime], True, "timezone_aware"),
        (Annotated[datetime, AwareDatetime, NaiveDatetime], False, "timezone_naive"),
        (Annotated[datetime, "other metadata"], True, None),
    ],
)
def test_datetime_types(
    annotation: Any, timezone_enabled: bool, error_type: str | None, nullable: bool
) -> None:
    if nullable:
        annotation = annotation | None

    class Event(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        occurred_at: annotation

    column = SQLModel.metadata.tables["event"].c.occurred_at
    assert isinstance(column.type, UTCDateTime if timezone_enabled else DateTime)
    assert column.type.timezone is timezone_enabled
    assert column.nullable is nullable

    aware = datetime(2026, 1, 1, 12, tzinfo=timezone(timedelta(hours=2)))
    naive = datetime(2026, 1, 1, 12)
    valid = aware if timezone_enabled else naive
    assert Event.model_validate({"occurred_at": valid}).occurred_at == valid
    if error_type is None:
        assert Event.model_validate({"occurred_at": naive}).occurred_at == naive
    else:
        invalid = naive if timezone_enabled else aware
        with pytest.raises(ValidationError) as exc_info:
            Event.model_validate({"occurred_at": invalid})
        assert exc_info.value.errors()[0]["type"] == error_type
    if nullable:
        assert Event.model_validate({"occurred_at": None}).occurred_at is None


def test_inherited_annotated_datetime() -> None:
    class EventBase(SQLModel):
        occurred_at: Annotated[datetime, NaiveDatetime, Field(index=True)]

    class Event(EventBase, table=True):
        id: int | None = Field(default=None, primary_key=True)

    column = SQLModel.metadata.tables["event"].c.occurred_at
    assert column.type.timezone is False
    assert column.index is True


@pytest.mark.parametrize("annotation", [datetime, AwareDatetime, NaiveDatetime])
@pytest.mark.parametrize("timezone_enabled", [False, True])
@pytest.mark.parametrize("use_column", [False, True])
def test_explicit_datetime_type(
    annotation: Any, timezone_enabled: bool, use_column: bool
) -> None:
    sa_type = DateTime(timezone=timezone_enabled)
    if use_column:
        field = Field(sa_column=Column(sa_type))
    else:
        field = Field(sa_type=sa_type)

    class Event(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        occurred_at: annotation = field

    assert SQLModel.metadata.tables["event"].c.occurred_at.type is sa_type


def test_explicit_datetime_type_class() -> None:
    class Event(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        occurred_at: datetime = Field(sa_type=DateTime)

    assert SQLModel.metadata.tables["event"].c.occurred_at.type.timezone is False


def test_other_temporal_types() -> None:
    class Event(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        day: date
        at: time
        duration: timedelta

    columns = SQLModel.metadata.tables["event"].c
    assert isinstance(columns.day.type, Date)
    assert isinstance(columns.at.type, Time)
    assert isinstance(columns.duration.type, Interval)


@pytest.mark.parametrize(
    "dialect, aware_type, naive_type",
    [
        (
            postgresql.dialect(),
            "TIMESTAMP WITH TIME ZONE",
            "TIMESTAMP WITHOUT TIME ZONE",
        ),
        (mysql.dialect(), "DATETIME", "DATETIME"),
        (sqlite.dialect(), "DATETIME", "DATETIME"),
    ],
)
def test_datetime_column_types(dialect: Any, aware_type: str, naive_type: str) -> None:
    class Event(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        occurred_at: datetime
        local_time: NaiveDatetime

    ddl = str(CreateTable(SQLModel.metadata.tables["event"]).compile(dialect=dialect))
    assert f"occurred_at {aware_type} NOT NULL" in ddl
    assert f"local_time {naive_type} NOT NULL" in ddl


def test_sqlite_datetime_round_trip() -> None:
    class Event(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        occurred_at: datetime
        local_time: NaiveDatetime
        optional_time: datetime | None = None

    aware = datetime(2026, 1, 1, 12, tzinfo=timezone(timedelta(hours=2)))
    naive = datetime(2026, 1, 1, 12)
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        event = Event(occurred_at=aware, local_time=naive)
        session.add(event)
        session.flush()
        # Binding doesn't change the original value on the model.
        assert event.occurred_at is aware
        assert (
            session.connection()
            .exec_driver_sql("SELECT occurred_at FROM event")
            .scalar_one()
            == "2026-01-01 10:00:00.000000"
        )
        session.commit()
        session.refresh(event)
        assert event.occurred_at == aware
        assert event.occurred_at.tzinfo is timezone.utc
        assert event.local_time == naive
        assert event.optional_time is None
        event_id = event.id

    with Session(engine) as session:
        loaded = session.get(Event, event_id)
        assert loaded is not None
        assert loaded.occurred_at.tzinfo is timezone.utc
        # Query parameters use the same UTC normalization as inserted values.
        assert (
            session.exec(select(Event).where(Event.occurred_at == aware)).one()
            is loaded
        )
        assert session.exec(select(Event.occurred_at)).one().tzinfo is timezone.utc
        later = aware + timedelta(hours=1)
        session.exec(update(Event).values(occurred_at=later))
        session.commit()
        session.refresh(loaded)
        assert loaded.occurred_at == later
        assert loaded.occurred_at.tzinfo is timezone.utc


class UndefinedOffset(tzinfo):
    def utcoffset(self, dt: datetime | None) -> None:
        return None


@pytest.mark.parametrize("offset", [None, UndefinedOffset()])
@pytest.mark.parametrize("operation", ["insert", "update", "filter"])
def test_naive_database_parameters(offset: tzinfo | None, operation: str) -> None:
    class Event(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        occurred_at: datetime

    naive = datetime(2026, 1, 1, 12, tzinfo=offset)
    event = Event.model_validate({"occurred_at": naive})
    # Plain datetime validation remains permissive, including a tzinfo object
    # that doesn't actually provide an offset.
    assert event.occurred_at is naive
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        with pytest.raises(StatementError, match="timezone information") as exc_info:
            if operation == "insert":
                session.add(event)
                session.flush()
            elif operation == "update":
                session.exec(update(Event).values(occurred_at=naive))
            else:
                session.exec(select(Event).where(Event.occurred_at > naive))
        assert isinstance(exc_info.value.orig, ValueError)
        assert "NaiveDatetime" in str(exc_info.value.orig)


@pytest.mark.parametrize("timezone_enabled", [False, True])
def test_explicit_datetime_bypasses_utc_processing(timezone_enabled: bool) -> None:
    class Event(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        occurred_at: datetime = Field(sa_type=DateTime(timezone=timezone_enabled))

    aware = datetime(2026, 1, 1, 12, tzinfo=timezone(timedelta(hours=2)))
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        event = Event(occurred_at=aware)
        session.add(event)
        session.commit()
        session.refresh(event)
        assert event.occurred_at == datetime(2026, 1, 1, 12)
        assert event.occurred_at.tzinfo is None


def test_postgresql_datetime_processing() -> None:
    # PostgreSQL drivers receive aware parameters and may return values in the
    # connection's timezone. Exercise the complete SQLAlchemy type processors.
    dialect = postgresql.dialect()
    type_ = UTCDateTime().dialect_impl(dialect)
    bind = type_.bind_processor(dialect)
    result = type_.result_processor(dialect, None)
    assert bind is not None
    assert result is not None
    aware = datetime(2026, 1, 1, 12, tzinfo=timezone(timedelta(hours=2)))
    bound = bind(aware)
    assert bound == aware
    assert bound.tzinfo is timezone.utc
    loaded = result(aware)
    assert loaded == aware
    assert loaded.tzinfo is timezone.utc
    assert bind(None) is None
    assert result(None) is None


def test_existing_sqlite_utc_data() -> None:
    class Event(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        occurred_at: datetime

    engine = create_engine("sqlite://")
    with engine.begin() as connection:
        connection.exec_driver_sql(
            "CREATE TABLE event (id INTEGER NOT NULL PRIMARY KEY, "
            "occurred_at DATETIME NOT NULL)"
        )
        connection.exec_driver_sql(
            "INSERT INTO event VALUES (1, '2026-01-01 12:00:00.000000')"
        )
        context = MigrationContext.configure(connection, opts={"compare_type": True})
        assert compare_metadata(context, SQLModel.metadata) == []

    with Session(engine) as session:
        event = session.get(Event, 1)
        assert event is not None
        assert event.occurred_at == datetime(2026, 1, 1, 12, tzinfo=timezone.utc)
        assert event.occurred_at.tzinfo is timezone.utc


def test_alembic_datetime_rendering() -> None:
    class Event(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        occurred_at: datetime

    table = SQLModel.metadata.tables["event"]
    migration = ops.UpgradeOps(ops=[ops.CreateTableOp.from_table(table)])
    rendered = render_python_code(migration)
    assert "sqlmodel.sql.sqltypes.UTCDateTime()" in rendered
    # Execute the generated migration, including the custom type constructor.
    namespace: dict[str, Any] = {}
    exec(
        "import sqlalchemy as sa\nimport sqlmodel.sql.sqltypes\n"
        "from alembic import op\ndef upgrade():\n    " + rendered,
        namespace,
    )
    output = StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql",
        opts={"as_sql": True, "output_buffer": output},
    )
    with Operations.context(context):
        namespace["upgrade"]()
    assert "occurred_at TIMESTAMP WITH TIME ZONE NOT NULL" in output.getvalue()
