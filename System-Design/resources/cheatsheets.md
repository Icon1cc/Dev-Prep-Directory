# System Design Cheatsheets

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      QUICK REFERENCE CHEATSHEETS                              ║
║                Last-Minute Review Before Your Interview                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## The Ultimate Interview Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SYSTEM DESIGN INTERVIEW STEPS                             │
│                         (45 minute interview)                                │
│                                                                              │
│  STEP 1: REQUIREMENTS (3-5 min)                                             │
│  ═════════════════════════════                                              │
│  □ Clarify functional requirements (what features?)                         │
│  □ Clarify non-functional requirements (scale, latency, availability)      │
│  □ Identify core use cases (prioritize 3-4)                                │
│                                                                              │
│  STEP 2: ESTIMATES (3-5 min)                                                │
│  ══════════════════════════                                                 │
│  □ Users (DAU, MAU)                                                         │
│  □ Traffic (QPS for read/write)                                            │
│  □ Storage (data size * users * time)                                      │
│  □ Bandwidth (QPS * request size)                                          │
│                                                                              │
│  STEP 3: HIGH-LEVEL DESIGN (10-15 min)                                      │
│  ════════════════════════════════════                                       │
│  □ API design (main endpoints)                                             │
│  □ Data model (main entities, relationships)                               │
│  □ Architecture diagram (boxes and arrows)                                 │
│                                                                              │
│  STEP 4: DEEP DIVE (15-20 min)                                              │
│  ════════════════════════════                                               │
│  □ Database choice and schema                                              │
│  □ Scaling strategies                                                       │
│  □ Caching layer                                                           │
│  □ Handle bottlenecks                                                      │
│                                                                              │
│  STEP 5: WRAP UP (3-5 min)                                                  │
│  ═════════════════════════                                                  │
│  □ Summarize trade-offs                                                    │
│  □ Discuss monitoring/alerting                                             │
│  □ Future improvements                                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Numbers Everyone Should Know

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LATENCY NUMBERS                                           │
│                                                                              │
│  L1 cache reference:                    0.5 ns                              │
│  L2 cache reference:                    7 ns                                │
│  Main memory reference:                 100 ns                              │
│  SSD random read:                       150 μs                              │
│  HDD seek:                              10 ms                               │
│  Network roundtrip (same DC):           0.5 ms                              │
│  Network roundtrip (cross-continent):   150 ms                              │
│                                                                              │
│  RULE OF THUMB:                                                             │
│  Memory: 100 ns                                                             │
│  SSD: 100 μs (1000x memory)                                                │
│  HDD: 10 ms (100x SSD)                                                      │
│  Network: 0.5-150 ms (depends on distance)                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    DATA SIZE REFERENCE                                       │
│                                                                              │
│  Character:         1 byte                                                  │
│  Integer:           4-8 bytes                                               │
│  UUID:              16 bytes (as binary), 36 chars as string                │
│  Timestamp:         8 bytes                                                 │
│                                                                              │
│  Tweet text:        ~140 chars = 280 bytes (UTF-8)                         │
│  Metadata:          ~500 bytes                                              │
│  Image thumbnail:   10-50 KB                                                │
│  Full image:        200 KB - 2 MB                                          │
│  1 min video (HD):  100-500 MB                                             │
│                                                                              │
│  1 KB = 1,000 bytes                                                        │
│  1 MB = 1,000 KB                                                           │
│  1 GB = 1,000 MB                                                           │
│  1 TB = 1,000 GB                                                           │
│  1 PB = 1,000 TB                                                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    TIME CONVERSIONS                                          │
│                                                                              │
│  1 day    = 86,400 seconds ≈ 100,000 seconds                               │
│  1 month  = 2.5 million seconds                                            │
│  1 year   = 31.5 million seconds ≈ 30 million                              │
│                                                                              │
│  AVAILABILITY:                                                              │
│  99%      = 3.65 days/year downtime                                        │
│  99.9%    = 8.76 hours/year downtime                                       │
│  99.99%   = 52.6 minutes/year downtime                                     │
│  99.999%  = 5.26 minutes/year downtime                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Capacity Estimation Formulas

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ESTIMATION FORMULAS                                       │
│                                                                              │
│  TRAFFIC (QPS):                                                             │
│  ═════════════                                                              │
│  Daily active users (DAU) * actions per user / 86400                       │
│                                                                              │
│  Example: 10M DAU, 10 tweets/day                                           │
│  Write QPS: 10M * 10 / 86400 ≈ 1,160 QPS                                  │
│  Read QPS: typically 10-100x write                                         │
│                                                                              │
│                                                                              │
│  STORAGE:                                                                   │
│  ════════                                                                   │
│  Items per day * size per item * retention period                          │
│                                                                              │
│  Example: 100M tweets/day, 500 bytes each, 5 years                        │
│  100M * 500B * 365 * 5 = 91 PB                                             │
│                                                                              │
│                                                                              │
│  BANDWIDTH:                                                                 │
│  ══════════                                                                 │
│  QPS * request/response size                                                │
│                                                                              │
│  Example: 10,000 QPS, 1 KB response                                        │
│  10,000 * 1 KB = 10 MB/s = 80 Mbps                                         │
│                                                                              │
│                                                                              │
│  SERVERS NEEDED:                                                            │
│  ═══════════════                                                            │
│  QPS / QPS per server                                                       │
│  Assume: 1 server handles ~1000-10000 QPS (depends on complexity)          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Database Selection Guide

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DATABASE SELECTION                                        │
│                                                                              │
│  RELATIONAL (PostgreSQL, MySQL):                                            │
│  Use when:                                                                  │
│  ├── Complex queries with JOINs                                            │
│  ├── ACID transactions required                                            │
│  ├── Data integrity critical                                               │
│  └── Structured, relational data                                           │
│                                                                              │
│  DOCUMENT (MongoDB):                                                        │
│  Use when:                                                                  │
│  ├── Flexible/evolving schema                                              │
│  ├── Hierarchical data                                                     │
│  ├── Rapid prototyping                                                     │
│  └── Document-centric access                                               │
│                                                                              │
│  WIDE-COLUMN (Cassandra):                                                   │
│  Use when:                                                                  │
│  ├── Write-heavy workloads                                                 │
│  ├── Time-series data                                                      │
│  ├── Geographic distribution                                               │
│  └── High availability required                                            │
│                                                                              │
│  KEY-VALUE (Redis, DynamoDB):                                               │
│  Use when:                                                                  │
│  ├── Simple get/set patterns                                               │
│  ├── Caching                                                               │
│  ├── Session storage                                                       │
│  └── Real-time leaderboards                                                │
│                                                                              │
│  GRAPH (Neo4j):                                                             │
│  Use when:                                                                  │
│  ├── Many-to-many relationships                                            │
│  ├── Social networks                                                       │
│  ├── Recommendation engines                                                │
│  └── Fraud detection                                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Caching Cheatsheet

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CACHING PATTERNS                                          │
│                                                                              │
│  CACHE-ASIDE (most common):                                                 │
│  1. App checks cache                                                        │
│  2. If miss, query DB                                                       │
│  3. Store in cache                                                          │
│  4. Return to user                                                          │
│                                                                              │
│  WRITE-THROUGH:                                                             │
│  1. Write to cache                                                          │
│  2. Cache writes to DB                                                      │
│  3. Return to user                                                          │
│  Good for: Read-heavy with consistent writes                               │
│                                                                              │
│  WRITE-BEHIND (Write-Back):                                                 │
│  1. Write to cache                                                          │
│  2. Return to user                                                          │
│  3. Async write to DB                                                       │
│  Good for: Write-heavy workloads                                           │
│                                                                              │
│  EVICTION POLICIES:                                                         │
│  ├── LRU: Evict least recently used                                        │
│  ├── LFU: Evict least frequently used                                      │
│  └── TTL: Evict after time expires                                         │
│                                                                              │
│  CACHE INVALIDATION:                                                        │
│  ├── TTL-based: Simple but may serve stale                                 │
│  ├── Event-based: Invalidate on write                                      │
│  └── Version-based: Include version in key                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Scaling Cheatsheet

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SCALING STRATEGIES                                        │
│                                                                              │
│  HORIZONTAL vs VERTICAL:                                                    │
│  ├── Vertical: Bigger machine (easy, limited)                              │
│  └── Horizontal: More machines (complex, unlimited)                        │
│                                                                              │
│  LOAD BALANCING:                                                            │
│  ├── Round Robin: Simple, equal distribution                               │
│  ├── Least Connections: Send to least busy                                 │
│  ├── IP Hash: Same user → same server                                      │
│  └── Weighted: Prefer more powerful servers                                │
│                                                                              │
│  DATABASE SCALING:                                                          │
│  ├── Read Replicas: Scale reads                                            │
│  ├── Sharding: Split data across DBs                                       │
│  │   ├── Range: user_id 1-1M → shard1                                     │
│  │   ├── Hash: hash(user_id) % N                                          │
│  │   └── Directory: Lookup table for routing                              │
│  └── Caching: Reduce DB load                                               │
│                                                                              │
│  SHARDING KEYS (choose carefully!):                                         │
│  ├── High cardinality (many unique values)                                 │
│  ├── Even distribution                                                     │
│  ├── Query pattern alignment                                               │
│  └── Avoid: timestamps, status, low-cardinality fields                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Common System Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COMPONENT REFERENCE                                       │
│                                                                              │
│  LOAD BALANCER                                                              │
│  When: Multiple servers                                                     │
│  Options: Nginx, HAProxy, AWS ALB                                          │
│  L4 (transport) vs L7 (application)                                        │
│                                                                              │
│  CDN                                                                        │
│  When: Static content, global users                                        │
│  Options: CloudFront, Cloudflare, Akamai                                   │
│  Reduces latency, offloads origin                                          │
│                                                                              │
│  MESSAGE QUEUE                                                              │
│  When: Async processing, decoupling                                        │
│  Options: Kafka, RabbitMQ, SQS                                             │
│  Patterns: pub/sub, work queues                                            │
│                                                                              │
│  CACHE                                                                      │
│  When: Read-heavy, repeated queries                                        │
│  Options: Redis, Memcached                                                 │
│  Patterns: cache-aside, write-through                                      │
│                                                                              │
│  SEARCH                                                                     │
│  When: Full-text search, fuzzy matching                                    │
│  Options: Elasticsearch, Solr, Algolia                                     │
│  Uses inverted index                                                       │
│                                                                              │
│  OBJECT STORAGE                                                             │
│  When: Images, videos, large files                                         │
│  Options: S3, GCS, Azure Blob                                              │
│  Not for frequent small reads                                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## CAP Theorem Quick Reference

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CAP THEOREM                                               │
│                                                                              │
│  During network partition, choose:                                          │
│  ├── CP: Consistency (reject requests)                                     │
│  └── AP: Availability (serve potentially stale data)                       │
│                                                                              │
│  COMMON SYSTEMS:                                                            │
│  CP Systems: MongoDB, HBase, Redis (cluster)                               │
│  AP Systems: Cassandra, DynamoDB, CouchDB                                  │
│  CA Systems: Single-node RDBMS (no partition tolerance)                    │
│                                                                              │
│  KEY INSIGHT:                                                               │
│  Partitions are rare but happen                                            │
│  Most of the time you can have C+A                                         │
│  CAP is about what happens DURING partition                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Quick Trade-offs Reference

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TRADE-OFFS CHEATSHEET                                     │
│                                                                              │
│  Performance vs Cost                                                        │
│  ├── More caching = faster but more $$$                                    │
│  └── More replicas = higher availability but more $$$                      │
│                                                                              │
│  Consistency vs Availability                                                │
│  ├── Strong consistency = potential unavailability                         │
│  └── High availability = potential staleness                               │
│                                                                              │
│  Latency vs Throughput                                                      │
│  ├── Batching = higher throughput, higher latency                         │
│  └── Real-time = lower latency, lower throughput                          │
│                                                                              │
│  Simplicity vs Flexibility                                                  │
│  ├── Monolith = simple but hard to scale parts                            │
│  └── Microservices = flexible but complex                                  │
│                                                                              │
│  SQL vs NoSQL                                                               │
│  ├── SQL = ACID, complex queries, harder to scale                         │
│  └── NoSQL = scalable, flexible, limited queries                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Interview Red Flags to Avoid

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DON'T DO THESE                                            │
│                                                                              │
│  ❌ Jumping to solution without requirements                                │
│  ❌ Not doing back-of-envelope math                                         │
│  ❌ Over-engineering from the start                                         │
│  ❌ Designing in silence                                                    │
│  ❌ Ignoring trade-offs                                                     │
│  ❌ Forgetting about failure scenarios                                      │
│  ❌ Not considering scalability                                             │
│  ❌ Using buzzwords without understanding                                   │
│  ❌ Running out of time before key components                               │
│  ❌ Not asking clarifying questions                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**Print this page and review before your interview!**

**Back to:** [Resources Home](./README.md)
