from pydantic import ConfigDict as PydanticConfigDict
from sqlmodel import ConfigDict, Field, SQLModel, SQLModelConfig


def test_sqlmodel_config_export():
    import sqlmodel
    import sqlmodel.main

    assert hasattr(sqlmodel, "SQLModelConfig")
    assert hasattr(sqlmodel.main, "SQLModelConfig")
    assert hasattr(sqlmodel, "ConfigDict")
    assert sqlmodel.SQLModelConfig is SQLModelConfig
    assert sqlmodel.ConfigDict is ConfigDict


def test_model_with_sqlmodel_config():
    class Item(SQLModel):
        id: int
        name: str
        model_config = SQLModelConfig(from_attributes=True)

    assert Item.model_config.get("from_attributes") is True


def test_model_with_sqlmodel_reexported_config_dict():
    class Item(SQLModel):
        id: int
        name: str
        model_config = ConfigDict(from_attributes=True)

    assert Item.model_config.get("from_attributes") is True


def test_model_with_pydantic_config_dict():
    class Item(SQLModel):
        id: int
        name: str
        model_config = PydanticConfigDict(from_attributes=True)

    assert Item.model_config.get("from_attributes") is True


def test_model_with_plain_dict_config():
    class Item(SQLModel):
        id: int
        name: str
        model_config = {"from_attributes": True}

    assert Item.model_config.get("from_attributes") is True


def test_table_model_with_sqlmodel_config():
    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        model_config = SQLModelConfig(extra="ignore")

    assert Hero.model_config.get("extra") == "ignore"
    assert Hero.model_config.get("table") is True
