"""
Circular List implementation of Queue in Python.
"""

class CircularQueue:
    def __init__(self, capacity):
        """Initialize a fixed-size circular queue."""
        self.capacity = capacity
        # Pre-allocate the list with None to represent empty slots
        self.queue = [None] * capacity
        self.front = -1
        self.rear = -1
        self._size = 0

    def is_empty(self):
        """Check if the queue is empty."""
        return self._size == 0

    def is_full(self):
        """Check if the queue is full."""
        return self._size == self.capacity

    def enqueue(self, item):
        """Add an element to the rear of the queue in O(1) time."""
        if self.is_full():
            raise OverflowError("Enqueue into a full circular queue")

        # If it's the very first element, set front to 0
        if self.is_empty():
            self.front = 0

        # Move rear forward, wrapping around if necessary using modulo
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = item
        self._size += 1
        print(f"Enqueued: {item}")

    def dequeue(self):
        """Remove and return the front element in O(1) time."""
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")

        removed_item = self.queue[self.front]
        self.queue[self.front] = None  # Clear the slot (optional but clean)

        # If we just removed the last remaining element, reset pointers
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            # Move front forward, wrapping around if necessary
            self.front = (self.front + 1) % self.capacity

        self._size -= 1
        return removed_item

    def get_front(self):
        """Retrieve the front element without removing it."""
        if not self.is_empty():
            return self.queue[self.front]
        return "Queue is empty"

    def get_rear(self):
        """Retrieve the rear element without removing it."""
        if not self.is_empty():
            return self.queue[self.rear]
        return "Queue is empty"

    def size(self):
        """Return the current number of elements."""
        return self._size

    def display(self):
        """Display elements in logical queue order (Front to Rear)."""
        if self.is_empty():
            return []
        
        elements = []
        current = self.front
        for _ in range(self._size):
            elements.append(self.queue[current])
            current = (current + 1) % self.capacity
        return elements

# --- Demonstration ---
if __name__ == "__main__":
    # Initialize a circular queue with a strict maximum size of 5
    cq = CircularQueue(5)
    
    # 1. Fill the queue
    cq.enqueue(10)
    cq.enqueue(20)
    cq.enqueue(30)
    cq.enqueue(40)
    cq.enqueue(50)
    
    print(f"\nCurrent Queue: {cq.display()}")
    print(f"Is queue full? {cq.is_full()}")
    
    # 2. Dequeue two elements to free up space at the "front"
    print(f"\nDequeued: {cq.dequeue()}")
    print(f"Dequeued: {cq.dequeue()}")
    
    # 3. Enqueue new elements to demonstrate the wrap-around
    cq.enqueue(60)
    cq.enqueue(70)
    
    print(f"\nQueue after wrap-around: {cq.display()}")
    
    # 4. Show internal state to prove it wrapped
    print(f"Internal List State: {cq.queue}")
    print(f"Front Index: {cq.front} | Rear Index: {cq.rear}")