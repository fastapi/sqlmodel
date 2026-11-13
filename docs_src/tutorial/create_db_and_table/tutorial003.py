from sqlmodel import Field, SQLModel, create_engine  # (1)!


class Hero(SQLModel, table=True):  # (2)!
    id: int | None = Field(default=None, primary_key=True)  # (3)!
    name: str  # (4)!
    secret_name: str  # (5)!
    age: int | None = None  # (6)!


sqlite_file_name = "database.db"  # (7)!
sqlite_url = f"sqlite:///{sqlite_file_name}"  # (8)!

engine = create_engine(sqlite_url, echo=True)  # (9)!


def create_db_and_tables():  # (10)!
    SQLModel.metadata.create_all(engine)  # (11)!


if __name__ == "__main__":  # (12)!
    create_db_and_tables()  # (13)!
