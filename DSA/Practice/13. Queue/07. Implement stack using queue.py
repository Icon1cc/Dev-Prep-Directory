"""
Implementing a Stack using Queues in Python.
"""

from collections import deque

class StackUsingQueue:
    def __init__(self):
        """Initialize a single queue to act as a stack."""
        self.queue = deque()

    def push(self, x):
        """
        Push element x onto stack.
        Time Complexity: O(n)
        """
        # 1. Get the current size before adding the new item
        size = len(self.queue)
        
        # 2. Add the new element to the back
        self.queue.append(x)
        
        # 3. Rotate the queue: move all previous elements to the back
        # This puts the newest element at the front (Top of Stack)
        for _ in range(size):
            self.queue.append(self.queue.popleft())
        
        print(f"Pushed: {x}")

    def pop(self):
        """
        Removes the element on top of the stack and returns it.
        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        return self.queue.popleft()

    def top(self):
        """
        Get the top element.
        Time Complexity: O(1)
        """
        if self.is_empty():
            return "Stack is empty"
        return self.queue[0]

    def is_empty(self):
        """Returns whether the stack is empty."""
        return len(self.queue) == 0

    def size(self):
        """Returns the number of elements in the stack."""
        return len(self.queue)

# --- Demonstration ---
if __name__ == "__main__":
    s = StackUsingQueue()
    
    s.push(10)
    s.push(20)
    s.push(30)
    
    print(f"\nTop element: {s.top()}") # Should be 30
    
    print(f"Popped: {s.pop()}")       # Removes 30
    print(f"New Top: {s.top()}")      # Should be 20
    
    print(f"Stack size: {s.size()}")
    print(f"Is empty? {s.is_empty()}")