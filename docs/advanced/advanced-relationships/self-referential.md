# Self-referential relationships

Oftentimes we need to model a relationship between one entity of some class and another entity (or multiple entities) of that **same** class. This is known as a **self-referential** or **recursive** relationship, sometimes also called an **adjacency list**.

In database terms this means having a table with a foreign key reference to the primary key in the same table.

Say, for example, we want to introduce a `Villain` class. 😈 Every villain can have a **boss**, who also must be a villain. If a villain is the boss to other villains, we want to call those his **minions**.

Let's implement this with **SQLModel**. 🤓

## Using SQLAlchemy arguments

We already learned a lot about [Relationship attributes](../../tutorial/relationship-attributes/index.md){.internal-link target=_blank} in previous chapters. We know that **SQLModel** is built on top of **SQLAlchemy**, which supports defining self-referential relationships (see [their documentation](https://docs.sqlalchemy.org/en/20/orm/self_referential.html){.external-link target=_blank}).

To allow more fine-grained control over it, the `Relationship` constructor allows explicitly passing additional keyword-arguments to the [`sqlalchemy.orm.relationship`](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship){.external-link target=_blank} constructor that is being called under the hood via the `sa_relationship_kwargs` parameter. This should be a mapping (e.g. a dictionary) of strings representing the SQLAlchemy **parameter names** to the **values** we want to pass through as arguments.

Since SQLAlchemy relationships provide the [`remote_side`](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.remote_side){.external-link target=_blank} parameter for just such an occasion, we can leverage that directly to construct the self-referential pattern with minimal code.

{* ./docs_src/advanced/self_referential/tutorial001.py ln[6:18] hl[16] *}

Using the `sa_relationship_kwargs` parameter, we pass the keyword argument `remote_side='Villain.id'` to the underlying relationship property.

/// info

The `remote_side` parameter accepts a Python-evaluable string when using Declarative. This allows us to reference `Villain.id` even though the class is still being defined.

Alternatively, you can use a callable:

```py
sa_relationship_kwargs={"remote_side": lambda : Villain.id}
```

///

## Back-populating and self-referencing

Notice that we explicitly defined the relationship attributes we wanted for referring to the `boss` **as well as** the `minions` of a `Villain`.

For our purposes, it is necessary that we also provide the `back_populates` parameter to both relationships as explained in detail in a [dedicated chapter](../../tutorial/relationship-attributes/back-populates.md){.internal-link target=_blank}.

In addition, the type annotations were made by enclosing our `Villain` class name in quotes, since we are referencing a class that is not yet fully defined by the time the interpreter reaches those lines. See the chapter on [type annotation strings](../../tutorial/relationship-attributes/type-annotation-strings.md){.internal-link target=_blank} for a detailed explanation.

Finally, as with regular (i.e. non-self-referential) foreign key relationships, it is up to us to decide whether it makes sense to allow the field to be **empty** or not. In our example, not every villain must have a boss (in fact, we would otherwise introduce a circular reference chain, which would not make sense in this context). Therefore we declare `boss_id: Optional[int]` and `boss: Optional['Villain']`. This is analogous to the `Hero`→`Team` relationship we saw [in an earlier chapter](../../tutorial/relationship-attributes/define-relationships-attributes.md#relationship-attributes-or-none){.internal-link target=_blank}.

## Creating instances

Now let's see how we can create villains with a boss:

{* ./docs_src/advanced/self_referential/tutorial001.py ln[31:50] hl[34:35] *}

Just as with regular relationships, we can simply pass our boss villain as an argument to the constructor using `boss=thinnus`.

If we later learn that a villain actually had a secret boss after we've already created him, we can just as easily assign that boss retroactively:

{* ./docs_src/advanced/self_referential/tutorial001.py ln[31:32,52:56] hl[52] *}

And if we want to add minions to a boss afterward, it's as easy as adding items to a Python list (because that's all it is 🤓):

{* ./docs_src/advanced/self_referential/tutorial001.py ln[31:32,58:69] hl[61] *}

Since our relationships work both ways, we don't even need to add all our `clone_bot_`s to the session individually. Instead, we can simply add ultra_bot again and commit the changes. We do need to refresh them individually, though, if we want to access their updated attributes.

## Traversing the relationship graph

By setting up our relationships this way, we can easily go back and forth along the graph representing all the relationships we've created so far.

For example, we can verify that our `clone_bot_1` has a boss, who has his own boss, and that one of that top boss's minions is `ebonite_mew`:

```Python
top_boss_minions = clone_bot_3.boss.boss.minions
assert any(minion is ebonite_mew for minion in top_boss_minions)  # passes
```

/// info

Notice that we can, in fact, check for **identity** using `is` instead of `==` here, since we are dealing with the exact same objects, not just objects containing the same **data**.

///
