"""
Problem 085: Implementing a State Machine

Difficulty: Advanced
Topic: Real-world Application

=== PROBLEM DESCRIPTION ===

Build a finite state machine (FSM) framework that can model any stateful
system like order processing, game states, or workflow management.

Your Task:
-----------
1. Create `State` class:
   - `name` - state identifier
   - `on_enter()` - called when entering state
   - `on_exit()` - called when leaving state
   - `on_event(event)` - handle event, return next state or None

2. Create `Transition` class:
   - `from_state`, `to_state` - state names
   - `event` - trigger event name
   - `condition` - optional guard condition (callable)
   - `action` - optional action to perform

3. Create `StateMachine` class:
   - `add_state(state)`
   - `add_transition(transition)`
   - `process_event(event, data=None)`
   - `current_state` property
   - History tracking

4. Create example: Order State Machine
   - States: PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
   - Events: confirm, ship, deliver, cancel

Expected Output:
----------------
Order #1001 State Machine:
Initial state: PENDING

Event 'confirm' -> State: CONFIRMED
  Action: Payment processed

Event 'ship' -> State: SHIPPED
  Action: Shipping notification sent

Event 'cancel' while SHIPPED:
  Transition denied: Cannot cancel shipped order

Event 'deliver' -> State: DELIVERED
  Action: Delivery confirmation sent

State history: PENDING -> CONFIRMED -> SHIPPED -> DELIVERED

=== CONCEPTS TO LEARN ===
- Finite State Machines
- State transitions with guards
- Event-driven state changes
- Formal modeling of behavior

=== STARTER CODE ===
"""

from typing import Callable, Optional, Any
from dataclasses import dataclass

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Create order state machine and process events
