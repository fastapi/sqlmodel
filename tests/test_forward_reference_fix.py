"""
Test forward reference resolution in SQLModel conversion functions.
"""

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
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


def test_forward_reference_single_conversion(clear_sqlmodel):
    """Test conversion of a single Pydantic model with forward reference target."""

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

        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional["Author"] = Relationship(back_populates="books")

    # Create a Pydantic model
    author_pydantic = AuthorPydantic(name="J.K. Rowling", bio="British author")

    # Test the conversion function directly with forward reference as string
    result = _convert_single_pydantic_to_table_model(author_pydantic, "Author")

    # Verify the result is correctly converted
    assert isinstance(result, Author), f"Expected Author, got {type(result)}"
    assert result.name == "J.K. Rowling"
    assert result.bio == "British author"


def test_forward_reference_list_conversion(clear_sqlmodel):
    """Test conversion of a list of Pydantic models with forward reference target."""

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

        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional["Author"] = Relationship(back_populates="books")

    # Create list of Pydantic models
    books_pydantic = [
        BookPydantic(title="Harry Potter", isbn="123-456"),
        BookPydantic(title="Fantastic Beasts", isbn="789-012"),
    ]

    # Test the conversion function directly with forward reference as string
    result = _convert_pydantic_to_table_model(books_pydantic, "books", Author)

    # Verify the result is correctly converted
    assert isinstance(result, list), f"Expected list, got {type(result)}"
    assert len(result) == 2, f"Expected 2 items, got {len(result)}"

    for i, book in enumerate(result):
        assert isinstance(book, Book), f"Expected Book at index {i}, got {type(book)}"
        assert book.title == books_pydantic[i].title
        assert book.isbn == books_pydantic[i].isbn


def test_forward_reference_unresolvable(clear_sqlmodel):
    """Test behavior when forward reference cannot be resolved."""

    # Create a Pydantic model
    author_pydantic = AuthorPydantic(name="Unknown Author", bio="Mystery writer")

    # Test with non-existent forward reference
    result = _convert_single_pydantic_to_table_model(
        author_pydantic, "NonExistentClass"
    )

    # Should return the original item when forward reference can't be resolved
    assert result is author_pydantic, f"Expected original object, got {result}"


def test_forward_reference_none_input(clear_sqlmodel):
    """Test behavior with None input."""

    result = _convert_single_pydantic_to_table_model(None, "Author")

    assert result is None, f"Expected None, got {result}"


def test_forward_reference_already_correct_type(clear_sqlmodel):
    """Test behavior when input is already the correct type."""

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

        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional["Author"] = Relationship(back_populates="books")

    # Create an actual Author instance
    author = Author(name="Test Author", bio="Test bio")

    result = _convert_single_pydantic_to_table_model(author, "Author")

    # Should return the same object
    assert result is author, f"Expected same object, got {result}"


def test_registry_population(clear_sqlmodel):
    """Test that the class registry is properly populated."""

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

        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional["Author"] = Relationship(back_populates="books")

    from sqlmodel.main import default_registry

    # Should contain our classes
    assert "Author" in default_registry._class_registry, "Author not found in registry"
    assert "Book" in default_registry._class_registry, "Book not found in registry"

    # Verify the classes are correct
    assert default_registry._class_registry["Author"] is Author
    assert default_registry._class_registry["Book"] is Book
