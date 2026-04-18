# Message Queues

## What is a Message Queue?

A **Message Queue** is a form of asynchronous communication between services. Messages are stored in a queue until processed by a consumer, decoupling producers from consumers.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Message Queue Concept                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Synchronous (Without Queue):                                         │
│   ────────────────────────────                                          │
│                                                                         │
│   User ──► API ──► Email Service ──► SMS Service ──► Response          │
│                        │                  │                             │
│                     (waits)            (waits)                         │
│                                                                         │
│   Total time: 50ms + 100ms + 80ms = 230ms                              │
│   Problem: User waits for everything!                                  │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   Asynchronous (With Queue):                                           │
│   ──────────────────────────                                            │
│                                                                         │
│   User ──► API ──► Queue ──► Response (50ms)                           │
│                      │                                                  │
│                      ├──────────► Email Worker (processes later)       │
│                      └──────────► SMS Worker (processes later)         │
│                                                                         │
│   User gets response immediately!                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Core Concepts

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Message Queue Components                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────┐    ┌─────────────────────┐    ┌──────────┐             │
│   │ Producer │───►│       Queue         │───►│ Consumer │             │
│   └──────────┘    │                     │    └──────────┘             │
│                   │  [msg1][msg2][msg3] │                              │
│                   │        FIFO         │                              │
│                   └─────────────────────┘                              │
│                                                                         │
│   PRODUCER: Sends messages to the queue                                │
│   QUEUE: Stores messages until consumed                                │
│   CONSUMER: Receives and processes messages                            │
│   MESSAGE: Data payload being transmitted                              │
│   BROKER: The server managing queues (Kafka, RabbitMQ, etc.)          │
│                                                                         │
│   Message Lifecycle:                                                    │
│   ──────────────────                                                    │
│   1. Producer creates message                                          │
│   2. Message sent to broker                                            │
│   3. Broker persists message to queue                                  │
│   4. Consumer pulls message from queue                                 │
│   5. Consumer processes message                                        │
│   6. Consumer sends ACK (acknowledgment)                               │
│   7. Broker removes message from queue                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Queue vs Topic (Pub/Sub)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Queue vs Topic                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   QUEUE (Point-to-Point):                                              │
│   ───────────────────────                                               │
│   Each message consumed by ONE consumer                                │
│                                                                         │
│   Producer ──► [Queue] ──┬──► Consumer A (gets msg1, msg3)            │
│                          └──► Consumer B (gets msg2, msg4)            │
│                                                                         │
│   Use case: Task distribution (work queue)                             │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   TOPIC (Publish/Subscribe):                                           │
│   ──────────────────────────                                            │
│   Each message delivered to ALL subscribers                            │
│                                                                         │
│   Publisher ──► [Topic] ──┬──► Subscriber A (gets ALL messages)       │
│                           ├──► Subscriber B (gets ALL messages)       │
│                           └──► Subscriber C (gets ALL messages)       │
│                                                                         │
│   Use case: Broadcasting events (notifications)                        │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   CONSUMER GROUP (Kafka-style):                                        │
│   ─────────────────────────────                                         │
│   Combines both: topics with parallel processing                       │
│                                                                         │
│   Producer ──► [Topic: orders]                                        │
│                     │                                                   │
│                     ├──► Group A ──┬──► Consumer A1                   │
│                     │              └──► Consumer A2                   │
│                     │                                                   │
│                     └──► Group B ──┬──► Consumer B1                   │
│                                    └──► Consumer B2                   │
│                                                                         │
│   Each group gets ALL messages                                         │
│   Within a group, messages are distributed                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Delivery Guarantees

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Delivery Semantics                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. AT-MOST-ONCE                                                      │
│      ───────────────                                                    │
│      Message delivered 0 or 1 time                                     │
│      Fire and forget - no retries                                      │
│                                                                         │
│      Producer ──► Broker                                               │
│                   (no ack)                                             │
│                                                                         │
│      Pros: Fastest, lowest latency                                     │
│      Cons: Messages can be lost                                        │
│      Use: Metrics, logs (where loss is acceptable)                     │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   2. AT-LEAST-ONCE (Most Common)                                       │
│      ──────────────────────────────                                     │
│      Message delivered 1 or more times                                 │
│      Retry until acknowledged                                          │
│                                                                         │
│      Producer ──► Broker ──► Consumer                                 │
│               ◄── ACK                                                  │
│                                                                         │
│      Pros: No message loss                                             │
│      Cons: Duplicates possible                                         │
│      Use: Email sending, order processing (with idempotency)          │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   3. EXACTLY-ONCE                                                      │
│      ─────────────                                                      │
│      Message delivered exactly 1 time                                  │
│      Hardest to achieve                                                │
│                                                                         │
│      Requires:                                                         │
│      • Idempotent producers (dedup by ID)                             │
│      • Transactional consumers                                         │
│      • Message deduplication                                           │
│                                                                         │
│      Pros: Perfect delivery                                            │
│      Cons: Complex, slower, more expensive                             │
│      Use: Financial transactions, payments                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Achieving Exactly-Once (In Practice)

```python
# Idempotent Consumer Pattern
class OrderProcessor:
    def __init__(self):
        self.processed_ids = set()  # Or use database

    def process_order(self, message):
        order_id = message['order_id']

        # Check if already processed
        if order_id in self.processed_ids:
            print(f"Order {order_id} already processed, skipping")
            return

        # Process the order
        self._create_order(message)

        # Mark as processed
        self.processed_ids.add(order_id)
```

---

## Popular Message Queue Systems

### Apache Kafka

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Apache Kafka                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Architecture:                                                         │
│   ─────────────                                                         │
│                                                                         │
│   Topic: user-events                                                   │
│   ┌───────────────────────────────────────────────────────┐            │
│   │ Partition 0: [msg1][msg4][msg7][msg10]...             │            │
│   │ Partition 1: [msg2][msg5][msg8][msg11]...             │            │
│   │ Partition 2: [msg3][msg6][msg9][msg12]...             │            │
│   └───────────────────────────────────────────────────────┘            │
│                                                                         │
│   Key Features:                                                         │
│   ─────────────                                                         │
│   • Distributed, partitioned, replicated commit log                    │
│   • High throughput (millions of messages/sec)                         │
│   • Messages retained for configurable time (days/weeks)               │
│   • Consumer groups for parallel processing                            │
│   • Strong ordering within partition                                   │
│   • Replayable (consumers can re-read old messages)                    │
│                                                                         │
│   Best For:                                                            │
│   ─────────                                                             │
│   • Event streaming                                                    │
│   • Log aggregation                                                    │
│   • Stream processing                                                  │
│   • Event sourcing                                                     │
│   • High-throughput scenarios                                          │
│                                                                         │
│   Trade-offs:                                                          │
│   ───────────                                                           │
│   • More complex to operate                                            │
│   • No built-in dead letter queue                                      │
│   • Not ideal for fine-grained routing                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### RabbitMQ

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    RabbitMQ                                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Architecture:                                                         │
│   ─────────────                                                         │
│                                                                         │
│   Producer ──► Exchange ──┬──► Queue A ──► Consumer A                  │
│                           │                                            │
│                           ├──► Queue B ──► Consumer B                  │
│                           │                                            │
│                           └──► Queue C ──► Consumer C                  │
│                                                                         │
│   Exchange Types:                                                       │
│   ───────────────                                                       │
│   • Direct: Route by exact routing key                                 │
│   • Fanout: Broadcast to all queues                                    │
│   • Topic: Route by pattern (orders.*, *.critical)                    │
│   • Headers: Route by message headers                                  │
│                                                                         │
│   Key Features:                                                         │
│   ─────────────                                                         │
│   • AMQP protocol support                                              │
│   • Flexible routing with exchanges                                    │
│   • Built-in dead letter queues                                        │
│   • Message acknowledgments                                            │
│   • Priority queues                                                    │
│   • Plugin ecosystem                                                   │
│                                                                         │
│   Best For:                                                            │
│   ─────────                                                             │
│   • Complex routing scenarios                                          │
│   • Task queues                                                        │
│   • Request/reply patterns                                             │
│   • Smaller scale messaging                                            │
│                                                                         │
│   Trade-offs:                                                          │
│   ───────────                                                           │
│   • Lower throughput than Kafka                                        │
│   • Messages deleted after consumption                                 │
│   • Not designed for replay                                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Comparison

| Feature | Kafka | RabbitMQ |
|---------|-------|----------|
| Throughput | Very High (millions/sec) | High (tens of thousands/sec) |
| Message Retention | Configurable (days) | Until consumed |
| Replay | Yes | No |
| Ordering | Per partition | Per queue |
| Routing | Basic (partitions) | Advanced (exchanges) |
| Use Case | Event streaming, logs | Task queues, RPC |
| Complexity | Higher | Lower |
| Protocol | Custom | AMQP |

---

## Common Patterns

### 1. Work Queue (Task Distribution)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Work Queue Pattern                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Producer: API Server                                                 │
│   Queue: Tasks to process                                              │
│   Consumers: Worker pool                                               │
│                                                                         │
│   API ──► [task1][task2][task3][task4] ──┬──► Worker 1                │
│                                          ├──► Worker 2                │
│                                          └──► Worker 3                │
│                                                                         │
│   Use cases:                                                           │
│   • Background jobs                                                    │
│   • Image processing                                                   │
│   • Report generation                                                  │
│   • Email sending                                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2. Publish/Subscribe (Fan-out)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Pub/Sub Pattern                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Event: "order.created"                                               │
│                                                                         │
│   Order Service ──► [order.created] ──┬──► Email Service              │
│                                       ├──► Inventory Service          │
│                                       ├──► Analytics Service          │
│                                       └──► Notification Service       │
│                                                                         │
│   All services receive the event independently                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3. Request/Reply (RPC)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Request/Reply Pattern                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Client ──► [Request Queue] ──► Server                                │
│                                     │                                   │
│   Client ◄── [Reply Queue] ◄───────┘                                   │
│                                                                         │
│   Request includes: correlation_id, reply_to queue                     │
│   Reply includes: correlation_id for matching                          │
│                                                                         │
│   Use cases:                                                           │
│   • Synchronous-like calls over async infrastructure                   │
│   • Remote procedure calls                                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4. Dead Letter Queue (DLQ)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Dead Letter Queue                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   When messages fail repeatedly, move to DLQ for investigation        │
│                                                                         │
│   [Main Queue] ──► Consumer                                            │
│        │              │                                                 │
│        │              │ Processing fails 3 times                       │
│        │              ▼                                                 │
│        └────────► [Dead Letter Queue] ──► Manual review               │
│                                                                         │
│   Why messages fail:                                                   │
│   • Invalid message format                                             │
│   • Missing required data                                              │
│   • Downstream service unavailable                                     │
│   • Bug in consumer code                                               │
│                                                                         │
│   Handling DLQ:                                                        │
│   • Alert on DLQ growth                                                │
│   • Manual inspection and retry                                        │
│   • Automated retry with backoff                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Handling Failures

### Consumer Failure

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Consumer Failure Handling                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Scenario: Consumer crashes while processing                          │
│                                                                         │
│   Message lifecycle with ACK:                                          │
│   ───────────────────────────                                           │
│   1. Consumer pulls message (message marked "in-flight")               │
│   2. Consumer processes message                                        │
│   3a. Success → Send ACK → Message removed from queue                  │
│   3b. Failure → No ACK → Message returned to queue (redelivered)       │
│                                                                         │
│   Implementation:                                                       │
│   ───────────────                                                       │
│   def process_message(message):                                        │
│       try:                                                             │
│           result = do_work(message)                                    │
│           channel.basic_ack(message.delivery_tag)  # Success          │
│       except Exception as e:                                           │
│           channel.basic_nack(message.delivery_tag,                    │
│                              requeue=True)  # Retry                    │
│           # Or send to DLQ after N retries                            │
│                                                                         │
│   Visibility Timeout (SQS-style):                                      │
│   ───────────────────────────────                                       │
│   Message hidden from other consumers for X seconds                    │
│   If not ACK'd in time → becomes visible again                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Ordering Guarantees

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Message Ordering                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Problem: With multiple consumers, order can be lost                  │
│                                                                         │
│   Queue: [msg1][msg2][msg3]                                           │
│                 │                                                       │
│        ┌───────┼───────┐                                               │
│        ▼       ▼       ▼                                               │
│   Worker 1  Worker 2  Worker 3                                         │
│   (msg1)    (msg2)    (msg3)                                          │
│     ↓         ↓         ↓                                              │
│   Done     [slow]     Done                                             │
│                                                                         │
│   Actual order: msg1, msg3, msg2  (wrong!)                            │
│                                                                         │
│   Solutions:                                                           │
│   ──────────                                                            │
│                                                                         │
│   1. Single Consumer                                                   │
│      Process all messages sequentially (limits throughput)             │
│                                                                         │
│   2. Partition by Key (Kafka approach)                                 │
│      Messages with same key → same partition → same consumer          │
│      Order guaranteed WITHIN partition                                 │
│                                                                         │
│      order.user_id = 123 → hash(123) % partitions → partition 2       │
│      All orders for user 123 go to partition 2                        │
│                                                                         │
│   3. Sequence Numbers                                                  │
│      Include sequence in message, consumer reorders                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## When to Use / When NOT to Use

### When to Use Message Queues

✅ Async processing needed (don't block user)
✅ Decouple services (producer doesn't need consumer online)
✅ Handle traffic spikes (queue absorbs burst)
✅ Reliable delivery required (retries, persistence)
✅ Distribute work across workers
✅ Event-driven architecture

### When NOT to Use

❌ Simple synchronous requests sufficient
❌ Need immediate response (queues add latency)
❌ Low volume, simple architecture
❌ Overhead not justified
❌ Strong transactional consistency required

---

## Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "How to ensure exactly-once?" | Understanding reality | True exactly-once is hard; use idempotent consumers |
| "Kafka vs RabbitMQ?" | Trade-off understanding | Kafka for high throughput/streaming; RabbitMQ for routing/tasks |
| "What if consumer is slow?" | Scaling knowledge | Add more consumers, use partitions, or implement backpressure |
| "How to handle poison messages?" | Operational thinking | Retry with backoff, DLQ, alerting |

---

**Next:** Continue to [04_cdn.md](./04_cdn.md) to learn about content delivery networks.
