from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.associationproxy import association_proxy
from sqlmodel import Field, Relationship, Session, SQLModel


def test_association_proxy_with_model_validate(clear_sqlmodel):
    """Test association proxy support in model_validate"""

    class UserSkill(SQLModel, table=True):
        __tablename__ = "user_skill"

        id: Optional[int] = Field(default=None, primary_key=True)
        user_id: int = Field(foreign_key="user.id")
        skill_name: str
        level: int = Field(default=1)

        # Relationship back to user
        user: Optional["User"] = Relationship(back_populates="user_skills")

    class User(SQLModel, table=True):
        __tablename__ = "user"

        id: Optional[int] = Field(default=None, primary_key=True)
        name: str

        # Relationship to UserSkill
        user_skills: List[UserSkill] = Relationship(back_populates="user")

        # Association proxy for direct access to skill names
        skill_names = association_proxy("user_skills", "skill_name")

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    # Test that association proxy is registered in the class
    assert hasattr(User, "__sqlalchemy_association_proxies__")
    assert "skill_names" in User.__sqlalchemy_association_proxies__

    # Create user with skills through UserSkill objects
    skill1 = UserSkill(user_id=1, skill_name="Python", level=5)
    skill2 = UserSkill(user_id=1, skill_name="JavaScript", level=3)

    test_data = {"id": 1, "name": "John Updated", "user_skills": [skill1, skill2]}

    validated_user = User.model_validate(test_data)

    assert validated_user.id == 1
    assert validated_user.name == "John Updated"
    assert len(validated_user.user_skills) == 2


def test_association_proxy_direct_assignment(clear_sqlmodel):
    """Test direct assignment through association proxy"""

    class UserSkill(SQLModel, table=True):
        __tablename__ = "user_skill"

        id: Optional[int] = Field(default=None, primary_key=True)
        user_id: int = Field(foreign_key="user.id")
        skill_name: str
        level: int = Field(default=1)

        # Relationship back to user
        user: Optional["User"] = Relationship(back_populates="user_skills")

    class User(SQLModel, table=True):
        __tablename__ = "user"

        id: Optional[int] = Field(default=None, primary_key=True)
        name: str

        # Relationship to UserSkill
        user_skills: List[UserSkill] = Relationship(back_populates="user")

        # Association proxy for direct access to skill names
        skill_names = association_proxy("user_skills", "skill_name")

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(name="Jane Doe")
        session.add(user)
        session.commit()
        session.refresh(user)

        # Create some UserSkill objects first
        skill1 = UserSkill(user_id=user.id, skill_name="React", level=4)
        skill2 = UserSkill(user_id=user.id, skill_name="Node.js", level=3)
        user.user_skills = [skill1, skill2]

        session.add_all([skill1, skill2])
        session.commit()

        # Test that association proxy is accessible
        assert hasattr(user, "skill_names")
        assert "skill_names" in user.__class__.__sqlalchemy_association_proxies__


def test_association_proxy_in_setattr(clear_sqlmodel):
    """Test that association proxy is handled in __setattr__"""

    class UserRole(SQLModel, table=True):
        __tablename__ = "user_role"

        id: Optional[int] = Field(default=None, primary_key=True)
        user_id: int = Field(foreign_key="user.id")
        role_name: str

        # Relationship back to user
        user: Optional["User"] = Relationship(back_populates="user_roles")

    class User(SQLModel, table=True):
        __tablename__ = "user"

        id: Optional[int] = Field(default=None, primary_key=True)
        name: str

        # Relationship to UserRole
        user_roles: List[UserRole] = Relationship(back_populates="user")

        # Association proxy for direct access to role names
        role_names = association_proxy(
            "user_roles",
            "role_name",
            creator=lambda role_name: UserRole(user_id=0, role_name=role_name),
        )

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(name="Test User")
        session.add(user)
        session.commit()
        session.refresh(user)

        # Verify association proxy is registered
        assert hasattr(User, "__sqlalchemy_association_proxies__")
        assert "role_names" in User.__sqlalchemy_association_proxies__

        # Create test data to assign through model_validate
        role1 = UserRole(user_id=user.id, role_name="admin")
        role2 = UserRole(user_id=user.id, role_name="user")

        test_data = {
            "id": user.id,
            "name": "Updated User",
            "user_roles": [role1, role2],
            "role_names": ["admin", "user"],  # This should trigger association proxy
        }

        # Test model_validate with association proxy data
        validated_user = User.model_validate(test_data)

        assert validated_user.name == "Updated User"
        assert len(validated_user.user_roles) == 2


def test_association_proxy_registration(clear_sqlmodel):
    """Test that association proxies are properly registered"""

    class Item(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        tag_id: int = Field(foreign_key="tag.id")

        tag: Optional["Tag"] = Relationship(back_populates="items")

    class Tag(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str

        items: List[Item] = Relationship(back_populates="tag")

        # Association proxy
        item_names = association_proxy("items", "name")

    # Verify the association proxy is registered
    assert hasattr(Tag, "__sqlalchemy_association_proxies__")
    assert "item_names" in Tag.__sqlalchemy_association_proxies__

    # Verify the proxy is of correct type
    proxy = Tag.__sqlalchemy_association_proxies__["item_names"]
    assert hasattr(proxy, "__set__")  # Should have setter method
    assert hasattr(proxy, "__get__")  # Should have getter method
