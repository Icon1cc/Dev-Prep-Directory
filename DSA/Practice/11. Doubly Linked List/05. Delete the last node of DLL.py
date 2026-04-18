"""
Delete the last node of a doubly linked list (DLL).
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

def delete_tail(head):
    # Case 1: Empty List
    if head is None:
        return None
    
    # Case 2: Only one node in the list
    if head.next is None:
        return None  # List becomes empty
    
    # Case 3: Multiple nodes
    # Traverse to the last node
    curr = head
    while curr.next:
        curr = curr.next
    
    # 'curr' is now the last node (Tail)
    # 'curr.prev' is the second-to-last node (New Tail)
    
    curr.prev.next = None  # Disconnect the new tail from the old tail
    
    return head

# --- Helper Functions for Testing ---

def create_doubly_linked_list(arr):
    if not arr: return None
    head = Node(int(arr[0]))
    current = head
    for i in range(1, len(arr)):
        new_node = Node(int(arr[i]))
        current.next = new_node
        new_node.prev = current
        current = new_node
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

# 1. Create List
user_input = input("Enter list values (e.g., 10 20 30): ")
values = user_input.split()
head = create_doubly_linked_list(values)

print("Original List:")
display(head)

# 2. Delete Tail
head = delete_tail(head)

print("After Deleting Tail:")
display(head)