from typing import List, Optional

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


def test_relation_resolution_if_include_relations_not_set(clear_sqlmodel):
    class Team(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        heroes: List["Hero"] = Relationship(back_populates="team")  # noqa: F821

        class Config:
            orm_mode = True

    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        team_id: Optional[int] = Field(default=None, foreign_key="team.id")
        team: Optional[Team] = Relationship(back_populates="heroes")

    hero_1 = Hero(name="Deadpond")
    hero_2 = Hero(name="PhD Strange")
    team = Team(name="Marble", heroes=[hero_1, hero_2])

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(team)
        session.commit()
        session.refresh(team)
    keys = team._calculate_keys(include=None, exclude=None, exclude_unset=False)

    # expected not to include the relationship "heroes" since this
    # fields since the relationship field was not enabled in
    # Config.include_relations
    assert keys == {"id", "name"}


def test_relation_resolution_if_include_relations_is_set(clear_sqlmodel):
    class Team(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        heroes: List["Hero"] = Relationship(back_populates="team")  # noqa: F821

        class Config:
            orm_mode = True
            include_relations = {"heroes"}

    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        team_id: Optional[int] = Field(default=None, foreign_key="team.id")
        team: Optional[Team] = Relationship(back_populates="heroes")

    hero_1 = Hero(name="Deadpond")
    hero_2 = Hero(name="PhD Strange")
    team = Team(name="Marble", heroes=[hero_1, hero_2])

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(team)
        session.commit()
        session.refresh(team)
    keys = team._calculate_keys(include=None, exclude=None, exclude_unset=False)

    # expected to include the relationship "heroes" since this
    # fields was enabled in Config.include_relations
    assert keys == {"id", "name", "heroes"}


def test_relation_resolution_if_include_relations_is_set_for_nested(clear_sqlmodel):
    class Team(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        heroes: List["Hero"] = Relationship(back_populates="team")  # noqa: F821

        class Config:
            orm_mode = True
            include_relations = {"heroes"}

    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        powers: List["Power"] = Relationship(back_populates="hero")  # noqa: F821
        team_id: Optional[int] = Field(default=None, foreign_key="team.id")
        team: Optional[Team] = Relationship(back_populates="heroes")

        class Config:
            orm_mode = True
            include_relations = {"powers"}

    class Power(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        description: str
        hero_id: Optional[int] = Field(default=None, foreign_key="hero.id")
        hero: Optional[Hero] = Relationship(back_populates="powers")

    power_hero_1 = Power(description="Healing Power")
    power_hero_2 = Power(description="Levitating Cloak")
    hero_1 = Hero(name="Deadpond", powers=[power_hero_1])
    hero_2 = Hero(name="PhD Strange", powers=[power_hero_2])
    team = Team(name="Marble", heroes=[hero_1, hero_2])

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(team)
        session.commit()
        session.refresh(team)
        session.refresh(hero_1)
    team_keys = team._calculate_keys(include=None, exclude=None, exclude_unset=False)
    hero_1_keys = hero_1._calculate_keys(
        include=None, exclude=None, exclude_unset=False
    )

    assert team_keys == {"id", "name", "heroes"}
    assert hero_1_keys == {"id", "name", "powers", "team_id"}


def test_relation_resolution_if_lazy_selectin_not_set_with_fastapi(clear_sqlmodel):
    class Team(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        heroes: List["Hero"] = Relationship(back_populates="team")  # noqa: F821

        class Config:
            orm_mode = True
            include_relations = {"heroes"}

    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        powers: List["Power"] = Relationship(back_populates="hero")  # noqa: F821
        team_id: Optional[int] = Field(default=None, foreign_key="team.id")
        team: Optional[Team] = Relationship(back_populates="heroes")

        class Config:
            orm_mode = True
            include_relations = {"powers"}

    class Power(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        description: str
        hero_id: Optional[int] = Field(default=None, foreign_key="hero.id")
        hero: Optional[Hero] = Relationship(back_populates="powers")

    power_hero_1 = Power(description="Healing Power")
    power_hero_2 = Power(description="Levitating Cloak")
    hero_1 = Hero(name="Deadpond", powers=[power_hero_1])
    hero_2 = Hero(name="PhD Strange", powers=[power_hero_2])
    team = Team(name="Marble", heroes=[hero_1, hero_2])

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(team)
        session.commit()
        session.refresh(team)

    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    app = FastAPI()

    @app.get("/")
    async def read_main(response_model=List[Team]):
        with Session(engine) as session:
            teams = session.execute(select(Team)).all()
        return teams

    client = TestClient(app)
    teams = client.get("/")
    expected_json = [{"Team": {"name": "Marble", "id": 1}}]

    # if sa_relationship_kwargs={"lazy": "selectin"}) not set in relation
    # there is no effect on the relations even though the Config was set
    # to load the relation fields.
    assert teams.json() == expected_json


def test_relation_resolution_if_lazy_selectin_is_set_with_fastapi(clear_sqlmodel):
    class Team(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        heroes: List["Hero"] = Relationship(  # noqa: F821
            back_populates="team", sa_relationship_kwargs={"lazy": "selectin"}
        )

        class Config:
            orm_mode = True
            include_relations = {"heroes"}

    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        powers: List["Power"] = Relationship(  # noqa: F821
            back_populates="hero", sa_relationship_kwargs={"lazy": "selectin"}
        )
        team_id: Optional[int] = Field(default=None, foreign_key="team.id")
        team: Optional[Team] = Relationship(back_populates="heroes")

        class Config:
            orm_mode = True
            include_relations = {"powers"}

    class Power(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        description: str
        hero_id: Optional[int] = Field(default=None, foreign_key="hero.id")
        hero: Optional[Hero] = Relationship(back_populates="powers")

    power_hero_1 = Power(description="Healing Power")
    power_hero_2 = Power(description="Levitating Cloak")
    hero_1 = Hero(name="Deadpond", powers=[power_hero_1])
    hero_2 = Hero(name="PhD Strange", powers=[power_hero_2])
    team = Team(name="Marble", heroes=[hero_1, hero_2])

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(team)
        session.commit()
        session.refresh(team)

    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    app = FastAPI()

    @app.get("/")
    async def read_main(response_model=List[Team]):
        with Session(engine) as session:
            teams = session.execute(select(Team)).all()
        return teams

    client = TestClient(app)
    teams = client.get("/")
    expected_json = [
        {
            "Team": {
                "name": "Marble",
                "id": 1,
                "heroes": [
                    {
                        "id": 1,
                        "team_id": 1,
                        "name": "Deadpond",
                        "powers": [
                            {"id": 1, "hero_id": 1, "description": "Healing Power"}
                        ],
                    },
                    {
                        "id": 2,
                        "team_id": 1,
                        "name": "PhD Strange",
                        "powers": [
                            {"id": 2, "hero_id": 2, "description": "Levitating Cloak"}
                        ],
                    },
                ],
            }
        }
    ]

    # if sa_relationship_kwargs={"lazy": "selectin"}) is set
    # the relations in the Config are considered and the relation fields are
    # included in the response.
    assert teams.json() == expected_json
