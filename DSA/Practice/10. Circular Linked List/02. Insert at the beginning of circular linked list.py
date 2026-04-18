"""
Insert a key at the beginning of a circular linked list.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        # We maintain both head and tail pointers for O(1) operations
        self.head = None
        self.tail = None

    def append(self, data):
        """Adds a node to the end of the list."""
        new_node = Node(data)
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            new_node.next = self.head # Point to itself
        else:
            self.tail.next = new_node # Link old tail to new node
            self.tail = new_node      # Move tail pointer to new node
            self.tail.next = self.head # Link new tail back to head

    def insert_at_beginning(self, key):
        """Inserts a node at the beginning of the list (O(1))."""
        new_node = Node(key)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            new_node.next = self.head
        else:
            new_node.next = self.head  # 1. New node points to current head
            self.tail.next = new_node  # 2. Tail updates its 'next' to new node
            self.head = new_node       # 3. Head pointer moves to new node

    def display(self):
        """Prints the list."""
        if self.head is None:
            print("List is empty")
            return

        current = self.head
        nodes = []
        while True:
            nodes.append(str(current.data))
            current = current.next
            if current == self.head:
                break
        print(" -> ".join(nodes) + " -> (HEAD)")

# --- User Input Section ---

cll = CircularLinkedList()

# 1. Input for the initial list
print("Enter the list elements separated by spaces (e.g., 1 2 3 4):")
elements = input().split()
for el in elements:
    cll.append(el)

print("\nOriginal List:")
cll.display()

# 2. Input for the key to insert at beginning
key = input("\nEnter the key to insert at the beginning: ")
cll.insert_at_beginning(key)

# 3. Final Output
print("\nUpdated List:")
cll.display()