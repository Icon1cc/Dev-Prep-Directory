"""
Problem 073: State Design Pattern

Difficulty: Intermediate-Advanced
Topic: Behavioral Design Pattern

=== PROBLEM DESCRIPTION ===

The State pattern allows an object to change its behavior when its internal
state changes. The object appears to change its class.

Your Task:
-----------
1. Create a `VendingMachineState` ABC:
   - `insert_coin(machine)`
   - `eject_coin(machine)`
   - `select_product(machine)`
   - `dispense(machine)`

2. Create concrete states:
   - `NoCoinState` - waiting for coin
   - `HasCoinState` - coin inserted, waiting for selection
   - `SoldState` - product being dispensed
   - `SoldOutState` - no products left

3. Create a `VendingMachine` context:
   - `state` - current state
   - `count` - number of products
   - Methods delegate to current state

4. Demonstrate state transitions:
   - Insert coin -> select product -> dispense
   - Try invalid actions (eject when no coin, etc.)

Expected Output:
----------------
Vending Machine (5 products):
Insert coin...
  Coin inserted
Select product...
  Product selected, dispensing...
Dispense...
  Product dispensed, enjoy!

Current state: NoCoinState (waiting for coin)

Trying to select without coin...
  Please insert a coin first

When sold out:
  Machine is sold out, come back later

=== CONCEPTS TO LEARN ===
- State encapsulates behavior for each state
- Context delegates to current state
- State changes happen inside state methods
- Avoids complex if/else chains

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate state transitions in the vending machine
