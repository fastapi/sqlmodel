from datetime import datetime

try:
    from datetime import UTC
except ImportError:
    UTC = None
from typing import TypedDict

from sqlalchemy import PickleType
from sqlmodel import Field, Session, SQLModel, create_engine, select


class ModelOutput(TypedDict):
    model_checkpoint: datetime
    score: float


class ModelResult(SQLModel, table=True):
    id: int = Field(default=..., primary_key=True)
    output: ModelOutput = Field(sa_type=PickleType())


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_model_results():
    checkpoint = datetime.now(tz=UTC)

    result_1 = ModelResult(
        output={
            "model_checkpoint": checkpoint,
            "score": 0.9123,
        }
    )
    result_2 = ModelResult(
        output={
            "model_checkpoint": checkpoint,
            "score": 0.1294,
        }
    )
    result_3 = ModelResult(
        output={
            "model_checkpoint": checkpoint,
            "score": 0.4821,
        }
    )

    with Session(engine) as session:
        session.add(result_1)
        session.add(result_2)
        session.add(result_3)

        session.commit()


def get_average_score():
    with Session(engine) as session:
        statement = select(ModelResult)
        result = session.exec(statement)
        model_results = result.all()

    scores = [model_result.output["score"] for model_result in model_results]

    print("Average score:", sum(scores) / len(scores))


def main():
    create_db_and_tables()
    create_model_results()
    get_average_score()


if __name__ == "__main__":
    main()
