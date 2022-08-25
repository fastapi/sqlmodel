# Self-referential relationships

Oftentimes we need to model a relationship between one entity of some class and another entity (or multiple entities) of that **same** class. This is called a **self-referential** or **recursive** relationship. (The pattern is also sometimes referred to as an **adjacency list**.)

In database terms this means having a table with a foreign key reference to the primary key in the same table.

Say, for example, we want to introduce a `Villain` class. 😈 Every villain can have a **boss**, who also must be a villain. If a villain is the boss to other villains, we want to call those his **minions**.

Let's do this with **SQLModel**. 🤓

## Using SQLAlchemy arguments

We already learned a lot about [Relationship attributes](../tutorial/relationship-attributes/index.md){.internal-link target=_blank} in previous chapters. We know that **SQLModel** is built on top of **SQLAlchemy** and we know that the latter allows defining self-referential relationships (see [their documentation](https://docs.sqlalchemy.org/en/14/orm/self_referential.html){.external-link target=_blank}).

To allow more fine-grained control over it, the `Relationship` constructor allows explicitly passing additional keyword-arguments to the [`sqlalchemy.orm.relationship`](https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship){.external-link target=_blank} constructor that is being called under the hood via the `sa_relationship_kwargs` parameter. This is supposed to be a mapping (e.g. a dictionary) of strings representing the SQLAlchemy **parameter names** to the **values** we want to pass through as arguments.

Since SQLAlchemy relationships provide the [`remote_side`](https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship.params.remote_side){.external-link target=_blank} parameter for just such an occasion, we can leverage that directly to construct the self-referential pattern with minimal code.

```Python hl_lines="12"
# Code above omitted 👆

{!./docs_src/advanced/self_referential/tutorial001.py[ln:6-17]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/advanced/self_referential/tutorial001.py!}
```

</details>

Using the `sa_relationship_kwargs` parameter, we pass the keyword-argument `remote_side='Villain.id'` to the underlying relationship property.

!!! info
    The SQLAlchemy documentation mentions this in passing, but crucially the `remote_side` value _"may be passed as a Python-evaluable string when using Declarative."_

    This allows us to pass the `id` field of the class we are just now defining as the remote side of that relationship.

## Back-populating and self-referencing

Notice that we explicitly defined the relationship attributes we wanted for referring to the `boss` **as well as** the `minions` of a `Villain`.

For our purposes, it is necessary that we also provide the `back_populates` parameter to both relationships as explained in detail in a [dedicated chapter](../tutorial/relationship-attributes/back-populates.md){.internal-link target=_blank}.

In addition, the type annotations were made by enclosing our `Villain` class name in quotes, since we are referencing a class that is not yet fully defined by the time the interpreter reaches those lines. (See the chapter on [type annotation strings](../tutorial/relationship-attributes/type-annotation-strings.md){.internal-link target=_blank} for a detailed explanation.)

Finally, as with regular (i.e. non-self-referential) foreign key relationships, it is up to us to decide, whether it makes sense to allow the field to be **empty** or not. In our example, not every villain must have a boss. (In fact, we would otherwise introduce a circular reference chain, which would not make sense in this context.) Therefore we declare `boss_id: Optional[int]` and `boss: Optional['Villain']`. This is analogous to the `Hero`→`Team` relationship we saw [in an earlier chapter](../tutorial/relationship-attributes/define-relationships-attributes.md#optional-relationship-attributes){.internal-link target=_blank}.

## Creating instances

Now let us see how we can create villains with a boss:

```Python hl_lines="6-7"
# Code above omitted 👆

{!./docs_src/advanced/self_referential/tutorial001.py[ln:30-49]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/advanced/self_referential/tutorial001.py!}
```

</details>

Just as with regular relationships, we can simply pass our boss villain as an argument to the constructor with `boss=thinnus`.

If we only learn that a villain actually had a secret boss after we have already created him, we can just as easily assign him that boss retroactively:

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/advanced/self_referential/tutorial001.py[ln:30-31]!}

        # Previous code here omitted 👈

{!./docs_src/advanced/self_referential/tutorial001.py[ln:51-55]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/advanced/self_referential/tutorial001.py!}
```

</details>

And if we want to add minions to a boss after the fact, this is as easy as adding items to a Python list (because that's all it is 🤓):

```Python hl_lines="11"
# Code above omitted 👆

{!./docs_src/advanced/self_referential/tutorial001.py[ln:30-31]!}

        # Previous code here omitted 👈

{!./docs_src/advanced/self_referential/tutorial001.py[ln:57-68]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/advanced/self_referential/tutorial001.py!}
```

</details>

Since our relationships work both ways, we don't even need to add all our `clone_bot_`s  to the session individually. Instead we can simply add `ultra_bot` once again and commit the changes. We do need to refresh them all individually though, if we want to get their updated attributes.

## Traversing the relationship graph

By setting up our relationships this way, we can easily go back and forth along the graph representing all relationships we have created so far.

For example, we can verify that our `clone_bot_1` has a boss, who has his own boss, and one of that top-boss' minions is `ebonite_mew`:

```Python
top_boss_minions = clone_bot_3.boss.boss.minions
assert any(minion is ebonite_mew for minion in top_boss_minions)  # passes
```

!!! info
    Notice that we can in fact check for **identity** using `is` as opposed to `==` here, since we are dealing with those exact same objects, not just objects that hold the same **data**.
