"""
Write a function to search for a specific value in a linked list and return the position if found, otherwise return -1.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    
    def search(self, target):
        current = self
        pos = 1
        while current:
            if current.data == target:
                return pos
            current = current.next
            pos += 1
        return -1
    
    # Build: 5 -> 10 -> 15 -> 20 -> 25
node1 = Node(5)
node2 = Node(10)
node3 = Node(15)
node4 = Node(20)
node5 = Node(25)
node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5
head = node1

# Search for a value in the linked list
target_value = 15
position = head.search(target_value)
if position != -1:
    print(f"Value {target_value} found at position: {position}")
else:
    print(f"Value {target_value} not found in the linked list.")
