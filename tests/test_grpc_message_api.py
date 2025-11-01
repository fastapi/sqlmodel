from typing import List, Optional

import pytest
from google.protobuf import struct_pb2
from sqlmodel import Field, SQLModel


class Thing(SQLModel):
    a: int = 0
    b: Optional[str] = None
    c: Optional[int] = None
    tags: List[str] = Field(default_factory=list)


def test_serialize_and_parse_roundtrip(clear_sqlmodel) -> None:
    t = Thing(a=123, b="x", c=None, tags=["alpha", "beta"])
    data = t.SerializeToString()

    t2 = Thing()
    t2.ParseFromString(data)

    assert t2.a == 123
    assert t2.b == "x"
    assert t2.c is None
    assert t2.tags == ["alpha", "beta"]


def test_merge_from_string_uses_struct(clear_sqlmodel) -> None:
    # Build a Struct that encodes Thing-like data
    s = struct_pb2.Struct()
    s.update({"a": 7, "b": "bee", "tags": ["t1", "t2"]})
    blob = s.SerializeToString()

    t = Thing(a=0)
    read = t.MergeFromString(blob)

    assert isinstance(read, int)
    assert t.a == 7
    assert t.b == "bee"
    assert t.tags == ["t1", "t2"]


def test_merge_from_message_and_copy_from(clear_sqlmodel) -> None:
    t1 = Thing(a=1, b="one", tags=["x"]) 
    t2 = Thing(a=2)

    # Merge from SQLModel instance
    t2.MergeFrom(t1)
    assert t2.a == 1
    assert t2.b == "one"
    assert t2.tags == ["x"]

    # CopyFrom should clear then merge
    s = Thing(a=9, b=None, tags=["z"])
    t2.CopyFrom(s)
    assert t2.a == 9
    assert t2.b is None
    assert t2.tags == ["z"]


def test_merge_from_struct_message(clear_sqlmodel) -> None:
    s = struct_pb2.Struct()
    s.update({"a": 11, "b": "bee"})

    t = Thing(a=0, b=None)
    t.MergeFrom(s)

    assert t.a == 11
    assert t.b == "bee"


def test_hasfield_presence_and_errors(clear_sqlmodel) -> None:
    t = Thing()
    # Optional scalar supports presence
    assert t.HasField("b") is False
    t.b = "hi"
    assert t.HasField("b") is True

    # Non-optional scalar raises for HasField in proto3 style
    with pytest.raises(ValueError):
        t.HasField("a")

    # Repeated fields raise
    with pytest.raises(ValueError):
        t.HasField("tags")


def test_clear_and_clearfield_defaults(clear_sqlmodel) -> None:
    t = Thing(a=3, b="txt", c=5, tags=["a"]) 
    t.ClearField("b")
    assert t.b is None  # optional cleared to None

    t.Clear()
    # Defaults after Clear
    assert t.a == 0
    assert t.b is None
    assert t.c is None
    assert t.tags == []


def test_misc_message_api(clear_sqlmodel) -> None:
    t = Thing(a=4)
    # SerializePartialToString behaves like SerializeToString
    p = t.SerializePartialToString()
    q = t.SerializeToString()
    assert isinstance(p, bytes) and isinstance(q, bytes)
    assert len(p) == len(q)

    # ByteSize should equal serialized length
    assert t.ByteSize() == len(q)

    # ListFields is empty in dynamic implementation
    assert t.ListFields() == []

    # DiscardUnknownFields returns None (no-op)
    assert t.DiscardUnknownFields() is None

    # UnknownFields returns an empty Struct
    uf = t.UnknownFields()
    assert isinstance(uf, struct_pb2.Struct)
    assert len(uf.fields) == 0

    # SetInParent and WhichOneof no-ops/None
    assert t.SetInParent() is None
    assert t.WhichOneof("anything") is None


