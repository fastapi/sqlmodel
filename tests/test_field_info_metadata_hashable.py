from typing import Annotated

from sqlmodel import Field
from sqlmodel.main import FieldInfoMetadata


def test_field_info_metadata_is_hashable():
    """FieldInfoMetadata must be hashable so that Annotated types containing it
    can be used in sets (e.g. FastAPI's OpenAPI schema generation)."""
    meta = FieldInfoMetadata(primary_key=True)
    hash(meta)


def test_annotated_with_field_info_metadata_in_set():
    """Annotated types carrying FieldInfoMetadata must work inside a set,
    which is required by FastAPI's get_definitions()."""
    t = Annotated[int, FieldInfoMetadata(unique=True)]
    s = {t}
    assert t in s


def test_annotated_field_type_in_set():
    """Realistic scenario: custom Annotated field aliases used in a set."""
    PositiveInt = Annotated[int, Field(ge=0)]
    ShortStr = Annotated[str, Field(max_length=32)]

    s = {PositiveInt, ShortStr}
    assert PositiveInt in s
    assert ShortStr in s
