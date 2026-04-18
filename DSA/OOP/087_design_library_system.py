"""
Problem 087: Interview Problem - Design a Library Management System

Difficulty: Advanced
Topic: System Design Interview Question

=== PROBLEM DESCRIPTION ===

Design a library management system. Another classic OOP interview question.

Requirements:
- Manage books, members, and librarians
- Books have copies; track availability
- Members can borrow/return books (max 5 at a time)
- Reservation system when books are unavailable
- Fine calculation for overdue books
- Search books by title, author, ISBN

Your Task:
-----------
1. Create `BookItem` (physical copy) vs `Book` (catalog entry):
   - `Book`: ISBN, title, author, category
   - `BookItem`: barcode, book reference, status, due_date

2. Create `Person` hierarchy:
   - `Member`: can borrow, return, reserve books
   - `Librarian`: can add books, manage members

3. Create `Library` class:
   - `add_book(book, num_copies)`
   - `search_by_title(title)`, `search_by_author(author)`
   - `checkout(member, book_item)` - borrow book
   - `return_book(member, book_item)` - return with fine calc
   - `reserve(member, book)` - reserve unavailable book

4. Create `Loan` record:
   - `member`, `book_item`, `checkout_date`, `due_date`
   - `calculate_fine()` - $0.50 per day overdue

5. Create `Reservation` queue:
   - First-come, first-served when book returns

Expected Output:
----------------
Library: City Central Library
Books in catalog: 3

Searching for 'Python':
- "Learning Python" by Mark Lutz (3 copies, 2 available)
- "Python Cookbook" by David Beazley (2 copies, 2 available)

Member 'Alice' checking out "Learning Python"...
Checkout successful. Due date: 2024-04-01

Member 'Bob' checking out "Learning Python"...
Checkout successful. Due date: 2024-04-01

Member 'Charlie' reserving "Learning Python"...
All copies checked out. Added to reservation queue (position: 1)

Alice returning "Learning Python"...
Book returned. No fine.
Notification: Charlie, your reserved book is now available!

=== STARTER CODE ===
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Simulate library operations
