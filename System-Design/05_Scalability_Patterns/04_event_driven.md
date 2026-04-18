# Event-Driven Architecture

## What is Event-Driven Architecture?

**Simple explanation**: Instead of services calling each other directly, services communicate by publishing events ("something happened") that other services can listen to and react to.

**Technical definition**: Event-Driven Architecture (EDA) is a software design pattern where program flow is determined by events—significant state changes published by producers and consumed by subscribers asynchronously.

```
TRADITIONAL REQUEST-RESPONSE:         EVENT-DRIVEN:
┌─────────┐  Request   ┌─────────┐   ┌─────────┐         ┌─────────┐
│ Service │ ─────────► │ Service │   │ Service │ ──────► │  Event  │
│    A    │ ◄───────── │    B    │   │    A    │         │   Bus   │
└─────────┘  Response  └─────────┘   └─────────┘         └────┬────┘
                                                              │
     A waits for B                         ┌──────────────────┼──────┐
     Tight coupling                        ▼                  ▼      ▼
                                      ┌─────────┐      ┌─────────┐  ...
                                      │ Service │      │ Service │
                                      │    B    │      │    C    │
                                      └─────────┘      └─────────┘
                                      A doesn't wait, loose coupling
```

## Core Concepts

### Events

An event represents something that happened—a fact about the past.

```json
{
  "event_id": "evt_abc123",
  "event_type": "OrderPlaced",
  "timestamp": "2024-03-15T10:30:00Z",
  "source": "order-service",
  "data": {
    "order_id": "ord_789",
    "user_id": "usr_456",
    "total": 99.99
  }
}
```

### Producers and Consumers

```
┌──────────┐        ┌─────────────────┐        ┌──────────┐
│  Order   │ ─────► │   EVENT BUS     │ ─────► │Inventory │
│ Service  │        │                 │        │ Service  │
│(Producer)│        │  Topic: orders  │        │(Consumer)│
└──────────┘        └─────────────────┘        └──────────┘
                            │
                            └─────────────────► ┌──────────┐
                                                │  Email   │
                                                │ Service  │
                                                └──────────┘
```

## Event-Driven Patterns

### 1. Publish-Subscribe (Pub/Sub)

Publishers send events to topics; all subscribers receive all events.

```
Topic: "orders"
       │
       ├──► Inventory Service (gets ALL orders)
       ├──► Analytics Service (gets ALL orders)
       └──► Notification Service (gets ALL orders)
```

### 2. Event Streaming

Events stored in durable log; consumers read at own pace.

```
EVENT LOG:
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
          ▲               ▲
     Consumer A      Consumer B
     (offset 2)      (offset 5)

- Events persist (days/weeks)
- Consumers track their own position
- Can replay from any point
```

### 3. Saga Pattern

Coordinate long-running transactions using events.

```
ORDER SAGA:
┌─────────┐  OrderPlaced  ┌───────────┐  InventoryReserved  ┌─────────┐
│  Order  │ ────────────► │ Inventory │ ──────────────────► │ Payment │
│ Service │               │  Service  │                     │ Service │
└─────────┘               └───────────┘                     └────┬────┘
     ▲                                                           │
     │                    PaymentReceived                        │
     └───────────────────────────────────────────────────────────┘

If Payment fails: Compensating events to rollback
```

## Popular Event Brokers

| Broker | Best For | Notes |
|--------|----------|-------|
| **Apache Kafka** | High throughput, durability | Log-based |
| **RabbitMQ** | Flexibility, routing | Traditional queue |
| **AWS SNS/SQS** | Cloud-native, managed | Easy setup |
| **Redis Streams** | Low latency | In-memory |

## Error Handling

### Dead Letter Queues (DLQ)

```
Event Queue ──► Consumer ──► Success
                   │
                   │ Retry 3x, then
                   ▼
              Dead Letter Queue
              (Manual inspection)
```

## Advantages and Disadvantages

| Advantage | Disadvantage |
|-----------|--------------|
| Loose coupling | Harder to debug |
| Scalability | Eventual consistency |
| Resilience | Event ordering issues |
| Audit trail | Duplication handling |

## Interview Questions

1. "What is event-driven architecture?"
2. "How do you handle event ordering?"
3. "What happens when a consumer fails?"

## Key Takeaways

```
┌────────────────────────────────────────────────────────────────┐
│  USE EVENT-DRIVEN WHEN:                                        │
│  ├── Multiple services react to same event                    │
│  ├── Producers shouldn't wait for consumers                   │
│  ├── Need audit trail / replay                                │
│                                                                 │
│  AVOID WHEN:                                                   │
│  ├── Simple request-response is sufficient                    │
│  ├── Strong consistency required                              │
│  └── Small team, complexity not justified                     │
└────────────────────────────────────────────────────────────────┘
```

---

*Next: [Microservices vs Monolith](05_microservices_monolith.md) →*
