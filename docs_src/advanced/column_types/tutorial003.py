from datetime import datetime
try:
    from datetime import UTC
except ImportError:
    UTC = None
from pathlib import Path
from uuid import UUID, uuid4

from pydantic import EmailStr, IPvAnyAddress
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Avatar(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    source_ip_address: IPvAnyAddress
    upload_location: Path
    uploaded_at: datetime = Field(default=datetime.now(tz=UTC))
    author_email: EmailStr


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_avatars():
    avatar_1 = Avatar(
        source_ip_address="127.0.0.1",
        upload_location="/uploads/1/123456789.jpg",
        author_email="tiangolo@example.com",
    )

    avatar_2 = Avatar(
        source_ip_address="192.168.0.1",
        upload_location="/uploads/9/987654321.png",
        author_email="rmasters@example.com",
    )

    with Session(engine) as session:
        session.add(avatar_1)
        session.add(avatar_2)

        session.commit()


def read_avatars():
    with Session(engine) as session:
        statement = select(Avatar).where(Avatar.author_email == "tiangolo@example.com")
        result = session.exec(statement)
        avatar_1: Avatar = result.one()

    print(
        "Avatar 1:",
        {
            "email": avatar_1.author_email,
            "email_type": type(avatar_1.author_email),
            "ip_address": avatar_1.source_ip_address,
            "ip_address_type": type(avatar_1.source_ip_address),
            "upload_location": avatar_1.upload_location,
            "upload_location_type": type(avatar_1.upload_location),
        },
    )


def main():
    create_db_and_tables()
    create_avatars()
    read_avatars()


if __name__ == "__main__":
    main()
