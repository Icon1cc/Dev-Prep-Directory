"""
Problem 086: Interview Problem - Design a Parking Lot

Difficulty: Advanced
Topic: System Design Interview Question

=== PROBLEM DESCRIPTION ===

Design a parking lot system. This is a classic OOP interview question
that tests your ability to model real-world systems with classes.

Requirements:
- Multiple floors, each with multiple spots
- Different spot sizes: Small, Medium, Large
- Different vehicle types: Motorcycle, Car, Bus
- Motorcycles can fit in any spot, cars in Medium/Large, buses need Large
- Track occupied/available spots
- Support hourly rates and payment

Your Task:
-----------
1. Create `VehicleType` enum: MOTORCYCLE, CAR, BUS
2. Create `SpotSize` enum: SMALL, MEDIUM, LARGE

3. Create `Vehicle` ABC with subclasses:
   - `Motorcycle`, `Car`, `Bus`
   - Each knows its type and license plate

4. Create `ParkingSpot`:
   - `size`, `spot_number`, `floor`
   - `is_available`, `vehicle` (if occupied)
   - `can_fit(vehicle)` - check compatibility
   - `park(vehicle)`, `leave()`

5. Create `ParkingFloor`:
   - Contains multiple ParkingSpots
   - `get_available_spot(vehicle)` - finds suitable spot

6. Create `ParkingLot`:
   - Multiple floors
   - `park_vehicle(vehicle)` - finds spot and parks
   - `leave(vehicle)` - vehicle leaves, calculate fee
   - `get_available_spots()` - count by type

7. Create `ParkingTicket`:
   - Issued when vehicle enters
   - `entry_time`, `vehicle`, `spot`
   - `calculate_fee()` based on duration and vehicle type

Expected Output:
----------------
Parking Lot: 3 floors, 30 spots per floor

Available spots: 90

Parking car ABC-123...
Ticket #1: Car parked at Floor 1, Spot M-05

Parking motorcycle XYZ-789...
Ticket #2: Motorcycle parked at Floor 1, Spot S-01

Parking bus BUS-001...
Ticket #3: Bus parked at Floor 1, Spot L-01

Available spots: 87

Vehicle ABC-123 leaving...
Duration: 2.5 hours
Fee: $7.50

=== STARTER CODE ===
"""

from enum import Enum
from datetime import datetime
from abc import ABC, abstractmethod

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Create parking lot and simulate operations
