"""
Implementing a Queue in Python using Deque
"""

from collections import deque

class Queue:
    def __init__(self):
        """Initialize an empty deque to represent the queue."""
        self.items = deque()

    def enqueue(self, item):
        """Add an element to the rear of the queue. O(1) complexity."""
        self.items.append(item)
        print(f"Enqueued: {item}")

    def dequeue(self):
        """Remove and return the front element. O(1) complexity."""
        if not self.is_empty():
            return self.items.popleft()
        else:
            raise IndexError("Dequeue from an empty queue")

    def display(self):
        """Show all elements in the queue."""
        return list(self.items)

    def get_front(self):
        """Retrieve the front element without removing it."""
        if not self.is_empty():
            return self.items[0]
        return "Queue is empty"

    def get_rear(self):
        """Retrieve the rear element without removing it."""
        if not self.is_empty():
            return self.items[-1]
        return "Queue is empty"

    def is_empty(self):
        """Check if the queue is empty."""
        return len(self.items) == 0

    def size(self):
        """Check the number of elements in the queue."""
        return len(self.items)

# --- Demonstration ---
if __name__ == "__main__":
    q = Queue()
    
    # Adding elements
    q.enqueue("Task 1")
    q.enqueue("Task 2")
    q.enqueue("Task 3")
    
    print(f"\nCurrent Queue: {q.display()}")
    print(f"Front: {q.get_front()} | Rear: {q.get_rear()}")
    
    # Removing an element
    print(f"Processing: {q.dequeue()}")
    
    print(f"Queue after processing: {q.display()}")
    print(f"Total remaining tasks: {q.size()}")