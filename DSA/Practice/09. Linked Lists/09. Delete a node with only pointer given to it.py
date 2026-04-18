"""
Write a function to delete a node with only a pointer given to it.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def delete_node_without_head(node_to_delete):
    """
    Deletes the node_to_delete by copying the next node's value 
    into it and then skipping the next node.
    """
    # Safety Check: We cannot delete the Last Node with this method
    # because there is no 'next' data to copy!
    if node_to_delete is None or node_to_delete.next is None:
        print("Error: Cannot delete the last node with this technique.")
        return

    # Step 1: Steal the data from the next node
    # Example: If we are '20' and next is '30', we become '30'.
    next_node = node_to_delete.next
    node_to_delete.data = next_node.data

    # Step 2: Delete the next node (which we just copied)
    # We point our 'next' to the node AFTER the next one.
    node_to_delete.next = next_node.next

# --- Driver Code ---

head = Node(10)
node_20 = Node(20) # We keep a variable for this so we can pass it directly
node_30 = Node(30)
head.next = node_20
node_20.next = node_30

print("Original List: 10 -> 20 -> 30")

# We want to delete '20', but we ONLY pass the node '20' itself.
delete_node_without_head(node_20)

# Print result
print("After Deletion: ", end="")
current = head
while current:
    print(f"{current.data} -> ", end="")
    current = current.next
print("None")