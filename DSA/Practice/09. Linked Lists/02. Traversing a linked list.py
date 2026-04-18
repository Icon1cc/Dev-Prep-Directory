"""
Write a function to traverse a linked list and print each element's value.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    
    def traverse_and_print(self):
        current = self
        while current:
            print(current.data)
            current = current.next
    

# Build: 10 -> 20 -> 15 -> 30
node1 = Node(10)
node2 = Node(20)
node3 = Node(15)
node4 = Node(30)
node1.next = node2
node2.next = node3
node3.next = node4  
head = node1
# Traverse and print the linked list
head.traverse_and_print()   