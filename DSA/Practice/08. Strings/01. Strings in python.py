"""
Implement functions to demonstrate various string operations.
This includes:
1. Indexing (first, second, last characters).
2. ASCII conversion using ord() and chr().
3. Counting unique characters without a Set (using a boolean array).
4. Demonstrating String Immutability.
"""

def demonstrate_string_ops(s):
    if not s:
        print(">> Empty string provided.")
        return 0
        
    print(f"\n--- Processing String: '{s}' ---")

    # 1. Indexing: s[0], s[1], s[-1]
    # s[0] is the Head, s[-1] is the Tail
    first = s[0]
    last = s[-1]
    print(f"First character s[0]:  '{first}'")
    
    if len(s) > 1:
        print(f"Second character s[1]: '{s[1]}'")
        
    print(f"Last character s[-1]:  '{last}'")

    # 2. Immutability Check
    # Strings cannot be changed in place. We must catch the error.
    try:
        print("Attempting to change s[0] to 'X'...", end=" ")
        s[0] = 'X' 
    except TypeError:
        print("FAILED.")
        print(">> Reason: Strings are IMMUTABLE (cannot be changed in-place).")

    # 3. Counting Unique Characters using ord() and a fixed array
    # We use a list of 256 False values (Direct Addressing)
    seen = [False] * 256 
    unique_count = 0
    
    print("\n--- Scanning Characters (ASCII Map) ---")
    for i in range(len(s)):
        char = s[i]
        
        # Convert Char -> Integer (ASCII)
        ascii_val = ord(char)
        
        # Convert Integer -> Char (Demonstrating chr)
        reverted_char = chr(ascii_val)
        
        # Check our boolean array
        if not seen[ascii_val]:
            seen[ascii_val] = True
            unique_count += 1
            print(f"Position {i}: '{char}' -> ASCII {ascii_val} -> New Unique Found")
        else:
            print(f"Position {i}: '{char}' -> ASCII {ascii_val} -> Already Seen")
    
    return unique_count

# --- Main Interactive Loop ---
if __name__ == "__main__":
    print("--- String Operations & ASCII Tool ---")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("\nEnter a string to analyze: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
            
        count = demonstrate_string_ops(user_input)
        print(f"Total Unique Characters: {count}")