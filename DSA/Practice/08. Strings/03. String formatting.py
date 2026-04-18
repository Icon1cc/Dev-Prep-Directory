"""
STRING FORMATTING TECHNIQUES
----------------------------
This script demonstrates the evolution of Python string formatting:
1. The Old Way (% Operator): C-style formatting.
2. The Middle Way (.format()): The Python 3.0 standard.
3. The Modern Way (f-strings): The Python 3.6+ standard (Fastest & Cleanest).
"""

class FormatMaster:
    def __init__(self):
        # Sample data for demonstration
        self.name = "Alice"
        self.age = 30
        self.price = 123.456789
    
    def demo_percent_operator(self):
        """
        1. The % Operator (Old School)
        Good for: Legacy code, simple C-style formatting.
        Bad for: Readability with many variables.
        """
        print("\n[1] --- The % Operator (Legacy) ---")
        
        # %s = string, %d = integer, %.2f = float with 2 decimal places
        s = "User: %s | Age: %d | Cost: $%.2f" % (self.name, self.age, self.price)
        
        print(f"Code:   'User: %s ...' % (name, age, price)")
        print(f"Result: {s}")

    def demo_dot_format(self):
        """
        2. The .format() Method
        Good for: Reusing format templates, compatibility with Python < 3.6.
        """
        print("\n[2] --- The .format() Method ---")
        
        # {} are placeholders. You can control order with indices {0}, {1}
        # {:.2f} formats the number
        s = "User: {} | Age: {} | Cost: ${:.2f}".format(self.name, self.age, self.price)
        
        # You can also use named arguments for clarity
        s_named = "User: {n} | Cost: ${p:.2f}".format(n=self.name, p=self.price)
        
        print(f"Code:   'User: {{}} ...'.format(name, age, price)")
        print(f"Result: {s}")
        print(f"Named:  {s_named}")

    def demo_f_strings(self):
        """
        3. f-strings (Formatted String Literals)
        Good for: EVERYTHING. Readability, speed, and clean syntax.
        Introduced in Python 3.6.
        """
        print("\n[3] --- f-strings (The Modern Standard) ---")
        
        # Variables go directly inside {}. 
        # Expressions (math) work inside {} too!
        s = f"User: {self.name} | Age: {self.age} | Cost: ${self.price:.2f}"
        
        # Advanced: Calculations inside the string
        calc = f"Next Year: {self.age + 1}"
        
        print(f"Code:   f'User: {{name}} | Cost: ${{price:.2f}}'")
        print(f"Result: {s}")
        print(f"Calc:   {calc}")

    def compare_alignment(self):
        """Demonstrate padding/alignment (Left, Right, Center)."""
        print("\n[4] --- Alignment & Padding (f-string power) ---")
        
        # < : Left align
        # > : Right align
        # ^ : Center align
        # 10 : The width of the space
        
        print(f"|{self.name:<10}| (Left)")
        print(f"|{self.name:>10}| (Right)")
        print(f"|{self.name:^10}| (Center)")
        print(f"|{self.name:*^10}| (Center with fill)")

# --- Main Execution ---
if __name__ == "__main__":
    tool = FormatMaster()
    
    tool.demo_percent_operator()
    tool.demo_dot_format()
    tool.demo_f_strings()
    tool.compare_alignment()