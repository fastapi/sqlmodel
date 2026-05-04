from typing import Any, ClassVar, get_origin

from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import (
    _collect_inherited_namespace,
    _is_polymorphic_subclass,
    _relationship_keys,
    _wrap_inherited_relationships_as_classvar,
)


class _PolyBase(SQLModel, table=True):
    __tablename__ = "helpers_poly_base"
    id: int | None = Field(default=None, primary_key=True)
    kind: str = Field(default="base")
    __mapper_args__ = {"polymorphic_on": "kind", "polymorphic_identity": "base"}


def test_is_polymorphic_subclass_true_with_table_base():
    assert _is_polymorphic_subclass((_PolyBase,)) is True


def test_is_polymorphic_subclass_false_with_plain_base():
    assert _is_polymorphic_subclass((object,)) is False


def test_collect_inherited_namespace_merges_base_fields():
    merged = _collect_inherited_namespace(
        (_PolyBase,), {"__annotations__": {"extra": str}}
    )
    assert "extra" in merged["__annotations__"]
    assert "id" in merged or "id" in merged["__annotations__"]


def test_relationship_keys_table_model_uses_mapper():
    # table model: keys come from the SQLAlchemy mapper (includes inherited relationships)
    class RkOwner(SQLModel, table=True):
        __tablename__ = "rk_owner"
        id: int | None = Field(default=None, primary_key=True)
        items: list["RkItem"] = Relationship(back_populates="owner")

    class RkItem(SQLModel, table=True):
        __tablename__ = "rk_item"
        id: int | None = Field(default=None, primary_key=True)
        owner_id: int | None = Field(default=None, foreign_key="rk_owner.id")
        owner: RkOwner | None = Relationship(back_populates="items")

    assert "owner" in list(_relationship_keys(RkItem()))


def test_relationship_keys_non_table_model_uses_sqlmodel_relationships():
    # non-table model: mapper is None, falls back to __sqlmodel_relationships__
    class Plain(SQLModel):
        name: str = ""

    plain = Plain()
    assert list(_relationship_keys(plain)) == list(plain.__sqlmodel_relationships__)


def test_wrap_inherited_relationships_marks_classvar():
    class FakeBase:
        __sqlmodel_relationships__ = {"owner": None}

    dict_used: dict[str, Any] = {"__annotations__": {}}
    _wrap_inherited_relationships_as_classvar(
        FakeBase, {"owner": Any | None}, dict_used
    )
    assert get_origin(dict_used["__annotations__"]["owner"]) is ClassVar

    dict_used: dict[str, Any] = {"__annotations__": {}}
    _wrap_inherited_relationships_as_classvar(object, {}, dict_used)
    assert dict_used["__annotations__"] == {}
