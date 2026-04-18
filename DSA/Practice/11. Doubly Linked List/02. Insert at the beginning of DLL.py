"""
Write a function to insert a new node at the beginning of a doubly linked list. 
The function should take the head of the doubly linked list and the data for the new node as input.
It should return the new head of the doubly linked list after insertion.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

def insert_at_beginning(head, data):
    new_node = Node(data)

    # If the list is empty, the new node becomes the head
    if head is None:
        return new_node

    # Otherwise, we need to insert the new node before the current head
    new_node.next = head     # New node points to current head
    head.prev = new_node     # Current head points back to new node
    return new_node          # New node is the new head

# Helper function to create list from user input
def create_doubly_linked_list(arr):
    if not arr:
        return None
    
    head = Node(int(arr[0]))
    current = head
    
    for i in range(1, len(arr)):
        new_node = Node(int(arr[i]))
        current.next = new_node  # Link forward
        new_node.prev = current  # Link backward
        current = new_node       # Move current
        
    return head

def display(head):
    if not head:
        print("List is empty")
        return
    nodes = []
    temp = head
    while temp:
        nodes.append(str(temp.data))
        temp = temp.next
    print(" <-> ".join(nodes))

# --- Main Execution ---

# 1. Get input for the initial list
user_input = input("Enter the list values separated by space (e.g., 10 20 30): ")
values = user_input.split()

# Create the list
head = create_doubly_linked_list(values)
print("Original List:")
display(head)

# 2. Get input for the new node
val_to_insert = int(input("Enter value to insert at beginning: "))

# 3. Insert and update head
head = insert_at_beginning(head, val_to_insert)

print("Updated List:")
display(head)