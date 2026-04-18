"""
Write a function to insert a new node at the end of a doubly linked list. 
The function should take the head of the doubly linked list and the data for the new node as input.
It should return the new head of the doubly linked list after insertion.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

def insert_at_end(head, data):
    new_node = Node(data)

    # Case 1: If list is empty, new node is the head
    if head is None:
        return new_node

    # Case 2: Traverse to the last node
    current = head
    while current.next:
        current = current.next  # Stop when current.next is None

    # Link the nodes
    current.next = new_node  # Old tail points to new node
    new_node.prev = current  # New node points back to old tail
    
    return head              # Head stays the same!

# Helper: Create list from input
def create_doubly_linked_list(arr): 
    if not arr: 
        return None 
    head = Node(int(arr[0])) 
    current = head 
    for i in range(1, len(arr)): 
        new_node = Node(int(arr[i])) 
        current.next = new_node 
        new_node.prev = current 
        current = new_node 
    return head

# Helper: Display function
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

# 1. Input initial list
user_input = input("Enter list values (e.g., 10 20 30): ")
values = user_input.split() if user_input else []
head = create_doubly_linked_list(values)

print("Original List:")
display(head)

# 2. Input value to append
val_to_insert = int(input("Enter value to insert at end: "))

# 3. Perform insertion
head = insert_at_end(head, val_to_insert)

print("Updated List:")
display(head)