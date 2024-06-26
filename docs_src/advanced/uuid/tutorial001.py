import uuid
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


class Item(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: Optional[str] = None


def create_sample_data_and_return_id(engine) -> uuid.UUID:
    with Session(engine) as session:
        item = Item(title="Example Item", description="An example item")
        session.add(item)
        session.commit()
        session.refresh(item)
        return item.id


def get_item_by_uuid(engine, item_id: uuid.UUID):
    with Session(engine) as session:
        item = session.exec(select(Item).where(Item.id == item_id)).one_or_none()
        return item


def delete_item_by_uuid(engine, item_id: uuid.UUID):
    with Session(engine) as session:
        item = session.exec(select(Item).where(Item.id == item_id)).one_or_none()
        session.delete(item)
        session.commit()
        print("Item deleted successfully.")


def main() -> None:
    engine = create_engine("sqlite:///database.db", echo=True)
    SQLModel.metadata.create_all(engine)

    item_id = create_sample_data_and_return_id(engine)

    item = get_item_by_uuid(engine, item_id)
    if item:
        print(f"Found item: {item.title}")

    delete_item_by_uuid(engine, item_id)


if __name__ == "__main__":
    main()
