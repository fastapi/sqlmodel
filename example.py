from sqlmodel import Field, SQLModel
from sqlmodel.repository.crud_repository import CrudRepository, native_query


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


class HeroRepository(CrudRepository[int, Hero]):
    @native_query("SELECT * FROM hero WHERE name = '{name}'", Hero)
    def get_hero_by_name(self, name: str) -> Hero:
        ...


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = CrudRepository.create_all_tables(sqlite_url)

hero_repo = HeroRepository(engine)

deadpond = Hero(name="Deadpond", secret_name="Dive Wilson")
hero_repo.save(deadpond)
print(hero_repo.find_all())
print(hero_repo.get_hero_by_name(name="Deadpond"))
