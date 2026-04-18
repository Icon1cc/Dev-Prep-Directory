# Object-Oriented Programming in Python - Interview Preparation

A comprehensive collection of 100 OOP problems to prepare you for big tech interviews.

## How to Use This Guide

1. **Start from the beginning** - Problems are ordered from basic to advanced
2. **Read the problem description carefully** - Each file contains detailed explanations
3. **Try to solve without looking at hints** - Struggle is part of learning
4. **Understand, don't just memorize** - Focus on WHY, not just HOW
5. **Practice explaining your solutions** - Interviews require verbal communication

## Topics Covered

### Fundamentals (Problems 001-020)
- Classes and Objects
- `__init__` Constructor
- Instance Methods
- `self` Parameter
- Default Parameters
- Class vs Instance Attributes
- `__str__` and `__repr__`
- Class Methods (`@classmethod`)
- Static Methods (`@staticmethod`)

### Inheritance & Polymorphism (Problems 021-030)
- Basic Inheritance
- Method Overriding
- `super()` Function
- `isinstance()` and `issubclass()`
- Multiple Inheritance
- Method Resolution Order (MRO)
- Polymorphism
- Abstract Base Classes (ABC)

### Encapsulation & Properties (Problems 015-020, 033)
- Public, Protected, Private Attributes
- Property Decorators
- Getters and Setters
- Descriptors

### Magic/Dunder Methods (Problems 026-032)
- `__eq__`, `__lt__`, `__gt__` (Comparison)
- `__add__`, `__sub__`, `__mul__` (Arithmetic)
- `__hash__` (Hashability)
- `__len__`, `__getitem__`, `__setitem__` (Containers)
- `__call__` (Callable Objects)
- `__enter__`, `__exit__` (Context Managers)

### Advanced OOP (Problems 034-047)
- `__slots__` Optimization
- Composition vs Inheritance
- Mixins
- Metaclasses
- `__getattr__`, `__setattr__`
- `__new__` vs `__init__`
- Iterators and Generators

### Data Structures (Problems 050-058)
- Linked List
- Stack
- Queue
- Binary Search Tree
- Hash Table
- Graph
- Heap
- LRU Cache
- Trie

### SOLID Principles (Problems 059-063)
- Single Responsibility Principle
- Open/Closed Principle
- Liskov Substitution Principle
- Interface Segregation Principle
- Dependency Inversion Principle

### Design Patterns (Problems 037-042, 071-078)
- Singleton
- Factory
- Observer
- Strategy
- Decorator (Pattern)
- Adapter
- Builder
- Prototype
- State
- Command
- Chain of Responsibility
- Proxy
- Facade
- Flyweight

### Real-World Applications (Problems 079-090)
- Card Game System
- File System (Composite Pattern)
- Event System (Pub/Sub)
- Plugin System
- Mini ORM
- Dependency Injection Container
- State Machine
- Parking Lot (Interview Classic)
- Library Management System
- Elevator System
- Chess Game
- URL Shortener

### Modern Python OOP (Problems 043-044, 065-067, 093-099)
- Dataclasses
- Named Tuples
- Type Hints
- Protocol Classes
- Enum Classes
- Async OOP
- Thread Safety
- Memory Management
- `__init_subclass__`
- Class Decorators
- functools for OOP

### Testing & Best Practices (Problems 091-092, 100)
- Unit Testing
- Serialization
- Best Practices Summary

## Interview Tips

### Common Interview Questions
1. "Explain the four pillars of OOP"
   - Encapsulation, Abstraction, Inheritance, Polymorphism

2. "What is the difference between a class and an object?"
   - Class is a blueprint, object is an instance

3. "Explain method resolution order in Python"
   - C3 linearization, left-to-right depth-first

4. "When would you use composition over inheritance?"
   - When you want "has-a" vs "is-a" relationship
   - When you need runtime flexibility

5. "What are magic methods?"
   - Methods with double underscores that Python calls implicitly

### System Design Tips
- Start with requirements clarification
- Identify main entities (nouns become classes)
- Identify relationships (inheritance, composition)
- Consider SOLID principles
- Think about scalability

### Code Interview Tips
- Think out loud
- Start with a simple solution, then optimize
- Consider edge cases
- Write clean, readable code
- Test your solution

## Prerequisites
- Basic Python syntax (variables, loops, functions)
- Basic understanding of data types

## Running the Problems
```bash
# Navigate to the folder
cd OOP-Python

# Run a specific problem
python 001_create_first_class.py

# After solving, uncomment the test code and run again
```

## Progress Tracker

- [ ] Fundamentals (001-020)
- [ ] Inheritance & Polymorphism (021-030)
- [ ] Magic Methods (026-032)
- [ ] Advanced OOP (033-049)
- [ ] Data Structures (050-058)
- [ ] SOLID Principles (059-063)
- [ ] Design Patterns (071-078)
- [ ] Real-World Applications (079-090)
- [ ] Modern Python (091-099)
- [ ] Best Practices (100)

Good luck with your interview preparation!
