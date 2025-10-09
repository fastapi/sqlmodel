import os
from typing import Optional

from sqlalchemy import Column
from sqlalchemy_utils.types.encrypted.encrypted_type import (
    AesEngine,
    StringEncryptedType,
)
from sqlmodel import Field, Session, SQLModel, create_engine, select

# In a real application, load this from a secure source (e.g., environment variable or secrets manager)
ENCRYPTION_KEY = os.getenv("SQLMODEL_ENCRYPTION_KEY", "a-super-secret-key")


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    # Because the secret name should stay a secret
    secret_name: str = Field(
        sa_column=Column(
            StringEncryptedType(
                key=ENCRYPTION_KEY,
                engine=AesEngine,
                padding="pkcs5",
            )
        )
    )
    age: Optional[int] = None


sqlite_file_name = "database_encrypted.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def create_heroes() -> None:
    hero_1 = Hero(name="Ted Lasso", secret_name="Coach")
    hero_2 = Hero(name="Roy Kent", secret_name="Roy")
    hero_3 = Hero(name="Keeley Jones", secret_name="Keeley", age=29)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.commit()


def select_heroes() -> None:
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Ted Lasso")
        hero_1 = session.exec(statement).one()
        print("Hero 1:", hero_1)
        print("Hero 1 secret_name (decrypted in Python):", hero_1.secret_name)

        statement = select(Hero).where(Hero.name == "Roy Kent")
        hero_2 = session.exec(statement).one()
        print("Hero 2:", hero_2)
        print("Hero 2 secret_name (decrypted in Python):", hero_2.secret_name)


def main() -> None:
    create_db_and_tables()
    create_heroes()
    select_heroes()


if __name__ == "__main__":
    main()
