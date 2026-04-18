"""
Problem 072: Prototype Design Pattern

Difficulty: Intermediate
Topic: Creational Design Pattern

=== PROBLEM DESCRIPTION ===

The Prototype pattern creates new objects by cloning existing ones.
Useful when object creation is expensive or complex.

Your Task:
-----------
1. Create a `Prototype` ABC:
   - Abstract method `clone()` that creates a copy

2. Create a `Document` class:
   - Attributes: title, content, author, created_date, metadata (dict)
   - `clone()` creates a deep copy with new created_date

3. Create a `DocumentRegistry` (Prototype Manager):
   - Stores prototype documents by name
   - `register(name, prototype)` - add a prototype
   - `create(name)` - return a clone of the named prototype

4. Demonstrate cloning:
   - Create a template document
   - Clone it multiple times with modifications

Expected Output:
----------------
Original: Report Template (created 2024-01-01)
Clone 1: Q1 Report (created 2024-03-18)
Clone 2: Q2 Report (created 2024-03-18)

Original metadata: {'version': '1.0', 'department': 'Sales'}
Clone metadata modified: {'version': '1.0', 'department': 'Sales', 'quarter': 'Q1'}
Original unchanged: {'version': '1.0', 'department': 'Sales'}

Using DocumentRegistry:
Created 'Sales Report' from 'report' template
Created 'Welcome Email' from 'email' template

=== CONCEPTS TO LEARN ===
- Clone existing objects instead of creating from scratch
- Use deep copy to avoid shared mutable state
- Prototype registry manages available prototypes
- Useful for expensive object creation

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod
import copy
from datetime import datetime

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate the Prototype pattern
