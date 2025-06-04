"""
Test relationship updates with forward references and Pydantic to SQLModel conversion.
"""

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine
from pydantic import BaseModel


def test_relationships_update_with_forward_references(clear_sqlmodel):
    """Test updating relationships with forward reference conversion."""

    # Pydantic models (non-table models)
    class AuthorPydantic(BaseModel):
        name: str
        bio: str

    class BookPydantic(BaseModel):
        title: str
        isbn: str
        pages: int

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
        author: Optional["Author"] = Relationship(back_populates="books")

    # Create engine and tables
    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Create initial data using table models
        author = Author(name="Initial Author", bio="Initial Bio")
        session.add(author)
        session.commit()
        session.refresh(author)

        book1 = Book(title="Initial Book 1", isbn="111", pages=100, author_id=author.id)
        book2 = Book(title="Initial Book 2", isbn="222", pages=200, author_id=author.id)
        session.add_all([book1, book2])
        session.commit()
        session.refresh(book1)
        session.refresh(book2)

        # Test 1: Update single relationship with Pydantic model (forward reference)
        author_pydantic = AuthorPydantic(name="Updated Author", bio="Updated Bio")

        # This should trigger the forward reference conversion
        book1.author = author_pydantic

        # The author should be converted from Pydantic to table model
        assert isinstance(book1.author, Author)
        assert book1.author.name == "Updated Author"
        assert book1.author.bio == "Updated Bio"

        # Test 2: Update list relationship with Pydantic models (forward reference)
        books_pydantic = [
            BookPydantic(title="New Book 1", isbn="333", pages=300),
            BookPydantic(title="New Book 2", isbn="444", pages=400),
            BookPydantic(title="New Book 3", isbn="555", pages=500),
        ]

        # This should trigger the forward reference conversion for a list
        author.books = books_pydantic

        # The books should be converted from Pydantic to table models
        assert isinstance(author.books, list)
        assert len(author.books) == 3

        for i, book in enumerate(author.books):
            assert isinstance(book, Book)
            assert book.title == books_pydantic[i].title
            assert book.isbn == books_pydantic[i].isbn
            assert book.pages == books_pydantic[i].pages


def test_relationships_update_edge_cases(clear_sqlmodel):
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


def test_relationships_update_performance(clear_sqlmodel):
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

        # Test with a larger number of items to ensure performance is reasonable
        large_book_list = [
            BookPydantic(title=f"Book {i}", isbn=f"{i:06d}")
            for i in range(50)  # Reduced for faster testing
        ]

        # This should complete in reasonable time
        import time

        start_time = time.time()

        author.books = large_book_list

        end_time = time.time()
        conversion_time = end_time - start_time

        # Verify all items were converted correctly
        assert len(author.books) == 50
        assert all(isinstance(book, Book) for book in author.books)
        assert all(book.title == f"Book {i}" for i, book in enumerate(author.books))

        # Performance should be reasonable (less than 1 second for 50 items)
        assert (
            conversion_time < 1.0
        ), f"Conversion took too long: {conversion_time:.3f}s"
