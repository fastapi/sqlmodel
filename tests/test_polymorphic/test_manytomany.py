"""Mirrors sqlalchemy/test/orm/inheritance/test_manytomany.py"""

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine


# Two jointed table inheritance subclasses (User, Group) linked many to many; both sides of the relationship resolve correctly.
def test_jti_m2m_subclass_to_subclass():
    class UserGroupLink(SQLModel, table=True):
        __tablename__ = "prin_user_group_map"
        user_id: int | None = Field(
            default=None, foreign_key="prin_users.id", primary_key=True
        )
        group_id: int | None = Field(
            default=None, foreign_key="prin_groups.id", primary_key=True
        )

    class Principal(SQLModel, table=True):
        __tablename__ = "principals"
        id: int | None = Field(default=None, primary_key=True)
        name: str
        type: str = Field(default="principal")

        __mapper_args__ = {
            "polymorphic_on": "type",
            "polymorphic_identity": "principal",
        }

    class User(Principal, table=True):
        __tablename__ = "prin_users"
        id: int | None = Field(
            default=None, primary_key=True, foreign_key="principals.id"
        )
        password: str
        email: str
        login_id: str
        groups: list["Group"] = Relationship(
            back_populates="users", link_model=UserGroupLink
        )

        __mapper_args__ = {"polymorphic_identity": "user"}

    class Group(Principal, table=True):
        __tablename__ = "prin_groups"
        id: int | None = Field(
            default=None, primary_key=True, foreign_key="principals.id"
        )
        users: list[User] = Relationship(
            back_populates="groups", link_model=UserGroupLink
        )

        __mapper_args__ = {"polymorphic_identity": "group"}

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        u = User(name="user1", password="pw", email="foo@bar.com", login_id="lg1")
        g = Group(name="group1")
        g.users.append(u)
        db.add(g)
        db.flush()
        group_id, user_id = g.id, u.id
        db.commit()

    with Session(engine) as db:
        g = db.get(Group, group_id)
        assert len(g.users) == 1
        assert g.users[0].id == user_id
        assert g.users[0].name == "user1"

        u = db.get(User, user_id)
        assert len(u.groups) == 1
        assert u.groups[0].id == group_id


# db.get(Bar, id) works when Bar is a jointed table inheritance subclass with its own primary key column.
def test_jti_m2m_get_by_subclass_pk():
    class FooBarLink(SQLModel, table=True):
        __tablename__ = "foo_bar_link"
        foo_id: int | None = Field(
            default=None, foreign_key="m2m_foo.id", primary_key=True
        )
        bar_id: int | None = Field(
            default=None, foreign_key="m2m_bar.id", primary_key=True
        )

    class Foo(SQLModel, table=True):
        __tablename__ = "m2m_foo"
        id: int | None = Field(default=None, primary_key=True)
        data: str | None = None
        type: str = Field(default="foo")

        __mapper_args__ = {
            "polymorphic_on": "type",
            "polymorphic_identity": "foo",
        }

    class Bar(Foo, table=True):
        __tablename__ = "m2m_bar"
        id: int | None = Field(default=None, primary_key=True, foreign_key="m2m_foo.id")
        foos: list[Foo] = Relationship(link_model=FooBarLink)

        __mapper_args__ = {"polymorphic_identity": "bar"}

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        b = Bar(data="bar1")
        db.add(b)
        db.flush()
        bar_id = b.id

        f1 = Foo(data="foo1")
        f2 = Foo(data="foo2")
        b.foos.append(f1)
        b.foos.append(f2)
        db.commit()

    with Session(engine) as db:
        b = db.get(Bar, bar_id)
        assert b is not None
        assert b.id == bar_id
        assert {f.data for f in b.foos} == {"foo1", "foo2"}


# Three-level jointed table inheritance (Foo → Bar → Blub); Blub holds two many to many collections, one to each ancestor level.
def test_jti_m2m_three_level():
    class BlubBarLink(SQLModel, table=True):
        __tablename__ = "blub_bar_link"
        blub_id: int | None = Field(
            default=None, foreign_key="m3_blub.id", primary_key=True
        )
        bar_id: int | None = Field(
            default=None, foreign_key="m3_bar.id", primary_key=True
        )

    class BlubFooLink(SQLModel, table=True):
        __tablename__ = "blub_foo_link"
        blub_id: int | None = Field(
            default=None, foreign_key="m3_blub.id", primary_key=True
        )
        foo_id: int | None = Field(
            default=None, foreign_key="m3_foo.id", primary_key=True
        )

    class Foo(SQLModel, table=True):
        __tablename__ = "m3_foo"
        id: int | None = Field(default=None, primary_key=True)
        data: str | None = None
        type: str = Field(default="foo")

        __mapper_args__ = {
            "polymorphic_on": "type",
            "polymorphic_identity": "foo",
        }

    class Bar(Foo, table=True):
        __tablename__ = "m3_bar"
        id: int | None = Field(default=None, primary_key=True, foreign_key="m3_foo.id")
        bar_data: str | None = None

        __mapper_args__ = {"polymorphic_identity": "bar"}

    class Blub(Bar, table=True):
        __tablename__ = "m3_blub"
        id: int | None = Field(default=None, primary_key=True, foreign_key="m3_bar.id")
        blub_data: str | None = None
        bars: list[Bar] = Relationship(link_model=BlubBarLink)
        foos: list[Foo] = Relationship(link_model=BlubFooLink)

        __mapper_args__ = {"polymorphic_identity": "blub"}

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        f1 = Foo(data="foo1")
        b1 = Bar(data="bar1", bar_data="bdata1")
        b2 = Bar(data="bar2", bar_data="bdata2")
        bl = Blub(data="blub1", blub_data="blubdata1")
        db.add_all([f1, b1, b2, bl])
        db.flush()
        bl.foos.append(f1)
        bl.bars.append(b2)
        db.commit()
        blub_id = bl.id

    with Session(engine) as db:
        bl = db.get(Blub, blub_id)
        assert {f.data for f in bl.foos} == {"foo1"}
        assert {b.data for b in bl.bars} == {"bar2"}
