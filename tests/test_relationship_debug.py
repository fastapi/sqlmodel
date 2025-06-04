"""
Test relationship updates without fixture to debug collection issues.
"""

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine
from pydantic import BaseModel


def test_relationship_update_basic():
    """Basic test for relationship updates with forward references."""

    # Clear any existing metadata
    SQLModel.metadata.clear()

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

    # Clean up
    SQLModel.metadata.clear()
