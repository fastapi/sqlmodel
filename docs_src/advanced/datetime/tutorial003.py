from datetime import datetime

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(sa_type=DateTime(timezone=False))


def main():
    event = Event(created_at=datetime(2026, 1, 1, 12))
    print("Event:", event)


if __name__ == "__main__":
    main()
