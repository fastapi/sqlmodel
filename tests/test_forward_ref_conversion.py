"""
Test script to verify that forward reference resolution works in Pydantic to SQLModel conversion.
"""

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine
from pydantic import BaseModel


# Pydantic models (not table models)
class TeamPydantic(BaseModel):
    name: str
    headquarters: str


class HeroPydantic(BaseModel):
    name: str
    secret_name: str
    age: Optional[int] = None


def test_forward_reference_conversion(clear_sqlmodel):
    """Test that forward references work in Pydantic to SQLModel conversion."""

    # SQLModel table models with forward references - defined inside test
    class Team(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(index=True)
        headquarters: str

        heroes: List["Hero"] = Relationship(back_populates="team")

    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(index=True)
        secret_name: str
        age: Optional[int] = Field(default=None, index=True)

        team_id: Optional[int] = Field(default=None, foreign_key="team.id")
        team: Optional["Team"] = Relationship(back_populates="heroes")

    # Create engine and tables
    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Create Pydantic models first
        team_pydantic = TeamPydantic(name="Avengers", headquarters="Stark Tower")
        hero_pydantic = HeroPydantic(name="Iron Man", secret_name="Tony Stark", age=45)

        # Create SQLModel table instances
        team = Team(name=team_pydantic.name, headquarters=team_pydantic.headquarters)
        session.add(team)
        session.commit()
        session.refresh(team)

        hero = Hero(
            name=hero_pydantic.name,
            secret_name=hero_pydantic.secret_name,
            age=hero_pydantic.age,
            team_id=team.id,
        )
        session.add(hero)
        session.commit()
        session.refresh(hero)

        print(f"Created team: {team}")
        print(f"Created hero: {hero}")

        # Now test the conversion scenario that was failing
        # This simulates assigning a Pydantic model to a relationship that uses forward references
        try:
            # This should trigger the conversion logic
            hero.team = team_pydantic  # This should convert TeamPydantic to Team
            session.add(hero)
            session.commit()
            print("✅ Forward reference conversion succeeded!")
        except Exception as e:
            print(f"❌ Forward reference conversion failed: {e}")
            import traceback

            traceback.print_exc()
            assert False, f"Forward reference conversion failed: {e}"


if __name__ == "__main__":
    success = test_forward_reference_conversion()
    exit(0 if success else 1)
