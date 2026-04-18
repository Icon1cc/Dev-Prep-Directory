"""
Problem 092: Object Serialization (Pickle and JSON)

Difficulty: Intermediate
Topic: Data Persistence

=== PROBLEM DESCRIPTION ===

Learn how to serialize and deserialize Python objects for storage and
transmission. Compare pickle (Python-specific) and JSON (universal).

Your Task:
-----------
1. Create classes to serialize:
   - `Person` with name, age, address
   - `Address` with street, city, country
   - `Company` with name, employees (list of Person)

2. Implement pickle serialization:
   - `save_pickle(obj, filename)`
   - `load_pickle(filename)`
   - Understand __getstate__ and __setstate__

3. Implement JSON serialization:
   - Custom `to_dict()` method
   - Custom `from_dict()` classmethod
   - Use json.JSONEncoder/JSONDecoder subclasses

4. Implement custom __reduce__ for pickle:
   - Control exactly how object is pickled
   - Useful for objects with external resources

5. Compare and understand:
   - When to use pickle vs JSON
   - Security considerations (pickle is unsafe for untrusted data!)
   - Versioning and compatibility

Expected Output:
----------------
Original Person: Alice (30) at 123 Main St, NYC

Pickle serialization:
Saved to person.pkl (156 bytes)
Loaded: Alice (30) at 123 Main St, NYC

JSON serialization:
{
    "name": "Alice",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "NYC",
        "country": "USA"
    }
}
Loaded from JSON: Alice (30) at 123 Main St, NYC

Company with employees:
TechCorp: 3 employees
JSON: {"name": "TechCorp", "employees": [...]}

=== CONCEPTS TO LEARN ===
- pickle.dump/load for binary serialization
- json.dumps/loads for text serialization
- Custom serialization methods
- Security implications of pickle

=== STARTER CODE ===
"""

import pickle
import json

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate serialization and deserialization
