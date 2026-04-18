"""
Reverse a Doubly Linked List
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

def reverse(head):
    # Case 1: Empty List
    if head is None:
        return None
        
    current = head
    
    # Traverse and Swap
    while current is not None:
        # Swap the pointers
        current.prev, current.next = current.next, current.prev
        
        # Track the new head (it will be the last node processed)
        head = current
        
        # Move to the "next" node (which is now stored in prev!)
        current = current.prev
        
    return head

# --- Helper Functions ---
def create_doubly_linked_list(arr):
    if not arr: return None
    head = Node(int(arr[0]))
    curr = head
    for i in range(1, len(arr)):
        new_node = Node(int(arr[i]))
        curr.next = new_node
        new_node.prev = curr
        curr = new_node
    return head

def display(head):
    nodes = []
    curr = head
    while curr:
        nodes.append(str(curr.data))
        curr = curr.next
    print(" <-> ".join(nodes) if nodes else "Empty")

# --- Test It ---
vals = input("Enter list (e.g., 10 20 30): ").split()
head = create_doubly_linked_list(vals)

print("Original:")
display(head)

head = reverse(head)

print("Reversed:")
display(head)