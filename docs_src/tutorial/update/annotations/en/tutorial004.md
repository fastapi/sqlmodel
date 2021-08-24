1. Select the hero `Spider-Boy`.

2. Execute the select statement.

    This generates the output:

    ```
    INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age 
    FROM hero 
    WHERE hero.name = ?
    INFO Engine [no key 0.00018s] ('Spider-Boy',)
    ```

3. Get one hero object, the only one that should be there for **Spider-Boy**.

4. Print this hero.

    This generates the output:

    ```
    Hero 1: name='Spider-Boy' secret_name='Pedro Parqueador' age=None id=2
    ```

5. Select another hero.

6. Execute the select statement.

    This generates the output:

    ```
    INFO Engine BEGIN (implicit)
    INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age 
    FROM hero 
    WHERE hero.name = ?
    INFO Engine [no key 0.00020s] ('Captain North America',)
    ```

    !!! tip
        See the `BEGIN` at the top?

        This is SQLAlchemy automatically starting a transaction for us.

        This way, we could revert the last changes (if there were some) if we wanted to, even if the SQL to create them was already sent to the database.

7. Get one hero object for this new query.

    The only one that should be there for **Captain North America**.

8. Print this second hero.

    This generates the output:

    ```
    Hero 2: name='Captain North America' secret_name='Esteban Rogelios' age=93 id=7
    ```

9. Update the age for the first hero.

    Set the value of the attribute `age` to `16`.

    This updates the hero object in memory, but not yet in the database.

10. Update the name of the first hero.

    Now the name of the hero will not be `"Spider-Boy"` but `"Spider-Youngster"`.

    Also, this updates the object in memory, but not yet in the database.

11. Add this first hero to the session.

    This puts it in the temporary space in the **session** before committing it to the database.

    It is not saved yet.

12. Update the name of the second hero.

    Now the hero has a bit more precision in the name. 😜

    This updates the object in memory, but not yet in the database.

13. Update the age of the second hero.

    This updates the object in memory, but not yet in the database.

14. Add the second hero to the session.

    This puts it in the temporary space in the **session** before committing it to the database.

15. Commit all the changes tracked in the session.

    This commits everything in one single batch.

    This generates the output:

    ```
    INFO Engine UPDATE hero SET name=?, age=? WHERE hero.id = ?
    INFO Engine [generated in 0.00028s] (('Spider-Youngster', 16, 2), ('Captain North America Except Canada', 110, 7))
    INFO Engine COMMIT
    ```

    !!! tip
        See how SQLAlchemy (that powers SQLModel) optimizes the SQL to do as much work as possible in a single batch.

        Here it updates both heroes in a single SQL query.

16. Refresh the first hero.

    This generates the output:

    ```
    INFO Engine BEGIN (implicit)
    INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age 
    FROM hero 
    WHERE hero.id = ?
    INFO Engine [generated in 0.00023s] (2,)
    ```

    !!! tip
        Because we just committed a SQL transaction with `COMMIT`, SQLAlchemy will automatically start a new transaction with `BEGIN`.

17. Refresh the second hero.

    This generates the output:

    ```
    INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age 
    FROM hero 
    WHERE hero.id = ?
    INFO Engine [cached since 0.001709s ago] (7,)
    ```

    !!! tip
        SQLAlchemy is still using the previous transaction, so it doesn't have to create a new one.

18. Print the first hero, now udpated.

    This generates the output:

    ```
    Updated hero 1: name='Spider-Youngster' secret_name='Pedro Parqueador' age=16 id=2
    ```

19. Print the second hero, now updated.

    This generates the output:

    ```
    Updated hero 2: name='Captain North America Except Canada' secret_name='Esteban Rogelios' age=110 id=7
    ```

20. Here is the end of the `with` block statement, so the session can execute its terminating code.

    The session will `ROLLBACK` (undo) any possible changes in the last transaction that were not committed.

    This generates the output:

    ```
    INFO Engine ROLLBACK
    ```
