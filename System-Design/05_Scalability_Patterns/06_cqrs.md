# CQRS - Command Query Responsibility Segregation

## What is CQRS?

**Simple explanation**: CQRS means using different models for reading and writing data. Instead of using the same database structure for both, you optimize each separately.

**Technical definition**: Command Query Responsibility Segregation is a pattern that separates read operations (queries) from write operations (commands) into different models, potentially using different data stores optimized for each use case.

```
TRADITIONAL (Same model for read/write):
┌─────────────────────────────────────────┐
│            Application                   │
│                                          │
│  ┌─────────────────────────────────┐    │
│  │        Single Model              │    │
│  │   (Reads AND Writes)             │    │
│  └──────────────┬──────────────────┘    │
│                 │                        │
│          ┌──────▼──────┐                │
│          │  Database   │                │
│          └─────────────┘                │
└─────────────────────────────────────────┘

CQRS (Separate models):
┌─────────────────────────────────────────────────────────────┐
│                      Application                             │
│                                                              │
│  ┌───────────────────┐        ┌───────────────────┐        │
│  │   Command Model   │        │   Query Model     │        │
│  │     (Writes)      │        │    (Reads)        │        │
│  └─────────┬─────────┘        └─────────┬─────────┘        │
│            │                            │                   │
│     ┌──────▼──────┐              ┌──────▼──────┐           │
│     │ Write Store │  ──sync──►   │ Read Store  │           │
│     │ (Normalized)│              │(Denormalized)│           │
│     └─────────────┘              └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## Why CQRS?

### The Problem

In many applications, read and write patterns are fundamentally different:

```
TYPICAL E-COMMERCE:
┌────────────────────────────────────────────────────────────┐
│                                                             │
│  WRITES (Commands):              READS (Queries):          │
│  - Place order                   - Browse products         │
│  - Update profile                - View order history      │
│  - Add to cart                   - Search products         │
│                                  - View product details    │
│  ~100 writes/second              - List recommendations    │
│  Complex validation              ~10,000 reads/second      │
│  Normalized data                 Denormalized, fast        │
│                                                             │
│  RATIO: 1:100 or higher!                                   │
│                                                             │
└────────────────────────────────────────────────────────────┘

Problem: Single model optimized for writes → slow reads
         Single model optimized for reads → complex writes
```

### The Solution

```
CQRS separates concerns:

COMMAND SIDE                        QUERY SIDE
┌─────────────────────┐            ┌─────────────────────┐
│                     │            │                     │
│ - Optimized for     │            │ - Optimized for     │
│   data integrity    │            │   fast retrieval    │
│                     │            │                     │
│ - Normalized        │            │ - Denormalized      │
│   schema            │   sync     │   views             │
│                     │  ──────►   │                     │
│ - Complex           │            │ - Pre-computed      │
│   validation        │            │   results           │
│                     │            │                     │
│ - Transactional     │            │ - Eventually        │
│   consistency       │            │   consistent        │
│                     │            │                     │
└─────────────────────┘            └─────────────────────┘
```

## CQRS Architecture

### Basic CQRS

```
┌────────────────────────────────────────────────────────────────┐
│                         API LAYER                               │
│                                                                 │
│   POST /orders (Command)              GET /orders (Query)      │
│         │                                    │                  │
│         ▼                                    ▼                  │
│  ┌──────────────┐                    ┌──────────────┐          │
│  │   Command    │                    │    Query     │          │
│  │   Handler    │                    │   Handler    │          │
│  └──────┬───────┘                    └──────┬───────┘          │
│         │                                   │                   │
│         ▼                                   ▼                   │
│  ┌──────────────┐      Sync         ┌──────────────┐          │
│  │ Write Model  │ ────────────────► │ Read Model   │          │
│  │  (Source)    │                   │  (Derived)   │          │
│  └──────────────┘                   └──────────────┘          │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### CQRS with Event Sourcing

Often combined with Event Sourcing for powerful results:

```
┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│   Command ────► Command Handler ────► Event Store              │
│                        │                   │                    │
│                        │             ┌─────┴─────┐             │
│                        │             │  Events   │             │
│                        │             │ Published │             │
│                        │             └─────┬─────┘             │
│                        │                   │                    │
│                        │         ┌─────────┼─────────┐         │
│                        │         │         │         │         │
│                        │         ▼         ▼         ▼         │
│                        │    ┌────────┐┌────────┐┌────────┐    │
│                        │    │ Read   ││ Read   ││ Read   │    │
│                        │    │Model 1 ││Model 2 ││Model 3 │    │
│                        │    └───┬────┘└───┬────┘└───┬────┘    │
│                        │        │         │         │          │
│   Query ───────────────┴────────┴─────────┴─────────┘          │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Implementation Example

### Traditional Approach (Single Model)

```python
# Single model serves both reads and writes
class OrderService:
    def create_order(self, user_id, items):
        # Write: Complex business logic
        order = Order(user_id=user_id, items=items)
        order.validate()
        order.calculate_total()
        order.save()
        return order

    def get_user_orders(self, user_id):
        # Read: Complex joins for display
        return Order.objects.filter(user_id=user_id) \
            .select_related('user') \
            .prefetch_related('items__product') \
            .annotate(item_count=Count('items'))
        # Slow! Many joins, computed fields
```

### CQRS Approach (Separate Models)

```python
# Command Side - Optimized for writes
class OrderCommandHandler:
    def handle_create_order(self, command):
        # Validate and process
        order = Order(
            user_id=command.user_id,
            items=command.items
        )
        order.validate()
        order.calculate_total()
        order.save()

        # Publish event for read side
        self.event_bus.publish(OrderCreatedEvent(
            order_id=order.id,
            user_id=order.user_id,
            total=order.total,
            item_count=len(order.items)
        ))


# Query Side - Optimized for reads
class OrderQueryHandler:
    def get_user_orders(self, user_id):
        # Simple query on denormalized read model
        return OrderReadModel.objects.filter(user_id=user_id)
        # Fast! No joins, pre-computed fields


# Read Model (Denormalized)
class OrderReadModel:
    order_id: str
    user_id: str
    user_name: str          # Denormalized
    total: Decimal
    item_count: int         # Pre-computed
    status: str
    created_at: datetime


# Event Handler - Keeps read model in sync
class OrderReadModelUpdater:
    def handle_order_created(self, event):
        user = User.objects.get(id=event.user_id)

        OrderReadModel.objects.create(
            order_id=event.order_id,
            user_id=event.user_id,
            user_name=user.name,  # Denormalize
            total=event.total,
            item_count=event.item_count,
            status='created'
        )
```

## Synchronization Strategies

### 1. Synchronous Updates

```
Command ──► Write DB ──► Immediately update Read DB

┌─────────┐    ┌──────────┐    ┌──────────┐
│ Command │───►│ Write DB │───►│ Read DB  │
│         │    │  Update  │    │  Update  │
└─────────┘    └──────────┘    └──────────┘

✓ Strong consistency
✗ Slower writes
✗ Coupled systems
```

### 2. Asynchronous Updates (Preferred)

```
Command ──► Write DB ──► Event ──► Eventually update Read DB

┌─────────┐    ┌──────────┐    ┌───────┐    ┌──────────┐
│ Command │───►│ Write DB │───►│ Event │───►│ Read DB  │
│         │    │  Update  │    │ Queue │    │  Update  │
└─────────┘    └──────────┘    └───────┘    └──────────┘
                    │                            │
                    │      Eventual Consistency  │
                    │◄───────────────────────────┘

✓ Fast writes
✓ Decoupled systems
✗ Eventual consistency (stale reads possible)
```

## When to Use CQRS

### Good Fit

```
✓ Read and write patterns are significantly different
✓ Read-heavy workloads (10:1 or higher ratio)
✓ Complex queries that would require many joins
✓ Need different scaling for reads vs writes
✓ Multiple read representations of same data
✓ Event-driven architecture already in place
```

### Bad Fit

```
✗ Simple CRUD applications
✗ Small data sets
✗ Team unfamiliar with pattern
✗ Strong consistency requirements everywhere
✗ Read and write patterns are similar
```

## Benefits and Tradeoffs

### Benefits

| Benefit | Explanation |
|---------|-------------|
| **Independent scaling** | Scale read and write sides separately |
| **Optimized models** | Each model optimized for its purpose |
| **Simpler queries** | Read models are denormalized |
| **Better performance** | Reads don't compete with writes |
| **Flexibility** | Multiple read models for different needs |

### Tradeoffs

| Tradeoff | Explanation |
|----------|-------------|
| **Eventual consistency** | Read model may be stale |
| **Increased complexity** | Two models instead of one |
| **Synchronization overhead** | Must keep models in sync |
| **More code** | Command handlers, event handlers, models |
| **Debugging difficulty** | State spread across systems |

## Interview Questions

### Basic
1. "What is CQRS and why would you use it?"
2. "What's the difference between the command and query models?"
3. "How do you keep read and write models synchronized?"

### Intermediate
4. "How does CQRS relate to event sourcing?"
5. "What are the consistency implications of CQRS?"
6. "When would CQRS be overkill?"

### Advanced
7. "Design a CQRS system for a high-traffic e-commerce product catalog"
8. "How would you handle read model failures in CQRS?"
9. "How do you test a CQRS system?"

## Sample Interview Answer

**Q: "When would you recommend using CQRS?"**

**Strong Answer**:
"I'd recommend CQRS when there's a significant mismatch between read and write patterns.

**Ideal scenarios:**
1. **Read-heavy workloads**: If reads outnumber writes 10:1 or more, we can scale them independently
2. **Complex read queries**: When reads require many joins or computations, denormalized read models are faster
3. **Different representations**: When we need the same data presented differently (mobile vs web, search vs detail view)

**Example**: For a product catalog system:
- Writes are infrequent (merchants update products)
- Reads are constant (customers browsing)
- Reads need different views (search results, full details, recommendations)

CQRS lets us optimize the read side with denormalized views pre-computed for each use case, while keeping the write side normalized for data integrity.

**I'd avoid CQRS for:**
- Simple CRUD apps where read/write patterns are similar
- Small teams or MVPs where complexity isn't justified
- Cases requiring strong consistency (use traditional approach or accept eventual consistency)"

## Key Takeaways

```
┌────────────────────────────────────────────────────────────────┐
│                    CQRS DECISION GUIDE                          │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CONSIDER CQRS WHEN:                                           │
│  ├── Read patterns differ significantly from write patterns    │
│  ├── Need to scale reads and writes independently              │
│  ├── Complex queries would benefit from denormalization        │
│  └── Already using event-driven architecture                   │
│                                                                 │
│  AVOID CQRS WHEN:                                              │
│  ├── Simple CRUD operations                                    │
│  ├── Strong consistency required everywhere                    │
│  ├── Small team / early-stage product                         │
│  └── Read and write patterns are similar                      │
│                                                                 │
│  REMEMBER:                                                      │
│  └── Eventual consistency is a feature, not a bug              │
│  └── CQRS + Event Sourcing is powerful but complex            │
│  └── Start simple, add CQRS when pain points emerge           │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

*Next: [Event Sourcing](07_event_sourcing.md) →*
