"""
Test relationship updates with forward references and Pydantic to SQLModel conversion.
This test specifically verifies that the forward reference resolution fix works
when updating relationships with Pydantic models.
"""

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine
from pydantic import BaseModel


def test_single_relationship_update_with_forward_reference(clear_sqlmodel):
    """Test updating a single relationship with forward reference conversion."""

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
        book = Book(title="Test Book")
        session.add(book)
        session.commit()
        session.refresh(book)

        # Test updating with Pydantic model (should convert via forward reference)
        author_pydantic = AuthorPydantic(name="Test Author", bio="Test Bio")
        book.author = author_pydantic

        # Should be converted to Author instance
        assert isinstance(
            book.author, Author
        ), f"Expected Author, got {type(book.author)}"
        assert book.author.name == "Test Author"
        assert book.author.bio == "Test Bio"


def test_list_relationship_update_with_forward_reference(clear_sqlmodel):
    """Test updating a list relationship with forward reference conversion."""

    class BookPydantic(BaseModel):
        title: str
        isbn: str

    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
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
        author = Author(name="Test Author")
        session.add(author)
        session.commit()
        session.refresh(author)

        # Test updating with list of Pydantic models
        books_pydantic = [
            BookPydantic(title="Book 1", isbn="111"),
            BookPydantic(title="Book 2", isbn="222"),
        ]

        author.books = books_pydantic

        # Should be converted to Book instances
        assert isinstance(author.books, list)
        assert len(author.books) == 2
        assert all(isinstance(book, Book) for book in author.books)
        assert author.books[0].title == "Book 1"
        assert author.books[1].title == "Book 2"
        assert author.books[0].isbn == "111"
        assert author.books[1].isbn == "222"


def test_relationship_update_edge_cases(clear_sqlmodel):
    """Test edge cases for relationship updates."""

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
        book = Book(title="Test Book")
        session.add(book)
        session.commit()
        session.refresh(book)

        # Test 1: Update with None (should work)
        book.author = None
        assert book.author is None

        # Test 2: Update with already correct type (should not convert)
        existing_author = Author(name="Existing", bio="Existing Bio")
        session.add(existing_author)
        session.commit()
        session.refresh(existing_author)

        book.author = existing_author
        assert book.author is existing_author
        assert isinstance(book.author, Author)

        # Test 3: Update with Pydantic model (should convert)
        author_pydantic = AuthorPydantic(name="Pydantic Author", bio="Pydantic Bio")
        book.author = author_pydantic

        assert isinstance(book.author, Author)
        assert book.author.name == "Pydantic Author"
        assert book.author.bio == "Pydantic Bio"


def test_mixed_relationship_updates(clear_sqlmodel):
    """Test mixed updates with existing table models and new Pydantic models."""

    class BookPydantic(BaseModel):
        title: str
        isbn: str

    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
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
        author = Author(name="Test Author")
        session.add(author)
        session.commit()
        session.refresh(author)

        # Create an existing book
        existing_book = Book(
            title="Existing Book", isbn="existing", author_id=author.id
        )
        session.add(existing_book)
        session.commit()
        session.refresh(existing_book)

        # Create new Pydantic book
        new_book_pydantic = BookPydantic(title="New Pydantic Book", isbn="new")

        # Mix existing table model with new Pydantic model
        author.books = [existing_book, new_book_pydantic]

        assert len(author.books) == 2
        assert isinstance(author.books[0], Book)
        assert isinstance(author.books[1], Book)
        assert author.books[0].title == "Existing Book"
        assert author.books[1].title == "New Pydantic Book"
        assert author.books[1].isbn == "new"


def test_relationship_update_performance(clear_sqlmodel):
    """Test performance characteristics of relationship updates."""

    class BookPydantic(BaseModel):
        title: str
        isbn: str

    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
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
        author = Author(name="Performance Test Author")
        session.add(author)
        session.commit()
        session.refresh(author)

        # Test with a reasonable number of items to ensure performance is good
        book_list = [
            BookPydantic(title=f"Book {i}", isbn=f"{i:06d}")
            for i in range(25)  # Reasonable size for CI testing
        ]

        # This should complete in reasonable time
        import time

        start_time = time.time()

        author.books = book_list

        end_time = time.time()
        conversion_time = end_time - start_time

        # Verify all items were converted correctly
        assert len(author.books) == 25
        assert all(isinstance(book, Book) for book in author.books)
        assert all(book.title == f"Book {i}" for i, book in enumerate(author.books))

        # Performance should be reasonable (less than 1 second for 25 items)
        assert (
            conversion_time < 1.0
        ), f"Conversion took too long: {conversion_time:.3f}s"


def test_relationship_update_error_handling(clear_sqlmodel):
    """Test error handling during relationship updates."""

    class InvalidPydantic(BaseModel):
        name: str
        # Missing required field that Book expects

    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        books: List["Book"] = Relationship(back_populates="author")

    class Book(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str
        isbn: str  # Required field
        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        author: Optional["Author"] = Relationship(back_populates="books")

    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        author = Author(name="Error Test Author")
        session.add(author)
        session.commit()
        session.refresh(author)

        # Test with incompatible Pydantic model
        # The conversion should gracefully handle this
        invalid_item = InvalidPydantic(name="Invalid")

        # This should not raise an exception, but should return the original item
        # when conversion is not possible
        author.books = [invalid_item]

        # The invalid item should remain as-is since conversion failed
        assert len(author.books) == 1
        assert isinstance(author.books[0], InvalidPydantic)
        assert author.books[0].name == "Invalid"


def test_nested_forward_references(clear_sqlmodel):
    """Test nested relationships with forward references."""

    class CategoryPydantic(BaseModel):
        name: str
        description: str

    class BookPydantic(BaseModel):
        title: str
        isbn: str

    class Category(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        description: str
        books: List["Book"] = Relationship(back_populates="category")

    class Author(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        books: List["Book"] = Relationship(back_populates="author")

    class Book(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str
        isbn: str
        author_id: Optional[int] = Field(default=None, foreign_key="author.id")
        category_id: Optional[int] = Field(default=None, foreign_key="category.id")
        author: Optional["Author"] = Relationship(back_populates="books")
        category: Optional["Category"] = Relationship(back_populates="books")

    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Test multiple forward reference conversions
        category_pydantic = CategoryPydantic(
            name="Fiction", description="Fiction books"
        )
        book_pydantic = BookPydantic(title="Test Book", isbn="123")

        category = Category(name="Test Category", description="Test")
        session.add(category)
        session.commit()
        session.refresh(category)

        # Update category with pydantic model
        book = Book(title="Initial Title", isbn="000")
        session.add(book)
        session.commit()
        session.refresh(book)

        book.category = category_pydantic

        # Verify conversion worked
        assert isinstance(book.category, Category)
        assert book.category.name == "Fiction"
        assert book.category.description == "Fiction books"

        # Update list relationship
        category.books = [book_pydantic]

        assert len(category.books) == 1
        assert isinstance(category.books[0], Book)
        assert category.books[0].title == "Test Book"
        assert category.books[0].isbn == "123"
