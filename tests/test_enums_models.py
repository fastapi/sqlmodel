import enum
import uuid

from sqlmodel import Field, SQLModel


class MyEnum1(str, enum.Enum):
    A = "A"
    B = "B"


class MyEnum2(str, enum.Enum):
    C = "C"
    D = "D"


class BaseModel(SQLModel):
    id: uuid.UUID = Field(primary_key=True)
    enum_field: MyEnum2


class FlatModel(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True)
    enum_field: MyEnum1


class InheritModel(BaseModel, table=True):
    pass
