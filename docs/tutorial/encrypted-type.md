# Encrypting Data

In this tutorial, you'll learn how to encrypt data before storing it in your database using SQLModel and `sqlalchemy-utils`.

## The Scenario

Let's imagine we're building an application to store information about characters from our favorite TV show, Ted Lasso. We want to store their names, secret names (which should be encrypted), and their ages.

## The Code

Here's the complete code to achieve this:

{* ./docs_src/tutorial/encrypted_type/tutorial001.py *}

### Understanding the Code

Let's break down the key parts of the code:

1.  **`EncryptedType`**: We use `EncryptedType` from `sqlalchemy-utils` as a `sa_column` for the `secret_name` field. This tells SQLModel to use this special type for the column in the database.

2.  **Encryption Key**: We provide an encryption key to `EncryptedType`. In a real-world application, you should **never** hardcode the key like this. Instead, you should load it from a secure source like a secret manager or an environment variable.

3.  **`demonstrate_encryption` function**: This function shows the power of `EncryptedType`.
    *   First, it queries the database directly using raw SQL. When we print the `secret_name` from this query, you'll see the encrypted string, not the original secret name.
    *   Then, it queries the database using SQLModel. When we access the `secret_name` attribute of the `Character` objects, `EncryptedType` automatically decrypts the data for us, so we get the original, readable secret names.

## How to Test

To run this example, first create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Then, install the required packages from the `requirements.txt` file:

```bash
pip install -r docs_src/tutorial/encrypted_type/requirements.txt
```

Then, you can run the python script:

```bash
python docs_src/tutorial/encrypted_type/tutorial001.py
```

## Running the Code

When you run the code, you'll see the following output:

```console
Creating database and tables...
Creating characters...

Demonstrating encryption...
Data as stored in the database:
Name: Roy Kent, Encrypted Secret Name: b'5dBrkurIL+fEin+1eUBc0A=='
Name: Jamie Tartt, Encrypted Secret Name: b'CDLkQWx5ezXn+U4kRlVFyQ=='
Name: Dani Rojas, Encrypted Secret Name: b'SqSjH+biJttbs9zH+DBw8A=='

Data as accessed through SQLModel:
Name: Roy Kent, Decrypted Secret Name: The Special One
Name: Jamie Tartt, Decrypted Secret Name: Baby Shark
Name: Dani Rojas, Decrypted Secret Name: Fútbol is Life
```

As you can see, `EncryptedType` handles the encryption and decryption for you automatically, making it easy to store sensitive data securely.
