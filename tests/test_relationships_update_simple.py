"""
Simple test for relationship updates.
"""

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine
from pydantic import BaseModel


def test_simple_relationship_update(clear_sqlmodel):
    """Simple test for relationship updates with forward references."""

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
        assert isinstance(book.author, Author)
        assert book.author.name == "Test Author"
        assert book.author.bio == "Test Bio"


def test_list_relationship_update(clear_sqlmodel):
    """Test updating list relationships with Pydantic models."""

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
