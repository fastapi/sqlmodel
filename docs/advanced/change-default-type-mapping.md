# Change default Pydantic to SQLAlchemy mappings

In most cases, you do not need to know how SQLAlchemy transforms the Python types to the type suitable for storing data
in the database, and you can use the default mapping.

But in some cases you may need to have possibility to change default mapping provided by SQLmodel. For example to use
mssql dialect with some UTF-8 data you should use NVARCHAR field (sa.Unicode)

Now changing default mapping is simple to use - see example bellow:

```python
import sqlmodel.main
import sqlalchemy as sa
from sqlmodel import Field, SQLModel
from typing import Optional

sqlmodel.main.sa_types_map[str] = lambda type_, meta, annotation: sa.Unicode(
    length=getattr(meta, "max_length", None)
)


class Hero(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    history: Optional[str]


assert isinstance(Hero.name.type, sa.Unicode)
```

# Some details

Let's get little deeper to process of mapping. At the `sqlmodel.main` module defined the `sa_types_map` dictionary,
which uses the Python types as keys, and the sqlalchemy type or callable that takes the input of 3 parameters and
returns the sqlalchemy type as values.

Callable format present bellow:

```python
def map_python_type_to_sa_type(type_: "PythonType", meta: "PydanticMeta", annotation: "FieldAnnotatedType"):
    return sqlalchemyType(length=getattr(meta, "max_length", None))
```

* `type_` - used to pass python type, provided by pydantic annotation, cleared from Union/Optional and other wrappers.
  Can be passed to sa.Enum type to properly store enumerated data.
* `meta` - pydantic metadata used to store field params e.g. length of str field or precision of decimal field
* `annotation` - original annotation given by pydantic. Used to provide `type` parameter for PydanticJSONType

## Current mapping

| Python type           | SqlAlchemy type                                                                                                                    | 
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Enum                  | `lambda type_, meta, annotation: sa_Enum(type_)`                                                                                   |
| str                   | `lambda type_, meta, annotation: AutoString(length=getattr(meta, "max_length", None))`                                             | 
| float                 | Float                                                                                                                              |
| bool                  | Boolean                                                                                                                            |
| int                   | Integer                                                                                                                            |
| datetime              | DateTime                                                                                                                           |
| date                  | Date                                                                                                                               |
| timedelta             | Interval                                                                                                                           |
| time                  | Time                                                                                                                               |
| bytes                 | LargeBinary                                                                                                                        |
| Decimal               | `lambda type_, meta, annotation: Numeric(precision=getattr(meta, "max_digits", None),scale=getattr(meta, "decimal_places", None))` |
| ipaddress.IPv4Address | AutoString                                                                                                                         |
| ipaddress.IPv4Network | AutoString                                                                                                                         |
| ipaddress.IPv6Address | AutoString                                                                                                                         |
| ipaddress.IPv6Network | AutoString                                                                                                                         |
| Path                  | AutoString                                                                                                                         |
| uuid.UUID             | Uuid                                                                                                                               |
| BaseModel             | `lambda type_, meta, annotation: PydanticJSONType(type=annotation)`                                                                |