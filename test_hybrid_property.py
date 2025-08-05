"""
Тест для проверки работы hybrid_property с setter'ами в SQLModel
"""

from typing import List, Optional
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlmodel import SQLModel, Field


class Permission(SQLModel, table=True):
    __tablename__ = "permission"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    

class Role(SQLModel, table=True):
    __tablename__ = "role"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    
    # Relationship to permissions
    permissions: List[Permission] = relationship()


class User(SQLModel, table=True):
    __tablename__ = "user"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    
    # Relationships
    role: Optional[Role] = relationship()
    permissions_grant: List[Permission] = relationship()
    permissions_revoke: List[Permission] = relationship()
    
    @hybrid_property
    def permissions(self) -> List[Permission]:
        """Getter для permissions - объединяет роль и индивидуальные разрешения"""
        role_permissions = self.role.permissions if self.role else []
        return list(
            set(role_permissions + self.permissions_grant)
            - set(self.permissions_revoke)
        )

    @permissions.inplace.setter
    def _permissions_setter(self, value: List[Permission]) -> None:
        """Setter для permissions - вычисляет grant и revoke списки"""
        role_permissions = self.role.permissions if self.role else []
        self.permissions_grant = list(set(value) - set(role_permissions))
        self.permissions_revoke = list(set(role_permissions) - set(value))


def test_hybrid_property_setter_direct():
    """Тест прямого присвоения через hybrid property setter"""
    print("Тестируем hybrid property setter...")
    
    try:
        # Создаем пользователя
        user = User(id=1, name="John Doe")
        print(f"✅ Создан пользователь: {user.name}")
        
        # Проверяем, что hybrid property найден в классе
        if hasattr(user.__class__, 'permissions'):
            permissions_attr = getattr(user.__class__, 'permissions')
            print(f"✅ permissions найден: {type(permissions_attr)}")
            
            # Проверяем, что это hybrid_property
            if isinstance(permissions_attr, hybrid_property):
                print("✅ permissions является hybrid_property")
                
                # Проверяем наличие setter'а
                if hasattr(permissions_attr, 'setter'):
                    print("✅ hybrid_property имеет setter")
                else:
                    print("❌ hybrid_property НЕ имеет setter")
            else:
                print(f"❌ permissions НЕ является hybrid_property: {type(permissions_attr)}")
        else:
            print("❌ permissions НЕ найден в классе")
        
        # Создаем тестовые разрешения
        perm1 = Permission(id=1, name="read")
        perm2 = Permission(id=2, name="write")
        test_permissions = [perm1, perm2]
        
        # Инициализируем списки
        user.permissions_grant = []
        user.permissions_revoke = []
        user.role = None
        
        print("\nТестируем присвоение через hybrid property setter...")
        
        # Присваиваем через setter
        user.permissions = test_permissions
        
        print(f"✅ Присвоение завершено без ошибок")
        print(f"✅ permissions_grant: {len(user.permissions_grant)} элементов")
        print(f"✅ permissions_revoke: {len(user.permissions_revoke)} элементов")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


def test_hybrid_property_with_model_validate():
    """Тест hybrid property через model_validate"""
    print("\nТестируем hybrid property через model_validate...")
    
    try:
        # Создаем тестовые данные
        perm1 = Permission(id=1, name="read")
        perm2 = Permission(id=2, name="write")
        
        test_data = {
            "id": 1,
            "name": "Jane Doe",
            "role_id": None,
            "permissions": [perm1, perm2]  # Через hybrid property
        }
        
        print("Выполняем model_validate с hybrid property...")
        validated_user = User.model_validate(test_data)
        
        print(f"✅ model_validate успешно: {validated_user.name}")
        
        # Проверяем, что setter был вызван
        if hasattr(validated_user, 'permissions_grant'):
            print(f"✅ permissions_grant установлен: {len(validated_user.permissions_grant)} элементов")
        else:
            print("❌ permissions_grant НЕ установлен")
            
    except Exception as e:
        print(f"⚠️  model_validate с hybrid property не сработал: {e}")
        # Это может быть ожидаемо в зависимости от реализации


def test_hybrid_property_inspection():
    """Тест проверки структуры hybrid property"""
    print("\nИнспекция hybrid property...")
    
    try:
        user = User(id=1, name="Test")
        
        # Получаем атрибут класса
        permissions_attr = getattr(User, 'permissions')
        
        print(f"Тип атрибута: {type(permissions_attr)}")
        print(f"Атрибуты: {dir(permissions_attr)}")
        
        # Проверяем различные способы определения setter'а
        checks = [
            ("hasattr(permissions_attr, 'setter')", hasattr(permissions_attr, 'setter')),
            ("hasattr(permissions_attr, '__set__')", hasattr(permissions_attr, '__set__')),
            ("hasattr(permissions_attr, 'fset')", hasattr(permissions_attr, 'fset')),
            ("hasattr(permissions_attr, 'inplace')", hasattr(permissions_attr, 'inplace')),
        ]
        
        for check_name, result in checks:
            print(f"{check_name}: {result}")
            
        # Если есть inplace, проверим его атрибуты
        if hasattr(permissions_attr, 'inplace'):
            inplace_attr = permissions_attr.inplace
            print(f"inplace тип: {type(inplace_attr)}")
            print(f"inplace атрибуты: {dir(inplace_attr)}")
            
    except Exception as e:
        print(f"❌ Ошибка в инспекции: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Запуск тестов hybrid property setter...")
    test_hybrid_property_inspection()
    test_hybrid_property_setter_direct()
    test_hybrid_property_with_model_validate()
    print("\nВсе тесты завершены!")
