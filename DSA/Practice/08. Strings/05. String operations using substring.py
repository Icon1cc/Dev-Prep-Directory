"""
String operations: Membership, Concatenation, and Indexing.
"""

def demo_operations():
    s1 = "Python Programming"
    s2 = "gram"
    s3 = "Java"

    # --- 1. Membership Operators (in, not in) ---
    print("\n--- 1. Membership (in / not in) ---")
    
    # Check if s2 is inside s1
    print(f"Is '{s2}' in '{s1}'?      {s2 in s1}")
    
    # Check if s3 is NOT inside s1
    print(f"Is '{s3}' not in '{s1}'?  {s3 not in s1}")


    # --- 2. Concatenation (+) ---
    print("\n--- 2. Concatenation (+) ---")
    
    # Joining two strings
    combined_2 = "Hello " + "World"
    print(f"Two strings:   '{combined_2}'")
    
    # Joining three strings (Chaining +)
    combined_3 = "Deep " + "Learning " + "Rocks"
    print(f"Three strings: '{combined_3}'")


    # --- 3. Indexing Methods (index vs rindex) ---
    # NOTE: index() raises ValueError if not found. find() returns -1.
    print("\n--- 3. Indexing (index, rindex) ---")
    
    text = "banana banana"
    print(f"Text: '{text}' (Length: {len(text)})")

    # A. Basic index() - Finds the FIRST occurrence
    idx_first = text.index("ana")
    print(f"s1.index('ana'):         {idx_first}  (First match)")

    # B. Basic rindex() - Finds the LAST occurrence (Right Index)
    idx_last = text.rindex("ana")
    print(f"s1.rindex('ana'):        {idx_last} (Last match)")


    # --- 4. Indexing with Parameters (start, end) ---
    print("\n--- 4. Indexing with Start/End constraints ---")
    
    # s1.index(substring, start_pos)
    # Skip the first 'ana' (at index 1). Start searching from index 2.
    idx_skip = text.index("ana", 2)
    print(f"s1.index('ana', 2):      {idx_skip}  (Skipped first 'ana')")

    # s1.index(substring, start_pos, end_pos)
    # Search for 'ana' between index 7 and 13.
    # The second 'ana' starts at 8, so this finds it.
    idx_range = text.index("ana", 7, 13)
    print(f"s1.index('ana', 7, 13):  {idx_range}  (Found inside range)")

    # Error Handling Example
    # If we search in a range where it doesn't exist, Python raises an error.
    print("\n--- 5. Handling Search Failures ---")
    try:
        # Try to find 'ana' only in the first 3 characters [0:3] -> 'ban'
        text.index("ana", 0, 3) 
    except ValueError as e:
        print(f"s1.index('ana', 0, 3):   FAILED -> {e}")

if __name__ == "__main__":
    demo_operations()