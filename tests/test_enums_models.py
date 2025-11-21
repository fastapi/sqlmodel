import enum
import uuid

from sqlmodel import Field, IntEnum, SQLModel


class MyEnum1(str, enum.Enum):
    A = "A"
    B = "B"


class MyEnum2(str, enum.Enum):
    C = "C"
    D = "D"


class MyEnum3(enum.IntEnum):
    E = 1
    F = 2


class BaseModel(SQLModel):
    id: uuid.UUID = Field(primary_key=True)
    enum_field: MyEnum2
    int_enum_field: MyEnum3 = Field(sa_type=IntEnum(MyEnum3))


class FlatModel(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True)
    enum_field: MyEnum1
    int_enum_field: MyEnum3 = Field(sa_type=IntEnum(MyEnum3))


class InheritModel(BaseModel, table=True):
    pass
