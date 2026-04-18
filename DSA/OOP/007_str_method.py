"""
Problem 007: The __str__ Method (String Representation)

Difficulty: Beginner
Topic: Magic/Dunder Methods

=== PROBLEM DESCRIPTION ===

The `__str__` method defines how an object is converted to a string.
It's called when you use `print()` on an object or `str()` function.
Without it, printing an object shows something like <__main__.Book object at 0x...>

Your Task:
-----------
1. Create a class called `Book`
2. The `__init__` should accept `title`, `author`, and `pages`
3. Implement `__str__` to return a nicely formatted string
4. Create a Book and print it directly

Expected Output:
----------------
"The Great Gatsby" by F. Scott Fitzgerald (180 pages)

=== CONCEPTS TO LEARN ===
- `__str__` must return a string
- It's automatically called by print() and str()
- Makes objects human-readable
- This is one of many "magic methods" or "dunder methods"

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------

class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        return f'"{self.title}" by {self.author} ({self.pages} pages)'

# Test your solution
# ------------------
book = Book("The Great Gatsby", "F. Scott Fitzgerald", 180)
print(book)  # This should print nicely now!
