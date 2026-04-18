"""
Reverse a singly linked list.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def reverse_linked_list(head):
    prev = None
    current = head

    while current is not None:
        # 1. Save the next node (so we don't lose the rest of the list)
        next_node = current.next
        
        # 2. Reverse the link (Point backwards)
        current.next = prev
        
        # 3. Move 'prev' forward (It becomes the new anchor)
        prev = current
        
        # 4. Move 'current' forward (To continue the loop)
        current = next_node
        
    # At the end, 'current' is None, and 'prev' is the new Head.
    return prev

def print_list(head):
    curr = head
    while curr:
        print(f"{curr.data} -> ", end="")
        curr = curr.next
    print("None")

# --- Driver Code ---
if __name__ == "__main__":
    # Build list: 1 -> 2 -> 3 -> 4 -> 5
    head = Node(1)
    head.next = Node(2)
    head.next.next = Node(3)
    head.next.next.next = Node(4)
    head.next.next.next.next = Node(5)

    print("Original List: ", end="")
    print_list(head)

    # Reverse it
    head = reverse_linked_list(head)

    print("Reversed List: ", end="")
    print_list(head)