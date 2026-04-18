"""
Recursively reverse a linked list using TAIL RECURSION.
Strategy: Reverse the current node immediately, then move to the next.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# --- Internal Helper Function ---
# This does the actual work. It needs 'prev' and 'curr' to track state.
def _reverse_recursive_helper(prev, curr):
    # BASE CASE:
    # If we have reached the end (curr is None), 
    # then 'prev' must be the new Head of the reversed list.
    if curr is None:
        return prev
    
    # 1. Save the next node (so we don't lose the rest of the list)
    next_node = curr.next
    
    # 2. Reverse the link (Point current node backwards)
    curr.next = prev
    
    # 3. Recursive Call (The "Step Forward")
    # We pass 'curr' as the new 'prev', and 'next_node' as the new 'curr'.
    return _reverse_recursive_helper(curr, next_node)


# --- Main Function ---
# This is the nice wrapper the user calls.
def reverse_linked_list(head):
    # We start with 'prev' as None (because the first node points to nothing)
    # and 'curr' as the head.
    return _reverse_recursive_helper(None, head)


def print_list(head):
    temp = head
    while temp:
        print(f"{temp.data} -> ", end="")
        temp = temp.next
    print("None")

# --- Driver Code ---
if __name__ == "__main__":
    # Create list: 10 -> 20 -> 30
    head = Node(10)
    head.next = Node(20)
    head.next.next = Node(30)

    print("Original List: ", end="")
    print_list(head)

    # Call the wrapper function
    head = reverse_linked_list(head)

    print("Reversed List: ", end="")
    print_list(head)