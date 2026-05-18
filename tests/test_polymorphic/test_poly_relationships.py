"""
Mirrors sqlalchemy/test/orm/inheritance/test_relationship.py ::
    SelfReferentialTestJoinedToBase
    SelfReferentialJ2JTest
"""

from typing import Optional

from sqlalchemy.orm import aliased
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


# SelfReferentialTestJoinedToBase
# Engineer has a relationship back to the Person base class.
def _make_person_engineer_classes():
    class Person(SQLModel, table=True):
        __tablename__ = "rel_person"
        id: int | None = Field(default=None, primary_key=True)
        name: str
        type: str = Field(default="person")

        __mapper_args__ = {
            "polymorphic_on": "type",
            "polymorphic_identity": "person",
        }

    class Engineer(Person, table=True):
        __tablename__ = "rel_engineer"
        id: int | None = Field(
            default=None, primary_key=True, foreign_key="rel_person.id"
        )
        primary_language: str | None = None
        # plain integer — no FK constraint, so inherit_condition stays unambiguous
        reports_to_id: int | None = None
        reports_to: Person | None = Relationship(
            sa_relationship_kwargs={
                "primaryjoin": "Engineer.reports_to_id == Person.id",
                "foreign_keys": "[Engineer.reports_to_id]",
            }
        )

        __mapper_args__ = {"polymorphic_identity": "engineer"}

    return Person, Engineer


def test_jti_subclass_relationship_to_base_persists():
    # mirrors SelfReferentialTestJoinedToBase.test_has
    Person, Engineer = _make_person_engineer_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        p1 = Person(name="dogbert")
        e1 = Engineer(name="dilbert", primary_language="java")
        db.add_all([p1, e1])
        db.flush()
        e1.reports_to = p1
        db.commit()
        e1_id = e1.id

    with Session(engine) as db:
        e = db.get(Engineer, e1_id)
        assert e.reports_to.name == "dogbert"


def test_jti_subclass_relationship_to_base_fk():
    # reports_to_id is set when the relationship is assigned
    Person, Engineer = _make_person_engineer_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        mgr = Person(name="pointy_hair")
        eng = Engineer(name="wally", primary_language="c")
        db.add_all([mgr, eng])
        db.flush()
        mgr_id = mgr.id

        eng.reports_to = mgr
        db.commit()
        eng_id = eng.id

    with Session(engine) as db:
        eng = db.get(Engineer, eng_id)
        assert eng.reports_to_id == mgr_id


def test_jti_subclass_relationship_to_base_filter():
    # mirrors SelfReferentialTestJoinedToBase.test_join
    Person, Engineer = _make_person_engineer_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        boss = Person(name="boss")
        e1 = Engineer(name="alice", primary_language="python")
        e2 = Engineer(name="bob", primary_language="java")
        db.add_all([boss, e1, e2])
        db.flush()
        e1.reports_to = boss
        db.commit()

    with Session(engine) as db:
        # alias Person to avoid ambiguity: rel_person is already joined for JTI
        manager = aliased(Person)
        results = db.exec(
            select(Engineer)
            .join(manager, Engineer.reports_to_id == manager.id)
            .where(manager.name == "boss")
        ).all()
        assert len(results) == 1
        assert results[0].name == "alice"


# Engineer has a self-referential foreign key to the same subclass table.
def _make_engineer_self_ref_classes():
    class SPerson(SQLModel, table=True):
        __tablename__ = "rel_sperson"
        id: int | None = Field(default=None, primary_key=True)
        name: str
        type: str = Field(default="person")

        __mapper_args__ = {
            "polymorphic_on": "type",
            "polymorphic_identity": "person",
        }

    class SEngineer(SPerson, table=True):
        __tablename__ = "rel_sengineer"
        id: int | None = Field(
            default=None, primary_key=True, foreign_key="rel_sperson.id"
        )
        primary_language: str | None = None
        reports_to_id: int | None = Field(default=None, foreign_key="rel_sengineer.id")
        reports_to: Optional["SEngineer"] = Relationship(
            sa_relationship_kwargs={
                "primaryjoin": "SEngineer.reports_to_id == SEngineer.id",
                "foreign_keys": "[SEngineer.reports_to_id]",
                "remote_side": "SEngineer.id",
            }
        )

        __mapper_args__ = {"polymorphic_identity": "engineer"}

    return SPerson, SEngineer


def test_jti_subclass_self_referential_persists():
    # mirrors SelfReferentialJ2JTest.test_has
    SPerson, SEngineer = _make_engineer_self_ref_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        lead = SEngineer(name="lead", primary_language="python")
        junior = SEngineer(name="junior", primary_language="java")
        db.add_all([lead, junior])
        db.flush()
        junior.reports_to = lead
        db.commit()
        junior_id = junior.id

    with Session(engine) as db:
        e = db.get(SEngineer, junior_id)
        assert e.reports_to.name == "lead"
        assert isinstance(e.reports_to, SEngineer)


def test_jti_subclass_self_referential_chain():
    # mirrors SelfReferentialJ2JTest.test_join — three-level reporting chain
    SPerson, SEngineer = _make_engineer_self_ref_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        vp = SEngineer(name="vp", primary_language="c")
        mgr = SEngineer(name="mgr", primary_language="java")
        ic = SEngineer(name="ic", primary_language="python")
        db.add_all([vp, mgr, ic])
        db.flush()
        mgr.reports_to = vp
        ic.reports_to = mgr
        db.commit()
        ic_id = ic.id

    with Session(engine) as db:
        e = db.get(SEngineer, ic_id)
        assert e.reports_to.name == "mgr"
        assert e.reports_to.reports_to.name == "vp"
