"""
Write a python function that takes head and n as arguments and returns the n-th node from the end of the linked list.
"""

class Node:
    """
    A class to represent a Node in a Singly Linked List.
    """
    def __init__(self, data):
        self.data = data
        self.next = None

def find_nth_from_end(head, n):
    """
    Finds the n-th node from the end of the list using the Two-Pointer technique.
    Returns the Node object, or None if n is invalid.
    """
    
    # Initialize two pointers. Both start at the head.
    first_pointer = head
    second_pointer = head

    # Step 1: Create a gap of size 'n'
    # Move first_pointer 'n' steps ahead.
    count = 0
    while count < n:
        if first_pointer is None:
            # Edge Case: The list is shorter than 'n'
            print(f"Error: List has fewer than {n} nodes.")
            return None
        
        first_pointer = first_pointer.next
        count += 1

    # Step 2: Move both pointers at the same speed
    # We slide the "gap" down the list until first_pointer falls off the end.
    while first_pointer is not None:
        first_pointer = first_pointer.next
        second_pointer = second_pointer.next

    # At this point, first_pointer is at None (end).
    # Since second_pointer is 'n' steps behind, it is exactly at the target.
    return second_pointer

# --- Driver Code ---
if __name__ == "__main__":
    # 1. Build a list: 10 -> 20 -> 30 -> 40 -> 50
    head = Node(10)
    head.next = Node(20)
    head.next.next = Node(30)
    head.next.next.next = Node(40)
    head.next.next.next.next = Node(50)

    print("Original List: 10 -> 20 -> 30 -> 40 -> 50")

    # 2. Test Case: Find the 2nd node from the end
    n = 2
    result_node = find_nth_from_end(head, n)

    if result_node:
        print(f"The {n}nd node from the end is: {result_node.data}")
    else:
        print("Node not found.")

    # 3. Test Case: Find the 5th node from the end (should be 10)
    n = 5
    result_node = find_nth_from_end(head, n)
    
    if result_node:
        print(f"The {n}th node from the end is: {result_node.data}")