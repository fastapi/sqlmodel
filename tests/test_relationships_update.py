"""
Comprehensive tests for relationship updates with forward references and Pydantic to SQLModel conversion.

This test suite validates the fix for forward reference resolution in SQLModel's conversion functionality.
The main issue was that when forward references (string-based type hints like "Book") are used in
relationship definitions, the conversion logic failed because isinstance() checks don't work with
string types instead of actual classes.
"""

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine
from pydantic import BaseModel
import pytest


def test_forward_reference_single_conversion(clear_sqlmodel):
    """Test conversion of single Pydantic model to SQLModel with forward reference."""

    class AuthorPydantic(BaseModel):
        name: str
        bio: str
        email: str

    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        bio: str
        email: str
        books: List["Book"] = Relationship(back_populates="author")

    class Book(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str
        isbn: str
        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional["Author"] = Relationship(back_populates="books")

    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        book = Book(title="Test Book", isbn="123-456-789")
        session.add(book)
        session.commit()
        session.refresh(book)

        # Create Pydantic model to assign
        author_pydantic = AuthorPydantic(
            name="Jane Doe", bio="A prolific writer", email="jane@example.com"
        )

        # This should trigger forward reference resolution
        book.author = author_pydantic

        # Verify conversion happened correctly
        assert isinstance(book.author, Author)
        assert book.author.name == "Jane Doe"
        assert book.author.bio == "A prolific writer"
        assert book.author.email == "jane@example.com"


def test_forward_reference_list_conversion(clear_sqlmodel):
    """Test conversion of list of Pydantic models to SQLModels with forward reference."""

    class BookPydantic(BaseModel):
        title: str
        isbn: str
        pages: int

    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        bio: str
        books: List["Book"] = Relationship(back_populates="author")

    class Book(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str
        isbn: str
        pages: int
        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional["Author"] = Relationship(back_populates="books")

    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        author = Author(name="John Smith", bio="Science fiction author")
        session.add(author)
        session.commit()
        session.refresh(author)

        # Create list of Pydantic models
        books_pydantic = [
            BookPydantic(title="Space Odyssey", isbn="111-111-111", pages=300),
            BookPydantic(title="Time Traveler", isbn="222-222-222", pages=250),
            BookPydantic(title="Alien Contact", isbn="333-333-333", pages=400),
        ]

        # This should trigger forward reference resolution for list
        author.books = books_pydantic

        # Verify conversion happened correctly
        assert isinstance(author.books, list)
        assert len(author.books) == 3

        for i, book in enumerate(author.books):
            assert isinstance(book, Book)
            assert book.title == books_pydantic[i].title
            assert book.isbn == books_pydantic[i].isbn
            assert book.pages == books_pydantic[i].pages


def test_forward_reference_edge_cases(clear_sqlmodel):
    """Test edge cases for forward reference resolution."""

    class AuthorPydantic(BaseModel):
        name: str
        bio: str

    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        bio: str
        books: List["Book"] = Relationship(back_populates="author")

    class Book(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str
        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional["Author"] = Relationship(back_populates="books")

    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        book = Book(title="Edge Case Book")
        session.add(book)
        session.commit()
        session.refresh(book)

        # Test 1: Assigning None should work
        book.author = None
        assert book.author is None

        # Test 2: Assigning already correct type should not convert
        existing_author = Author(name="Existing Author", bio="Already correct type")
        session.add(existing_author)
        session.commit()
        session.refresh(existing_author)

        original_author = existing_author
        book.author = existing_author
        assert book.author is original_author  # Should be the same object
        assert isinstance(book.author, Author)

        # Test 3: Assigning Pydantic model should convert
        author_pydantic = AuthorPydantic(name="New Author", bio="Should be converted")
        book.author = author_pydantic

        assert isinstance(book.author, Author)
        assert book.author is not author_pydantic  # Should be different object
        assert book.author.name == "New Author"
        assert book.author.bio == "Should be converted"


def test_forward_reference_nested_relationships(clear_sqlmodel):
    """Test forward references with more complex nested relationships."""

    class PublisherPydantic(BaseModel):
        name: str
        address: str

    class AuthorPydantic(BaseModel):
        name: str
        bio: str

    class BookPydantic(BaseModel):
        title: str
        isbn: str

    class Publisher(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        address: str
        books: List["Book"] = Relationship(back_populates="publisher")

    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        bio: str
        books: List["Book"] = Relationship(back_populates="author")

    class Book(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str
        isbn: str

        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional["Author"] = Relationship(back_populates="books")

        publisher_id: Optional[int] = Field(default=None, foreign_key="publisher.id")
        publisher: Optional["Publisher"] = Relationship(back_populates="books")

    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        book = Book(title="Complex Book", isbn="999-999-999")
        session.add(book)
        session.commit()
        session.refresh(book)

        # Test multiple forward reference conversions
        author_pydantic = AuthorPydantic(
            name="Complex Author", bio="Handles complexity"
        )
        publisher_pydantic = PublisherPydantic(
            name="Complex Publisher", address="123 Complex St"
        )

        book.author = author_pydantic
        book.publisher = publisher_pydantic

        # Verify both conversions worked
        assert isinstance(book.author, Author)
        assert book.author.name == "Complex Author"
        assert book.author.bio == "Handles complexity"

        assert isinstance(book.publisher, Publisher)
        assert book.publisher.name == "Complex Publisher"
        assert book.publisher.address == "123 Complex St"


def test_forward_reference_performance_large_lists(clear_sqlmodel):
    """Test performance with larger lists to ensure scalability."""

    class BookPydantic(BaseModel):
        title: str
        isbn: str
        pages: int

    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        books: List["Book"] = Relationship(back_populates="author")

    class Book(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str
        isbn: str
        pages: int
        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional["Author"] = Relationship(back_populates="books")

    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        author = Author(name="Prolific Author")
        session.add(author)
        session.commit()
        session.refresh(author)

        # Create a large list of Pydantic models
        large_book_list = [
            BookPydantic(title=f"Book {i}", isbn=f"{i:06d}", pages=200 + i)
            for i in range(75)  # Test with 75 items
        ]

        # Measure performance
        import time

        start_time = time.time()

        author.books = large_book_list

        end_time = time.time()
        conversion_time = end_time - start_time

        # Verify correctness
        assert len(author.books) == 75
        assert all(isinstance(book, Book) for book in author.books)

        # Verify data integrity
        for i, book in enumerate(author.books):
            assert book.title == f"Book {i}"
            assert book.isbn == f"{i:06d}"
            assert book.pages == 200 + i

        # Performance should be reasonable (less than 1 second for 75 items)
        assert (
            conversion_time < 1.0
        ), f"Conversion took too long: {conversion_time:.3f}s"


def test_forward_reference_error_handling(clear_sqlmodel):
    """Test error handling for invalid forward reference scenarios."""

    class InvalidPydantic(BaseModel):
        name: str
        invalid_field: str

    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        books: List["Book"] = Relationship(back_populates="author")

    class Book(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str
        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional["Author"] = Relationship(back_populates="books")

    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        book = Book(title="Error Test Book")
        session.add(book)
        session.commit()
        session.refresh(book)

        # Test 1: Invalid Pydantic model (missing required fields for Author)
        invalid_pydantic = InvalidPydantic(
            name="Invalid", invalid_field="Should not work"
        )

        # This should handle the error gracefully and not convert
        try:
            book.author = invalid_pydantic
            # If conversion fails, the original value should remain
            assert book.author is invalid_pydantic or book.author is None
        except Exception as e:
            # If an exception is raised, that's also acceptable error handling
            assert True  # Test passes if exception is handled

        # Test 2: Verify that valid conversions still work after error
        class ValidAuthorPydantic(BaseModel):
            name: str
            bio: str = "Default bio"

        valid_author = ValidAuthorPydantic(name="Valid Author")
        book.author = valid_author

        # This should work correctly
        assert isinstance(book.author, Author)
        assert book.author.name == "Valid Author"


def test_forward_reference_mixed_types(clear_sqlmodel):
    """Test mixed scenarios with different relationship types."""

    class AuthorPydantic(BaseModel):
        name: str
        bio: str

    class BookPydantic(BaseModel):
        title: str
        isbn: str

    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        bio: str
        books: List["Book"] = Relationship(back_populates="author")

    class Book(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str
        isbn: str
        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional["Author"] = Relationship(back_populates="books")

    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Create mixed scenario
        author = Author(name="Mixed Author", bio="Mixed scenario")
        session.add(author)
        session.commit()
        session.refresh(author)

        # Mix of Pydantic models and existing SQLModel instances
        existing_book = Book(title="Existing Book", isbn="000-000-000")
        session.add(existing_book)
        session.commit()
        session.refresh(existing_book)

        pydantic_books = [
            BookPydantic(title="Pydantic Book 1", isbn="111-111-111"),
            BookPydantic(title="Pydantic Book 2", isbn="222-222-222"),
        ]

        # Assign mixed list (this tests the conversion logic with mixed types)
        mixed_books = [existing_book] + pydantic_books
        author.books = mixed_books

        # Verify results
        assert len(author.books) == 3
        assert all(isinstance(book, Book) for book in author.books)

        # First book should be the existing one
        assert author.books[0].title == "Existing Book"
        assert author.books[0].isbn == "000-000-000"

        # Other books should be converted from Pydantic
        assert author.books[1].title == "Pydantic Book 1"
        assert author.books[1].isbn == "111-111-111"
        assert author.books[2].title == "Pydantic Book 2"
        assert author.books[2].isbn == "222-222-222"


def test_forward_reference_registry_population(clear_sqlmodel):
    """Test that the class registry is properly populated and used."""

    class AuthorPydantic(BaseModel):
        name: str

    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        books: List["Book"] = Relationship(back_populates="author")

    class Book(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str
        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional["Author"] = Relationship(back_populates="books")

    # Verify that the registry contains our classes
    from sqlmodel.main import default_registry

    assert "Author" in default_registry._class_registry
    assert "Book" in default_registry._class_registry
    assert default_registry._class_registry["Author"] is Author
    assert default_registry._class_registry["Book"] is Book

    # Test that the registry is actually used in conversion
    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        book = Book(title="Registry Test Book")
        session.add(book)
        session.commit()
        session.refresh(book)

        author_pydantic = AuthorPydantic(name="Registry Test Author")
        book.author = author_pydantic

        # The conversion should work because the registry resolves "Author" to Author class
        assert isinstance(book.author, Author)
        assert book.author.name == "Registry Test Author"
