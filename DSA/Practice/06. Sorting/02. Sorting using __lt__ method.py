"""
Write a python program to sort a list of user-defined objects by implementing the __lt__ method.
"""

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
# Create a list of Point objects
points = [Point(1, 2), Point(3, 1), Point(2, 2), Point(1, 1), Point(2, 1)]
# Sort the list of points using the __lt__ method
sorted_points = sorted(points)
# Print the sorted list of points
print("Sorted Points:", sorted_points)