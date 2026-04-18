"""
Create a simple circular linked list with 4 nodes
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        
        # If the list is empty, make the new node the head and point it to itself
        if not self.head:
            self.head = new_node
            self.head.next = self.head
        else:
            # Traverse to the last node
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            
            # Point the last node to the new node
            temp.next = new_node
            # Point the new node back to the head
            new_node.next = self.head

    def display(self):
        nodes = []
        if self.head:
            temp = self.head
            while True:
                nodes.append(str(temp.data))
                temp = temp.next
                # Stop if we have circled back to the head
                if temp == self.head:
                    break
            # Visual representation of the circular connection
            print(" -> ".join(nodes) + " -> (HEAD)")
        else:
            print("List is empty")

# --- Usage Example ---

# 1. Create the list
cll = CircularLinkedList()

# 2. Add 4 nodes
cll.append("Node A")
cll.append("Node B")
cll.append("Node C")
cll.append("Node D")
# 3. Display the result
cll.display()
