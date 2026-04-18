"""
Perform operations in stack 
1. Push
2. Pop
3. Peek
4. IsEmpty
5. Size
"""

class Stack:
    def __init__(self):
        self.stack = []
    
    def push(self, data):
        self.stack.append(data)
    
    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            raise IndexError("Stack Underflow")
    
    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            raise IndexError("Stack is empty")
    
    def is_empty(self):
        return len(self.stack) == 0
    
    def size(self):
        return len(self.stack)
    
# --- Test It ---
s = Stack()
s.push(10)
s.push(20)
s.push(30)
print("Top element:", s.peek())  # Should print 30
print("Stack size:", s.size())    # Should print 3
print("Popped element:", s.pop())  # Should print 30
print("Top element after pop:", s.peek())  # Should print 20
print("Is stack empty?", s.is_empty())  # Should print False
s.pop()
s.pop()
print("Is stack empty after popping all elements?", s.is_empty())  # Should print True  