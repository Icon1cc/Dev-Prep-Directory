# Project 6: Simple Message Queue

Build a basic in-memory message queue.

## Problem Description

```
┌────────────────────────────────────────────────────────────────┐
│                     MESSAGE QUEUE                               │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Build a message queue that supports:                          │
│  • Publish messages to topics                                  │
│  • Subscribe consumers to topics                               │
│  • Deliver messages to subscribers                             │
│  • Handle multiple consumers (fan-out)                         │
│                                                                 │
│  Producer ──► [Topic: orders] ──► Consumer 1                   │
│                     │                                           │
│                     └──────────► Consumer 2                    │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Python Implementation

```python
import threading
import queue
import time
from typing import Callable, Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Message:
    """Represents a message in the queue."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    topic: str = ""
    body: Any = None
    timestamp: datetime = field(default_factory=datetime.now)
    headers: Dict = field(default_factory=dict)


class Topic:
    """Represents a topic that holds messages."""

    def __init__(self, name: str, max_size: int = 10000):
        self.name = name
        self.messages = queue.Queue(maxsize=max_size)
        self.subscribers: List['Consumer'] = []
        self.lock = threading.Lock()

    def publish(self, message: Message) -> bool:
        """Add a message to the topic."""
        try:
            message.topic = self.name
            self.messages.put_nowait(message)
            self._notify_subscribers(message)
            return True
        except queue.Full:
            return False

    def subscribe(self, consumer: 'Consumer'):
        """Add a subscriber to this topic."""
        with self.lock:
            if consumer not in self.subscribers:
                self.subscribers.append(consumer)

    def unsubscribe(self, consumer: 'Consumer'):
        """Remove a subscriber from this topic."""
        with self.lock:
            if consumer in self.subscribers:
                self.subscribers.remove(consumer)

    def _notify_subscribers(self, message: Message):
        """Notify all subscribers of new message."""
        with self.lock:
            for subscriber in self.subscribers:
                subscriber.receive(message)


class Consumer:
    """Represents a message consumer."""

    def __init__(self, name: str, handler: Callable[[Message], None] = None):
        self.name = name
        self.handler = handler or self._default_handler
        self.message_queue = queue.Queue()
        self.running = False
        self.thread = None
        self.processed_count = 0

    def _default_handler(self, message: Message):
        """Default message handler - just print."""
        print(f"[{self.name}] Received: {message.body}")

    def receive(self, message: Message):
        """Receive a message (called by topic)."""
        self.message_queue.put(message)

    def start(self):
        """Start processing messages."""
        self.running = True
        self.thread = threading.Thread(target=self._process_loop)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """Stop processing messages."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)

    def _process_loop(self):
        """Main processing loop."""
        while self.running:
            try:
                message = self.message_queue.get(timeout=0.1)
                self.handler(message)
                self.processed_count += 1
            except queue.Empty:
                continue


class MessageBroker:
    """Central message broker managing topics and routing."""

    def __init__(self):
        self.topics: Dict[str, Topic] = {}
        self.lock = threading.Lock()

    def create_topic(self, name: str, max_size: int = 10000) -> Topic:
        """Create a new topic."""
        with self.lock:
            if name not in self.topics:
                self.topics[name] = Topic(name, max_size)
            return self.topics[name]

    def get_topic(self, name: str) -> Topic:
        """Get existing topic or create new one."""
        if name not in self.topics:
            return self.create_topic(name)
        return self.topics[name]

    def publish(self, topic_name: str, body: Any, headers: Dict = None) -> bool:
        """Publish a message to a topic."""
        topic = self.get_topic(topic_name)
        message = Message(body=body, headers=headers or {})
        return topic.publish(message)

    def subscribe(self, topic_name: str, consumer: Consumer):
        """Subscribe a consumer to a topic."""
        topic = self.get_topic(topic_name)
        topic.subscribe(consumer)

    def unsubscribe(self, topic_name: str, consumer: Consumer):
        """Unsubscribe a consumer from a topic."""
        if topic_name in self.topics:
            self.topics[topic_name].unsubscribe(consumer)


# Demonstration
def order_processor(message: Message):
    """Example handler for order messages."""
    print(f"  Processing order: {message.body}")
    time.sleep(0.1)  # Simulate processing time


def notification_sender(message: Message):
    """Example handler for sending notifications."""
    print(f"  Sending notification for: {message.body}")


def analytics_recorder(message: Message):
    """Example handler for analytics."""
    print(f"  Recording analytics: {message.body}")


if __name__ == "__main__":
    print("=== Message Queue Demo ===\n")

    # Create broker
    broker = MessageBroker()

    # Create consumers with different handlers
    order_consumer = Consumer("OrderProcessor", order_processor)
    notification_consumer = Consumer("NotificationService", notification_sender)
    analytics_consumer = Consumer("AnalyticsService", analytics_recorder)

    # Subscribe to topics
    broker.subscribe("orders", order_consumer)
    broker.subscribe("orders", notification_consumer)  # Multiple consumers
    broker.subscribe("orders", analytics_consumer)

    # Start consumers
    order_consumer.start()
    notification_consumer.start()
    analytics_consumer.start()

    print("Publishing orders...\n")

    # Publish some messages
    for i in range(5):
        order = {"order_id": i + 1, "item": f"Product_{i+1}", "quantity": i + 1}
        broker.publish("orders", order)
        time.sleep(0.2)

    # Wait for processing
    time.sleep(1)

    # Stop consumers
    order_consumer.stop()
    notification_consumer.stop()
    analytics_consumer.stop()

    print(f"\n--- Statistics ---")
    print(f"OrderProcessor processed: {order_consumer.processed_count}")
    print(f"NotificationService processed: {notification_consumer.processed_count}")
    print(f"AnalyticsService processed: {analytics_consumer.processed_count}")


    # Demo: Consumer Groups (competing consumers)
    print("\n\n=== Consumer Groups Demo ===")
    print("(Multiple consumers sharing work)\n")

    class ConsumerGroup:
        """Group of consumers that share messages (each message to one consumer)."""

        def __init__(self, name: str, num_consumers: int, handler: Callable):
            self.name = name
            self.message_queue = queue.Queue()
            self.consumers = []
            self.running = False

            for i in range(num_consumers):
                consumer_name = f"{name}-{i}"
                self.consumers.append(consumer_name)

            self.handler = handler
            self.threads = []

        def receive(self, message: Message):
            """Receive message for the group."""
            self.message_queue.put(message)

        def start(self):
            """Start all consumers in the group."""
            self.running = True
            for name in self.consumers:
                t = threading.Thread(target=self._worker, args=(name,))
                t.daemon = True
                t.start()
                self.threads.append(t)

        def stop(self):
            self.running = False

        def _worker(self, name: str):
            """Worker that processes messages."""
            while self.running:
                try:
                    message = self.message_queue.get(timeout=0.1)
                    print(f"  [{name}] handling: {message.body}")
                    self.handler(message)
                except queue.Empty:
                    continue

    # Create a consumer group with 3 workers
    def handle_task(msg):
        time.sleep(0.2)  # Simulate work

    group = ConsumerGroup("Workers", 3, handle_task)
    broker.subscribe("tasks", group)
    group.start()

    # Publish tasks
    for i in range(6):
        broker.publish("tasks", f"Task-{i+1}")
        time.sleep(0.05)

    time.sleep(2)
    group.stop()

    print("\nDemo complete!")
```

---

## Key Concepts Demonstrated

### 1. Pub/Sub Pattern
```
Publisher ──► Topic ──┬──► Subscriber 1 (gets copy)
                      ├──► Subscriber 2 (gets copy)
                      └──► Subscriber 3 (gets copy)

All subscribers receive ALL messages
```

### 2. Consumer Groups
```
Publisher ──► Topic ──► Consumer Group ──┬──► Worker 1 (gets some)
                                         ├──► Worker 2 (gets some)
                                         └──► Worker 3 (gets some)

Messages are distributed among workers (each message to ONE worker)
```

### 3. Competing Consumers
```
Good for: Parallel processing of tasks
Example: Order processing where each order handled once
```

---

## Extensions

### 1. Message Acknowledgment
```python
def ack(self, message_id: str):
    """Acknowledge message processing."""
    # Remove from pending, mark as processed
    pass

def nack(self, message_id: str):
    """Negative ack - requeue for retry."""
    # Put back in queue
    pass
```

### 2. Dead Letter Queue
```python
def process_with_dlq(self, message: Message):
    """Send to DLQ after max retries."""
    try:
        self.handler(message)
    except Exception as e:
        message.retry_count += 1
        if message.retry_count >= self.max_retries:
            self.dead_letter_queue.put(message)
        else:
            self.requeue(message)
```

### 3. Persistence
```python
def persist_message(self, message: Message):
    """Write message to disk for durability."""
    with open(f"messages/{message.id}.json", 'w') as f:
        json.dump(asdict(message), f)
```

---

## Comparison with Real Systems

| Feature | This Implementation | Kafka | RabbitMQ |
|---------|-------------------|-------|----------|
| Persistence | No | Yes | Yes |
| Ordering | Within topic | Within partition | Within queue |
| Consumer Groups | Basic | Full support | Competing consumers |
| Scalability | Single process | Distributed | Clustered |

---

*Congratulations! You've completed the Hands-On Projects section!*
