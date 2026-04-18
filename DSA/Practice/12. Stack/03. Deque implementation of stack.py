"""
Implemmentation of stack using deque
Operations:
1. Push
2. Pop
3. Peek
4. IsEmpty
5. Size
"""

from collections import deque

class StackDeque:
    def __init__(self):
        # Initialize an empty deque
        self.stack = deque()

    # 1. Push: Add element to the top
    def push(self, item):
        self.stack.append(item)
        print(f"--> Pushed: {item}")

    # 2. Pop: Remove element from the top
    def pop(self):
        if self.is_empty():
            print("Stack Underflow! (Empty)")
            return None
        return self.stack.pop()

    # 3. Peek: Look at the top element without removing it
    def peek(self):
        if self.is_empty():
            print("Stack is Empty")
            return None
        # Access the last element (Top of stack)
        return self.stack[-1]

    # 4. IsEmpty: Check if stack has no elements
    def is_empty(self):
        return len(self.stack) == 0

    # 5. Size: Return number of elements
    def size(self):
        return len(self.stack)

    def display(self):
        print(f"Current Stack: {list(self.stack)}")


# --- Interactive Driver Code ---
if __name__ == "__main__":
    s = StackDeque()
    
    while True:
        print("\n--- STACK (DEQUE) OPERATIONS ---")
        print("1. Push")
        print("2. Pop")
        print("3. Peek")
        print("4. Is Empty?")
        print("5. Size")
        print("6. Display")
        print("7. Exit")
        
        try:
            choice = int(input("Enter choice: "))
            
            if choice == 1:
                val = input("Enter value to push: ")
                s.push(val)
            elif choice == 2:
                print(f"Popped: {s.pop()}")
            elif choice == 3:
                print(f"Top Element: {s.peek()}")
            elif choice == 4:
                print(f"Is Empty: {s.is_empty()}")
            elif choice == 5:
                print(f"Size: {s.size()}")
            elif choice == 6:
                s.display()
            elif choice == 7:
                print("Exiting...")
                break
            else:
                print("Invalid Choice")
        except ValueError:
            print("Please enter a valid number.")