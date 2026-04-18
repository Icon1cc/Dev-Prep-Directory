"""
Write a program to implement basic operations of a queue data structure using a list in Python. The operations should include:
1. Enqueue: Add an element to the rear of the queue.
2. Dequeue: Remove an element from the front of the queue.
3. Display: Show all elements in the queue.
4. Get Front: Retrieve the front element of the queue without removing it.
5. Get Rear: Retrieve the rear element of the queue without removing it.
6. Check if the queue is empty.
7. Check the size of the queue.
"""

from collections import deque
from queue import Queue

class FastQueue:
    def __init__(self):
        # deque is much faster for popping from the left
        self.queue = deque()

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.popleft() # O(1) complexity
        raise IndexError("Dequeue from empty queue")

    def get_front(self):
        return self.queue[0] if not self.is_empty() else None

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)
    
# Example usage:
if __name__ == "__main__":
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    print("Queue:", q.display())
    print("Front element:", q.get_front())
    print("Rear element:", q.get_rear())
    print("Dequeue element:", q.dequeue())
    print("Queue after dequeue:", q.display())
    print("Is the queue empty?", q.is_empty())
    print("Size of the queue:", q.size())