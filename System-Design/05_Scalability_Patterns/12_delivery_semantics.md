# Message Delivery Semantics

## Overview

When sending messages between services, you need to decide how many times each message gets delivered. This is one of the most important decisions in distributed systems.

```
┌─────────────────────────────────────────────────────────────────┐
│                  DELIVERY SEMANTICS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  AT-MOST-ONCE:     Message delivered 0 or 1 time               │
│                    "Fire and forget"                            │
│                    May LOSE messages                            │
│                                                                  │
│  AT-LEAST-ONCE:    Message delivered 1 or more times           │
│                    "Keep trying until ACK"                      │
│                    May have DUPLICATES                          │
│                                                                  │
│  EXACTLY-ONCE:     Message delivered exactly 1 time            │
│                    "The holy grail"                             │
│                    HARD to achieve                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## At-Most-Once Delivery

**Definition**: Send the message once. If it fails, don't retry.

```
FLOW:
┌────────────┐         ┌────────────┐
│  Producer  │──msg───►│  Consumer  │
└────────────┘         └────────────┘
                           │
               ┌───────────┴───────────┐
               │                       │
           Received                 Lost
           (count: 1)              (count: 0)

Either way, message sent only ONCE
```

**When to use**: Metrics, logs, non-critical notifications

**Implementation**: Send without waiting for ACK
```python
def send_at_most_once(message):
    try:
        queue.send(message)  # No retry
    except:
        pass  # Accept loss
```

---

## At-Least-Once Delivery

**Definition**: Keep sending until acknowledged. May result in duplicates.

```
FLOW:
┌────────────┐         ┌────────────┐
│  Producer  │──msg───►│  Consumer  │
└────────────┘    │    └────────────┘
      ▲           │         │
      │        (lost)    (process)
      │           │         │
      └───retry───┘    (ACK lost)
                            │
Producer sends again ◄──────┘
Message processed TWICE!
```

**When to use**: Most applications (with idempotent consumers)

**Implementation**: Retry until ACK received
```python
def send_at_least_once(message):
    while True:
        try:
            queue.send(message)
            ack = queue.wait_for_ack(timeout=5)
            if ack:
                break
        except Timeout:
            continue  # Retry
```

---

## Exactly-Once Delivery

**The Hard Truth**: True exactly-once delivery is theoretically impossible in distributed systems. What we call "exactly-once" is actually "effectively exactly-once" through idempotency.

```
"EXACTLY-ONCE" = AT-LEAST-ONCE + IDEMPOTENT CONSUMER
┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Producer ──msg──► Queue ──msg──► Consumer                     │
│                                      │                          │
│                              ┌───────┴───────┐                 │
│                              │               │                  │
│                          Received        Duplicate              │
│                              │               │                  │
│                         Process          Detect &               │
│                              │           Discard                │
│                              │               │                  │
│                              └───────┬───────┘                  │
│                                      │                          │
│                            EFFECT: Exactly once                │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

**How Kafka achieves "exactly-once"**:
1. Idempotent producer (deduplicates on send)
2. Transactional writes (atomic batch commits)
3. Consumer offset management (tracks position)

## Comparison

| Aspect | At-Most-Once | At-Least-Once | Exactly-Once |
|--------|--------------|---------------|--------------|
| **Messages lost** | Possible | No | No |
| **Duplicates** | No | Possible | No |
| **Complexity** | Simple | Medium | High |
| **Performance** | Fastest | Fast | Slower |
| **Use case** | Metrics, logs | Most apps | Financial, critical |

## Interview Questions

1. "Explain the difference between at-least-once and exactly-once delivery."
2. "Why is exactly-once delivery considered impossible?"
3. "How would you handle duplicate messages?"

## Key Takeaways

```
┌────────────────────────────────────────────────────────────────┐
│              DELIVERY SEMANTICS SUMMARY                         │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  AT-MOST-ONCE:                                                 │
│  └── Accept message loss, no duplicates                       │
│  └── Good for: metrics, logs                                   │
│                                                                 │
│  AT-LEAST-ONCE:                                                │
│  └── No message loss, handle duplicates                       │
│  └── Good for: most applications                               │
│                                                                 │
│  EXACTLY-ONCE:                                                 │
│  └── Actually "at-least-once + idempotency"                   │
│  └── Good for: financial, critical operations                  │
│                                                                 │
│  PRACTICAL ADVICE:                                             │
│  └── Default to at-least-once                                  │
│  └── Make consumers idempotent                                 │
│  └── Use idempotency keys for critical ops                    │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

*Congratulations! You've completed the Scalability Patterns section. Continue to [Case Studies](../06_Case_Studies/README.md) for real-world applications.*
