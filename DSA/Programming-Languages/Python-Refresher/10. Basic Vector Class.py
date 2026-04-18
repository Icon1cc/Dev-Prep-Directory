"""
Description: Create a class named Vector2D. The constructor should accept two arguments, x and y, and store them as instance attributes.
Example:
Input: v1 = Vector2D(3, 4)
Usage: print(v1.x, v1.y)
Output: 3 4
"""

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
# Creating an object
v1 = Vector2D(3, 4)
    
print(v1.x, v1.y)
