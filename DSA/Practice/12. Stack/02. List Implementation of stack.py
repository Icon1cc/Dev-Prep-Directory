"""
Implementing Stack using List in Python
Operations:
1. Push
2. Pop
3. Peek
4. IsEmpty
5. Size
"""

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)
        print(f"--> Pushed {item} onto stack.")

    def pop(self):
        if self.is_empty():
            return "Stack is Empty"
        return self.stack.pop()

    def peek(self):
        if self.is_empty():
            return "Stack is Empty"
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

    def display(self):
        print("Current Stack:", self.stack)


# --- Interactive Driver Code ---
if __name__ == "__main__":
    s = Stack()
    
    while True:
        print("\n--- STACK OPERATIONS ---")
        print("1. Push")
        print("2. Pop")
        print("3. Peek (Top Element)")
        print("4. Is Empty?")
        print("5. Size")
        print("6. Display Stack")
        print("7. Exit")
        
        try:
            choice = int(input("Enter your choice (1-7): "))
            
            if choice == 1:
                val = input("Enter value to push: ")
                s.push(val)
                
            elif choice == 2:
                print(f"--> Popped element: {s.pop()}")
                
            elif choice == 3:
                print(f"--> Top element: {s.peek()}")
                
            elif choice == 4:
                print(f"--> Is Stack Empty? {s.is_empty()}")
                
            elif choice == 5:
                print(f"--> Stack Size: {s.size()}")
                
            elif choice == 6:
                s.display()
                
            elif choice == 7:
                print("Exiting...")
                break
                
            else:
                print("Invalid choice! Please select 1-7.")
                
        except ValueError:
            print("Please enter a valid number.")
    

