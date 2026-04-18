"""
Problem 083: Implementing a Mini ORM

Difficulty: Advanced
Topic: Real-world Application

=== PROBLEM DESCRIPTION ===

Build a simplified Object-Relational Mapper (ORM) that maps Python classes
to database tables. This demonstrates descriptors, metaclasses, and real-world
OOP patterns.

Your Task:
-----------
1. Create `Field` descriptors:
   - `IntegerField(primary_key=False)`
   - `StringField(max_length=255)`
   - `BooleanField(default=False)`
   - `ForeignKey(model_class)`

2. Create `ModelMeta` metaclass:
   - Collects all fields defined on the class
   - Creates `_fields` dict mapping name -> Field
   - Sets up table name (class name lowercase + 's')

3. Create `Model` base class:
   - `save()` - generates INSERT/UPDATE SQL
   - `delete()` - generates DELETE SQL
   - `find(id)` - classmethod, generates SELECT SQL
   - `all()` - classmethod, returns all records
   - `filter(**kwargs)` - classmethod, filtered query

4. Create sample models:
   - `User(Model)` with id, name, email, is_active
   - `Post(Model)` with id, title, content, user (ForeignKey)

Expected Output:
----------------
Creating User table...
SQL: CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    is_active BOOLEAN DEFAULT False
)

Creating user...
SQL: INSERT INTO users (name, email, is_active) VALUES ('Alice', 'alice@email.com', True)

Finding user...
SQL: SELECT * FROM users WHERE id = 1

Filtering users...
SQL: SELECT * FROM users WHERE is_active = True

=== CONCEPTS TO LEARN ===
- Descriptors for field types
- Metaclasses for class configuration
- Active Record pattern
- SQL generation from objects

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Create models and generate SQL
