"""
Problem 024: Abstract Base Classes (ABC)

Difficulty: Intermediate
Topic: Abstract Classes

=== PROBLEM DESCRIPTION ===

Abstract Base Classes (ABCs) define a template that subclasses MUST follow.
They can have abstract methods (must be overridden) and concrete methods
(inherited as-is). You CANNOT instantiate an abstract class.

Your Task:
-----------
1. Import ABC and abstractmethod from abc module

2. Create abstract class `Database(ABC)`:
   - Abstract method: `connect()`
   - Abstract method: `execute(query)`
   - Abstract method: `close()`
   - Concrete method: `execute_many(queries)` - loops and calls execute()

3. Create `MySQLDatabase(Database)`:
   - Implement all abstract methods (can just print/return strings)

4. Create `PostgreSQLDatabase(Database)`:
   - Implement all abstract methods

5. Try to instantiate Database directly (should fail)
6. Instantiate MySQLDatabase and PostgreSQLDatabase (should work)

Expected Output:
----------------
Cannot instantiate abstract class Database
MySQL: Connecting to MySQL server...
MySQL: Executing: SELECT * FROM users
MySQL: Executing: SELECT * FROM orders
MySQL: Connection closed
---
PostgreSQL: Connecting to PostgreSQL server...
PostgreSQL: Executing: SELECT * FROM users

=== CONCEPTS TO LEARN ===
- from abc import ABC, abstractmethod
- Abstract methods have no implementation (just `pass` or docstring)
- Subclasses MUST implement all abstract methods
- ABCs can have concrete (implemented) methods too
- Cannot create instances of abstract classes

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# # This should fail:
# try:
#     db = Database()
# except TypeError:
#     print("Cannot instantiate abstract class Database")
#
# # These should work:
# mysql = MySQLDatabase()
# mysql.connect()
# mysql.execute_many(["SELECT * FROM users", "SELECT * FROM orders"])
# mysql.close()
#
# print("---")
#
# postgres = PostgreSQLDatabase()
# postgres.connect()
# postgres.execute("SELECT * FROM users")
