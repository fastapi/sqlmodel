1. Select the hero we will work with.

2. Execute the query with the select statement object.

    This generates the output:

    ```
    INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age 
    FROM hero 
    WHERE hero.name = ?
    INFO Engine [no key 0.00017s] ('Spider-Boy',)
    ```

3. Get one hero object, expecting exactly one.

    !!! tip
        This ensures there's no more than one, and that there's exactly one, not `None`.

        This would never return `None`, instead it would raise an exception.

4. Print the hero object.

    This generates the output:

    ```
    Hero: name='Spider-Boy' secret_name='Pedro Parqueador' age=None id=2
    ```

5. Set the hero's age field to the new value `16`.

    Now the `hero` object in memory has a different value for the age, but it is still not saved to the database.

6. Add the hero to the session.

    This puts it in that temporary place in the session before committing.

    But it's still not saved in the database yet.

7. Commit the session.

    This saves the updated hero to the database.

    And this generates the output:

    ```
    INFO Engine UPDATE hero SET age=? WHERE hero.id = ?
    INFO Engine [generated in 0.00017s] (16, 2)
    INFO Engine COMMIT
    ```

8. Refresh the hero object to have the recent data, including the age we just committed.

    This generates the output:

    ```
    INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age 
    FROM hero 
    WHERE hero.id = ?
    INFO Engine [generated in 0.00018s] (2,)
    ```

9. Print the updated hero object.

    This generates the output:

    ```
    Updated hero: name='Spider-Boy' secret_name='Pedro Parqueador' age=16 id=2
    ```
