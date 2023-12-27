import ipaddress
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlmodel import Field, SQLModel, create_engine


class Avatar(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    source_ip_address: ipaddress.IPv4Address
    upload_location: Path
    uploaded_at: datetime = Field(default=datetime.now(tz=UTC))
    author_email: EmailStr


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)
