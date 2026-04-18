# Sharding Strategies

## What is Sharding?

**Simple explanation**: Sharding is splitting your database into smaller pieces (shards), where each piece holds a portion of the total data. Think of it like dividing a library's books across multiple buildings instead of cramming everything into one.

**Technical definition**: Sharding (also called horizontal partitioning) is a database architecture pattern where rows of a database table are held separately in different database instances, called shards, to spread load and enable horizontal scaling.

```
WITHOUT SHARDING:                    WITH SHARDING:
┌─────────────────────┐              ┌─────────┐ ┌─────────┐ ┌─────────┐
│    Single Database  │              │ Shard 1 │ │ Shard 2 │ │ Shard 3 │
│                     │              │         │ │         │ │         │
│  Users: 1-10M       │    ───►      │Users 1-3M│Users 3-6M│Users 6-10M
│  All data in one    │              │         │ │         │ │         │
│  place              │              └─────────┘ └─────────┘ └─────────┘
└─────────────────────┘
     Bottleneck!                     Load distributed!
```

## Why Shard?

| Problem | How Sharding Helps |
|---------|-------------------|
| Database too large for single server | Split data across multiple servers |
| Too many reads/writes for one machine | Distribute load across shards |
| Single point of failure | Each shard can be replicated independently |
| Slow queries due to table size | Smaller tables = faster queries |

## Sharding Strategies

### 1. Hash-Based Sharding

**How it works**: Apply a hash function to a key (like user_id) and use the result to determine which shard stores the data.

```
shard_number = hash(user_id) % number_of_shards

Example:
user_id = 12345
hash(12345) = 987654321
987654321 % 4 = 1

User 12345 goes to Shard 1
```

**Diagram**:
```
                    ┌─────────────────────┐
                    │    Hash Function    │
                    │ hash(key) % shards  │
                    └──────────┬──────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
    ┌─────────┐           ┌─────────┐           ┌─────────┐
    │ Shard 0 │           │ Shard 1 │           │ Shard 2 │
    │ hash%3=0│           │ hash%3=1│           │ hash%3=2│
    └─────────┘           └─────────┘           └─────────┘
```

**Pros**:
- Even data distribution (if hash function is good)
- Simple to implement
- Fast routing (just compute hash)

**Cons**:
- Adding/removing shards requires massive data migration
- Range queries become difficult (scanning all shards)
- Hot partitions if hash function isn't uniform

**When to use**:
- Data access is primarily by key (user_id, order_id)
- No need for range queries
- Even distribution is priority

---

### 2. Range-Based Sharding

**How it works**: Assign continuous ranges of the sharding key to each shard.

```
Shard 0: user_id 1 - 1,000,000
Shard 1: user_id 1,000,001 - 2,000,000
Shard 2: user_id 2,000,001 - 3,000,000
```

**Diagram**:
```
User IDs:  1 ─────────────────────────────────────────────► 10M

           ├────────────┬────────────┬────────────┬────────┤
           │            │            │            │        │
        Shard 0      Shard 1      Shard 2      Shard 3   Shard 4
        1-2M         2M-4M        4M-6M        6M-8M     8M-10M
```

**Pros**:
- Range queries are efficient (query one shard)
- Easy to add new shards at the end
- Intuitive to understand and manage

**Cons**:
- Uneven distribution (new users all hit latest shard)
- Hot spots for time-series data
- Rebalancing is complex

**When to use**:
- Range queries are common (dates, alphabetical sorting)
- Data has natural ordering
- Sequential data (timestamps, auto-increment IDs)

---

### 3. Directory-Based Sharding

**How it works**: A lookup service (directory) maintains a mapping of which shard contains which data.

```
┌─────────────────────┐
│  Directory Service  │
│                     │
│  user_1 → Shard A   │
│  user_2 → Shard B   │
│  user_3 → Shard A   │
│  user_4 → Shard C   │
└──────────┬──────────┘
           │
           │ 1. Lookup shard
           │ 2. Route request
           ▼
    ┌──────────────────────────────────┐
    │                                  │
┌───┴───┐        ┌─────────┐      ┌───┴───┐
│Shard A│        │ Shard B │      │Shard C│
└───────┘        └─────────┘      └───────┘
```

**Pros**:
- Maximum flexibility in data placement
- Easy to rebalance (just update directory)
- Can optimize for specific access patterns

**Cons**:
- Directory becomes single point of failure
- Extra network hop for every query
- Directory must be highly available

**When to use**:
- Need flexibility in data placement
- Complex rebalancing requirements
- Can afford infrastructure for directory service

---

### 4. Geographic Sharding

**How it works**: Data is distributed based on geographic location (country, region, city).

```
┌─────────────────────────────────────────────────────────────┐
│                        GLOBAL                                │
├─────────────────┬─────────────────┬─────────────────────────┤
│   US Region     │   EU Region     │   APAC Region           │
│                 │                 │                         │
│  ┌───────────┐  │  ┌───────────┐  │  ┌───────────┐         │
│  │ US Users  │  │  │ EU Users  │  │  │APAC Users │         │
│  │ US Data   │  │  │ EU Data   │  │  │APAC Data  │         │
│  └───────────┘  │  └───────────┘  │  └───────────┘         │
└─────────────────┴─────────────────┴─────────────────────────┘
```

**Pros**:
- Low latency (data close to users)
- Compliance with data residency laws (GDPR)
- Natural isolation for regional features

**Cons**:
- Cross-region queries are expensive
- Uneven distribution if user base varies by region
- Complex for global users/transactions

**When to use**:
- Legal requirements for data locality
- Latency-sensitive applications
- Regional features/pricing

---

## Choosing a Sharding Key

The sharding key is **the most critical decision**. Choose poorly and you'll face:
- Hot partitions (one shard overwhelmed)
- Cross-shard queries (slow, complex joins)
- Difficult rebalancing

### Good Sharding Key Characteristics

| Characteristic | Why It Matters |
|---------------|----------------|
| High cardinality | Many unique values = better distribution |
| Even distribution | No hot partitions |
| Immutable | Changing keys requires data migration |
| Query-aligned | Most queries use this key |

### Common Sharding Keys

```
GOOD KEYS:                          BAD KEYS:
✓ user_id                           ✗ status (low cardinality)
✓ order_id                          ✗ created_date (hot partition)
✓ tenant_id (multi-tenant)          ✗ country (uneven distribution)
✓ hash(email)                       ✗ boolean fields
```

### Example: E-Commerce Platform

```
Table: orders
┌──────────┬─────────┬─────────┬────────────┐
│ order_id │ user_id │ status  │ created_at │
├──────────┼─────────┼─────────┼────────────┤
│ 1001     │ 42      │ shipped │ 2024-01-15 │
│ 1002     │ 73      │ pending │ 2024-01-16 │
└──────────┴─────────┴─────────┴────────────┘

Sharding key analysis:
- order_id: ✓ High cardinality, unique, but queries often by user
- user_id: ✓ Good if queries are "get user's orders"
- status: ✗ Only 5 values, uneven distribution
- created_at: ✗ All new orders hit same shard

Best choice: user_id (if user-centric queries)
            or order_id (if order-centric queries)
```

## Cross-Shard Operations

The biggest challenge with sharding is operations spanning multiple shards.

### Problem: Cross-Shard Joins

```
Query: Get all orders with product details

Sharded by user_id:
┌─────────────┐      ┌─────────────┐
│  Orders     │      │  Products   │
│  Shard A    │──────│  Shard B    │  ← Different shards!
└─────────────┘      └─────────────┘

Solution approaches:
1. Denormalize (store product name in orders)
2. Application-level join (query both, join in code)
3. Broadcast queries (expensive, avoid if possible)
```

### Problem: Cross-Shard Transactions

```
Scenario: Transfer money between users on different shards

User A (Shard 1): -$100
User B (Shard 2): +$100

Solutions:
1. Two-phase commit (2PC) - complex, slow
2. Saga pattern - eventual consistency
3. Design to avoid (same shard for related data)
```

### Problem: Global Counts/Aggregations

```
Query: Count total orders across all shards

┌─────────┐ ┌─────────┐ ┌─────────┐
│ Shard 1 │ │ Shard 2 │ │ Shard 3 │
│ 1.2M    │ │ 1.1M    │ │ 1.3M    │
└────┬────┘ └────┬────┘ └────┬────┘
     │           │           │
     └───────────┼───────────┘
                 │
                 ▼
         Total: 3.6M orders

Solutions:
1. Scatter-gather (query all, aggregate)
2. Maintain counter service
3. Approximate counts (HyperLogLog)
```

## Resharding and Rebalancing

As data grows, you'll need to redistribute data.

### Adding a Shard

```
BEFORE (2 shards):
hash(key) % 2 = 0 or 1

AFTER (3 shards):
hash(key) % 3 = 0, 1, or 2

Problem: ~67% of keys need to move!
```

### Solution: Consistent Hashing

```
                    ┌───────┐
               ┌────│Node A │────┐
               │    └───────┘    │
               │                 │
          ┌────▼───┐        ┌────▼───┐
          │ Data 1 │        │ Data 2 │
          └────────┘        └────────┘
               │                 │
               │    ┌───────┐    │
               └────│Node B │────┘
                    └───────┘

Adding Node C:
- Only data between B and C moves
- Other data stays in place
- Much less migration!
```

### Live Resharding Strategy

```
1. Create new shard
2. Start writing to both old and new shard
3. Migrate historical data in background
4. Verify data consistency
5. Switch reads to new shard
6. Stop writes to old location
7. Clean up old data

Timeline:
├──────────────────────────────────────────────────────────────┤
│ [Double Write] [Background Migration] [Verify] [Switch] [Cleanup]
```

## Common Pitfalls

### Pitfall 1: Sharding Too Early

```
DON'T:
"We might have millions of users someday, let's shard now!"

DO:
"We have 10M users and the database is at 80% capacity.
 Let's plan sharding with clear migration path."

Why: Sharding adds massive complexity. Premature optimization
     is the root of all evil.
```

### Pitfall 2: Wrong Sharding Key

```
DON'T:
Shard by timestamp for a social app
└── All activity hits the "current" shard (hot partition)

DO:
Shard by user_id
└── Activity spreads across all shards
```

### Pitfall 3: Ignoring Cross-Shard Queries

```
DON'T:
Shard orders by order_id, then wonder why
"get all orders for user X" is slow

DO:
Analyze query patterns BEFORE choosing sharding key
```

## Interview Questions

### Basic
1. "What is sharding and why would you use it?"
2. "What's the difference between sharding and replication?"
3. "How do you choose a sharding key?"

### Intermediate
4. "How would you handle a cross-shard transaction?"
5. "What happens when you need to add a new shard?"
6. "How do you handle queries that need data from multiple shards?"

### Advanced
7. "Design a sharding strategy for Twitter's tweets table"
8. "How would you migrate from a single database to sharded architecture with zero downtime?"
9. "How do you handle hot partitions?"

## Sample Interview Answer

**Q: "How would you shard a user messages table for a chat application?"**

**Strong Answer**:
"First, I'd analyze the access patterns. Chat apps typically query messages by conversation, so I'd shard by `conversation_id` rather than `user_id` or `message_id`.

For the sharding strategy, I'd use consistent hashing on conversation_id. This keeps all messages in a conversation together (no cross-shard queries for conversation history) and distributes evenly across shards.

The tradeoff is that 'get all messages for a user' becomes a scatter-gather across all shards. I'd handle this by maintaining a secondary index mapping user_id to conversation_ids, stored in a separate service.

For hot conversations (viral group chats), I'd implement a tiered approach: hot conversations on dedicated high-performance shards, cold conversations on standard shards.

I'd also plan for rebalancing by using virtual nodes in consistent hashing, making it easier to add capacity without massive data migration."

## Key Takeaways

```
┌────────────────────────────────────────────────────────────────┐
│                    SHARDING DECISION TREE                       │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Do you actually need sharding?                                │
│          │                                                      │
│          ├── NO: Have you tried: vertical scaling,             │
│          │       read replicas, caching, query optimization?   │
│          │                                                      │
│          └── YES: Proceed with sharding                        │
│                    │                                            │
│                    ├── Primary access by key? → Hash-based     │
│                    │                                            │
│                    ├── Need range queries? → Range-based       │
│                    │                                            │
│                    ├── Complex placement? → Directory-based    │
│                    │                                            │
│                    └── Data locality laws? → Geographic        │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

*Next: [Replication Strategies](02_replication.md) →*
