from datetime import datetime

from pydantic import NaiveDatetime
from sqlmodel import Field, SQLModel


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: NaiveDatetime


def main():
    event = Event.model_validate({"created_at": datetime(2026, 1, 1, 12)})
    print("Event:", event)


if __name__ == "__main__":
    main()
