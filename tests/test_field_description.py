from pytest import LogCaptureFixture
from sqlmodel import Field, SQLModel, create_engine


def test_sa_column_description(clear_sqlmodel: None, caplog: LogCaptureFixture) -> None:
    class Team(SQLModel, table=True):
        id: int = Field(primary_key=True, description="an id")
        name: str = Field(description="a name")
        age: int = Field()

    assert Team.model_fields["id"].description == "an id"
    assert Team.model_fields["name"].description == "a name"
    assert Team.model_fields["age"].description is None

    engine = create_engine("sqlite://", echo=True)  # TODO: this should go to Postgres
    SQLModel.metadata.create_all(engine)
    msgs = []
    for msg in caplog.messages:
        if "COMMENT ON COLUMN" in msg:
            msgs.append(msg)
    assert len(msgs) == 2
    assert "COMMENT ON COLUMN team.id IS 'an id'" in msgs[0]
    assert "COMMENT ON COLUMN team.name IS 'a name'" in msgs[1]
