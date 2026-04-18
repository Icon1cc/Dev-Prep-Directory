"""
Problem 062: SOLID Principles - Interface Segregation Principle

Difficulty: Intermediate
Topic: Design Principles

=== PROBLEM DESCRIPTION ===

The Interface Segregation Principle (ISP) states that clients should not be
forced to depend on interfaces they don't use. Instead of one fat interface,
create multiple small, specific interfaces.

Your Task:
-----------
1. BEFORE (Bad Design) - Fat interface:
   - `Worker` ABC with: work(), eat(), sleep(), code(), manage()
   - `Robot` extends Worker but can't eat() or sleep()
   - Forces Robot to implement meaningless methods

2. AFTER (Good Design) - Segregated interfaces:
   - `Workable` ABC: work()
   - `Eatable` ABC: eat()
   - `Sleepable` ABC: sleep()
   - `Codeable` ABC: code()
   - `Manageable` ABC: manage()
   - Classes implement only the interfaces they need

3. Create different worker types:
   - `Developer` - Workable, Eatable, Sleepable, Codeable
   - `Manager` - Workable, Eatable, Sleepable, Manageable
   - `Robot` - Workable only

Expected Output:
----------------
BAD: Fat interface forces Robot to implement eat() and sleep()
Robot.eat() raises NotImplementedError - ISP VIOLATED!

GOOD: Segregated interfaces
Developer: work, eat, sleep, code
Manager: work, eat, sleep, manage
Robot: work only

All types can work():
Developer is working...
Manager is working...
Robot is working...

=== CONCEPTS TO LEARN ===
- Many specific interfaces > one general interface
- Clients shouldn't implement methods they don't need
- Reduces coupling between components
- Makes system more flexible and maintainable

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod

# Write your solution below this line
# -----------------------------------

# BAD: Fat interface


# GOOD: Segregated interfaces



# Test your solution
# ------------------
# Demonstrate the difference between bad and good design
