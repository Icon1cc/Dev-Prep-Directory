"""
Problem 077: Facade Design Pattern

Difficulty: Intermediate
Topic: Structural Design Pattern

=== PROBLEM DESCRIPTION ===

The Facade pattern provides a simplified interface to a complex subsystem.
It doesn't hide the subsystem but provides a convenient entry point.

Your Task:
-----------
1. Create a complex subsystem for home automation:
   - `Light` - on(), off(), dim(level)
   - `Thermostat` - set_temperature(temp), get_temperature()
   - `SecuritySystem` - arm(), disarm(), get_status()
   - `MusicPlayer` - play(song), stop(), set_volume(level)
   - `Television` - on(), off(), set_channel(channel)
   - `CoffeeMaker` - brew(), get_status()

2. Create a `SmartHomeFacade`:
   - `good_morning()` - raises blinds, starts coffee, plays music, sets temp
   - `leaving_home()` - turns off lights, arms security, adjusts temp
   - `movie_time()` - dims lights, turns on TV, sets volume
   - `good_night()` - turns off everything, arms security, adjusts temp

3. Show that subsystems can still be accessed directly when needed

Expected Output:
----------------
--- Good Morning Routine ---
Lights: Dimming to 50%
Thermostat: Setting to 72°F
Coffee: Brewing...
Music: Playing 'Morning Jazz'

--- Leaving Home ---
Lights: All off
Security: Armed
Thermostat: Setting to 65°F

--- Movie Time ---
Lights: Dimming to 20%
TV: On, Channel Netflix
Music: Volume 30%

Can still access subsystems directly:
Coffee status: Ready

=== CONCEPTS TO LEARN ===
- Facade simplifies complex interactions
- Doesn't prevent direct access to subsystems
- Reduces coupling between client and subsystem
- Common in frameworks and libraries

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate facade simplifying complex operations
