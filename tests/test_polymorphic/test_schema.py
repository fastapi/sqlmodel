# Verify that polymorphic inheritance produces the correct table structure at the database level.


from sqlalchemy import text
from sqlmodel import Field, Session, SQLModel, create_engine


# Joined inheritance table: each subclass gets its own table. The base table holds shared columns and the subclass table holds its own columns.
def _make_jti_classes():
    class Animal(SQLModel, table=True):
        __tablename__ = "schema_animal"
        id: int | None = Field(default=None, primary_key=True)
        type: str = Field(default="animal")
        name: str

        __mapper_args__ = {
            "polymorphic_on": "type",
            "polymorphic_identity": "animal",
        }

    class Dog(Animal, table=True):
        __tablename__ = "schema_dog"
        id: int | None = Field(
            default=None, primary_key=True, foreign_key="schema_animal.id"
        )
        breed: str | None = None

        __mapper_args__ = {"polymorphic_identity": "dog"}

    class Bulldog(Dog, table=True):
        __tablename__ = "schema_bulldog"
        id: int | None = Field(
            default=None, primary_key=True, foreign_key="schema_dog.id"
        )
        wrinkle_count: int | None = None

        __mapper_args__ = {"polymorphic_identity": "bulldog"}

    return Animal, Dog, Bulldog


def test_jti_data_split_across_tables():
    Animal, Dog, Bulldog = _make_jti_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        d = Dog(name="Rex", breed="Labrador")
        db.add(d)
        db.commit()
        dog_id = d.id

    with engine.connect() as conn:
        animal_row = conn.execute(
            text("SELECT name, type FROM schema_animal WHERE id = :id"),
            {"id": dog_id},
        ).fetchone()
        assert animal_row is not None
        assert animal_row[0] == "Rex"
        assert animal_row[1] == "dog"

        dog_row = conn.execute(
            text("SELECT breed FROM schema_dog WHERE id = :id"),
            {"id": dog_id},
        ).fetchone()
        assert dog_row is not None
        assert dog_row[0] == "Labrador"

        # Confirm no columns leaked across tables.
        animal_cols = {
            r[1]
            for r in conn.execute(text("PRAGMA table_info(schema_animal)")).fetchall()
        }
        dog_cols = {
            r[1] for r in conn.execute(text("PRAGMA table_info(schema_dog)")).fetchall()
        }
        assert animal_cols == {"id", "type", "name"}
        assert dog_cols == {"id", "breed"}


def test_jti_three_level_data_split_across_tables():
    Animal, Dog, Bulldog = _make_jti_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        b = Bulldog(name="Wrinkles", breed="English Bulldog", wrinkle_count=42)
        db.add(b)
        db.commit()
        bulldog_id = b.id

    with engine.connect() as conn:
        animal_row = conn.execute(
            text("SELECT name, type FROM schema_animal WHERE id = :id"),
            {"id": bulldog_id},
        ).fetchone()
        assert animal_row is not None
        assert animal_row[0] == "Wrinkles"
        assert animal_row[1] == "bulldog"

        dog_row = conn.execute(
            text("SELECT breed FROM schema_dog WHERE id = :id"),
            {"id": bulldog_id},
        ).fetchone()
        assert dog_row is not None
        assert dog_row[0] == "English Bulldog"

        bulldog_row = conn.execute(
            text("SELECT wrinkle_count FROM schema_bulldog WHERE id = :id"),
            {"id": bulldog_id},
        ).fetchone()
        assert bulldog_row is not None
        assert bulldog_row[0] == 42

        animal_cols = {
            r[1]
            for r in conn.execute(text("PRAGMA table_info(schema_animal)")).fetchall()
        }
        dog_cols = {
            r[1] for r in conn.execute(text("PRAGMA table_info(schema_dog)")).fetchall()
        }
        bulldog_cols = {
            r[1]
            for r in conn.execute(text("PRAGMA table_info(schema_bulldog)")).fetchall()
        }
        assert animal_cols == {"id", "type", "name"}
        assert dog_cols == {"id", "breed"}
        assert bulldog_cols == {"id", "wrinkle_count"}


# Single inheritance table: all subclasses share one table. The type column identifies which subclass each row belongs to.
def _make_sti_classes():
    class Vehicle(SQLModel, table=True):
        __tablename__ = "schema_vehicle"
        id: int | None = Field(default=None, primary_key=True)
        type: str = Field(default="vehicle")
        name: str

        __mapper_args__ = {
            "polymorphic_on": "type",
            "polymorphic_identity": "vehicle",
        }

    class Car(Vehicle):
        num_doors: int | None = None
        __mapper_args__ = {"polymorphic_identity": "car"}

    class Truck(Vehicle):
        payload_tons: int | None = None
        __mapper_args__ = {"polymorphic_identity": "truck"}

    return Vehicle, Car, Truck


def test_sti_data_in_single_table():
    Vehicle, Car, Truck = _make_sti_classes()
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        c = Car(name="Tesla", num_doors=4)
        t = Truck(name="Ford F-150", payload_tons=1)
        db.add(c)
        db.add(t)
        db.commit()
        car_id = c.id
        truck_id = t.id

    with engine.connect() as conn:
        # Each row has its own feature column set and the other subclass column is null.
        car_row = conn.execute(
            text(
                "SELECT name, type, num_doors, payload_tons FROM schema_vehicle WHERE id = :id"
            ),
            {"id": car_id},
        ).fetchone()
        assert car_row is not None
        assert car_row[0] == "Tesla"
        assert car_row[1] == "car"
        assert car_row[2] == 4
        assert car_row[3] is None

        truck_row = conn.execute(
            text(
                "SELECT name, type, num_doors, payload_tons FROM schema_vehicle WHERE id = :id"
            ),
            {"id": truck_id},
        ).fetchone()
        assert truck_row is not None
        assert truck_row[0] == "Ford F-150"
        assert truck_row[1] == "truck"
        assert truck_row[2] is None
        assert truck_row[3] == 1

        # Only one table should exist; subclasses must not create their own.
        tables = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table'")
        ).fetchall()
        table_names = {r[0] for r in tables}
        assert table_names == {"schema_vehicle"}

        vehicle_cols = {
            r[1]
            for r in conn.execute(text("PRAGMA table_info(schema_vehicle)")).fetchall()
        }
        assert vehicle_cols == {"id", "type", "name", "num_doors", "payload_tons"}
