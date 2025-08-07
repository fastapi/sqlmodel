"""Простые тесты для deferred_column_property с новой логикой."""

from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import undefer
from sqlmodel import Field, SQLModel, Session, select
from sqlmodel import deferred_column_property


def test_deferred_column_property_basic(clear_sqlmodel):
    """Комбинированный тест: проверяем fallback и undefer в одном тесте"""

    class TestEmployee(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        salary: int = 1000

        @classmethod
        def __declare_last__(cls):
            cls.is_owner = deferred_column_property(
                cls.__table__.c.salary > 50000,
                fallback_value=False,  # fallback значение
                deferred=True,
            )

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    # Создаём сотрудников с разными зарплатами
    with Session(engine) as session:
        emp1 = TestEmployee(salary=60000)  # Высокая зарплата
        emp2 = TestEmployee(salary=30000)  # Низкая зарплата
        session.add_all([emp1, emp2])
        session.commit()
        emp1_id, emp2_id = emp1.id, emp2.id

    # Тест 1: БЕЗ undefer - должен возвращать fallback
    print("=== Тест fallback значений ===")
    with Session(engine) as session:
        emp1 = session.get(TestEmployee, emp1_id)
        emp2 = session.get(TestEmployee, emp2_id)

        print(f"emp1: salary={emp1.salary}, is_owner={emp1.is_owner}")
        print(f"emp2: salary={emp2.salary}, is_owner={emp2.is_owner}")

        # И для высокой и для низкой зарплаты должен возвращать fallback
        assert emp1.is_owner is False  # fallback, НЕ True
        assert emp2.is_owner is False  # fallback

    # Тест 2: С undefer - должен возвращать реальные значения
    print("=== Тест реальных значений с undefer ===")
    with Session(engine) as session:
        emp1 = session.exec(
            select(TestEmployee)
            .options(undefer(TestEmployee.is_owner))
            .where(TestEmployee.id == emp1_id)
        ).one()

        emp2 = session.exec(
            select(TestEmployee)
            .options(undefer(TestEmployee.is_owner))
            .where(TestEmployee.id == emp2_id)
        ).one()

        print(f"emp1 (с undefer): salary={emp1.salary}, is_owner={emp1.is_owner}")
        print(f"emp2 (с undefer): salary={emp2.salary}, is_owner={emp2.is_owner}")

        # Теперь должны быть реальные значения из БД
        assert emp1.is_owner is True  # 60000 > 50000 = True
        assert emp2.is_owner is False  # 30000 > 50000 = False

    print("✅ Все тесты прошли!")
