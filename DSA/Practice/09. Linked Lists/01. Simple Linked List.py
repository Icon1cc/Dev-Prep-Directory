"""
Implement a simple linked list in Python
"""

# Just a simple Node class for linked list
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# Build: 10 -> 20 -> 30
temp1 = Node(10)
temp2 = Node(20)
temp3 = Node(30)

temp1.next = temp2
temp2.next = temp3

head = temp1


# Optional: print the list to verify
current = head
while current:
    print(current.data)
    current = current.next
