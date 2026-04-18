# Python Refresher - Complete Reference Guide

## Table of Contents

1. [List Statistics Calculator](#list-statistics-calculator) - [Code: 01. List Statistics Calculator.py](./01.%20List%20Statistics%20Calculator.py)
2. [Word Frequency Counter](#word-frequency-counter) - [Code: 02. Word Frequency Counter.py](./02.%20Word%20Frequency%20Counter.py)
3. [Advanced Number Properties](#advanced-number-properties) - [Code: 03. Advanced Number Properties.py](./03.%20Advanced%20Number%20Properties.py)
4. [Dynamic Formatter](#dynamic-formatter) - [Code: 04. Dynamic Formatter.py](./04.%20Dynamic%20Formatter.py)
5. [Matrix Transposition with Comprehensions](#matrix-transposition-with-comprehensions) - [Code: 05. Matrix Transposition with Comprehensions.py](./05.%20Matrix%20Transposition%20with%20Comprehensions.py)
6. [Find Common and Unique Items](#find-common-and-unique-items) - [Code: 06. Find Common and Unique Items.py](./06.%20Find%20Common%20and%20Unique%20Items.py)
7. [Slicing for Palindromes](#slicing-for-palindromes) - [Code: 07. Slicing for Palindromes.py](./07.%20Slicing%20for%20Palindromes.py)
8. [Bitwise Permission Manager](#bitwise-permission-manager) - [Code: 08. Bitwise Permission Manager.py](./08.%20Bitwise%20Permission%20Manager.py)
9. [Execution Time Decorator](#execution-time-decorator) - [Code: 09. Execution Time Decorator.py](./09.%20Execution%20Time%20Decorator.py)
10. [Basic Vector Class](#basic-vector-class) - [Code: 10. Basic Vector Class.py](./10.%20Basic%20Vector%20Class.py)
11. [Vector with Operator Overloading](#vector-with-operator-overloading) - [Code: 11. Vector with Operator Overloading.py](./11.%20Vector%20with%20Operator%20Overloading.py)
12. [Shapes and Polymorphism](#shapes-and-polymorphism) - [Code: 12. Shapes and Polymorphism.py](./12.%20Shapes%20and%20Polymorphism.py)
13. [Class and Static Methods](#class-and-static-methods) - [Code: 13. Class and Static method.py](./13.%20Class%20and%20Static%20method.py)
14. [Encapsulation with Bank Account](#encapsulation-with-bank-account) - [Code: 14. Encapsulation with Bank Account.py](./14.%20Encapsulation%20with%20Bank%20Account.py)
15. [Multiple Inheritance](#multiple-inheritance) - [Code: 15. Multiple Inheritance.py](./15.%20Multiple%20Inheritance.py)

---

## Overview

This section covers essential Python concepts and programming patterns that form the foundation for data structures and algorithms. Topics include:
- **Data manipulation**: Lists, dictionaries, sets
- **File handling**: Reading and processing files
- **String formatting**: Various formatting techniques
- **Bitwise operations**: Understanding binary operations
- **Decorators**: Function wrappers and timing
- **Object-Oriented Programming**: Classes, inheritance, polymorphism, encapsulation

---

## List Statistics Calculator
**📁 Implementation:** [01. List Statistics Calculator.py](./01.%20List%20Statistics%20Calculator.py)

### Problem
Calculate primary statistical properties (mean, median, mode) of a list of integers.

### Key Concepts

#### Mean (Average)
```python
mean = sum(numbers) / len(numbers)
```

#### Median (Middle Value)
```python
sorted_num = sorted(numbers)
n = len(sorted_num)

if n % 2 == 0:
    median = (sorted_num[n//2 - 1] + sorted_num[n//2]) / 2
else:
    median = sorted_num[n//2]
```

#### Mode (Most Frequent)
```python
counts = {}
for num in numbers:
    counts[num] = counts.get(num, 0) + 1

max_count = max(counts.values())
mode = [num for num, freq in counts.items() if freq == max_count]
```

### Time Complexity
| Operation | Complexity | Notes |
|-----------|------------|-------|
| Mean | O(n) | Sum all elements |
| Median | O(n log n) | Sorting required |
| Mode | O(n) | Single pass with dictionary |

### Space Complexity
- **Mean**: O(1)
- **Median**: O(n) - sorted copy
- **Mode**: O(k) where k = unique elements

---

## Word Frequency Counter
**📁 Implementation:** [02. Word Frequency Counter.py](./02.%20Word%20Frequency%20Counter.py)

### Problem
Read a text file, count word frequencies (case-insensitive, ignoring punctuation).

### Key Concepts

#### File Handling
```python
with open(filepath, "r") as file:
    content = file.read()
```

#### String Processing
```python
import string

# Remove punctuation
for char in string.punctuation:
    content = content.replace(char, "")

# Case-insensitive
content = content.lower()

# Split into words
words = content.split()
```

#### Frequency Dictionary
```python
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
```

### Error Handling
```python
try:
    # file operations
except FileNotFoundError:
    print("File not found.")
```

### Time Complexity
- **O(n)** where n = total characters in file
- Dictionary operations are O(1) average

---

## Advanced Number Properties
**📁 Implementation:** [03. Advanced Number Properties.py](./03.%20Advanced%20Number%20Properties.py)

### Problem
Check various mathematical properties of numbers.

### Common Number Properties

#### Prime Check
```python
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
```

#### Perfect Number
Sum of divisors (excluding itself) equals the number.
```python
def is_perfect(n):
    return sum(i for i in range(1, n) if n % i == 0) == n
```

#### Armstrong Number
Sum of digits raised to power of number of digits equals the number.
```python
def is_armstrong(n):
    digits = str(n)
    power = len(digits)
    return sum(int(d)**power for d in digits) == n
```

---

## Dynamic Formatter
**📁 Implementation:** [04. Dynamic Formatter.py](./04.%20Dynamic%20Formatter.py)

### Problem
Demonstrate different string formatting techniques in Python.

### Formatting Methods

#### 1. Old Style (% Operator)
```python
name = "Alice"
age = 25
print("Name: %s, Age: %d" % (name, age))
```

#### 2. str.format() Method
```python
print("Name: {}, Age: {}".format(name, age))
print("Name: {n}, Age: {a}".format(n=name, a=age))
```

#### 3. f-strings (Recommended - Python 3.6+)
```python
print(f"Name: {name}, Age: {age}")
print(f"Next year: {age + 1}")  # Expressions allowed
```

### Format Specifications
```python
pi = 3.14159
print(f"Pi: {pi:.2f}")      # 2 decimal places
print(f"Value: {42:05d}")   # Zero-padded
print(f"Align: {name:>10}") # Right-align with width 10
```

---

## Matrix Transposition with Comprehensions
**📁 Implementation:** [05. Matrix Transposition with Comprehensions.py](./05.%20Matrix%20Transposition%20with%20Comprehensions.py)

### Problem
Transpose a matrix using list comprehensions.

### What is Transposition?
Rows become columns and columns become rows.

```
Original:     Transposed:
[[1, 2, 3],   [[1, 4],
 [4, 5, 6]]    [2, 5],
               [3, 6]]
```

### List Comprehension Approach
```python
def transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    return [[matrix[i][j] for i in range(rows)] for j in range(cols)]
```

### Using zip()
```python
def transpose(matrix):
    return [list(row) for row in zip(*matrix)]
```

### Time Complexity
- **O(m × n)** where m = rows, n = columns

### Space Complexity
- **O(m × n)** - new matrix created

---

## Find Common and Unique Items
**📁 Implementation:** [06. Find Common and Unique Items.py](./06.%20Find%20Common%20and%20Unique%20Items.py)

### Problem
Find common and unique elements between two collections using set operations.

### Set Operations

#### Intersection (Common Elements)
```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

common = a & b           # {3, 4}
# or
common = a.intersection(b)
```

#### Union (All Elements)
```python
all_items = a | b        # {1, 2, 3, 4, 5, 6}
```

#### Difference (Unique to One Set)
```python
only_in_a = a - b        # {1, 2}
only_in_b = b - a        # {5, 6}
```

#### Symmetric Difference (Not in Both)
```python
unique = a ^ b           # {1, 2, 5, 6}
```

### Time Complexity
- Set operations: **O(min(len(a), len(b)))** average

---

## Slicing for Palindromes
**📁 Implementation:** [07. Slicing for Palindromes.py](./07.%20Slicing%20for%20Palindromes.py)

### Problem
Use Python slicing to check and manipulate palindromes.

### Slicing Syntax
```python
s[start:end:step]
```

### Palindrome Check
```python
def is_palindrome(s):
    return s == s[::-1]  # Reverse and compare
```

### Advanced Slicing Examples
```python
s = "Python"

s[::2]    # 'Pto'  - Every 2nd character
s[1::2]   # 'yhn'  - Start at 1, every 2nd
s[::-1]   # 'nohtyP' - Reverse
s[-3:]    # 'hon'  - Last 3 characters
s[:-2]    # 'Pyth' - All but last 2
```

### Time Complexity
- Slicing: **O(k)** where k = slice length
- Palindrome check: **O(n)**

---

## Bitwise Permission Manager
**📁 Implementation:** [08. Bitwise Permission Manager.py](./08.%20Bitwise%20Permission%20Manager.py)

### Problem
Manage permissions using bitwise operations (READ=4, WRITE=2, EXECUTE=1).

### Bitwise Operations

#### Setting a Bit (ADD Permission)
```python
# OR operator
result = current_permissions | permission_type
# Example: 5 | 2 = 7 (101 | 010 = 111)
```

#### Clearing a Bit (REMOVE Permission)
```python
# AND with NOT
result = current_permissions & ~permission_type
# Example: 7 & ~4 = 3 (111 & 011 = 011)
```

### Permission Values
| Permission | Binary | Decimal |
|------------|--------|---------|
| EXECUTE | 001 | 1 |
| WRITE | 010 | 2 |
| READ | 100 | 4 |
| READ+WRITE | 110 | 6 |
| ALL | 111 | 7 |

### Checking Permissions
```python
def has_permission(current, permission):
    return (current & permission) == permission
```

---

## Execution Time Decorator
**📁 Implementation:** [09. Execution Time Decorator.py](./09.%20Execution%20Time%20Decorator.py)

### Problem
Create a decorator to measure function execution time.

### What is a Decorator?
A decorator is a function that takes another function and extends its behavior without modifying it.

### Implementation
```python
import time

def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Execution time: {end - start:.4f} seconds")
        return result
    return wrapper
```

### Usage
```python
@time_it
def slow_function():
    time.sleep(1)
    return "Done"

slow_function()  # Prints execution time automatically
```

### Key Concepts
- **\*args**: Variable positional arguments
- **\*\*kwargs**: Variable keyword arguments
- **Closure**: Inner function accessing outer function's variables

---

## Basic Vector Class
**📁 Implementation:** [10. Basic Vector Class.py](./10.%20Basic%20Vector%20Class.py)

### Problem
Create a simple 2D vector class with x and y coordinates.

### Class Definition
```python
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

### Key OOP Concepts

#### Constructor (`__init__`)
- Called automatically when creating an object
- Initializes instance attributes

#### Instance Attributes
- Variables specific to each object
- Accessed via `self.attribute`

### Usage
```python
v1 = Vector2D(3, 4)
print(v1.x, v1.y)  # 3 4
```

---

## Vector with Operator Overloading
**📁 Implementation:** [11. Vector with Operator Overloading.py](./11.%20Vector%20with%20Operator%20Overloading.py)

### Problem
Extend Vector2D to support mathematical operations using operator overloading.

### Magic Methods (Dunder Methods)
```python
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"
```

### Common Magic Methods
| Method | Operator | Usage |
|--------|----------|-------|
| `__add__` | + | a + b |
| `__sub__` | - | a - b |
| `__mul__` | * | a * b |
| `__eq__` | == | a == b |
| `__lt__` | < | a < b |
| `__str__` | str() | print(a) |
| `__len__` | len() | len(a) |

---

## Shapes and Polymorphism
**📁 Implementation:** [12. Shapes and Polymorphism.py](./12.%20Shapes%20and%20Polymorphism.py)

### Problem
Demonstrate polymorphism with shape classes and area calculations.

### Abstract Base Class
```python
class Shape:
    def area(self):
        raise NotImplementedError("Subclasses must implement area()")
```

### Concrete Classes
```python
import math

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2
```

### Polymorphism in Action
```python
shapes = [Rectangle(3, 4), Circle(5)]

for shape in shapes:
    print(shape.area())  # Each calls its own area() method
```

### Key Concepts
- **Inheritance**: Child classes inherit from parent
- **Polymorphism**: Same method name, different implementations
- **Abstract Method**: Method that must be overridden

---

## Class and Static Methods
**📁 Implementation:** [13. Class and Static method.py](./13.%20Class%20and%20Static%20method.py)

### Problem
Understand the difference between instance, class, and static methods.

### Three Types of Methods

#### Instance Method
```python
class MyClass:
    def instance_method(self):
        # Has access to instance via self
        return self.attribute
```

#### Class Method
```python
class MyClass:
    count = 0

    @classmethod
    def class_method(cls):
        # Has access to class via cls
        return cls.count
```

#### Static Method
```python
class MyClass:
    @staticmethod
    def static_method(x, y):
        # No access to instance or class
        return x + y
```

### When to Use Each
| Type | Use When |
|------|----------|
| Instance | Need to access/modify instance data |
| Class | Need to access/modify class data, factory methods |
| Static | Utility function that doesn't need class/instance |

---

## Encapsulation with Bank Account
**📁 Implementation:** [14. Encapsulation with Bank Account.py](./14.%20Encapsulation%20with%20Bank%20Account.py)

### Problem
Demonstrate encapsulation by protecting internal data with private attributes.

### Encapsulation Implementation
```python
class BankAccount:
    def __init__(self, initial_balance):
        self._balance = initial_balance  # Protected (convention)

    def get_balance(self):
        return self._balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    def withdraw(self, amount):
        if amount <= self._balance:
            self._balance -= amount
        else:
            print("Insufficient funds")
```

### Python Naming Conventions
| Prefix | Meaning | Access |
|--------|---------|--------|
| `name` | Public | Anyone |
| `_name` | Protected | By convention, internal use |
| `__name` | Private | Name mangling, harder to access |

### Benefits of Encapsulation
1. **Data Protection**: Control how data is modified
2. **Validation**: Check inputs before changing state
3. **Flexibility**: Change internal implementation without breaking external code
4. **Maintainability**: Clear interface, hidden complexity

---

## Multiple Inheritance
**📁 Implementation:** [15. Multiple Inheritance.py](./15.%20Multiple%20Inheritance.py)

### Problem
Understand how a class can inherit from multiple parent classes.

### Syntax
```python
class Parent1:
    def method1(self):
        return "From Parent1"

class Parent2:
    def method2(self):
        return "From Parent2"

class Child(Parent1, Parent2):
    def child_method(self):
        return "From Child"
```

### Method Resolution Order (MRO)
Python uses C3 linearization to determine method lookup order.

```python
Child.__mro__
# (<class 'Child'>, <class 'Parent1'>, <class 'Parent2'>, <class 'object'>)
```

### Diamond Problem
```python
class A:
    def greet(self):
        return "A"

class B(A):
    def greet(self):
        return "B"

class C(A):
    def greet(self):
        return "C"

class D(B, C):
    pass

d = D()
d.greet()  # Returns "B" (follows MRO: D -> B -> C -> A)
```

### Using super() with Multiple Inheritance
```python
class Child(Parent1, Parent2):
    def __init__(self):
        super().__init__()  # Calls next in MRO
```

---

## Comparison Summary

### Data Manipulation Techniques

| Technique | Time | Space | Use Case |
|-----------|------|-------|----------|
| List Comprehension | O(n) | O(n) | Transforming lists |
| Dictionary Operations | O(1) avg | O(n) | Counting, mapping |
| Set Operations | O(n) | O(n) | Uniqueness, membership |
| Slicing | O(k) | O(k) | Extracting portions |

### OOP Concepts Covered

| Concept | Description |
|---------|-------------|
| **Encapsulation** | Hiding internal state |
| **Inheritance** | Reusing code from parent classes |
| **Polymorphism** | Same interface, different implementations |
| **Abstraction** | Hiding complexity behind simple interface |
| **Operator Overloading** | Custom behavior for operators |

---

## Best Practices

### 1. Use f-strings for Formatting
```python
# Preferred
f"Hello, {name}!"

# Avoid
"Hello, %s!" % name
"Hello, {}!".format(name)
```

### 2. Prefer List Comprehensions
```python
# Preferred
squares = [x**2 for x in range(10)]

# Avoid for simple cases
squares = []
for x in range(10):
    squares.append(x**2)
```

### 3. Use Context Managers for Files
```python
# Preferred - automatically closes file
with open(filename) as f:
    content = f.read()

# Avoid
f = open(filename)
content = f.read()
f.close()
```

### 4. Follow Naming Conventions
- **Classes**: PascalCase (`BankAccount`)
- **Functions/Variables**: snake_case (`calculate_sum`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_SIZE`)
- **Private**: Leading underscore (`_private_var`)

### 5. Document Your Code
```python
def calculate_area(width, height):
    """
    Calculate the area of a rectangle.

    Args:
        width: The width of the rectangle
        height: The height of the rectangle

    Returns:
        The area as width * height
    """
    return width * height
```

---
