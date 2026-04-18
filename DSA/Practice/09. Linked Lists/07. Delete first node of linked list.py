"""
Implement a function to delete the first node of a linked list
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
def delete_first_node(head):
    # Case 1: If the list is empty
    if head is None:
        print("Error: List is empty. Cannot delete.")
        return None

    # Case 2: If the list has at least one node
    new_head = head.next
    head.next = None  # Optional: Clear the next of the old head
    return new_head

# --- Driver Code ---
# Build a list: 10 -> 20 -> 30
head = Node(10)
head.next = Node(20)
head.next.next = Node(30)
print("Original List: 10 -> 20 -> 30")
# Delete the first node
head = delete_first_node(head)
# Print result
current = head
while current:
    print(current.data, end=" -> " if current.next else "\n")
    current = current.next
print("None")