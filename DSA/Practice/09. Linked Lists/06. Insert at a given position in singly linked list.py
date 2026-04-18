"""
Implement a function to insert a new node with a given value at a given position in a singly linked list.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def insert_at_position(head, data, position):
    new_node = Node(data)

    # Case 1: Insert at the beginning (Position 1)
    if position == 1:
        new_node.next = head
        return new_node

    # Case 2: Traverse to the node just BEFORE the position
    current = head
    
    # We run the loop (position - 2) times to find the predecessor
    # Example: To insert at Pos 3, we need Node 2. Start at Node 1. 
    # Logic: 3 - 2 = 1 jump.
    for _ in range(position - 2):
        if current is None:
            break 
        current = current.next

    # Edge Case: If position is out of bounds
    if current is None:
        print(f"Error: Position {position} is out of bounds.")
        return head

    # Case 3: Perform the insertion
    new_node.next = current.next
    current.next = new_node

    return head

# --- Driver Code ---

# Build a list: 10 -> 20 -> 30
# Positions:   (1)   (2)   (3)
head = Node(10)
head.next = Node(20)
head.next.next = Node(30)

print("Original List (1-based): 10 -> 20 -> 30")

# Insert 25 at Position 3
# We want: 10 -> 20 -> 25 -> 30
head = insert_at_position(head, 25, 3)

# Insert 5 at Position 1
# We want: 5 -> 10 -> 20 -> 25 -> 30
head = insert_at_position(head, 5, 1)

# Print result
current = head
while current:
    print(f"{current.data} -> ", end="")
    current = current.next
print("None")