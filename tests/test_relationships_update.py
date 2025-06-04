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


def test_relationships_update():
    """Test conversion of single Pydantic model to SQLModel with forward reference."""

    class IBookUpdate(BaseModel):
        id: int
        title: str | None = None

    class IAuthorUpdate(BaseModel):
        id: int
        name: str | None = None
        books: list[IBookUpdate] | None = None

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
        book = Book(title="Test Book")
        author = Author(name="Test Author", books=[book])
        session.add(author)
        session.commit()
        session.refresh(author)

        author_id = author.id
        book_id = book.id

    with Session(engine) as session:
        update_data = IAuthorUpdate(
            id=author_id,
            name="Updated Author",
            books=[IBookUpdate(id=book_id, title="Updated Book")],
        )
        updated_author = Author.model_validate(update_data)

        session.add(updated_author)
        session.commit()

        assert updated_author.id == author.id
        assert updated_author.name == "Updated Author"
        assert len(updated_author.books) == 1
        assert updated_author.books[0].id == book.id
        assert updated_author.books[0].title == "Updated Book"
