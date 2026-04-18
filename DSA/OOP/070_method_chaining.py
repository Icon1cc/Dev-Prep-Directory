"""
Problem 070: Method Chaining (Fluent Interface)

Difficulty: Intermediate
Topic: Design Pattern

=== PROBLEM DESCRIPTION ===

Method chaining allows calling multiple methods in a single statement.
Each method returns `self` to enable the chain. This creates a fluent,
readable API.

Your Task:
-----------
1. Create a `QueryBuilder` class with method chaining:
   - `select(*columns)` - columns to select
   - `from_table(table)` - table name
   - `where(condition)` - add WHERE clause
   - `order_by(column, direction='ASC')` - add ORDER BY
   - `limit(n)` - add LIMIT
   - `build()` - return the SQL string
   - All methods except build() return self

2. Create a `StringBuilder` class:
   - `append(text)` - add text
   - `append_line(text)` - add text with newline
   - `indent(spaces=2)` - add indentation
   - `build()` - return final string

3. Create a `HtmlBuilder` class:
   - `tag(name)` - start a tag
   - `attr(key, value)` - add attribute
   - `text(content)` - add text content
   - `close()` - close current tag
   - `build()` - return HTML string

Expected Output:
----------------
QueryBuilder:
SELECT name, email FROM users WHERE age > 18 ORDER BY name ASC LIMIT 10

StringBuilder:
Hello
  World
    Indented

HtmlBuilder:
<div class="container"><p id="intro">Welcome!</p></div>

=== CONCEPTS TO LEARN ===
- Return self from methods to enable chaining
- Creates readable, expressive APIs
- Common in query builders, configuration objects
- Follows Builder pattern principles

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# # QueryBuilder
# query = (QueryBuilder()
#     .select("name", "email")
#     .from_table("users")
#     .where("age > 18")
#     .order_by("name")
#     .limit(10)
#     .build())
# print("QueryBuilder:")
# print(query)
#
# print("\nStringBuilder:")
# text = (StringBuilder()
#     .append_line("Hello")
#     .indent(2).append_line("World")
#     .indent(4).append_line("Indented")
#     .build())
# print(text)
#
# print("HtmlBuilder:")
# html = (HtmlBuilder()
#     .tag("div").attr("class", "container")
#     .tag("p").attr("id", "intro").text("Welcome!").close()
#     .close()
#     .build())
# print(html)
