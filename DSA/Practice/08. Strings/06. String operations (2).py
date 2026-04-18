"""
Implementation of various string operations in Python.

Operations Covered:
1. len()          : Calculate string length.
2. upper(), lower() : Convert case.
3. isupper(), islower() : Check case.
4. startswith()   : Check prefix (supports start/end positions).
5. endswith()     : Check suffix.
6. split()        : Break string into a list.
7. join()         : Merge list into a string.
8. strip(), lstrip(), rstrip() : Remove whitespace or specific chars.
9. find()         : Search for substring index (supports start/end positions).
"""

def demo_string_operations():
    s1 = "  Python Programming is Fun  "
    
    print(f"Original String s1: '{s1}'")
    print("-" * 60)

    # --- 1. Length & Case Operations ---
    print("1. Length & Case")
    print(f"  len(s1):       {len(s1)}")          # Total characters
    print(f"  s1.upper():    '{s1.upper()}'")     # Convert to UPPERCASE
    print(f"  s1.lower():    '{s1.lower()}'")     # Convert to lowercase
    
    # Check Case
    temp_upper = "HELLO"
    temp_lower = "hello"
    print(f"  '{temp_upper}'.isupper(): {temp_upper.isupper()}")
    print(f"  '{temp_lower}'.islower(): {temp_lower.islower()}")


    # --- 2. StartsWith & EndsWith (Prefix/Suffix) ---
    print("\n2. StartsWith & EndsWith")
    clean_s1 = s1.strip() # Remove spaces for clearer testing
    
    # Basic usage
    print(f"  '{clean_s1}'.startswith('Py'):      {clean_s1.startswith('Py')}")
    print(f"  '{clean_s1}'.endswith('Fun'):       {clean_s1.endswith('Fun')}")
    
    # startswith(word, start_pos)
    # Check if 'Pro' starts at index 7
    print(f"  startswith('Pro', 7):             {clean_s1.startswith('Pro', 7)}")
    
    # startswith(word, start_pos, end_pos)
    # Check if 'Python' exists specifically in the range [0:6]
    print(f"  startswith('Python', 0, 6):       {clean_s1.startswith('Python', 0, 6)}")


    # --- 3. Stripping (Removing Whitespace) ---
    print("\n3. Stripping Whitespace")
    dirty_str = "***Python***"
    
    print(f"  Original:      '{dirty_str}'")
    print(f"  lstrip('*'):   '{dirty_str.lstrip('*')}' (Left strip)")
    print(f"  rstrip('*'):   '{dirty_str.rstrip('*')}' (Right strip)")
    print(f"  strip('*'):    '{dirty_str.strip('*')}'  (Both sides)")
    
    # Default strip() removes spaces/newlines
    print(f"  s1.strip():    '{s1.strip()}'")


    # --- 4. Split & Join ---
    print("\n4. Split & Join")
    
    # split(delimiter) -> Returns a LIST
    text = "apple,banana,cherry"
    fruits = text.split(",")
    print(f"  split(','):    {fruits} (Type: {type(fruits)})")
    
    # Default split() -> Splits by whitespace
    words = clean_s1.split()
    print(f"  s1.split():    {words}")
    
    # join(iterable) -> Returns a STRING
    # syntax: "delimiter".join(list)
    joined_text = "-".join(fruits)
    print(f"  '-'.join(...): '{joined_text}'")


    # --- 5. Find (Search) ---
    # Unlike index(), find() returns -1 if not found (No Crash)
    print("\n5. Find Substrings")
    text_search = "banana banana"
    
    # s1.find(word) -> First occurrence
    print(f"  '{text_search}'.find('ana'):      {text_search.find('ana')}")
    
    # s1.find(word, start) -> Search starting from index 2
    print(f"  find('ana', 2):                 {text_search.find('ana', 2)}")
    
    # s1.find(word, start, end) -> Search between index 7 and len()
    # This looks for the SECOND word 'banana'
    n = len(text_search)
    print(f"  find('ana', 7, {n}):             {text_search.find('ana', 7, n)}")
    
    # Find something that doesn't exist
    print(f"  find('xyz'):                    {text_search.find('xyz')} (Returns -1)")

if __name__ == "__main__":
    demo_string_operations()