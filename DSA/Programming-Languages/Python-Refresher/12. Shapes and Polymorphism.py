"""
12. Shapes and Polymorphism
Description: Define an abstract base concept for shapes.
Create a base class Shape with a method area() that raises a NotImplementedError.
Create a subclass Rectangle that inherits from Shape. Its constructor should accept width and height. It must implement the area() method correctly.
Create another subclass Circle that inherits from Shape. Its constructor should accept a radius. It must also implement the area() method correctly (use math.pi).
"""

import math 

class Shape:
    def area(self):
        raise NotImplementedError("Subclasses must implement the area method")

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
        return math.pi * self.radius * self.radius

width = float(input("Enter the width of the rectangle: "))
height = float(input("Enter the height of the rectangle: "))
radius = float(input("Enter the radius of the circle: "))

r = Rectangle(width, height)
c = Circle(radius)

print("Rectangle area:", r.area())
print("Circle area:", c.area())
