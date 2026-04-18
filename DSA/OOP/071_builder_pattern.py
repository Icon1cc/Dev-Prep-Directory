"""
Problem 071: Builder Design Pattern

Difficulty: Intermediate
Topic: Creational Design Pattern

=== PROBLEM DESCRIPTION ===

The Builder pattern separates object construction from its representation.
It's useful when objects have many optional parameters or complex construction.

Your Task:
-----------
1. Create a `Computer` class with many attributes:
   - cpu, ram, storage, gpu, os, keyboard, mouse, monitor, etc.
   - Too many parameters for a simple constructor!

2. Create a `ComputerBuilder` class:
   - Methods to set each attribute
   - `build()` method returns the Computer
   - Use method chaining

3. Create `Director` class with preset configurations:
   - `build_gaming_pc(builder)` - high-end gaming setup
   - `build_office_pc(builder)` - basic office setup
   - `build_workstation(builder)` - professional workstation

4. Alternative: Use a nested builder class:
   - Computer.Builder() returns builder
   - More encapsulated approach

Expected Output:
----------------
Gaming PC:
  CPU: Intel i9-12900K
  RAM: 32GB
  Storage: 2TB SSD
  GPU: RTX 4090
  OS: Windows 11

Office PC:
  CPU: Intel i5-12400
  RAM: 8GB
  Storage: 512GB SSD
  GPU: Integrated
  OS: Windows 11

Custom build:
  CPU: AMD Ryzen 7
  RAM: 16GB
  Storage: 1TB SSD

=== CONCEPTS TO LEARN ===
- Separates construction from representation
- Step-by-step object construction
- Director encapsulates common configurations
- Alternative to telescoping constructors

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# director = Director()
#
# # Gaming PC
# builder = ComputerBuilder()
# gaming_pc = director.build_gaming_pc(builder)
# print("Gaming PC:")
# print(gaming_pc)
#
# # Office PC
# builder = ComputerBuilder()
# office_pc = director.build_office_pc(builder)
# print("\nOffice PC:")
# print(office_pc)
#
# # Custom build
# custom = (ComputerBuilder()
#     .set_cpu("AMD Ryzen 7")
#     .set_ram("16GB")
#     .set_storage("1TB SSD")
#     .build())
# print("\nCustom build:")
# print(custom)
