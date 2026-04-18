"""
Implementing stack using Linked List in Python
Operations:
1. Push
2. Pop
3. Peek
4. IsEmpty
5. Size
"""

# 1. Create the Node Class
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# 2. Create the Stack Class
class StackLinkedList:
    def __init__(self):
        self.top = None  # This is the 'Head' of the list
        self.count = 0   # Track size to avoid traversing (O(1) size)

    # 1. Push: Add element to the Top (Head)
    def push(self, item):
        new_node = Node(item)
        new_node.next = self.top  # Point new node to old top
        self.top = new_node       # Update top to be the new node
        self.count += 1
        print(f"Pushed: {item}")

    # 2. Pop: Remove element from the Top (Head)
    def pop(self):
        if self.is_empty():
            return "Stack Underflow (Empty)"
        
        popped_data = self.top.data
        self.top = self.top.next  # Move top pointer to the next node
        self.count -= 1
        return popped_data

    # 3. Peek: Return Top element without removing
    def peek(self):
        if self.is_empty():
            return "Stack is Empty"
        return self.top.data

    # 4. IsEmpty: Check if top is None
    def is_empty(self):
        return self.top is None

    # 5. Size: Return the tracked count
    def size(self):
        return self.count

    # Helper: Display the full stack
    def display(self):
        if self.is_empty():
            print("Stack is Empty")
            return
        current = self.top
        print("Stack (Top -> Bottom):", end=" ")
        while current:
            print(f"| {current.data} | ->", end=" ")
            current = current.next
        print("None")


# --- Driver Code ---
if __name__ == "__main__":
    s = StackLinkedList()

    s.push(10)
    s.push(20)
    s.push(30)
    
    s.display()  # 30 -> 20 -> 10
    
    print(f"Top Element: {s.peek()}")   # 30
    print(f"Popped: {s.pop()}")         # 30
    
    s.display()  # 20 -> 10
    
    print(f"Size: {s.size()}")          # 2