from sqlmodel import Field, SQLModel, Relationship, create_engine, Session


def test_pydantic_to_table_conversion_single_relationship(clear_sqlmodel):
    """Test automatic conversion of Pydantic objects to table models for single relationships."""

    class Profile(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        bio: str

    class User(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        profile_id: int = Field(default=None, foreign_key="profile.id")
        profile: Profile = Relationship()

    class IProfileCreate(SQLModel):
        bio: str

    class IUserCreate(SQLModel):
        name: str
        profile: IProfileCreate

    # Create data using Pydantic models
    profile_data = IProfileCreate(bio="Software Engineer")
    user_data = IUserCreate(name="John Doe", profile=profile_data)

    # Convert to table model - this should automatically convert the profile
    user = User.model_validate(user_data)

    assert user.name == "John Doe"
    assert isinstance(user.profile, Profile)
    assert user.profile.bio == "Software Engineer"


def test_pydantic_to_table_conversion_list_relationship(clear_sqlmodel):
    """Test automatic conversion of Pydantic objects to table models for list relationships."""

    class Book(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        title: str
        author_id: int = Field(default=None, foreign_key="author.id")
        author: "Author" = Relationship(back_populates="books")

    class Author(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        books: list[Book] = Relationship(back_populates="author")

    class IBookCreate(SQLModel):
        title: str

    class IAuthorCreate(SQLModel):
        name: str
        books: list[IBookCreate] = []

    # Create data using Pydantic models
    book1 = IBookCreate(title="Book One")
    book2 = IBookCreate(title="Book Two")
    author_data = IAuthorCreate(name="Author Name", books=[book1, book2])

    # Convert to table model - this should automatically convert the books
    author = Author.model_validate(author_data)

    assert author.name == "Author Name"
    assert len(author.books) == 2
    assert all(isinstance(book, Book) for book in author.books)
    assert author.books[0].title == "Book One"
    assert author.books[1].title == "Book Two"


def test_pydantic_to_table_conversion_mixed_assignment(clear_sqlmodel):
    """Test assignment with mixed Pydantic and table model objects."""

    class Tag(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        post_id: int = Field(default=None, foreign_key="post.id")
        post: "Post" = Relationship(back_populates="tags")

    class Post(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        title: str
        tags: list[Tag] = Relationship(back_populates="post")

    class ITagCreate(SQLModel):
        name: str

    # Create mixed list of existing table models and Pydantic models
    existing_tag = Tag(name="Existing Tag")
    pydantic_tag = ITagCreate(name="Pydantic Tag")

    # Create post and assign mixed tags - should convert Pydantic objects
    post = Post(title="Test Post")
    post.tags = [existing_tag, pydantic_tag]

    assert post.title == "Test Post"
    assert len(post.tags) == 2
    assert all(isinstance(tag, Tag) for tag in post.tags)
    assert post.tags[0].name == "Existing Tag"
    assert post.tags[1].name == "Pydantic Tag"


def test_pydantic_to_table_conversion_with_database(clear_sqlmodel):
    """Test that converted models work correctly with database operations."""

    class Category(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        item_id: int = Field(default=None, foreign_key="item.id")
        item: "Item" = Relationship(back_populates="categories")

    class Item(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        categories: list[Category] = Relationship(back_populates="item")

    class ICategoryCreate(SQLModel):
        name: str

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
        assert item.categories[0].name == "Electronics"
        assert item.categories[1].name == "Gadgets"


def test_no_conversion_when_not_needed(clear_sqlmodel):
    """Test that no conversion happens when objects are already table models."""

    class ProductItem(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        category_id: int = Field(default=None, foreign_key="productcategory.id")
        category: "ProductCategory" = Relationship()

    class ProductCategory(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str

    # Create table model directly
    category = ProductCategory(name="Electronics")
    product = ProductItem(name="Phone", category=category)

    # Verify no conversion occurred (same object)
    assert product.category is category
    assert isinstance(product.category, ProductCategory)


def test_no_conversion_for_none_values(clear_sqlmodel):
    """Test that None values are not converted."""

    class UserAccount(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        profile_id: int = Field(default=None, foreign_key="userprofile.id")
        profile: "UserProfile" = Relationship()

    class UserProfile(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        bio: str

    # Create user with no profile
    user = UserAccount(name="John", profile=None)

    assert user.name == "John"
    assert user.profile is None
