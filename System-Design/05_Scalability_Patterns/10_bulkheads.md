# Bulkhead Pattern

## What is the Bulkhead Pattern?

**Simple explanation**: The Bulkhead pattern isolates different parts of your system so that if one part fails, it doesn't sink the whole ship. Just like compartments in a ship's hull prevent one leak from flooding the entire vessel.

**Technical definition**: The Bulkhead pattern partitions system resources (threads, connections, memory) into isolated pools so that failure in one component doesn't exhaust resources needed by other components.

```
WITHOUT BULKHEADS:
┌─────────────────────────────────────────────────────────────────┐
│                    SINGLE RESOURCE POOL                          │
│                                                                  │
│  Thread Pool: [T1][T2][T3][T4][T5][T6][T7][T8][T9][T10]         │
│                                                                  │
│  Service A (slow)    ──uses──►  [T1][T2][T3][T4][T5][T6]...     │
│  Service B (healthy) ──uses──►  No threads left!                │
│  Service C (healthy) ──uses──►  No threads left!                │
│                                                                  │
│  Result: One slow service starves ALL other services            │
└─────────────────────────────────────────────────────────────────┘

WITH BULKHEADS:
┌─────────────────────────────────────────────────────────────────┐
│                    ISOLATED RESOURCE POOLS                       │
│                                                                  │
│  Service A Pool: [T1][T2][T3]     ← Max 3 threads               │
│  Service B Pool: [T4][T5][T6]     ← Max 3 threads               │
│  Service C Pool: [T7][T8][T9]     ← Max 3 threads               │
│                                                                  │
│  Service A (slow)    ──uses──►  [T1][T2][T3] FULL               │
│  Service B (healthy) ──uses──►  [T4][T5] ✓ Still works!        │
│  Service C (healthy) ──uses──►  [T7] ✓ Still works!            │
│                                                                  │
│  Result: Slow service is ISOLATED, others continue working      │
└─────────────────────────────────────────────────────────────────┘
```

## Why Bulkheads?

### The Resource Exhaustion Problem

```
SCENARIO: E-commerce platform

┌──────────────────────────────────────────────────────────────┐
│                                                               │
│  API Gateway                                                  │
│  Connection Pool: 100 connections total                       │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Product Service  │ User Service │ Payment Service       │ │
│  │   (normal)       │  (normal)    │   (SLOW!)             │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  Without Bulkheads:                                          │
│  ────────────────────────────────────────────────────────    │
│  1. Payment requests pile up                                 │
│  2. All 100 connections waiting on Payment                   │
│  3. Product & User services can't get connections           │
│  4. ENTIRE SITE DOWN!                                        │
│                                                               │
│  With Bulkheads (33 connections each):                       │
│  ────────────────────────────────────────────────────────    │
│  1. Payment requests pile up                                 │
│  2. Payment uses its 33 connections (full)                   │
│  3. Product & User still have their 33 connections          │
│  4. Site still works! Only payments degraded                │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## Types of Bulkheads

### 1. Thread Pool Bulkheads

Isolate threads for different operations.

```python
from concurrent.futures import ThreadPoolExecutor

class BulkheadService:
    def __init__(self):
        # Separate thread pools for each downstream service
        self.payment_pool = ThreadPoolExecutor(max_workers=10, thread_name_prefix="payment")
        self.inventory_pool = ThreadPoolExecutor(max_workers=10, thread_name_prefix="inventory")
        self.notification_pool = ThreadPoolExecutor(max_workers=5, thread_name_prefix="notify")

    def process_payment(self, order):
        # Uses payment pool - won't affect other services
        return self.payment_pool.submit(self.payment_service.charge, order)

    def check_inventory(self, items):
        # Uses inventory pool - isolated
        return self.inventory_pool.submit(self.inventory_service.check, items)

    def send_notification(self, user, message):
        # Uses notification pool - isolated
        return self.notification_pool.submit(self.notify_service.send, user, message)
```

### 2. Connection Pool Bulkheads

Isolate database/HTTP connections.

```python
class DatabaseBulkheads:
    def __init__(self):
        # Separate connection pools per use case
        self.read_pool = create_pool(max_connections=50)
        self.write_pool = create_pool(max_connections=20)
        self.reporting_pool = create_pool(max_connections=5)

    def execute_read(self, query):
        with self.read_pool.connection() as conn:
            return conn.execute(query)

    def execute_write(self, query):
        with self.write_pool.connection() as conn:
            return conn.execute(query)

    def execute_report(self, query):
        # Heavy reporting queries don't affect main operations
        with self.reporting_pool.connection() as conn:
            return conn.execute(query)
```

### 3. Semaphore Bulkheads

Limit concurrent executions.

```python
from threading import Semaphore

class SemaphoreBulkhead:
    def __init__(self, max_concurrent: int):
        self.semaphore = Semaphore(max_concurrent)

    def execute(self, func, *args, **kwargs):
        if not self.semaphore.acquire(blocking=False):
            raise BulkheadFullException("Bulkhead capacity reached")
        try:
            return func(*args, **kwargs)
        finally:
            self.semaphore.release()

# Usage
payment_bulkhead = SemaphoreBulkhead(max_concurrent=10)
inventory_bulkhead = SemaphoreBulkhead(max_concurrent=20)

def process_order(order):
    payment_bulkhead.execute(charge_payment, order)  # Limited to 10 concurrent
    inventory_bulkhead.execute(reserve_items, order)  # Limited to 20 concurrent
```

## Bulkhead Sizing

```
┌─────────────────────────────────────────────────────────────────┐
│                    SIZING GUIDELINES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Consider:                                                      │
│  ├── Expected throughput for each service                       │
│  ├── Response time of downstream services                       │
│  ├── Criticality of each service                               │
│  └── Available resources                                        │
│                                                                  │
│  Formula:                                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Pool Size = (Requests/sec) × (Response Time) × Safety    │  │
│  │                                                           │  │
│  │ Example:                                                  │  │
│  │ - 100 requests/second                                     │  │
│  │ - 0.1 second average response                             │  │
│  │ - 2x safety factor                                        │  │
│  │ - Pool Size = 100 × 0.1 × 2 = 20 threads                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Bulkhead + Circuit Breaker

Best practice: Combine both patterns.

```
┌─────────────────────────────────────────────────────────────────┐
│                COMBINED RESILIENCE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Request ──► Bulkhead ──► Circuit Breaker ──► Service           │
│                │                │                │               │
│                │                │                │               │
│           "Is pool           "Is circuit       "Call            │
│            full?"              open?"          service"         │
│                │                │                │               │
│          If full:         If open:          If fails:          │
│          Reject fast      Fail fast         CB tracks          │
│                                                                  │
│  Bulkhead: Limits CONCURRENCY (how many at once)               │
│  Circuit: Limits FAILURES (stops if too many errors)           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Interview Questions

1. "What is the bulkhead pattern and why is it useful?"
2. "How does bulkhead differ from circuit breaker?"
3. "How would you size thread pool bulkheads?"

## Key Takeaways

```
┌────────────────────────────────────────────────────────────────┐
│                   BULKHEAD SUMMARY                              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PURPOSE:                                                      │
│  └── Isolate failures to prevent resource exhaustion          │
│  └── One slow/failing component doesn't sink the ship         │
│                                                                 │
│  TYPES:                                                        │
│  ├── Thread pool isolation                                    │
│  ├── Connection pool isolation                                │
│  └── Semaphore-based concurrency limits                       │
│                                                                 │
│  COMBINE WITH:                                                 │
│  └── Circuit breakers for failure detection                   │
│  └── Timeouts to prevent indefinite waits                     │
│  └── Fallbacks for graceful degradation                       │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

*Next: [Idempotency](11_idempotency.md) →*
