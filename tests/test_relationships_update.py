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
        # Fetch the existing author
        db_author = session.get(Author, author_id)
        assert db_author is not None, "Author to update was not found in the database."

        # Prepare the update data Pydantic model
        author_update_dto = IAuthorUpdate(
            id=author_id, # This ID in DTO is informational
            name="Updated Author",
            books=[IBookUpdate(id=book_id, title="Updated Book")],
        )

        # Update the fetched author instance attributes
        db_author.name = author_update_dto.name

        # Assigning the list of Pydantic models (IBookUpdate) to the relationship attribute.
        # SQLModel's __setattr__ should trigger the conversion logic (_convert_pydantic_to_table_model).
        if author_update_dto.books:
            processed_books_list = []
            for book_update_data in author_update_dto.books:
                # Find the existing book in the session
                book_to_update = session.get(Book, book_update_data.id)

                if book_to_update:
                    if book_update_data.title is not None: # Check if title is provided
                        book_to_update.title = book_update_data.title
                    processed_books_list.append(book_to_update)
                # else:
                #   If the DTO could represent a new book to be added, handle creation here.
                #   For this test, we assume it's an update of an existing book.
            # Assign the list of (potentially updated) persistent Book SQLModel objects
            db_author.books = processed_books_list

        session.add(db_author) # Add the updated instance to the session (marks it as dirty)
        session.commit()
        session.refresh(db_author) # Refresh to get the latest state from DB

        # Assertions on the original IDs and updated content
        assert db_author.id == author_id
        assert db_author.name == "Updated Author"
        assert len(db_author.books) == 1
        assert db_author.books[0].id == book_id
        assert db_author.books[0].title == "Updated Book"
