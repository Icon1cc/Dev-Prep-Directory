"""
String Comparison Operators: <, <=, >, >=, !=, ==
Includes demonstration of Case Sensitivity (Apple vs banana).
"""

def demo_operators():
    print("--- 1. Standard Comparison (Lower vs Lower) ---")
    s1 = "apple"
    s2 = "banana"
    
    # Logic: 'a' comes before 'b' in the dictionary, so apple is "less than" banana.
    print(f"Strings: '{s1}' vs '{s2}'")
    print(f"  <  (Less Than):           {s1 < s2}")   # True
    print(f"  <= (Less Equal):          {s1 <= s2}")  # True
    print(f"  >  (Greater Than):        {s1 > s2}")   # False
    print(f"  >= (Greater Equal):       {s1 >= s2}")  # False
    print(f"  == (Equal):               {s1 == s2}")  # False
    print(f"  != (Not Equal):           {s1 != s2}")  # True

    print("\n--- 2. The Capital Letter Rule (Apple vs banana) ---")
    # KEY CONCEPT: In ASCII, Capital letters (65-90) are SMALLER than Lowercase (97-122).
    # Therefore, 'Apple' comes BEFORE 'banana'.
    
    cap = "Apple"
    lower = "banana"
    
    print(f"Strings: '{cap}' vs '{lower}'")
    print(f"  '{cap}' < '{lower}':      {cap < lower}")  # True! (Because 'A' is 65, 'b' is 98)
    print(f"  '{cap}' > '{lower}':      {cap > lower}")  # False
    
    # Vice Versa check
    print(f"  '{lower}' > '{cap}':      {lower > cap}")  # True

    print("\n--- 3. Equality Checks ---")
    str_a = "hello"
    str_b = "hello"
    print(f"Strings: '{str_a}' vs '{str_b}'")
    print(f"  == (Equal):               {str_a == str_b}") # True
    print(f"  != (Not Equal):           {str_a != str_b}") # False

if __name__ == "__main__":
    demo_operators()