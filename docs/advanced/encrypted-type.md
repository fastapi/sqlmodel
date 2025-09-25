# Encrypted Type

Sometimes you need to store sensitive data like secrets, tokens, or personal information in your database in an encrypted format.

You can use the `EncryptedType` from the `sqlalchemy-utils` package to achieve this with SQLModel.

## A Model with an Encrypted Field

You can define a field with `EncryptedType` in your SQLModel model using `sa_column`:

{* ./docs_src/advanced/encrypted_type/tutorial001.py *}

In this example, the `secret_name` field will be automatically encrypted when you save a `Hero` object to the database and decrypted when you access it.

/// tip
For this to work, you need to have `sqlalchemy-utils` and `cryptography` installed.
///

For a more detailed walkthrough, including how to create and query data with encrypted fields, check out the [Encrypting Data Tutorial](../tutorial/encrypted-type.md).