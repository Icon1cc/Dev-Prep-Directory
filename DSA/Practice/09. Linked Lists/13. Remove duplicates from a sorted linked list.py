"""
Write a python function to remove duplicates from a sorted linked list.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def remove_duplicates(head):
    """
    Traverses a sorted list and removes any node that has the same value 
    as the current node.
    """
    current = head

    # Loop until we reach the last node
    # We need current.next to exist so we can compare data
    while current is not None and current.next is not None:
        
        # Check if the neighbor has the same value
        if current.data == current.next.data:
            # SKIP the next node (Delete it)
            # We do NOT move 'current' forward yet, because the new neighbor 
            # might also be a duplicate (e.g., 1 -> 1 -> 1)
            current.next = current.next.next
        else:
            # No duplicate found, safe to move to the next node
            current = current.next
            
    return head

def print_list(head):
    current = head
    while current:
        print(f"{current.data} -> ", end="")
        current = current.next
    print("None")

# --- Driver Code ---
if __name__ == "__main__":
    # Case 1: Triple duplicate (1 -> 1 -> 1 -> 2)
    head = Node(1)
    head.next = Node(1)
    head.next.next = Node(1)
    head.next.next.next = Node(2)
    head.next.next.next.next = Node(3)
    head.next.next.next.next.next = Node(3)

    print("Original List: 1 -> 1 -> 1 -> 2 -> 3 -> 3")
    
    remove_duplicates(head)
    
    print("Cleaned List:  ", end="")
    print_list(head)