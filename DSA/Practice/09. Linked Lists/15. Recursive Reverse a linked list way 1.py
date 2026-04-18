"""
Recursively reverse a linked list. 
Strategy: Go to the bottom, then reverse connections as we come back up.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def recursive_reverse(head):
    # --- BASE CASE ---
    # 1. If list is empty (head is None) -> Return None
    # 2. If single node (head.next is None) -> This is the new Head! Return it.
    if head is None or head.next is None:
        return head

    # --- RECURSIVE STEP (Diving Down) ---
    # We call the function on the neighbor.
    # This loop continues until we hit the last node (the Base Case).
    # 'new_head' will be the LAST node of the original list.
    new_head = recursive_reverse(head.next)

    # --- UNWINDING STEP (Coming Back Up) ---
    # We are now sitting at 'head'. 
    # 'head.next' is the node that was originally in front of us.
    
    # 1. Make the next node point BACK to us
    # Example: If 4 -> 5, we make 5 point to 4.
    head.next.next = head
    
    # 2. Break our own forward link to avoid a cycle
    # (Node 4 stops pointing to 5, so it points to None for now)
    head.next = None

    # 3. Pass the new head (the original last node) up the chain
    return new_head

def print_list(head):
    temp = head
    while temp:
        print(f"{temp.data} -> ", end="")
        temp = temp.next
    print("None")

# --- Driver Code ---
if __name__ == "__main__":
    # Create list: 1 -> 2 -> 3
    head = Node(1)
    head.next = Node(2)
    head.next.next = Node(3)

    print("Original List: ", end="")
    print_list(head)

    # The function returns the NEW head (which was the old last node)
    head = recursive_reverse(head)

    print("Reversed List: ", end="")
    print_list(head)