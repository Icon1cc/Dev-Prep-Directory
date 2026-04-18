"""
Demonstrate the use of escape sequences in Python strings.
STRING OPERATIONS & INTERNALS DEMO
----------------------------------
This script demonstrates:
1. String Internals: Indexing (s[0], s[-1]) and Immutability.
2. Optimization: Counting unique chars using Direct Addressing (ord() + Boolean Array).
3. Formatting: Escape Sequences (\n, \t, \\).
4. RAW STRINGS: Handling paths (r"C:\path") without double backslashes.
5. Safety: Handling single quotes ('s) correctly.
"""

import time

class StringAnalyzer:
    def __init__(self):
        # Fixed size array for ASCII optimization (0-255)
        self.seen_map = [False] * 256 

    def analyze_string_internals(self, s):
        """Demonstrates Indexing and Immutability."""
        if not s: return
        print(f"\n[1] --- Internal Structure of '{s}' ---")
        
        # Indexing Demo
        print(f"   Head (s[0]):  '{s[0]}'")
        if len(s) > 1: print(f"   Tail (s[-1]): '{s[-1]}'")
        
        # Immutability Demo
        print("   Test: Attempting to change s[0]...", end=" ")
        try:
            s[0] = 'X'
        except TypeError:
            print("FAILED. (Strings are Immutable)")

    def count_unique_optimized(self, s):
        """
        Counts unique characters using O(N) Direct Addressing.
        Includes safety check for non-ASCII characters (emojis, etc).
        """
        print(f"\n[2] --- Optimized Unique Count (ASCII Map) ---")
        
        # Reset map for new string
        self.seen_map = [False] * 256 
        unique_count = 0
        
        for i in range(len(s)):
            ascii_val = ord(s[i])
            
            # GUARD CLAUSE: Prevent crash on Emojis/Unicode
            if ascii_val > 255:
                print(f"     [!] Skipped non-ASCII char: '{s[i]}'")
                continue
                
            if not self.seen_map[ascii_val]:
                self.seen_map[ascii_val] = True
                unique_count += 1
        
        print(f"   >> Unique Count (ASCII only): {unique_count}")

    def demo_escape_sequences(self):
        """Demonstrates invisible characters."""
        print(f"\n[3] --- Escape Sequence Gallery ---")
        print(f"   {'Sequence':<10} | {'Output':<20}")
        print("   " + "-"*35)
        print(f"   {'New Line':<10} | Line 1\n{'':<14}| Line 2")
        print(f"   {'Tab':<10} | Col1\tCol2")
        print(f"   {'Backslash':<10} | Path\\To\\File")

    def demo_raw_strings(self):
        """
        [NEW] Demonstrates Raw Strings (r'').
        Crucial for File Paths and Regex.
        """
        print(f"\n[4] --- The Power of RAW STRINGS (r'') ---")
        
        # Scenario: Windows File Path
        hard_way = "C:\\Users\\name"
        raw_way = r"C:\Users\name"
        
        print(f"   Goal: Print a Windows path 'C:\\Users\\name'")
        print(f"   Normal String: \"C:\\\\Users\\\\name\" (Must double every slash)")
        print(f"   Raw String:    r\"C:\\Users\\name\"   (Write exactly what you see)")
        
        print(f"   >> Output match? {hard_way == raw_way}")

    def demo_quote_handling(self):
        """Demonstrates how to handle 's and other quotes."""
        print(f"\n[5] --- Handling Quotes ---")
        
        # FIX: Define variables first to avoid backslashes inside f-string expressions
        # This prevents the SyntaxError you saw.
        val_escaped = 'It\'s ok'
        val_mixed = "It's ok"
        
        print(f"   Escape: 'It\\'s ok'  -> {val_escaped}")
        print(f"   Mixed:  \"It's ok\"   -> {val_mixed}")

# --- Main Interactive Execution ---
if __name__ == "__main__":
    tool = StringAnalyzer()
    
    while True:
        user_input = input("\nEnter a string to analyze (or 'exit'): ")
        if user_input.lower() == 'exit': break
            
        # 1. Run Analysis Modules
        tool.analyze_string_internals(user_input)
        tool.count_unique_optimized(user_input)
        
        # 2. Show Reference Demos (with a pause for readability)
        print("\n... Displaying Reference Demos ...")
        time.sleep(0.5) 
        
        tool.demo_quote_handling()
        tool.demo_escape_sequences()
        tool.demo_raw_strings()