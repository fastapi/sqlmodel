from sqlmodel import Field, Relationship, Session, SQLModel, create_engine


def test_relationships_set_pydantic():
    class Book(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        title: str
        author_id: int = Field(foreign_key="author.id")
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

    book1 = IBookCreate(title="Book One")
    book2 = IBookCreate(title="Book Two")
    book3 = IBookCreate(title="Book Three")

    author_data = IAuthorCreate(name="Author Name", books=[book1, book2, book3])

    author = Author.model_validate(author_data)

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(author)
        session.commit()
        session.refresh(author)
        assert author.id is not None
        assert len(author.books) == 3
        assert author.books[0].title == "Book One"
        assert author.books[1].title == "Book Two"
        assert author.books[2].title == "Book Three"
        assert author.books[0].author_id == author.id
        assert author.books[1].author_id == author.id
        assert author.books[2].author_id == author.id
        assert author.books[0].id is not None
        assert author.books[1].id is not None
        assert author.books[2].id is not None


def test_relationships_set_dict():
    class Book(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        title: str
        author_id: int = Field(foreign_key="author.id")
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

    book1 = IBookCreate(title="Book One")
    book2 = IBookCreate(title="Book Two")
    book3 = IBookCreate(title="Book Three")

    author_data = IAuthorCreate(name="Author Name", books=[book1, book2, book3])

    author = Author.model_validate(author_data.model_dump(exclude={"id"}))

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(author)
        session.commit()
        session.refresh(author)
        assert author.id is not None
        assert len(author.books) == 3
        assert author.books[0].title == "Book One"
        assert author.books[1].title == "Book Two"
        assert author.books[2].title == "Book Three"
        assert author.books[0].author_id == author.id
        assert author.books[1].author_id == author.id
        assert author.books[2].author_id == author.id
        assert author.books[0].id is not None
        assert author.books[1].id is not None
        assert author.books[2].id is not None
