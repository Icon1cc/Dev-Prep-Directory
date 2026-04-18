"""
Write a function to delete the head of a circular linked list. The function should take the head of the circular linked list as input and return the new head of the circular linked list after deletion.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def delete_head(head):
    # Case 1: Empty List
    if head is None:
        return None

    # Case 2: Only one node in the list
    # (The node points to itself)
    if head.next == head:
        return None

    # Case 3: Multiple nodes
    # We need to find the tail (last node) to update its 'next' pointer
    current = head
    while current.next != head:
        current = current.next
    
    # 'current' is now the tail.
    # 1. Point tail to the new head (head.next)
    current.next = head.next
    
    # 2. The new head is the second node
    new_head = head.next
    
    # (Optional: Clear the old head's next pointer for safety)
    head.next = None
    
    return new_head

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

# 1. Create List: 10 -> 20 -> 30 -> 40
head = Node(10)
node2 = Node(20)
node3 = Node(30)
node4 = Node(40)

head.next = node2
node2.next = node3
node3.next = node4
node4.next = head # Circular link

print("Original:")
display(head)

# 2. Delete Head (10)
head = delete_head(head)

print("After Deleting Head:")
display(head)