from typing import List, Optional

import pytest
from google.protobuf import descriptor_pb2, descriptor_pool
from sqlmodel import Field, SQLModel


def _build_descriptor(*, pkg: str, filename: str, msg_name: str, fields: List[tuple]):
    """Helper to build and register a Descriptor in the default pool.

    fields: list of tuples (name, number, type_enum, label_enum)
    returns: Descriptor
    """
    pool = descriptor_pool.Default()
    file_proto = descriptor_pb2.FileDescriptorProto()
    file_proto.name = filename
    file_proto.package = pkg
    msg = file_proto.message_type.add()
    msg.name = msg_name
    for name, num, typ, lab in fields:
        f = msg.field.add()
        f.name = name
        f.number = num
        f.type = typ
        f.label = lab
    try:
        pool.FindFileByName(filename)
    except KeyError:
        pool.Add(file_proto)
    return pool.FindMessageTypeByName(f"{pkg}.{msg_name}" if pkg else msg_name)


def test_descriptor_missing_fields_raises(clear_sqlmodel) -> None:
    # Provided DESCRIPTOR does not include all model fields -> ValueError
    desc = _build_descriptor(
        pkg="tests.descriptors",
        filename="missing_fields_a.proto",
        msg_name="Hero",
        fields=[
            ("id", 1, descriptor_pb2.FieldDescriptorProto.TYPE_INT64, descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL),
            # missing "name"
        ],
    )

    with pytest.raises(ValueError, match="DESCRIPTOR missing fields: \['name'\]"):
        class Hero(SQLModel):  # noqa: F811
            DESCRIPTOR = desc
            id: int
            name: str


def test_provided_descriptor_is_used(clear_sqlmodel) -> None:
    desc = _build_descriptor(
        pkg="tests.descriptors",
        filename="provided_ok.proto",
        msg_name="Thing",
        fields=[
            ("a", 1, descriptor_pb2.FieldDescriptorProto.TYPE_INT64, descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL),
            ("b", 2, descriptor_pb2.FieldDescriptorProto.TYPE_STRING, descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL),
        ],
    )

    class Thing(SQLModel):
        DESCRIPTOR = desc
        a: int
        b: str

    assert Thing.DESCRIPTOR is desc
    assert set(Thing.DESCRIPTOR.fields_by_name.keys()) == {"a", "b"}


def test_synthesized_descriptor_infers_types_and_labels(clear_sqlmodel) -> None:
    class Model(SQLModel):
        id: int
        name: str
        scores: List[int] = Field(default_factory=list)
        data: bytes
        flag: bool
        value: float
        note: Optional[str] = None

    d = Model.DESCRIPTOR
    # Should synthesize a descriptor
    assert d is not None

    fb = d.fields_by_name
    assert fb["id"].type == descriptor_pb2.FieldDescriptorProto.TYPE_INT64
    assert fb["name"].type == descriptor_pb2.FieldDescriptorProto.TYPE_STRING
    assert fb["data"].type == descriptor_pb2.FieldDescriptorProto.TYPE_BYTES
    assert fb["flag"].type == descriptor_pb2.FieldDescriptorProto.TYPE_BOOL
    assert fb["value"].type == descriptor_pb2.FieldDescriptorProto.TYPE_DOUBLE

    # Repeated list should be labeled as REPEATED
    assert fb["scores"].label == descriptor_pb2.FieldDescriptorProto.LABEL_REPEATED
    # Optional scalar remains optional label
    assert fb["note"].label == descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL


def test_field_level_grpc_descriptor_overrides_and_duplicate_numbers_error(clear_sqlmodel) -> None:
    # Build a source descriptor to take number/type/label from
    src = _build_descriptor(
        pkg="tests.descriptors",
        filename="field_override_src.proto",
        msg_name="Src",
        fields=[
            ("x", 9, descriptor_pb2.FieldDescriptorProto.TYPE_INT64, descriptor_pb2.FieldDescriptorProto.LABEL_REPEATED),
            ("y", 10, descriptor_pb2.FieldDescriptorProto.TYPE_STRING, descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL),
        ],
    )
    x_fd = src.fields_by_name["x"]
    y_fd = src.fields_by_name["y"]

    class OK(SQLModel):
        f1: int = Field(grpc_descriptor=x_fd)
        f2: str = Field(grpc_descriptor=y_fd)

    d = OK.DESCRIPTOR
    assert d is not None
    fb = d.fields_by_name
    # Should reuse numbers and labels/types from provided descriptors
    assert fb["f1"].number == 9
    assert fb["f1"].type == descriptor_pb2.FieldDescriptorProto.TYPE_INT64
    assert fb["f1"].label == descriptor_pb2.FieldDescriptorProto.LABEL_REPEATED
    assert fb["f2"].number == 10
    assert fb["f2"].type == descriptor_pb2.FieldDescriptorProto.TYPE_STRING

    # Duplicate numbers should raise
    with pytest.raises(ValueError, match="Duplicate/invalid field number 9"):
        class Bad(SQLModel):  # noqa: F811
            a: int = Field(grpc_descriptor=x_fd)
            b: int = Field(grpc_descriptor=x_fd)


