from sqlmodel import SQLModel


def test_polymorphic_serialization_default():

    class User(SQLModel):
        name: str

    class UserLogin(User):
        password: str

    class OuterModel(SQLModel):
        user: User

    outer_model = OuterModel(
        user=UserLogin(name="pydantic", password="password"),
    )

    assert outer_model.model_dump() == {"user": {"name": "pydantic"}}


def test_polymorphic_serialization_false():

    class User(SQLModel):
        name: str

    class UserLogin(User):
        password: str

    class OuterModel(SQLModel):
        user: User

    outer_model = OuterModel(
        user=UserLogin(name="pydantic", password="password"),
    )

    assert outer_model.model_dump(polymorphic_serialization=False) == {
        "user": {"name": "pydantic"}
    }


def test_polymorphic_serialization_true():

    class User(SQLModel):
        name: str

    class UserLogin(User):
        password: str

    class OuterModel(SQLModel):
        user: User

    outer_model = OuterModel(
        user=UserLogin(name="pydantic", password="password"),
    )

    assert outer_model.model_dump(polymorphic_serialization=True) == {
        "user": {"name": "pydantic", "password": "password"}
    }
