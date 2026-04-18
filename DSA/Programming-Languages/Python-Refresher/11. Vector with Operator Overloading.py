"""
Vector with Operator Overloading
Description: Extend the Vector2D class from the previous problem. Implement the following special methods:
__add__(self, other): This method should allow two Vector2D objects to be added together using the + operator. The addition should be component-wise (i.e., new x is self.x + other.x). It should return a new Vector2D object.
__str__(self): This method should return a string representation of the vector in the format "(x, y)".
"""

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __str__(self):
        return f"({self.x},{self.y})"

v1 = Vector2D(2, 3)
v2 = Vector2D(3, 4)
v3 = v1 + v2
print(v3)