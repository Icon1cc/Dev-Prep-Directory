"""
Write a function that takes head as an argument and inserts a new node with given data in the middle of the linked list.
"""

"""
Function to insert a node in the middle of a Singly Linked List.
Strategy: Use the 'Tortoise and Hare' (Slow/Fast pointer) technique.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def insert_in_middle(head, new_node):
    # Case 1: If the linked list is empty, the new node becomes the head
    if head is None:
        return new_node
    
    # Step 1: Initialize two pointers starting at the head
    slow = head  # The Tortoise (moves 1 step)
    fast = head  # The Hare (moves 2 steps)

    # Step 2: Move fast pointer 2 steps and slow pointer 1 step
    # We loop as long as 'fast' has a valid next step and a step after that.
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next          # Move forward 1 node
        fast = fast.next.next     # Move forward 2 nodes
    
    # At this point, 'slow' is pointing to the middle node.
    # Example: In 1->2->3->4->5, 'slow' stops at 3.
    
    # Step 3: Perform the insertion (The "Safe Hand-Off")
    
    # 1. New node points to the second half of the list (what slow was pointing to)
    new_node.next = slow.next
    
    # 2. Middle node (slow) updates to point to the new node
    slow.next = new_node

    return head

# --- Driver Code to Test the Logic ---

# Create a list: 10 -> 20 -> 40 -> 50
head = Node(10)
head.next = Node(20)
head.next.next = Node(40)
head.next.next.next = Node(50)

print("Original List: 10 -> 20 -> 40 -> 50")

# We want to insert 30 in the middle
node_to_insert = Node(30)
head = insert_in_middle(head, node_to_insert)

# Print Result
print("Updated List:  ", end="")
current = head
while current:
    print(f"{current.data} -> ", end="")
    current = current.next
print("None")

