"""
Linked List implementation of Queue in Python.
"""

class Node:
    """A node object to store data and the reference to the next node."""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedListQueue:
    def __init__(self):
        """Initialize an empty queue with front and rear pointers."""
        self.front = None
        self.rear = None
        self._size = 0  # Track size to keep the size() method O(1)

    def enqueue(self, item):
        """Add an element to the rear of the queue."""
        new_node = Node(item)
        
        # If the queue is empty, the new node is both the front and the rear
        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            # Link the old rear to the new node, then update the rear pointer
            self.rear.next = new_node
            self.rear = new_node
            
        self._size += 1
        print(f"Enqueued: {item}")

    def dequeue(self):
        """Remove and return the front element of the queue."""
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        
        # Extract data and move the front pointer to the next node
        removed_data = self.front.data
        self.front = self.front.next
        
        # If the queue is now empty, ensure the rear pointer is also reset
        if self.front is None:
            self.rear = None
            
        self._size -= 1
        return removed_data

    def get_front(self):
        """Retrieve the front element without removing it."""
        if not self.is_empty():
            return self.front.data
        return "Queue is empty"

    def get_rear(self):
        """Retrieve the rear element without removing it."""
        if not self.is_empty():
            return self.rear.data
        return "Queue is empty"

    def is_empty(self):
        """Check if the queue is empty."""
        return self.front is None

    def size(self):
        """Return the total number of elements in the queue."""
        return self._size

    def display(self):
        """Traverse the linked list to display its elements."""
        elements = []
        current = self.front
        while current:
            elements.append(current.data)
            current = current.next
        return elements

# --- Demonstration ---
if __name__ == "__main__":
    q = LinkedListQueue()
    
    # 1. Enqueue operations
    q.enqueue("Customer A")
    q.enqueue("Customer B")
    q.enqueue("Customer C")
    
    # 2. Display Queue
    print(f"\nCurrent Queue: {q.display()}")
    
    # 3. Get Front and Rear
    print(f"Front element: {q.get_front()}")
    print(f"Rear element: {q.get_rear()}")
    
    # 4. Dequeue an element
    print(f"\nDequeued: {q.dequeue()}")
    
    # 5. Display Queue after Dequeue
    print(f"Queue after dequeue: {q.display()}")
    
    # 6. Check status and size
    print(f"Is the queue empty? {q.is_empty()}")
    print(f"Size of the queue: {q.size()}")