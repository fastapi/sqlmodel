from pydantic import AwareDatetime, NaiveDatetime
from sqlmodel import Field, SQLModel


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    starts_at: AwareDatetime
    local_time: NaiveDatetime


def main():
    data = {
        "starts_at": "2026-01-01T12:00:00Z",
        "local_time": "2026-01-01T12:00:00",
    }
    event = Event.model_validate(data)
    print("Event:", event)


if __name__ == "__main__":
    main()
