"""
Implementing a Queue in Python
"""

class Queue:
    def __init__(self):
        """Initialize an empty list to represent the queue."""
        self.queue = []

    def enqueue(self, item):
        """Add an element to the rear of the queue."""
        self.queue.append(item)
        print(f"Enqueued: {item}")

    def dequeue(self):
        """Remove and return the element from the front of the queue."""
        if not self.is_empty():
            return self.queue.pop(0)
        else:
            raise IndexError("Dequeue from an empty queue")

    def display(self):
        """Return the current state of the queue."""
        return self.queue

    def get_front(self):
        """Get the front element without removing it."""
        if not self.is_empty():
            return self.queue[0]
        else:
            return "Queue is empty"

    def get_rear(self):
        """Get the rear element without removing it."""
        if not self.is_empty():
            return self.queue[-1]
        else:
            return "Queue is empty"

    def is_empty(self):
        """Check if the queue has no elements."""
        return len(self.queue) == 0

    def size(self):
        """Return the total number of elements in the queue."""
        return len(self.queue)

# --- Demonstration ---
if __name__ == "__main__":
    my_queue = Queue()

    # 1. Enqueue operations
    my_queue.enqueue("Apple")
    my_queue.enqueue("Banana")
    my_queue.enqueue("Cherry")

    # 2. Display Queue
    print("\nCurrent Queue:", my_queue.display())

    # 3. Get Front and Rear
    print("Front element:", my_queue.get_front())
    print("Rear element:", my_queue.get_rear())

    # 4. Check Size
    print("Queue size:", my_queue.size())

    # 5. Dequeue operation
    print("Dequeued element:", my_queue.dequeue())

    # 6. Final state
    print("Queue after dequeue:", my_queue.display())
    print("Is queue empty?", my_queue.is_empty())