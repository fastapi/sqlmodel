from typing import Optional  # (1)

from sqlmodel import Field, SQLModel, create_engine  # (2)


class Hero(SQLModel, table=True):  # (3)
    id: Optional[int] = Field(default=None, primary_key=True)  # (4)
    name: str  # (5)
    secret_name: str  # (6)
    age: Optional[int] = None  # (7)


sqlite_file_name = "database.db"  # (8)
sqlite_url = f"sqlite:///{sqlite_file_name}"  # (9)

engine = create_engine(sqlite_url, echo=True)  # (10)


def create_db_and_tables():  # (11)
    SQLModel.metadata.create_all(engine)  # (12)


if __name__ == "__main__":  # (13)
    create_db_and_tables()  # (14)
