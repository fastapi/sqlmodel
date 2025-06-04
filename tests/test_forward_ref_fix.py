"""
Comprehensive test for forward reference resolution in SQLModel conversion.
This test specifically verifies that the fix for forward reference conversion works correctly.
"""

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine
from sqlmodel.main import (
    _convert_pydantic_to_table_model,
    _convert_single_pydantic_to_table_model,
)
from pydantic import BaseModel


# Pydantic models (not table models)
class AuthorPydantic(BaseModel):
    name: str
    bio: str


class BookPydantic(BaseModel):
    title: str
    isbn: str
    pages: int


def test_forward_reference_single_conversion(clear_sqlmodel):
    """Test conversion of a single Pydantic model with forward reference target."""
    print("\n🧪 Testing single forward reference conversion...")

    # SQLModel table models with forward references
    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(index=True)
        bio: str

        books: List["Book"] = Relationship(back_populates="author")

    class Book(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str = Field(index=True)
        isbn: str = Field(unique=True)
        pages: int

        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional[Author] = Relationship(back_populates="books")

    # Create a Pydantic model
    author_pydantic = AuthorPydantic(name="J.K. Rowling", bio="British author")

    # Test the conversion function directly with forward reference as string
    result = _convert_single_pydantic_to_table_model(author_pydantic, "Author")

    print(f"Input: {author_pydantic} (type: {type(author_pydantic)})")
    print(f"Result: {result} (type: {type(result)})")

    # Verify the result is correctly converted
    assert isinstance(result, Author), f"Expected Author, got {type(result)}"
    assert result.name == "J.K. Rowling"
    assert result.bio == "British author"
    print("✅ Single forward reference conversion test passed!")

    return True


def test_forward_reference_list_conversion(clear_sqlmodel):
    """Test conversion of a list of Pydantic models with forward reference target."""
    print("\n🧪 Testing list forward reference conversion...")

    # SQLModel table models with forward references
    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(index=True)
        bio: str

        books: List["Book"] = Relationship(back_populates="author")

    class Book(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str = Field(index=True)
        isbn: str = Field(unique=True)
        pages: int

        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional[Author] = Relationship(back_populates="books")

    # Create list of Pydantic models
    books_pydantic = [
        BookPydantic(title="Harry Potter", isbn="123-456", pages=300),
        BookPydantic(title="Fantastic Beasts", isbn="789-012", pages=250),
    ]

    # Test the conversion function directly with forward reference as string
    result = _convert_pydantic_to_table_model(books_pydantic, "books", Author)

    print(f"Input: {books_pydantic} (length: {len(books_pydantic)})")
    print(
        f"Result: {result} (length: {len(result) if isinstance(result, list) else 'N/A'})"
    )

    # Verify the result is correctly converted
    assert isinstance(result, list), f"Expected list, got {type(result)}"
    assert len(result) == 2, f"Expected 2 items, got {len(result)}"

    for i, book in enumerate(result):
        assert isinstance(book, Book), f"Expected Book at index {i}, got {type(book)}"
        assert book.title == books_pydantic[i].title
        assert book.isbn == books_pydantic[i].isbn
        assert book.pages == books_pydantic[i].pages

    print("✅ List forward reference conversion test passed!")
    return True


def test_forward_reference_unresolvable(clear_sqlmodel):
    """Test behavior when forward reference cannot be resolved."""
    print("\n🧪 Testing unresolvable forward reference...")

    # SQLModel table models with forward references
    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(index=True)
        bio: str

        books: List["Book"] = Relationship(back_populates="author")

    class Book(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str = Field(index=True)
        isbn: str = Field(unique=True)
        pages: int

        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional[Author] = Relationship(back_populates="books")

    # Create a Pydantic model
    author_pydantic = AuthorPydantic(name="Unknown Author", bio="Mystery writer")

    # Test with non-existent forward reference
    result = _convert_single_pydantic_to_table_model(
        author_pydantic, "NonExistentClass"
    )

    print(f"Input: {author_pydantic} (type: {type(author_pydantic)})")
    print(f"Result: {result} (type: {type(result)})")

    # Should return the original item when forward reference can't be resolved
    assert result is author_pydantic, f"Expected original object, got {result}"
    print("✅ Unresolvable forward reference test passed!")

    return True


def test_forward_reference_none_input(clear_sqlmodel):
    """Test behavior with None input."""
    print("\n🧪 Testing None input...")

    # SQLModel table models with forward references
    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(index=True)
        bio: str

        books: List["Book"] = Relationship(back_populates="author")

    class Book(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str = Field(index=True)
        isbn: str = Field(unique=True)
        pages: int

        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional[Author] = Relationship(back_populates="books")

    result = _convert_single_pydantic_to_table_model(None, "Author")

    print("Input: None")
    print(f"Result: {result}")

    assert result is None, f"Expected None, got {result}"
    print("✅ None input test passed!")

    return True


def test_forward_reference_already_correct_type(clear_sqlmodel):
    """Test behavior when input is already the correct type."""
    print("\n🧪 Testing already correct type...")

    # SQLModel table models with forward references
    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(index=True)
        bio: str

        books: List["Book"] = Relationship(back_populates="author")

    class Book(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str = Field(index=True)
        isbn: str = Field(unique=True)
        pages: int

        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional[Author] = Relationship(back_populates="books")

    # Create engine and tables first
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    # Create an actual Author instance
    author = Author(name="Test Author", bio="Test bio")

    result = _convert_single_pydantic_to_table_model(author, "Author")

    print(f"Input: {author} (type: {type(author)})")
    print(f"Result: {result} (type: {type(result)})")

    # Should return the same object
    assert result is author, f"Expected same object, got {result}"
    print("✅ Already correct type test passed!")

    return True


def test_registry_population(clear_sqlmodel):
    """Test that the class registry is properly populated."""
    print("\n🧪 Testing class registry population...")

    # SQLModel table models with forward references
    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(index=True)
        bio: str

        books: List["Book"] = Relationship(back_populates="author")

    class Book(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str = Field(index=True)
        isbn: str = Field(unique=True)
        pages: int

        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional[Author] = Relationship(back_populates="books")

    from sqlmodel.main import default_registry

    print(f"Registry contents: {list(default_registry._class_registry.keys())}")

    # Should contain our classes
    assert "Author" in default_registry._class_registry, "Author not found in registry"
    assert "Book" in default_registry._class_registry, "Book not found in registry"

    # Verify the classes are correct
    assert default_registry._class_registry["Author"] is Author
    assert default_registry._class_registry["Book"] is Book

    print("✅ Registry population test passed!")
    return True


def run_all_tests():
    """Run all forward reference tests."""
    print("🚀 Running comprehensive forward reference tests...\n")

    tests = [
        test_registry_population,
        test_forward_reference_single_conversion,
        test_forward_reference_list_conversion,
        test_forward_reference_unresolvable,
        test_forward_reference_none_input,
        test_forward_reference_already_correct_type,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            import traceback

            traceback.print_exc()
            failed += 1

    print(f"\n📊 Test Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
