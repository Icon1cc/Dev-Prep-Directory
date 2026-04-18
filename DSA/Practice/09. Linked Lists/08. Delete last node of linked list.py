"""
Write a function to delete the last node of the linked list.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def delete_last_node(head):

        if head is None:
            print("Error: List is empty. Cannot delete.")
            return None

        if head.next is None:
            return None
        
        current = head

        while current.next.next:
            current = current.next
        
        current.next = None

        return head
    
# --- Driver Code ---
# Build a list: 10 -> 20 -> 30
head = Node(10)
head.next = Node(20)
head.next.next = Node(30)
print("Original List: 10 -> 20 -> 30")
# Delete the last node
head = Node.delete_last_node(head)
# Print result
current = head
while current:  
    print(current.data, end=" -> " if current.next else "\n")
    current = current.next
print("None")