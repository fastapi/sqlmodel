from sqlmodel import Field, Session, SQLModel, create_engine, text


def test_select_using_text_statement(clear_sqlmodel):
    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        secret_name: str
        age: int | None = None

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)

    with Session(engine) as session:
        res = session.exec(text("SELECT * FROM hero")).all()
        assert len(res) == 1
        assert res[0] == (1, "Deadpond", "Dive Wilson", None)


def test_insert_using_text_statement(clear_sqlmodel):
    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        secret_name: str
        age: int | None = None

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        res = session.exec(
            text(
                "INSERT INTO hero (name, secret_name) VALUES ('Deadpond', 'Dive Wilson')"
            )
        )
        session.commit()

        assert res.rowcount == 1
