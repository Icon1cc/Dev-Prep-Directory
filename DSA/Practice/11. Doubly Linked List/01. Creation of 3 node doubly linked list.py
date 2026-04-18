"""
Create a 3 node doubly linked list with the following data: 10, 20, 30
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

# 1. Create nodes
node1 = Node(10)
node2 = Node(20)
node3 = Node(30)    

# 2. Connect nodes (Doubly Linked)
node1.next = node2
node2.prev = node1

node2.next = node3
node3.prev = node2

# Function to display Forward (using .next)
def display_forward(head):
    print("Forward List: ", end="")
    if not head:
        print("List is empty")
        return
    nodes = []
    temp = head
    while temp:
        nodes.append(str(temp.data))
        temp = temp.next
    print(" <-> ".join(nodes))

# Function to display Backward (using .prev)
def display_backward(tail):
    print("Backward List:", end=" ")
    temp = tail
    nodes = []
    
    # We traverse using .prev until we hit None
    while temp:
        nodes.append(str(temp.data))
        temp = temp.prev
    print(" <-> ".join(nodes))

# --- EXECUTION ---

# Call the functions!
display_forward(node1)   # Pass the HEAD (10)
display_backward(node3)  # Pass the TAIL (30)