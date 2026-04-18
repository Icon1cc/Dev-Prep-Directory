# Idempotency

## What is Idempotency?

**Simple explanation**: An operation is idempotent if doing it multiple times has the same effect as doing it once. Like pressing an elevator button—pressing it 10 times doesn't make the elevator come faster or arrive 10 times.

**Technical definition**: An operation is idempotent if applying it multiple times produces the same result as applying it once, with no additional side effects.

```
IDEMPOTENT:
┌──────────────────────────────────────────────────────────────────┐
│  Request: "Set user balance to $100"                             │
│                                                                   │
│  Send once:   Balance = $100  ✓                                  │
│  Send twice:  Balance = $100  ✓  (Same result)                   │
│  Send 10x:    Balance = $100  ✓  (Same result)                   │
└──────────────────────────────────────────────────────────────────┘

NOT IDEMPOTENT:
┌──────────────────────────────────────────────────────────────────┐
│  Request: "Add $100 to user balance"                             │
│                                                                   │
│  Send once:   Balance = $100  ✓                                  │
│  Send twice:  Balance = $200  ✗  (Wrong!)                        │
│  Send 10x:    Balance = $1000 ✗  (Very wrong!)                   │
└──────────────────────────────────────────────────────────────────┘
```

## Why Idempotency Matters

### The Duplicate Request Problem

```
┌─────────────────────────────────────────────────────────────────┐
│                  WHY DUPLICATES HAPPEN                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. NETWORK TIMEOUTS                                            │
│     Client ──request──► Server ──processes──► (success)         │
│     Client ◄──timeout── (response lost)                         │
│     Client ──retry──► Server ──processes──► (duplicate!)        │
│                                                                  │
│  2. USER DOUBLE-CLICKS                                          │
│     User clicks "Buy" → Request sent                            │
│     User clicks again → Another request sent                    │
│                                                                  │
│  3. MESSAGE QUEUE REDELIVERY                                    │
│     Consumer processes message → Crashes before ACK             │
│     Queue redelivers message → Processed again                  │
│                                                                  │
│  4. RETRY LOGIC                                                 │
│     Client gets error → Retries automatically                   │
│     But first request actually succeeded!                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Real-World Consequences

```
WITHOUT IDEMPOTENCY:
┌──────────────────────────────────────────────────────────────────┐
│                                                                   │
│  Payment Service:                                                │
│  - User clicks "Pay $100" twice due to slow response            │
│  - Two charges of $100 = $200 charged!                          │
│  - Customer angry, refund needed                                │
│                                                                   │
│  Order Service:                                                  │
│  - Retry on timeout                                              │
│  - Original request succeeded                                    │
│  - Retry creates duplicate order                                │
│  - Two shipments sent to customer                               │
│                                                                   │
│  Inventory Service:                                              │
│  - "Decrement stock by 1" message redelivered                   │
│  - Stock decremented twice                                       │
│  - Inventory count becomes negative!                            │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## Making Operations Idempotent

### 1. Idempotency Keys

Client sends a unique key with each request.

```
┌─────────────────────────────────────────────────────────────────┐
│                    IDEMPOTENCY KEY PATTERN                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Request 1:                                                     │
│  POST /payments                                                 │
│  Idempotency-Key: "pay_abc123"                                  │
│  { amount: 100, user: "usr_1" }                                 │
│                                                                  │
│  Server:                                                        │
│  1. Check: Have I seen "pay_abc123" before?                     │
│  2. No → Process payment, store result with key                 │
│  3. Return: { payment_id: "pmt_xyz", status: "success" }        │
│                                                                  │
│  Request 2 (duplicate/retry):                                   │
│  POST /payments                                                 │
│  Idempotency-Key: "pay_abc123"  ← Same key                      │
│  { amount: 100, user: "usr_1" }                                 │
│                                                                  │
│  Server:                                                        │
│  1. Check: Have I seen "pay_abc123" before?                     │
│  2. Yes → Return stored result (don't process again)           │
│  3. Return: { payment_id: "pmt_xyz", status: "success" }        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Implementation**:
```python
class IdempotentPaymentService:
    def process_payment(self, idempotency_key: str, amount: Decimal, user_id: str):
        # Check if we've processed this key before
        existing = self.idempotency_store.get(idempotency_key)
        if existing:
            return existing  # Return cached result

        # Process the payment
        result = self._charge_user(amount, user_id)

        # Store result with idempotency key (with TTL)
        self.idempotency_store.set(
            idempotency_key,
            result,
            ttl=timedelta(hours=24)
        )

        return result
```

### 2. Natural Idempotency

Design operations to be naturally idempotent.

```
MAKE IT NATURALLY IDEMPOTENT:
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Instead of:              Use:                                  │
│  ─────────────────────────────────────────────────────────────  │
│  "Add $100 to balance"    "Set balance to $200"                 │
│  (increment)              (absolute value)                      │
│                                                                  │
│  "Insert order"           "Upsert order with ID xyz"            │
│  (creates new)            (insert or update)                    │
│                                                                  │
│  "Decrement stock"        "Set stock to 49 if version=5"        │
│  (relative change)        (conditional update)                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Deduplication

Track processed requests to avoid reprocessing.

```python
class DeduplicatingQueue:
    def __init__(self):
        self.processed_ids = set()  # Or use Redis/DB

    def process_message(self, message):
        message_id = message.id

        # Check if already processed
        if message_id in self.processed_ids:
            return  # Skip duplicate

        # Process the message
        self._handle(message)

        # Mark as processed
        self.processed_ids.add(message_id)
```

## Database Techniques

### Upsert Pattern

```sql
-- Instead of: INSERT (might fail on duplicate)
INSERT INTO orders (order_id, user_id, amount)
VALUES ('ord_123', 'usr_456', 100);

-- Use: UPSERT (idempotent)
INSERT INTO orders (order_id, user_id, amount)
VALUES ('ord_123', 'usr_456', 100)
ON CONFLICT (order_id) DO NOTHING;  -- or DO UPDATE
```

### Conditional Updates

```sql
-- Instead of: UPDATE (always changes)
UPDATE inventory SET stock = stock - 1 WHERE product_id = 'prod_123';

-- Use: Conditional update with version
UPDATE inventory
SET stock = 49, version = 6
WHERE product_id = 'prod_123' AND version = 5;

-- If version doesn't match, no update (already processed)
```

## Interview Questions

1. "What is idempotency and why is it important?"
2. "How would you make a payment API idempotent?"
3. "What happens if idempotency key storage fails?"

## Key Takeaways

```
┌────────────────────────────────────────────────────────────────┐
│                   IDEMPOTENCY SUMMARY                           │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DEFINITION:                                                   │
│  └── Multiple identical requests = same result as one          │
│                                                                 │
│  WHY IT MATTERS:                                               │
│  ├── Retries happen (timeouts, failures)                      │
│  ├── Users double-click                                        │
│  └── Messages get redelivered                                  │
│                                                                 │
│  HOW TO ACHIEVE:                                               │
│  ├── Idempotency keys (client-provided unique ID)             │
│  ├── Natural idempotency (absolute vs relative)               │
│  ├── Deduplication (track processed IDs)                      │
│  └── Database upserts and conditional updates                 │
│                                                                 │
│  HTTP METHODS:                                                 │
│  ├── GET, PUT, DELETE: Naturally idempotent                   │
│  └── POST: Must be made idempotent explicitly                 │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

*Next: [Delivery Semantics](12_delivery_semantics.md) →*
