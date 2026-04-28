"""Mirrors sqlalchemy/test/orm/inheritance/test_concrete.py :: ConcreteTest, PropertyInheritanceTest"""

from typing import Optional

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


def test_basic():
    # mirrors ConcreteTest.test_basic
    class Manager(SQLModel, table=True):
        __tablename__ = "cti_managers"
        employee_id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        manager_data: str

    class Engineer(SQLModel, table=True):
        __tablename__ = "cti_engineers"
        employee_id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        engineer_info: str

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        db.add(Manager(name="Sally", manager_data="knows how to manage things"))
        db.add(Engineer(name="Karina", engineer_info="knows how to hack"))
        db.commit()

    with Session(engine) as db:
        managers = db.exec(select(Manager)).all()
        engineers = db.exec(select(Engineer)).all()

        db.expire(managers[0], ["manager_data"])
        assert managers[0].manager_data == "knows how to manage things"

    assert {m.name for m in managers} == {"Sally"}
    assert {e.name for e in engineers} == {"Karina"}


def test_multi_level_no_base():
    # mirrors ConcreteTest.test_multi_level_no_base
    class Manager(SQLModel, table=True):
        __tablename__ = "cti3_managers"
        employee_id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        manager_data: str

    class Engineer(SQLModel, table=True):
        __tablename__ = "cti3_engineers"
        employee_id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        engineer_info: str

    class Hacker(SQLModel, table=True):
        __tablename__ = "cti3_hackers"
        employee_id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        engineer_info: str
        nickname: str

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        db.add(Manager(name="Sally", manager_data="knows how to manage things"))
        db.add(Engineer(name="Jenn", engineer_info="knows how to program"))
        db.add(Hacker(name="Karina", engineer_info="knows how to hack", nickname="Badass"))
        db.commit()

    with Session(engine) as db:
        managers = db.exec(select(Manager)).all()
        engineers = db.exec(select(Engineer)).all()
        hackers = db.exec(select(Hacker)).all()

    assert len(managers) == 1 and managers[0].name == "Sally"
    assert len(engineers) == 1 and engineers[0].engineer_info == "knows how to program"
    assert len(hackers) == 1 and hackers[0].nickname == "Badass"

    with Session(engine) as db:
        assert db.exec(select(Manager).where(Manager.name == "Karina")).first() is None


def test_relationship():
    # mirrors ConcreteTest.test_relationship / PropertyInheritanceTest
    class Company(SQLModel, table=True):
        __tablename__ = "cti4_companies"
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        managers: list["CtiManager"] = Relationship(back_populates="company")
        engineers: list["CtiEngineer"] = Relationship(back_populates="company")

    class CtiManager(SQLModel, table=True):
        __tablename__ = "cti4_managers"
        employee_id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        manager_data: str
        company_id: Optional[int] = Field(default=None, foreign_key="cti4_companies.id")
        company: Optional[Company] = Relationship(back_populates="managers")

    class CtiEngineer(SQLModel, table=True):
        __tablename__ = "cti4_engineers"
        employee_id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        engineer_info: str
        company_id: Optional[int] = Field(default=None, foreign_key="cti4_companies.id")
        company: Optional[Company] = Relationship(back_populates="engineers")

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        corp = Company(name="Initech")
        db.add(corp)
        db.flush()
        cid = corp.id
        db.add(CtiManager(name="Bill", manager_data="TPS reports", company_id=cid))
        db.add(CtiEngineer(name="Peter", engineer_info="cubicle dweller", company_id=cid))
        db.commit()

    with Session(engine) as db:
        corp = db.get(Company, cid)
        assert len(corp.managers) == 1 and corp.managers[0].name == "Bill"
        assert len(corp.engineers) == 1 and corp.engineers[0].name == "Peter"