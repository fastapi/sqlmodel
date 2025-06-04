#!/usr/bin/env python3
"""
Test script to validate the Pydantic to table model conversion functionality.
"""

from sqlmodel import Field, SQLModel, Relationship, create_engine, Session


def test_single_relationship(clear_sqlmodel):
    """Test single relationship conversion."""

    class User(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        profile_id: int = Field(default=None, foreign_key="profile.id")
        profile: "Profile" = Relationship()

    class Profile(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        bio: str

    class IProfileCreate(SQLModel):
        bio: str

    class IUserCreate(SQLModel):
        name: str
        profile: IProfileCreate

    # Create data using Pydantic models
    profile_data = IProfileCreate(bio="Software Engineer")
    user_data = IUserCreate(name="John Doe", profile=profile_data)

    # Convert to table model - this should work without errors
    user = User.model_validate(user_data)

    print("✅ Single relationship conversion test passed")
    print(f"User: {user.name}")
    print(f"Profile: {user.profile.bio}")
    print(f"Profile type: {type(user.profile)}")
    assert isinstance(user.profile, Profile)


def test_list_relationship(clear_sqlmodel):
    """Test list relationship conversion."""

    class Book(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        title: str
        author_id: int = Field(default=None, foreign_key="author.id")
        author: "Author" = Relationship(back_populates="books")

    class IBookCreate(SQLModel):
        title: str

    class Author(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        books: list[Book] = Relationship(back_populates="author")

    class IAuthorCreate(SQLModel):
        name: str
        books: list[IBookCreate] = []

    # Create data using Pydantic models
    book1 = IBookCreate(title="Book One")
    book2 = IBookCreate(title="Book Two")
    author_data = IAuthorCreate(name="Author Name", books=[book1, book2])

    # Convert to table model - this should work without errors
    author = Author.model_validate(author_data)

    print("✅ List relationship conversion test passed")
    print(f"Author: {author.name}")
    print(f"Books: {[book.title for book in author.books]}")
    print(f"Book types: {[type(book) for book in author.books]}")
    assert all(isinstance(book, Book) for book in author.books)


def test_mixed_assignment(clear_sqlmodel):
    """Test mixed assignment with both Pydantic and table models."""

    class Tag(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        post_id: int = Field(default=None, foreign_key="post.id")
        post: "Post" = Relationship(back_populates="tags")

    class ITagCreate(SQLModel):
        name: str

    class Post(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        title: str
        tags: list[Tag] = Relationship(back_populates="post")

    # Create some existing table models
    existing_tag = Tag(name="Existing Tag")

    # Create some Pydantic models
    pydantic_tag = ITagCreate(name="Pydantic Tag")

    # Create post with mixed tag types
    post = Post(title="Test Post")
    post.tags = [existing_tag, pydantic_tag]  # This should trigger conversion

    print("✅ Mixed assignment test passed")
    print(f"Post: {post.title}")
    print(f"Tags: {[tag.name for tag in post.tags]}")
    print(f"Tag types: {[type(tag) for tag in post.tags]}")
    assert all(isinstance(tag, Tag) for tag in post.tags)


def test_database_integration(clear_sqlmodel):
    """Test that converted models work with database operations."""

    class Category(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        item_id: int = Field(default=None, foreign_key="item.id")
        item: "Item" = Relationship(back_populates="categories")

    class ICategoryCreate(SQLModel):
        name: str

    class Item(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        categories: list[Category] = Relationship(back_populates="item")

    class IItemCreate(SQLModel):
        name: str
        categories: list[ICategoryCreate] = []

    # Create data using Pydantic models
    cat1 = ICategoryCreate(name="Electronics")
    cat2 = ICategoryCreate(name="Gadgets")
    item_data = IItemCreate(name="Smartphone", categories=[cat1, cat2])

    # Convert to table model
    item = Item.model_validate(item_data)

    # Test database operations
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)

        # Verify data persisted correctly
        assert item.id is not None
        assert len(item.categories) == 2
        assert all(cat.id is not None for cat in item.categories)
        assert all(cat.item_id == item.id for cat in item.categories)

    print("✅ Database integration test passed")
    print(f"Item: {item.name} (ID: {item.id})")
    print(f"Categories: {[(cat.name, cat.id) for cat in item.categories]}")
