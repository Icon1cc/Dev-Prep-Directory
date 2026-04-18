"""
Write a function to delete the kth node of a circular linked list. The function should take the head of the circular linked list and the integer k as input and return the new head of the circular linked list after deletion.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def delete_kth_node(head, k):
    # Case 1: List is empty
    if head is None:
        return None

    # Case 2: Only 1 node in the list
    if head.next == head:
        # If we delete the only node, list becomes empty
        return None

    # Case 3: Deleting the First Node (Head)
    if k == 1:
        # We must find the tail to redirect it to the new head
        current = head
        while current.next != head:
            current = current.next
        
        # current is now the tail
        current.next = head.next  # Tail points to 2nd node
        head = head.next          # Move head to 2nd node
        return head

    # Case 4: Deleting any other node (k > 1)
    else:
        current = head
        # We need to stop at the node BEFORE the one we want to delete
        # So we jump k-2 times.
        # Example: to delete 3rd node (k=3), we want to stop at 2nd node.
        for _ in range(k - 2):
            current = current.next
            # Safety check: if k is larger than list length, this might loop endlessly
            # or we might want to handle it. For now, assuming valid k.
        
        # Now 'current' is the node BEFORE the target.
        # The node to delete is current.next
        node_to_delete = current.next
        
        # Skip the node to delete
        current.next = node_to_delete.next
        
        return head

# --- Usage Example ---
def display(head):
    if not head:
        print("List is empty")
        return
    nodes = []
    temp = head
    while True:
        nodes.append(str(temp.data))
        temp = temp.next
        if temp == head:
            break
    print(" -> ".join(nodes) + " -> (HEAD)")

# Create List: 10 -> 20 -> 30 -> 40 -> 50
head = Node(10)
nodes = [Node(20), Node(30), Node(40), Node(50)]
curr = head
for n in nodes:
    curr.next = n
    curr = n
curr.next = head # Make it circular

print("Original List:")
display(head)

# Delete the 3rd node (Node 30)
k = 3
head = delete_kth_node(head, k)
print(f"\nAfter deleting {k}rd node:")
display(head)

# Delete the 1st node (Node 10)
k = 1
head = delete_kth_node(head, k)
print(f"\nAfter deleting {k}st node:")
display(head)