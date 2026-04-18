"""
Problem 039: Observer Design Pattern

Difficulty: Intermediate-Advanced
Topic: Design Patterns

=== PROBLEM DESCRIPTION ===

The Observer pattern defines a one-to-many dependency. When one object (Subject)
changes state, all its dependents (Observers) are notified automatically.
Think: YouTube subscriptions - when a channel posts, all subscribers get notified.

Your Task:
-----------
1. Create a `Subject` base class (or use ABC):
   - `_observers` list to store observers
   - `attach(observer)` - add observer to list
   - `detach(observer)` - remove observer from list
   - `notify()` - call update() on all observers

2. Create an `Observer` ABC:
   - Abstract method `update(message)` - called when notified

3. Create `NewsPublisher(Subject)`:
   - `publish_news(news)` - stores news and notifies observers

4. Create observer classes:
   - `EmailSubscriber` - prints "Email to {name}: {news}"
   - `SMSSubscriber` - prints "SMS to {name}: {news}"
   - `PushSubscriber` - prints "Push notification to {name}: {news}"

Expected Output:
----------------
Publishing: Breaking News - Python 4.0 Released!
Email to alice@email.com: Breaking News - Python 4.0 Released!
SMS to +1234567890: Breaking News - Python 4.0 Released!
Push notification to Alice: Breaking News - Python 4.0 Released!

=== CONCEPTS TO LEARN ===
- Subject maintains list of observers
- Loose coupling: subject doesn't know observer details
- Observers can be added/removed dynamically
- Used in: GUI events, pub/sub systems, MVC architecture

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# publisher = NewsPublisher()
#
# email_sub = EmailSubscriber("alice@email.com")
# sms_sub = SMSSubscriber("+1234567890")
# push_sub = PushSubscriber("Alice")
#
# publisher.attach(email_sub)
# publisher.attach(sms_sub)
# publisher.attach(push_sub)
#
# publisher.publish_news("Breaking News - Python 4.0 Released!")
