# Remove Relationships

Now let's say that **Spider-Boy** tells **Rusty-Man** something like:

> I don't feel so good Mr. Sharp

And then for some reason needs to leave the **Preventers** for some years. 😭

We can remove the relationship by setting it to `None`, the same as with the `team_id`, it also works with the new relationship attribute `.team`:

```Python hl_lines="9"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/read_relationships/tutorial002.py[ln:105-116]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/relationship_attributes/read_relationships/tutorial002.py!}
```

</details>

And of course, we should remember to add this `update_heroes()` function to `main()` so that it runs when we call this program from the command line:

```Python hl_lines="7"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/read_relationships/tutorial002.py[ln:119-123]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/relationship_attributes/read_relationships/tutorial002.py!}
```

</details>

## Recap

This chapter was too short for a recap, wasn't it? 🤔

Anyway, **relationship attributes** make it easy and intuitive to work with relationships stored in the database. 🎉
