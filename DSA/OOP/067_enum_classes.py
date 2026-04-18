"""
Problem 067: Enum Classes

Difficulty: Intermediate
Topic: Enumeration Types

=== PROBLEM DESCRIPTION ===

Enum (enumeration) classes provide a way to define a set of named constants.
They improve code readability and prevent invalid values.

Your Task:
-----------
1. Create a basic `Color` enum:
   - Members: RED, GREEN, BLUE
   - Access by name and value

2. Create a `Status` enum with custom values:
   - PENDING = "pending"
   - PROCESSING = "processing"
   - COMPLETED = "completed"
   - FAILED = "failed"

3. Create an `HttpStatus` IntEnum:
   - OK = 200, CREATED = 201, BAD_REQUEST = 400, etc.
   - IntEnum allows comparison with integers

4. Create a `Permission` Flag enum:
   - READ = 1, WRITE = 2, EXECUTE = 4
   - Support bitwise operations (READ | WRITE)

5. Create an enum with methods:
   - `Planet` enum with mass and radius
   - Method `surface_gravity()` to calculate gravity

Expected Output:
----------------
Color.RED = 1
Status.PENDING = 'pending'
HttpStatus.OK == 200: True
Permission.READ | Permission.WRITE = Permission.READ|WRITE

Planet.EARTH:
  Mass: 5.97e+24 kg
  Surface gravity: 9.80 m/s²

Iterating Status enum:
- pending
- processing
- completed
- failed

=== CONCEPTS TO LEARN ===
- Enum provides named constants
- IntEnum for integer-valued enums
- Flag for bitwise combinable values
- auto() for automatic values
- Enums can have methods and properties

=== STARTER CODE ===
"""

from enum import Enum, IntEnum, Flag, auto

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate various enum features
