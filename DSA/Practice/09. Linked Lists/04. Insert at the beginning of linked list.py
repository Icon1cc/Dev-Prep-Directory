"""
Write a function to insert a new node at the beginning of a linked list.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None 

def insert_at_beginning(head, new_data):
    """
    Inserts a new node at the beginning of the list 
    and returns the new head.
    """
    # 1. Allocate the Node & put in the data
    new_node = Node(new_data)
    
    # 2. Make next of new Node as head
    new_node.next = head
    
    # 3. Return the new node (which is now the head)
    return new_node

# --- Driver Code ---

# Build initial list: 30 -> 40
head = Node(30)
head.next = Node(40)

# Insert 20 at the beginning
# List becomes: 20 -> 30 -> 40
head = insert_at_beginning(head, 20)

# Insert 10 at the beginning
# List becomes: 10 -> 20 -> 30 -> 40
head = insert_at_beginning(head, 10)

# Print the updated linked list
print("Linked List contents:")
current = head
while current:
    print(f"{current.data} -> ", end="")
    current = current.next
print("None")