from typing import List, Optional

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine


class Villain(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    power_level: int

    boss_id: Optional[int] = Field(
        foreign_key="villain.id", default=None, nullable=True
    )
    boss: Optional["Villain"] = Relationship(
        back_populates="minions", sa_relationship_kwargs=dict(remote_side="Villain.id")
    )
    minions: List["Villain"] = Relationship(back_populates="boss")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def create_villains() -> None:
    with Session(engine) as session:
        thinnus = Villain(name="Thinnus", power_level=9001)
        ebonite_mew = Villain(name="Ebonite Mew", power_level=400, boss=thinnus)
        dark_shorty = Villain(name="Dark Shorty", power_level=200, boss=thinnus)
        ultra_bot = Villain(name="Ultra Bot", power_level=2 ** 9)
        session.add(ebonite_mew)
        session.add(dark_shorty)
        session.add(ultra_bot)
        session.commit()

        session.refresh(thinnus)
        session.refresh(ebonite_mew)
        session.refresh(dark_shorty)
        session.refresh(ultra_bot)

        print("Created villain:", thinnus)
        print("Created villain:", ebonite_mew)
        print("Created villain:", dark_shorty)
        print("Created villain:", ultra_bot)

        ultra_bot.boss = thinnus
        session.add(ultra_bot)
        session.commit()
        session.refresh(ultra_bot)
        print("Updated villain:", ultra_bot)

        clone_bot_1 = Villain(name="Clone Bot 1", power_level=2 ** 6)
        clone_bot_2 = Villain(name="Clone Bot 2", power_level=2 ** 6)
        clone_bot_3 = Villain(name="Clone Bot 3", power_level=2 ** 6)
        ultra_bot.minions.extend([clone_bot_1, clone_bot_2, clone_bot_3])
        session.add(ultra_bot)
        session.commit()
        session.refresh(clone_bot_1)
        session.refresh(clone_bot_2)
        session.refresh(clone_bot_3)
        print("Added minion:", clone_bot_1)
        print("Added minion:", clone_bot_2)
        print("Added minion:", clone_bot_3)


def main() -> None:
    create_db_and_tables()
    create_villains()


if __name__ == "__main__":
    main()
