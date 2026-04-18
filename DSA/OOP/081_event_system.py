"""
Problem 081: Implementing an Event System (Pub/Sub)

Difficulty: Intermediate
Topic: Real-world Application

=== PROBLEM DESCRIPTION ===

Build an event-driven system where components can publish events and
subscribe to events they're interested in.

Your Task:
-----------
1. Create an `Event` class:
   - Attributes: name, data, timestamp, source
   - `__str__` shows event details

2. Create an `EventBus` (Singleton):
   - `subscribe(event_type, callback)` - register listener
   - `unsubscribe(event_type, callback)` - remove listener
   - `publish(event)` - notify all subscribers
   - Support wildcards: subscribe('user.*') matches 'user.created', 'user.deleted'

3. Create example publishers:
   - `UserService` - publishes 'user.created', 'user.updated', 'user.deleted'
   - `OrderService` - publishes 'order.placed', 'order.shipped', 'order.delivered'

4. Create example subscribers:
   - `EmailNotifier` - sends email for certain events
   - `Logger` - logs all events
   - `Analytics` - tracks specific events

Expected Output:
----------------
Subscribing to events...
Logger subscribed to *
EmailNotifier subscribed to user.created
Analytics subscribed to order.*

Publishing events:
[LOG] Event: user.created - {'id': 1, 'name': 'Alice'}
[EMAIL] Welcome email sent to Alice
[LOG] Event: order.placed - {'order_id': 101, 'user_id': 1}
[ANALYTICS] Order event tracked: order.placed
[LOG] Event: order.shipped - {'order_id': 101}
[ANALYTICS] Order event tracked: order.shipped

=== CONCEPTS TO LEARN ===
- Publish/Subscribe pattern
- Decoupled communication between components
- Event-driven architecture
- Wildcard matching for flexible subscriptions

=== STARTER CODE ===
"""

from datetime import datetime
from typing import Callable, Any
import re

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Create event bus, publishers, and subscribers
