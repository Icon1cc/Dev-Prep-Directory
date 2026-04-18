"""
Problem 054: Building a Hash Table Class

Difficulty: Advanced
Topic: Data Structure Implementation

=== PROBLEM DESCRIPTION ===

A hash table uses a hash function to map keys to indices in an array.
It provides O(1) average time for insert, search, and delete operations.

Your Task:
-----------
1. Create a `HashTable` class with chaining (linked list at each bucket):
   - `__init__(size=10)` - initialize with given capacity
   - `_hash(key)` - hash function: hash(key) % size
   - `put(key, value)` - insert or update key-value pair
   - `get(key)` - return value for key (raise KeyError if not found)
   - `remove(key)` - delete key-value pair
   - `contains(key)` - return True if key exists
   - `keys()` - return all keys
   - `values()` - return all values
   - `items()` - return all (key, value) pairs

2. Implement `__getitem__`, `__setitem__`, `__delitem__`:
   - Allow dict-like syntax: ht[key] = value, ht[key], del ht[key]

3. Implement automatic resizing:
   - When load factor (items/size) > 0.75, double the size
   - Rehash all existing items

Expected Output:
----------------
ht['name'] = Alice
ht['age'] = 30
Contains 'name': True
Keys: ['name', 'age', 'city']
Items: [('name', 'Alice'), ('age', 30), ('city', 'NYC')]
After delete: Contains 'age': False

=== CONCEPTS TO LEARN ===
- Hash function converts key to array index
- Collision handling: chaining or open addressing
- Load factor determines when to resize
- Foundation of dictionaries and sets

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# ht = HashTable()
#
# # Test put/get
# ht['name'] = 'Alice'
# ht['age'] = 30
# ht['city'] = 'NYC'
#
# print(f"ht['name'] = {ht['name']}")
# print(f"ht['age'] = {ht['age']}")
# print(f"Contains 'name': {ht.contains('name')}")
# print(f"Keys: {ht.keys()}")
# print(f"Items: {ht.items()}")
#
# # Test delete
# del ht['age']
# print(f"After delete: Contains 'age': {ht.contains('age')}")
