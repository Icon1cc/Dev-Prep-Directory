"""
Write a function that takes head of a circular linked list and a value, and inserts a new node with the given value at the end of the list.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        # We only need to store the TAIL.
        # Why? Because in a circle, Head is just tail.next!
        self.tail = None

    def insert_at_end(self, value):
        new_node = Node(value)

        # Case 1: List is empty
        if self.tail is None:
            self.tail = new_node
            self.tail.next = new_node  # Points to itself
        
        # Case 2: List is not empty (The O(1) Operation)
        else:
            # 1. Point new node to the current Head (tail.next)
            new_node.next = self.tail.next
            
            # 2. Point the old tail to the new node
            self.tail.next = new_node
            
            # 3. Update the 'tail' pointer to be the new node
            self.tail = new_node

    def display(self):
        if self.tail is None:
            print("List is empty")
            return

        # Start from Head (which is tail.next)
        head = self.tail.next
        temp = head
        while True:
            print(temp.data, end=" -> ")
            temp = temp.next
            if temp == head:
                break
        print("(HEAD)")

# --- Usage Example ---
cll = CircularLinkedList()

# 1. Insert 10 (List: 10)
cll.insert_at_end(10)

# 2. Insert 20 (List: 10 -> 20)
cll.insert_at_end(20)

# 3. Insert 30 (List: 10 -> 20 -> 30)
cll.insert_at_end(30)

cll.display()