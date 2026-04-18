"""
Problem 088: Interview Problem - Design an Elevator System

Difficulty: Advanced
Topic: System Design Interview Question

=== PROBLEM DESCRIPTION ===

Design an elevator system for a building. This tests your ability to
handle concurrent requests and scheduling algorithms.

Requirements:
- Multiple elevators in a building
- Handle up/down requests from floors
- Handle destination requests from inside elevator
- Efficient scheduling (minimize wait time)
- Handle weight limits and max capacity

Your Task:
-----------
1. Create `Direction` enum: UP, DOWN, IDLE

2. Create `Request`:
   - `floor` - where request originated
   - `direction` - desired direction
   - `timestamp`

3. Create `Elevator`:
   - `current_floor`, `direction`, `state`
   - `destination_floors` - set of floors to visit
   - `add_destination(floor)`
   - `move()` - move one floor toward next destination
   - `capacity`, `current_load`

4. Create `ElevatorController` (Scheduler):
   - Manages multiple elevators
   - `request_elevator(floor, direction)` - external request
   - `select_floor(elevator_id, floor)` - internal request
   - Scheduling algorithm (e.g., SCAN/LOOK algorithm)

5. Create `Building`:
   - `num_floors`, `elevators`
   - `call_elevator(floor, direction)`

Expected Output:
----------------
Building: 10 floors, 2 elevators

Elevator 1: Floor 1, IDLE
Elevator 2: Floor 1, IDLE

Request: Floor 5, going UP
Assigning Elevator 1

Elevator 1 moving: 1 -> 2 -> 3 -> 4 -> 5 (arrived)
Passenger enters, selects floor 8

Request: Floor 3, going UP
Elevator 1 is heading up, will stop at floor 3

Elevator 1 moving: 5 -> 4 -> 3 (picked up) -> 4 -> 5 -> 6 -> 7 -> 8 (arrived)

Status:
- Elevator 1: Floor 8, IDLE
- Elevator 2: Floor 1, IDLE

=== STARTER CODE ===
"""

from enum import Enum
from typing import Set
from dataclasses import dataclass
import time

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Simulate elevator operations
