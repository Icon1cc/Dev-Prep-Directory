"""
Write a function to delete the head of a doubly linked list.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

def delete_head(head):
    # Case 1: Empty List
    if head is None:
        return None
    
    # Case 2: Only one node
    if head.next is None:
        return None
    
    # Case 3: Multiple nodes
    new_head = head.next      # Move head forward
    new_head.prev = None      # Remove link to old head
    
    # Optional: Clean up old head (good practice in some languages, 
    # but Python's Garbage Collector handles it)
    head.next = None 
    
    return new_head

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

# 2. Create and Display
head = create_doubly_linked_list(values)
print("Original List:")
display(head)

# 3. Delete Head
print("\nDeleting Head...")
head = delete_head(head)

# 4. Display Result
print("Updated List:")
display(head)