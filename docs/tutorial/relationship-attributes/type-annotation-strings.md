## About the String in `List["Hero"]`

In the first Relationship attribute, we declare it with `List["Hero"]`, putting the `Hero` in quotes instead of just normally there:

//// tab | Python 3.10+

```Python hl_lines="9"
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001_py310.py[ln:1-19]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="11"
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001_py39.py[ln:1-21]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="11"
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001.py[ln:1-21]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001.py!}
```

////

///

What's that about? Can't we just write it normally as `List[Hero]`?

By that point, in that line in the code, the Python interpreter **doesn't know of any class `Hero`**, and if we put it just there, it would try to find it unsuccessfully, and then fail. 😭

But by putting it in quotes, in a string, the interpreter sees it as just a string with the text `"Hero"` inside.

But the editor and other tools can see that **the string is actually a type annotation inside**, and provide all the autocompletion, type checks, etc. 🎉

And of course, **SQLModel** can also understand it in the string correctly. ✨

That is actually part of Python, it's the current official solution to handle it.

/// info

There's a lot of work going on in Python itself to make that simpler and more intuitive, and find ways to make it possible to not wrap the class in a string.

///
