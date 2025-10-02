from typing import Optional

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from sqlmodel import Field, SQLModel, create_engine

# For a real application, use a securely managed key
ENCRYPTION_KEY = "a-super-secret-key"


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    # Because the secret name should stay a secret
    secret_name: str = Field(
        sa_column=Column(
            EncryptedType(
                sqlalchemy.Unicode,
                ENCRYPTION_KEY,
                AesEngine,
                "pkcs5",
            )
        )
    )
    age: Optional[int] = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
