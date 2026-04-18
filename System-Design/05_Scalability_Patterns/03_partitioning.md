# Partitioning Schemes

## What is Partitioning?

**Simple explanation**: Partitioning is dividing your data into separate, independent pieces. Unlike sharding (which specifically refers to distributing across servers), partitioning is the general concept of splitting data—which can happen within a single database or across many.

**Technical definition**: Data partitioning is a technique for breaking up large datasets into smaller, more manageable chunks based on certain criteria, enabling better performance, easier maintenance, and independent operations on each partition.

```
BEFORE PARTITIONING:                 AFTER PARTITIONING:
┌─────────────────────────┐         ┌───────┬───────┬───────┐
│                         │         │ P1    │ P2    │ P3    │
│   One Giant Table       │         │ 2023  │ 2024  │ 2025  │
│   (10 years of data)    │   ──►   │ data  │ data  │ data  │
│                         │         │       │       │       │
│   Slow queries          │         │ Fast! │ Fast! │ Fast! │
│   Huge backups          │         └───────┴───────┴───────┘
└─────────────────────────┘         Query only needed partition
```

## Types of Partitioning

### 1. Horizontal Partitioning (Row-based)

Different rows go to different partitions. All partitions have the same schema.

```
Original Table: orders
┌──────────┬─────────┬────────────┬─────────┐
│ order_id │ user_id │ created_at │ amount  │
├──────────┼─────────┼────────────┼─────────┤
│ 1        │ 100     │ 2024-01-15 │ $50     │
│ 2        │ 101     │ 2024-02-20 │ $75     │
│ 3        │ 100     │ 2024-03-10 │ $30     │
└──────────┴─────────┴────────────┴─────────┘

Horizontally Partitioned by month:

orders_jan_2024              orders_feb_2024
┌──────────┬─────────┐       ┌──────────┬─────────┐
│ order_id │ ...     │       │ order_id │ ...     │
├──────────┼─────────┤       ├──────────┼─────────┤
│ 1        │ ...     │       │ 2        │ ...     │
└──────────┴─────────┘       └──────────┴─────────┘
```

**Use cases**: Time-series data, logs, orders, transactions

---

### 2. Vertical Partitioning (Column-based)

Different columns go to different partitions.

```
Original Table: users
┌─────────┬────────┬───────┬─────────────────┬────────┐
│ user_id │ name   │ email │ bio (large)     │ avatar │
├─────────┼────────┼───────┼─────────────────┼────────┤
│ 1       │ Alice  │ a@... │ "Lorem ipsum.." │ [20KB] │
└─────────┴────────┴───────┴─────────────────┴────────┘

Vertically Partitioned:

users_core                    users_profile
┌─────────┬────────┬───────┐  ┌─────────┬──────┬────────┐
│ user_id │ name   │ email │  │ user_id │ bio  │ avatar │
├─────────┼────────┼───────┤  ├─────────┼──────┼────────┤
│ 1       │ Alice  │ a@... │  │ 1       │ ...  │ [20KB] │
└─────────┴────────┴───────┘  └─────────┴──────┴────────┘
Frequently accessed            Rarely accessed
```

**Use cases**: Separating hot and cold columns, isolating large BLOBs

---

### 3. Functional Partitioning

Data is partitioned based on business function or domain.

```
BEFORE: Single monolithic database
┌────────────────────────────────────────────────┐
│              Monolithic Database                │
│  ┌─────────┐ ┌───────┐ ┌────────┐ ┌─────────┐ │
│  │ Users   │ │Orders │ │Products│ │Analytics│ │
│  └─────────┘ └───────┘ └────────┘ └─────────┘ │
└────────────────────────────────────────────────┘

AFTER: Functionally partitioned by domain
┌────────────┐  ┌────────────┐  ┌────────────┐
│ User DB    │  │ Order DB   │  │ Product DB │
└────────────┘  └────────────┘  └────────────┘
```

**Use cases**: Microservices, domain-driven design

## Partitioning Strategies

### Range Partitioning

Partition based on ranges of the partition key.

```sql
-- PostgreSQL example
CREATE TABLE orders (
    order_id    SERIAL,
    user_id     INT,
    created_at  DATE
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');
```

**Best for**: Time-series data, sequential data

---

### List Partitioning

Partition based on specific values.

```sql
CREATE TABLE customers (
    customer_id  INT,
    region       VARCHAR(20)
) PARTITION BY LIST (region);

CREATE TABLE customers_north PARTITION OF customers
    FOR VALUES IN ('NY', 'MA', 'CT');

CREATE TABLE customers_south PARTITION OF customers
    FOR VALUES IN ('FL', 'GA', 'TX');
```

**Best for**: Geographic data, categorical data

---

### Hash Partitioning

Apply hash function to distribute evenly.

```sql
CREATE TABLE users (
    user_id  INT,
    name     VARCHAR(100)
) PARTITION BY HASH (user_id);

CREATE TABLE users_p0 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);
-- ... repeat for p1, p2, p3
```

**Best for**: Even distribution, avoiding hot spots

## Partition Pruning

Databases skip irrelevant partitions during queries.

```
Query: SELECT * FROM orders WHERE created_at = '2024-03-15';

WITHOUT PRUNING:          WITH PRUNING:
Scan ALL partitions       Scan ONLY March partition
      SLOW                       FAST
```

**Enable pruning**: Include partition key in WHERE clause.

## Interview Questions

1. "What is the difference between partitioning and sharding?"
2. "How would you partition a time-series table with 1 billion rows?"
3. "What is partition pruning?"

## Key Takeaways

```
┌────────────────────────────────────────────────────────────────┐
│                 PARTITIONING DECISION GUIDE                     │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Time-based queries → Range partitioning                       │
│  Categorical data → List partitioning                          │
│  Even distribution → Hash partitioning                         │
│  Separate hot/cold columns → Vertical partitioning             │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

*Next: [Event-Driven Architecture](04_event_driven.md) →*
