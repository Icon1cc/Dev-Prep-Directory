"""
Write a function that takes a sorted linked list and a new node as input, and inserts the new node into the correct position in the linked list to maintain the sorted order.
"""

class Node:
    """
    A class to represent a Node in a Singly Linked List.
    """
    def __init__(self, data):
        self.data = data  # The value stored in the node
        self.next = None  # The pointer to the next node


def sorted_insert(head, new_node):
    """
    Inserts a new_node into a sorted linked list while maintaining the sorted order.
    Returns the head of the updated list.
    """
    
    # CASE 1: Insert at the beginning
    # Logic: If the list is empty OR the new data is smaller than the current head
    if head is None or new_node.data < head.data:
        new_node.next = head  # Point the new node to the current head
        return new_node       # The new node becomes the new head

    # CASE 2: Insert in the middle or at the end
    # We need to find the node just BEFORE where the new node belongs.
    current = head
    
    # Loop condition explanation:
    # 1. current.next is not None: Prevents falling off the edge of the list
    # 2. current.next.data < new_node.data: Keep moving as long as the next value is too small
    while current.next is not None and current.next.data < new_node.data:
        current = current.next

    # Once the loop stops, 'current' is the node just BEFORE the insertion point.
    
    # Perform the insertion:
    new_node.next = current.next  # Step 1: New node grabs the rest of the list
    current.next = new_node       # Step 2: Previous node grabs the new node
    
    return head


def print_list(head):
    """
    Helper function to print the linked list nicely.
    """
    current = head
    while current:
        print(f"{current.data} -> ", end="")
        current = current.next
    print("None")


# --- Main Driver Code (User Input Section) ---
if __name__ == "__main__":
    head = None
    
    # 1. Build the initial sorted list
    try:
        count = int(input("How many nodes do you want in the initial list? "))
        print(f"Enter {count} numbers (order doesn't matter, we will sort them as we add):")
        
        for i in range(count):
            val = int(input(f"Enter number {i+1}: "))
            new_node = Node(val)
            # We use our own function to build the list so it is guaranteed to be sorted!
            head = sorted_insert(head, new_node)

        print("\nCurrent Sorted List: ", end="")
        print_list(head)

        # 2. Insert a new number
        insert_val = int(input("\nEnter a new number to insert: "))
        node_to_insert = Node(insert_val)
        
        head = sorted_insert(head, node_to_insert)

        # 3. Print the final result
        print("Updated Sorted List: ", end="")
        print_list(head)

    except ValueError:
        print("Invalid input! Please enter integers only.")
