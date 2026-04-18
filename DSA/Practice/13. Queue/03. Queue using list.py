"""
Implementing a Queue in Python using a List.
"""

# Global queue list
q = []

def enqueue(item):
    """Add an element to the rear of the queue."""
    q.append(item)
    print(f"Enqueued: {item}")

def dequeue():
    """Remove and return the front element of the queue."""
    if not is_empty():
        return q.pop(0)  # O(n) complexity in a standard list
    else:
        # Raising an error is better than returning a string for logic flow
        raise IndexError("Cannot dequeue from an empty queue")

def display():
    """Show all elements in the queue."""
    return q

def get_front():
    """Retrieve the front element without removing it."""
    return q[0] if not is_empty() else "Queue is empty"

def get_rear():
    """Retrieve the rear element without removing it."""
    return q[-1] if not is_empty() else "Queue is empty"

def is_empty():
    """Check if the queue is empty."""
    return len(q) == 0

def size():
    """Check the size of the queue."""
    return len(q)

# --- Demonstration ---
if __name__ == "__main__":  
    # 1. Enqueue operations
    enqueue("Apple")
    enqueue("Banana")
    enqueue("Cherry")

    # 2. Display Queue
    print(f"\nCurrent Queue: {display()}")

    # 3. Get Front and Rear
    print(f"Front element: {get_front()}")
    print(f"Rear element: {get_rear()}")

    # 4. Dequeue an element
    try:
        print(f"Dequeue element: {dequeue()}")
    except IndexError as e:
        print(e)

    # 5. Display Queue after Dequeue
    print(f"Queue after dequeue: {display()}")

    # 6. Check status and size
    print(f"Is the queue empty? {is_empty()}")
    print(f"Size of the queue: {size()}")