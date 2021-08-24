1. Create the `hero_1`.

    **Doesn't generate any output**.

2. Create the `hero_2`.

    **Doesn't generate any output**.

3. Create the `hero_3`.

    **Doesn't generate any output**.

4. Print the line `"Before interacting with the database"`.

    Generates the output:

    ```
    Before interacting with the database
    ```

5. Print the `hero_1` before interacting with the database.

    Generates the output:

    ```
    Hero 1: id=None name='Deadpond' secret_name='Dive Wilson' age=None
    ```

6. Print the `hero_2` before interacting with the database.

    Generates the output:

    ```
    Hero 2: id=None name='Spider-Boy' secret_name='Pedro Parqueador' age=None
    ```

7. Print the `hero_3` before interacting with the database.

    Generates the output:

    ```
    Hero 3: id=None name='Rusty-Man' secret_name='Tommy Sharp' age=48
    ```

8. Create the `Session` in a `with` block.

    **Doesn't generate any output**.

9. Add the `hero_1` to the session.

    This still doesn't save it to the database.

    **Doesn't generate any output**.

10. Add the `hero_2` to the session.

    This still doesn't save it to the database.

    **Doesn't generate any output**.

11. Add the `hero_3` to the session.

    This still doesn't save it to the database.

    **Doesn't generate any output**.

12. Print the line `"After adding to the session"`.

    Generates the output:

    ```
    After adding to the session
    ```

13. Print the `hero_1` after adding it to the session.

    It still has the same data as there hasn't been any interaction with the database yet. Notice that the `id` is still `None`.

    Generates the output:

    ```
    Hero 1: id=None name='Deadpond' secret_name='Dive Wilson' age=None
    ```

14. Print the `hero_2` after adding it to the session.

    It still has the same data as there hasn't been any interaction with the database yet. Notice that the `id` is still `None`.

    Generates the output:

    ```
    Hero 2: id=None name='Spider-Boy' secret_name='Pedro Parqueador' age=None
    ```

15. Print the `hero_3` after adding it to the session.

    It still has the same data as there hasn't been any interaction with the database yet. Notice that the `id` is still `None`.

    Generates the output:

    ```
    Hero 3: id=None name='Rusty-Man' secret_name='Tommy Sharp' age=48
    ```

16. `commit` the **session**.

    This will **save** all the data to the database. The **session** will use the **engine** to run a lot of SQL.

    Generates the output:

    ```
    INFO Engine BEGIN (implicit)
    INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
    INFO Engine [generated in 0.00018s] ('Deadpond', 'Dive Wilson', None)
    INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
    INFO Engine [cached since 0.0008968s ago] ('Spider-Boy', 'Pedro Parqueador', None)
    INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
    INFO Engine [cached since 0.001143s ago] ('Rusty-Man', 'Tommy Sharp', 48)
    INFO Engine COMMIT
    ```

17. Print the line `"After committing the session"`.

    Generates the output:

    ```
    After committing the session
    ```

18. Print the `hero_1` after committing the session.

    The `hero_1` is now internally marked as expired, and until it is refreshed, it looks like if it didn't contain any data.

    Generates the output:

    ```
    Hero 1:
    ```

19. Print the `hero_2` after committing the session.

    The `hero_2` is now internally marked as expired, and until it is refreshed, it looks like if it didn't contain any data.

    Generates the output:

    ```
    Hero 2:
    ```

20. Print the `hero_3` after committing the session.

    The `hero_3` is now internally marked as expired, and until it is refreshed, it looks like if it didn't contain any data.

    Generates the output:

    ```
    Hero 3:
    ```

21. Print the line `"After commiting the session, show IDs"`.

    Generates the output:

    ```
    After committing the session, show IDs
    ```

22. Print the `hero_1.id`. A lot happens here.

    Because we are accessing the attribute `id` of `hero_1`, **SQLModel** (actually SQLAlchemy) can detect that we are trying to access data from the `hero_1`.

    It then detects that `hero_1` is currently associated with a **session** (because we added it to the session and committed it), and it is marked as expired.

    Then with the **session**, it uses the **engine** to execute all the SQL to fetch the data for this object from the database.

    Next it updates the object with the new data and marks it internally as "fresh" or "not expired".

    Finally, it makes the ID value available for the rest of the Python expression. In this case, the Python expression just prints the ID.

    Generates the output:

    ```
    INFO Engine BEGIN (implicit)
    INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age 
    FROM hero 
    WHERE hero.id = ?
    INFO Engine [generated in 0.00017s] (1,)

    Hero 1 ID: 1
    ```

23. Print the `hero_2.id`.

    A lot happens here, all the same stuff that happened at point 22, but for this `hero_2` object.

    Generates the output:

    ```
    INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age 
    FROM hero 
    WHERE hero.id = ?
    INFO Engine [cached since 0.001245s ago] (2,)

    Hero 2 ID: 2
    ```

24. Print the `hero_3.id`.

    A lot happens here, all the same stuff that happened at point 22, but for this `hero_3` object.

    Generates the output:

    ```
    INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age 
    FROM hero 
    WHERE hero.id = ?
    INFO Engine [cached since 0.002215s ago] (3,)


    Hero 3 ID: 3
    ```

25. Print the line `"After committing the session, show names"`.

    Generates the output:

    ```
    After committing the session, show names
    ```

26. Print the `hero_1.name`.

    Because `hero_1` is still fresh, no additional data is fetched, no additional SQL is executed, and the name is available.

    Generates the output:

    ```
    Hero 1 name: Deadpond
    ```

27. Print the `hero_2.name`.

    Because `hero_2` is still fresh, no additional data is fetched, no additional SQL is executed, and the name is available.

    Generates the output:

    ```
    Hero 2 name: Spider-Boy
    ```

28. Print the `hero_3.name`.

    Because `hero_3` is still fresh, no additional data is fetched, no additional SQL is executed, and the name is available.

    Generates the output:

    ```
    Hero 3 name: Rusty-Man
    ```

29. Explicitly refresh the `hero_1` object.

    The **session** will use the **engine** to execute the SQL necessary to fetch fresh data from the database for the `hero_1` object.

    Generates the output:

    ```
    INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age 
    FROM hero 
    WHERE hero.id = ?
    INFO Engine [generated in 0.00024s] (1,)
    ```

30. Explicitly refresh the `hero_2` object.

    The **session** will use the **engine** to execute the SQL necessary to fetch fresh data from the database for the `hero_2` object.

    Generates the output:

    ```
    INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age 
    FROM hero 
    WHERE hero.id = ?
    INFO Engine [cached since 0.001487s ago] (2,)
    ```

31. Explicitly refresh the `hero_3` object.

    The **session** will use the **engine** to execute the SQL necessary to fetch fresh data from the database for the `hero_3` object.

    Generates the output:

    ```
    INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age 
    FROM hero 
    WHERE hero.id = ?
    INFO Engine [cached since 0.002377s ago] (3,)
    ```

32. Print the line `"After refreshing the heroes"`.

    Generates the output:

    ```
    After refreshing the heroes
    ```

33. Print the `hero_1`.

    !!! info
        Even if the `hero_1` wasn't fresh, this would **not** trigger a `refresh` making the **session** use the **engine** to fetch data from the database because it is not accessing an attribute.

    Because the `hero_1` is fresh it has all it's data available.

    Generates the output:

    ```
    Hero 1: age=None id=1 name='Deadpond' secret_name='Dive Wilson'
    ```

34. Print the `hero_2`.

    !!! info
        Even if the `hero_2` wasn't fresh, this would **not** trigger a `refresh` making the **session** use the **engine** to fetch data from the database because it is not accessing an attribute.

    Because the `hero_2` is fresh it has all it's data available.

    Generates the output:

    ```
    Hero 2: age=None id=2 name='Spider-Boy' secret_name='Pedro Parqueador'
    ```

35. Print the `hero_3`.

    !!! info
        Even if the `hero_3` wasn't fresh, this would **not** trigger a `refresh` making the **session** use the **engine** to fetch data from the database because it is not accessing an attribute.

    Because the `hero_3` is fresh it has all it's data available.

    Generates the output:

    ```
    Hero 3: age=48 id=3 name='Rusty-Man' secret_name='Tommy Sharp'
    ```

36. The `with` block ends here (there's no more indented code), so the **session** is closed, running all it's closing code.

    This includes doing a `ROLLBACK` of any possible transaction that could have been started.

    Generates the output:

    ```
    INFO Engine ROLLBACK
    ```

37. Print the line `"After the session closes"`.

    Generates the output:

    ```
    After the session closes
    ```

38. Print the `hero_1` after closing the session.

    Generates the output:

    ```
    Hero 1: age=None id=1 name='Deadpond' secret_name='Dive Wilson'
    ```

39. Print the `hero_2` after closing the session.

    Generates the output:

    ```
    Hero 2: age=None id=2 name='Spider-Boy' secret_name='Pedro Parqueador'
    ```

40. Print the `hero_3` after closing the session.

    Generates the output:

    ```
    Hero 3: age=48 id=3 name='Rusty-Man' secret_name='Tommy Sharp'
    ```
