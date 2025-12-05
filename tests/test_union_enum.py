"""
Tests for Union Enum type support in SQLModel.

This tests the ability to use Union of Enum types as field types, e.g.:
    BillingFeatureEnum = BillingBooleanFeature | BillingLimitFeature

Or using typing.Union:
    BillingFeatureEnum = Union[BillingBooleanFeature, BillingLimitFeature]
"""

import enum
from typing import Optional, Union

import pytest
from sqlalchemy import create_engine
from sqlmodel import Field, Session, SQLModel, select

from .conftest import needs_pydanticv2


class BillingBooleanFeature(str, enum.Enum):
    """Features that are either enabled or disabled."""

    chat_integration = "chat_integration"
    leads = "leads"
    schedule = "schedule"


class BillingLimitFeature(str, enum.Enum):
    """Features with numeric limits."""

    max_clients = "max_clients"
    max_trainers = "max_trainers"


# Union type using typing.Union (works in Python 3.9+)
BillingFeatureEnumUnion = Union[BillingBooleanFeature, BillingLimitFeature]


class TestIsEnumTypeHelper:
    """Test the _is_enum_type helper function."""

    def test_is_enum_type_with_enum(self):
        from sqlmodel._compat import _is_enum_type

        assert _is_enum_type(BillingBooleanFeature) is True
        assert _is_enum_type(BillingLimitFeature) is True

    def test_is_enum_type_with_non_enum(self):
        from sqlmodel._compat import _is_enum_type

        assert _is_enum_type(str) is False
        assert _is_enum_type(int) is False
        assert _is_enum_type(None) is False

    def test_is_enum_type_with_enum_base(self):
        from sqlmodel._compat import _is_enum_type

        # enum.Enum itself is a type, but not an Enum subclass in the same way
        assert _is_enum_type(enum.Enum) is True


@needs_pydanticv2
class TestGetSaTypeFromTypeAnnotation:
    """Test get_sa_type_from_type_annotation with Union Enum types."""

    def test_union_enum_returns_tuple_of_enums(self):
        from sqlmodel._compat import get_sa_type_from_type_annotation

        # Union of Enums returns tuple of enum types for SQLAlchemy Enum
        result = get_sa_type_from_type_annotation(BillingFeatureEnumUnion)
        assert isinstance(result, tuple)
        assert BillingBooleanFeature in result
        assert BillingLimitFeature in result

    def test_optional_union_enum_returns_tuple_of_enums(self):
        from sqlmodel._compat import get_sa_type_from_type_annotation

        OptionalUnionEnum = Optional[BillingFeatureEnumUnion]
        result = get_sa_type_from_type_annotation(OptionalUnionEnum)
        assert isinstance(result, tuple)
        assert BillingBooleanFeature in result
        assert BillingLimitFeature in result

    def test_simple_enum_still_works(self):
        from sqlmodel._compat import get_sa_type_from_type_annotation

        result = get_sa_type_from_type_annotation(BillingBooleanFeature)
        assert result is BillingBooleanFeature

    def test_optional_simple_enum_still_works(self):
        from sqlmodel._compat import get_sa_type_from_type_annotation

        OptionalEnum = Optional[BillingBooleanFeature]
        result = get_sa_type_from_type_annotation(OptionalEnum)
        assert result is BillingBooleanFeature

    def test_invalid_union_raises_error(self):
        from sqlmodel._compat import get_sa_type_from_type_annotation

        # Union of Enum and non-Enum should still raise
        InvalidUnion = Union[BillingBooleanFeature, str]
        with pytest.raises(ValueError, match="Cannot have a .* union"):
            get_sa_type_from_type_annotation(InvalidUnion)

    def test_non_enum_union_raises_error(self):
        from sqlmodel._compat import get_sa_type_from_type_annotation

        # Union of non-Enums should still raise
        InvalidUnion = Union[str, int]
        with pytest.raises(ValueError, match="Cannot have a .* union"):
            get_sa_type_from_type_annotation(InvalidUnion)


@needs_pydanticv2
class TestUnionEnumModel:
    """Test SQLModel with Union Enum field types."""

    def test_create_model_with_union_enum(self, clear_sqlmodel):
        """Test that a model with Union Enum field can be created."""

        class FeatureConfig(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            feature: BillingFeatureEnumUnion
            enabled: bool = True

        # Model should be created successfully
        assert "feature" in FeatureConfig.model_fields
        assert FeatureConfig.__tablename__ == "featureconfig"

    def test_create_model_with_optional_union_enum(self, clear_sqlmodel):
        """Test that a model with Optional Union Enum field can be created."""

        class FeatureConfigOptional(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            feature: Optional[BillingFeatureEnumUnion] = None

        assert "feature" in FeatureConfigOptional.model_fields

    def test_insert_and_query_union_enum(self, clear_sqlmodel):
        """Test inserting and querying records with Union Enum values."""

        class FeatureRecord(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            feature: BillingFeatureEnumUnion
            value: str

        engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(engine)

        with Session(engine) as session:
            # Insert a record with BillingBooleanFeature
            record1 = FeatureRecord(
                feature=BillingBooleanFeature.chat_integration, value="enabled"
            )
            session.add(record1)

            # Insert a record with BillingLimitFeature
            record2 = FeatureRecord(
                feature=BillingLimitFeature.max_clients, value="100"
            )
            session.add(record2)
            session.commit()

            # Query and verify
            statement = select(FeatureRecord)
            results = session.exec(statement).all()

            assert len(results) == 2
            assert results[0].feature == BillingBooleanFeature.chat_integration
            assert results[1].feature == BillingLimitFeature.max_clients

            # Verify that returned values are Enum instances, not strings
            assert isinstance(results[0].feature, BillingBooleanFeature)
            assert isinstance(results[1].feature, BillingLimitFeature)
            assert isinstance(results[0].feature, enum.Enum)
            assert isinstance(results[1].feature, enum.Enum)

    def test_insert_and_query_optional_union_enum(self, clear_sqlmodel):
        """Test inserting and querying records with Optional Union Enum values."""

        class FeatureRecordOptional(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            feature: Optional[BillingFeatureEnumUnion] = None

        engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(engine)

        with Session(engine) as session:
            # Insert a record with a value
            record1 = FeatureRecordOptional(feature=BillingBooleanFeature.leads)
            session.add(record1)

            # Insert a record with None
            record2 = FeatureRecordOptional(feature=None)
            session.add(record2)
            session.commit()

            # Query and verify
            statement = select(FeatureRecordOptional)
            results = session.exec(statement).all()

            assert len(results) == 2
            assert results[0].feature == BillingBooleanFeature.leads
            assert results[1].feature is None

    def test_model_instantiation_with_union_enum(self, clear_sqlmodel):
        """Test creating model instances with different enum values from the union."""

        class FeatureItem(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            feature: BillingFeatureEnumUnion

        # Create instance with first enum type
        item1 = FeatureItem(feature=BillingBooleanFeature.schedule)
        assert item1.feature == BillingBooleanFeature.schedule

        # Create instance with second enum type
        item2 = FeatureItem(feature=BillingLimitFeature.max_trainers)
        assert item2.feature == BillingLimitFeature.max_trainers

    def test_model_with_multiple_union_enum_fields(self, clear_sqlmodel):
        """Test model with multiple Union Enum fields."""

        class MultiFeatureRecord(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            primary_feature: BillingFeatureEnumUnion
            secondary_feature: Optional[BillingFeatureEnumUnion] = None

        engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(engine)

        with Session(engine) as session:
            record = MultiFeatureRecord(
                primary_feature=BillingBooleanFeature.chat_integration,
                secondary_feature=BillingLimitFeature.max_clients,
            )
            session.add(record)
            session.commit()

            statement = select(MultiFeatureRecord)
            result = session.exec(statement).first()

            assert result is not None
            assert result.primary_feature == BillingBooleanFeature.chat_integration
            assert result.secondary_feature == BillingLimitFeature.max_clients


@needs_pydanticv2
class TestUnionEnumThreeTypes:
    """Test Union of more than two Enum types."""

    def test_union_of_three_enums(self, clear_sqlmodel):
        """Test that Union of three Enum types works."""
        from sqlmodel._compat import get_sa_type_from_type_annotation

        class ThirdEnum(str, enum.Enum):
            x = "x"
            y = "y"

        ThreeEnumUnion = Union[BillingBooleanFeature, BillingLimitFeature, ThirdEnum]
        result = get_sa_type_from_type_annotation(ThreeEnumUnion)
        assert isinstance(result, tuple)
        assert len(result) == 3
        assert BillingBooleanFeature in result
        assert BillingLimitFeature in result
        assert ThirdEnum in result

    def test_optional_union_of_three_enums(self, clear_sqlmodel):
        """Test that Optional Union of three Enum types works."""
        from sqlmodel._compat import get_sa_type_from_type_annotation

        class ThirdEnum(str, enum.Enum):
            x = "x"
            y = "y"

        OptionalThreeEnumUnion = Optional[
            Union[BillingBooleanFeature, BillingLimitFeature, ThirdEnum]
        ]
        result = get_sa_type_from_type_annotation(OptionalThreeEnumUnion)
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_model_with_three_enum_union(self, clear_sqlmodel):
        """Test creating a model with a Union of three Enum types."""

        class ThirdEnum(str, enum.Enum):
            x = "x"
            y = "y"

        ThreeEnumUnion = Union[BillingBooleanFeature, BillingLimitFeature, ThirdEnum]

        class ThreeEnumModel(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            feature: ThreeEnumUnion

        engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(engine)

        with Session(engine) as session:
            record = ThreeEnumModel(feature=ThirdEnum.x)
            session.add(record)
            session.commit()

            result = session.exec(select(ThreeEnumModel)).first()
            assert result is not None
            assert result.feature == ThirdEnum.x
