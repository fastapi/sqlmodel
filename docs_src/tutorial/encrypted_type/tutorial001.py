# Import necessary modules
from typing import Optional

import sqlalchemy
from sqlalchemy import Column, text
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Define a secret key for encryption.
# In a real application, this key should be stored securely and not hardcoded.
# For example, you could load it from an environment variable or a secret management service.
ENCRYPTION_KEY = "a-super-secret-key"


# Define the Character model
# This model represents a table named 'character' in the database.
class Character(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    # The secret_name field is encrypted in the database.
    # We use EncryptedType from sqlalchemy-utils for this.
    secret_name: str = Field(
        sa_column=Column(
            EncryptedType(
                sqlalchemy.Unicode,
                ENCRYPTION_KEY,
                AesEngine,
                "pkcs5",
            )
        )
    )
    age: Optional[int] = None


# Define the database URL and create the engine
# We are using a SQLite database for this example.
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)


# This function creates the database and the Character table.
# It first drops the existing table to ensure a clean state for the example.
def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


# This function creates some sample characters and adds them to the database.
def create_characters():
    # Create instances of the Character model
    roy_kent = Character(name="Roy Kent", secret_name="The Special One", age=40)
    jamie_tartt = Character(name="Jamie Tartt", secret_name="Baby Shark", age=25)
    dani_rojas = Character(name="Dani Rojas", secret_name="Fútbol is Life", age=23)

    # Use a session to interact with the database
    with Session(engine) as session:
        # Add the characters to the session
        session.add(roy_kent)
        session.add(jamie_tartt)
        session.add(dani_rojas)

        # Commit the changes to the database
        session.commit()


# This function demonstrates how the encryption works.
def demonstrate_encryption():
    with Session(engine) as session:
        # Query the database directly to see the encrypted data
        # We use a raw SQL query for this.
        statement = text("SELECT name, secret_name FROM character")
        results = session.exec(statement).all()
        print("Data as stored in the database:")
        for row in results:
            # The secret_name will be an encrypted string.
            print(f"Name: {row.name}, Encrypted Secret Name: {row.secret_name}")

        # Query through SQLModel to see the decrypted data
        # SQLModel will automatically decrypt the secret_name.
        statement = select(Character)
        characters = session.exec(statement).all()
        print("\nData as accessed through SQLModel:")
        for character in characters:
            # The secret_name will be the original, decrypted string.
            print(
                f"Name: {character.name}, Decrypted Secret Name: {character.secret_name}"
            )


# The main function that runs the example.
def main():
    print("Creating database and tables...")
    create_db_and_tables()
    print("Creating characters...")
    create_characters()
    print("\nDemonstrating encryption...")
    demonstrate_encryption()


# Run the main function when the script is executed.
if __name__ == "__main__":
    main()
