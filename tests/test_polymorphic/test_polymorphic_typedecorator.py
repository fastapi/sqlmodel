import json
import typing as t
from typing import Optional

from pydantic import BaseModel, TypeAdapter
from sqlmodel import JSON, Column, Field, Session, SQLModel, TypeDecorator, create_engine, select

# See https://github.com/fastapi/sqlmodel/pull/1226#issuecomment-2568867964
def _make_classes():
    def pydantic_column_type(pydantic_type: type) -> type:
        class PydanticJSONType(TypeDecorator):
            impl = JSON()
            cache_ok = False

            def __init__(self, json_encoder: t.Any = json):
                self.json_encoder = json_encoder
                super().__init__()

            def result_processor(self, dialect: t.Any, coltype: t.Any) -> t.Any:
                def process(value: t.Any) -> t.Any:
                    if value is None:
                        return None
                    if isinstance(value, str):
                        value = json.loads(value)
                    return TypeAdapter(pydantic_type).validate_python(value)
                return process

            def compare_values(self, x: t.Any, y: t.Any) -> bool:
                return x == y

        return PydanticJSONType

    class MyModel(BaseModel):
        name: str | None = None

    class ComplexModel(SQLModel, table=True):
        __tablename__ = "complexmodel"
        id: Optional[int] = Field(default=None, primary_key=True)
        my_model: t.Annotated[
            MyModel | None,
            Field(sa_column=Column(pydantic_column_type(MyModel)())),
        ] = None

    class Hero(SQLModel, table=True):
        __tablename__ = "hero"
        id: Optional[int] = Field(default=None, primary_key=True)
        hero_type: str = Field(default="hero")
        __mapper_args__ = {"polymorphic_on": "hero_type", "polymorphic_identity": "hero"}

    class DarkHero(Hero):
        __mapper_args__ = {"polymorphic_identity": "dark"}

    return ComplexModel, Hero, DarkHero


def test_polymorphic_coexists_with_custom_type_decorator():
    """
    Defining a polymorphic subclass alongside a model with a custom
    TypeDecorator whose default holds a non-picklable object (e.g. the json
    module) should work.
    """
    ComplexModel, Hero, DarkHero = _make_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        db.add(Hero())
        db.add(DarkHero())
        db.commit()
        result = db.exec(select(DarkHero)).all()

    assert len(result) == 1
    assert isinstance(result[0], DarkHero)
