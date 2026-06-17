"""Tests for SQLModelMetaclass.__new__ registry kwarg handling."""
import pytest
from sqlalchemy.orm import registry
from sqlmodel import SQLModel


def test_custom_registry_base_stores_registry_in_model_config() -> None:
    """model_config['registry'] must hold the registry object passed as kwarg."""
    custom_registry = registry()

    class MyBase(SQLModel, registry=custom_registry):
        pass

    stored = MyBase.model_config.get("registry")
    assert stored is custom_registry, (
        f"model_config['registry'] should be the custom registry, got {stored!r}"
    )


def test_custom_registry_base_sets_sa_registry() -> None:
    """_sa_registry must reference the registry object passed as kwarg."""
    custom_registry = registry()

    class MyBase2(SQLModel, registry=custom_registry):
        pass

    sa_registry = getattr(MyBase2, "_sa_registry", None)
    assert sa_registry is custom_registry, (
        f"_sa_registry should be the custom registry, got {sa_registry!r}"
    )
