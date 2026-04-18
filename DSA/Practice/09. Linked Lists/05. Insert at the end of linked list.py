"""
Implement a function to insert a new node with a given value at the end of a singly linked list.
"""

class Node:
    def __init__(self, data):
        self.data = data 
        self.next = None

def insert_at_end(head, value):
    """
    Traverses to the end of the list and appends a new node.
    """
    new_node = Node(value)

    # Edge Case: If the list is empty, the new node becomes the head
    if head is None:
        return new_node

    # 1. Traverse to the last node
    current = head
    while current.next:
        current = current.next

    # 2. Link the last node to the new node
    current.next = new_node
    
    return head

# --- Driver Code ---

# Create the first node
head = Node(1)

# Insert new nodes at the end
head = insert_at_end(head, 2)
head = insert_at_end(head, 3)

# Print the linked list
print("Linked List contents:")
current = head
while current:
    print(f"{current.data} -> ", end="")
    current = current.next
print("None")