# Scalability Patterns

> "The art of system design is knowing which patterns to apply and when."

This section covers the essential scalability patterns that appear in every major distributed system. These patterns are the building blocks interviewers expect you to understand deeply.

## What You'll Learn

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SCALABILITY PATTERNS                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  DATA DISTRIBUTION          ARCHITECTURE           RELIABILITY      │
│  ┌─────────────┐           ┌─────────────┐       ┌─────────────┐   │
│  │ Sharding    │           │ Microservices│      │ Circuit     │   │
│  │ Replication │           │ Event-Driven │      │ Breakers    │   │
│  │ Partitioning│           │ CQRS        │       │ Bulkheads   │   │
│  └─────────────┘           └─────────────┘       └─────────────┘   │
│                                                                     │
│  MESSAGING                 CONSISTENCY            RESILIENCE        │
│  ┌─────────────┐           ┌─────────────┐       ┌─────────────┐   │
│  │ Event       │           │ Idempotency │       │ Backpressure│   │
│  │ Sourcing    │           │ Delivery    │       │ Retries     │   │
│  │ Async       │           │ Guarantees  │       │ Timeouts    │   │
│  └─────────────┘           └─────────────┘       └─────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Files in This Section

| File | Topic | Interview Frequency |
|------|-------|---------------------|
| [01_sharding.md](01_sharding.md) | Database sharding strategies | ⭐⭐⭐⭐⭐ |
| [02_replication.md](02_replication.md) | Data replication patterns | ⭐⭐⭐⭐⭐ |
| [03_partitioning.md](03_partitioning.md) | Partitioning schemes | ⭐⭐⭐⭐ |
| [04_event_driven.md](04_event_driven.md) | Event-driven architecture | ⭐⭐⭐⭐ |
| [05_microservices_monolith.md](05_microservices_monolith.md) | Microservices vs Monolith | ⭐⭐⭐⭐⭐ |
| [06_cqrs.md](06_cqrs.md) | Command Query Responsibility Segregation | ⭐⭐⭐ |
| [07_event_sourcing.md](07_event_sourcing.md) | Event Sourcing pattern | ⭐⭐⭐ |
| [08_backpressure.md](08_backpressure.md) | Backpressure handling | ⭐⭐⭐⭐ |
| [09_circuit_breakers.md](09_circuit_breakers.md) | Circuit breaker pattern | ⭐⭐⭐⭐ |
| [10_bulkheads.md](10_bulkheads.md) | Bulkhead pattern | ⭐⭐⭐ |
| [11_idempotency.md](11_idempotency.md) | Idempotency in distributed systems | ⭐⭐⭐⭐⭐ |
| [12_delivery_semantics.md](12_delivery_semantics.md) | Exactly-once vs At-least-once | ⭐⭐⭐⭐ |

## Study Order

```
START HERE
    │
    ▼
┌─────────────────────────────────────────────┐
│ 1. Sharding → Replication → Partitioning    │  ← Data Layer Fundamentals
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ 2. Microservices vs Monolith                │  ← Architecture Decision
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ 3. Event-Driven → CQRS → Event Sourcing     │  ← Advanced Architecture
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ 4. Circuit Breakers → Bulkheads             │  ← Resilience Patterns
│    → Backpressure                           │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ 5. Idempotency → Delivery Semantics         │  ← Correctness Guarantees
└─────────────────────────────────────────────┘
```

## Key Interview Insights

### What Interviewers Look For

1. **Pattern Recognition**: Can you identify which pattern solves which problem?
2. **Tradeoff Analysis**: Do you understand the costs of each approach?
3. **Real-World Application**: Can you apply patterns to actual systems?
4. **Failure Thinking**: Do you consider what happens when things go wrong?

### Common Interview Questions

- "How would you scale this database as traffic grows 100x?"
- "What happens when this service is down?"
- "How do you ensure data consistency across services?"
- "How do you handle duplicate messages?"

### Red Flags to Avoid

❌ Applying patterns without justification
❌ Not discussing tradeoffs
❌ Ignoring failure scenarios
❌ Over-engineering simple problems
❌ Using buzzwords without understanding

---

## Pattern Selection Guide

```
┌─────────────────────────────────────────────────────────────────┐
│                  WHEN TO USE WHICH PATTERN                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  "Data is too big for one machine"                              │
│     └──→ Sharding + Partitioning                                │
│                                                                 │
│  "Need high availability for reads"                             │
│     └──→ Replication (read replicas)                            │
│                                                                 │
│  "Read and write patterns are very different"                   │
│     └──→ CQRS                                                   │
│                                                                 │
│  "Need complete audit trail"                                    │
│     └──→ Event Sourcing                                         │
│                                                                 │
│  "Services need to communicate without tight coupling"          │
│     └──→ Event-Driven Architecture                              │
│                                                                 │
│  "Downstream service might fail"                                │
│     └──→ Circuit Breaker                                        │
│                                                                 │
│  "Producer faster than consumer"                                │
│     └──→ Backpressure                                           │
│                                                                 │
│  "Operations might be retried"                                  │
│     └──→ Idempotency                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

**Next**: Start with [Sharding Strategies](01_sharding.md) to understand how to distribute data across machines.
