"""
Write a Python program to sort a list of user-defined objects based on multiple attributes.
"""

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
# Create a list of Point objects
points = [Point(1, 2), Point(3, 1), Point(2, 2), Point(1, 1), Point(2, 1)]
# Sort the list of points first by x coordinate, then by y coordinate
sorted_points = sorted(points, key=lambda p: (p.x, p.y))
# Print the sorted list of points
print("Sorted Points:", sorted_points)