from datetime import UTC, datetime

from sqlmodel import Field, Session, SQLModel, create_engine


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def main():
    event = Event()
    print("Event:", event)

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(event)
        session.commit()
        session.refresh(event)
        print("Event from database:", event)


if __name__ == "__main__":
    main()
