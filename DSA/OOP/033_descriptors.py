"""
Problem 033: Descriptors (__get__, __set__, __delete__)

Difficulty: Advanced
Topic: Descriptor Protocol

=== PROBLEM DESCRIPTION ===

Descriptors are objects that customize attribute access. They implement the
descriptor protocol: __get__, __set__, and/or __delete__. Properties are
actually implemented using descriptors!

Your Task:
-----------
1. Create a descriptor class `PositiveNumber`:
   - `__init__(name)` - stores the attribute name
   - `__get__` - returns the stored value
   - `__set__` - validates that value is positive, raises ValueError if not
   - Store values in the instance's __dict__ to avoid infinite recursion

2. Create a class `Product`:
   - Use PositiveNumber descriptor for `price` and `quantity`
   - Attempting to set negative values should raise ValueError

3. Create a descriptor `TypeChecked`:
   - `__init__(name, expected_type)` - stores name and type
   - `__set__` - validates the value is of expected type
   - Example: TypeChecked("name", str) only accepts strings

Expected Output:
----------------
Product: Widget, Price: $25.00, Quantity: 100
Error setting negative price: Price must be positive
Error setting negative quantity: Quantity must be positive
Person: Alice (age 30)
Error setting wrong type: age must be of type <class 'int'>

=== CONCEPTS TO LEARN ===
- Descriptors control attribute access at the class level
- Data descriptors have __set__ or __delete__
- Non-data descriptors only have __get__
- Descriptors enable reusable attribute validation

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# # PositiveNumber descriptor
# product = Product("Widget", 25.00, 100)
# print(f"Product: {product.name}, Price: ${product.price:.2f}, Quantity: {product.quantity}")
#
# try:
#     product.price = -10
# except ValueError as e:
#     print(f"Error setting negative price: {e}")
#
# try:
#     product.quantity = -5
# except ValueError as e:
#     print(f"Error setting negative quantity: {e}")
#
# # TypeChecked descriptor
# person = Person("Alice", 30)
# print(f"Person: {person.name} (age {person.age})")
#
# try:
#     person.age = "thirty"  # Should fail - not an int
# except TypeError as e:
#     print(f"Error setting wrong type: {e}")
