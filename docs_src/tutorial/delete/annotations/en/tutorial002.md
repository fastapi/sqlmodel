1. Select the hero we will delete.

2. Execute the query with the select statement object.

    This generates the output:

    ```
    INFO Engine BEGIN (implicit)
    INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age 
    FROM hero 
    WHERE hero.name = ?
    INFO Engine [no key 0.00011s] ('Spider-Youngster',)
    ```

3. Get one hero object, expecting exactly one.

    !!! tip
        This ensures there's no more than one, and that there's exactly one, not `None`.

        This would never return `None`, instead it would raise an exception.

4. Print the hero object.

    This generates the output:

    ```
    Hero:  name='Spider-Youngster' secret_name='Pedro Parqueador' age=16 id=2
    ```

5. Delete the hero from the **session**.

    This marks the hero as deleted from the session, but it will not be removed from the database until we **commit** the changes.

6. Commit the session.

    This saves the changes in the session, including deleting this row.

    It generates the output:

    ```
    INFO Engine DELETE FROM hero WHERE hero.id = ?
    INFO Engine [generated in 0.00020s] (2,)
    INFO Engine COMMIT
    ```

7. Print the deleted hero object.

    The hero is deleted in the database. And is marked as deleted in the session.

    But we still have the object in memory with its data, so we can use it to print it.

    This generates the output:

    ```
    Deleted hero: name='Spider-Youngster' secret_name='Pedro Parqueador' age=16 id=2
    ```

8. Select the same hero again.

    We'll do this to confirm if the hero is really deleted.

9. Execute the select statement.

    This generates the output:

    ```
    INFO Engine BEGIN (implicit)
    INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age 
    FROM hero 
    WHERE hero.name = ?
    INFO Engine [no key 0.00013s] ('Spider-Youngster',)
    ```

10. Get the "first" item from the `results`.

    If no items were found, this will return `None`, which is what we expect.

11. Check if the first item from the results is `None`.

12. If this first item is indeed `None`, it means that it was correctly deleted from the database.

    Now we can print a message to confirm.

    This generates the output:

    ```
    There's no hero named Spider-Youngster
    ```

13. This is the end of the `with` block, here the **session** executes its closing code.

    This generates the output:

    ```
    INFO Engine ROLLBACK
    ```
