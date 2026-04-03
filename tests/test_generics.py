from enum import Enum
from typing import Generic, Literal, TypeVar

import pytest
from sqlalchemy import create_engine
from sqlmodel import Field, Session, SQLModel, select
from typing_extensions import assert_type


def test_generic_type_with_bound(clear_sqlmodel) -> None:
    TagT = TypeVar("TagT", bound=int)

    class HeroFields(SQLModel, Generic[TagT]):
        tag: TagT

    class Hero(HeroFields[int], table=True):
        id: int | None = Field(default=None, primary_key=True)

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        tag_number = 67
        hero = Hero(tag=tag_number)
        session.add(hero)

        hero = session.exec(select(Hero).where(Hero.tag == tag_number)).first()
        assert hero is not None
        assert hero.tag == tag_number


def test_generic_type_with_constraints(clear_sqlmodel) -> None:
    TagT = TypeVar("TagT", int, None)

    class HeroFields(SQLModel, Generic[TagT]):
        tag: TagT

    class Hero(HeroFields[int], table=True):
        id: int | None = Field(default=None, primary_key=True)

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        tag_number = 67
        hero = Hero(tag=tag_number)
        session.add(hero)

        hero = session.exec(select(Hero).where(Hero.tag == tag_number)).first()
        assert hero is not None
        assert hero.tag == tag_number


def test_generic_type_with_multiple_type_constraints_raises_error(
    clear_sqlmodel,
) -> None:
    with pytest.raises(ValueError):
        TagT = TypeVar("TagT", int, str)

        class HeroFields(SQLModel, Generic[TagT]):
            tag: TagT

        class Hero(HeroFields[int], table=True):
            id: int | None = Field(default=None, primary_key=True)


def test_discriminated_union_with_generics(clear_sqlmodel) -> None:
    AmountRefundedT = TypeVar("AmountRefundedT", bound=int | None)
    RejectionMessageT = TypeVar("RejectionMessageT", bound=str | None)

    class RefundStatus(str, Enum):
        ACCEPTED = "ACCEPTED"
        REJECTED = "REJECTED"

    DiscriminantT = TypeVar("DiscriminantT", bound=RefundStatus)

    class RefundRequestFields(
        SQLModel, Generic[AmountRefundedT, RejectionMessageT, DiscriminantT]
    ):
        item_name: str
        amount_refunded: AmountRefundedT
        rejection_message: RejectionMessageT
        status: DiscriminantT

    class RefundRequest(
        RefundRequestFields[int | None, str | None, RefundStatus], table=True
    ):
        id: int | None = Field(default=None, primary_key=True)
        status: RefundStatus

    class AcceptedRequest(RefundRequestFields[int, None, RefundStatus.ACCEPTED]):
        amount_refunded: int
        rejection_message: None = None
        status: Literal[RefundStatus.ACCEPTED] = RefundStatus.ACCEPTED

    class RejectedRequest(RefundRequestFields[None, str, RefundStatus.REJECTED]):
        rejection_message: str
        amount_refunded: None = None
        status: Literal[RefundStatus.REJECTED] = RefundStatus.REJECTED

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        c = RejectedRequest(
            item_name="EmptyJuice",
            rejection_message="This item cannot be refunded because it has been emptied",
        )
        session.add(RefundRequest.model_validate(c.model_dump()))

        requests = session.exec(
            select(RefundRequest).where(
                RefundRequest.status == RefundStatus.REJECTED,
            )
        ).all()
        rejected_requests = [
            RejectedRequest.model_validate(request.model_dump())
            for request in requests
            if request.status == RefundStatus.REJECTED
        ]
        assert_type(rejected_requests, list[RejectedRequest])
        assert len(rejected_requests) == 1
