# Final Revision Sheet

One-page reference for last-minute review before your interview.

---

## Interview Framework (45 min)

```
┌──────────────────────────────────────────────────────────────┐
│  0-5 min   │ REQUIREMENTS                                    │
│            │ • Ask 3-5 clarifying questions                  │
│            │ • Define functional requirements                │
│            │ • Define non-functional (scale, latency, etc.) │
├────────────┼─────────────────────────────────────────────────┤
│  5-10 min  │ ESTIMATION                                      │
│            │ • Traffic: users × actions = QPS               │
│            │ • Storage: items × size × retention            │
│            │ • Bandwidth: QPS × data size                   │
├────────────┼─────────────────────────────────────────────────┤
│  10-25 min │ HIGH-LEVEL DESIGN                               │
│            │ • API endpoints                                 │
│            │ • Data model                                    │
│            │ • Architecture diagram                          │
│            │ • Data flow explanation                         │
├────────────┼─────────────────────────────────────────────────┤
│  25-40 min │ DEEP DIVE                                       │
│            │ • Critical component details                    │
│            │ • Trade-off discussions                         │
│            │ • Edge cases                                    │
├────────────┼─────────────────────────────────────────────────┤
│  40-45 min │ WRAP-UP                                         │
│            │ • Summarize design                              │
│            │ • Bottlenecks + solutions                       │
│            │ • Future improvements                           │
└──────────────────────────────────────────────────────────────┘
```

---

## Quick Numbers Reference

### Traffic Conversions
```
1 day    = 86,400 seconds ≈ 100K seconds
1 month  = 2.5 million seconds
1 year   = 30 million seconds

1M daily = ~12 per second
100M daily = ~1,200 per second
```

### Storage Units
```
1 KB  = 1,000 bytes      (text record)
1 MB  = 1,000 KB         (image)
1 GB  = 1,000 MB         (1 hour video)
1 TB  = 1,000 GB         (large database)
1 PB  = 1,000 TB         (big data)
```

### Latency Numbers
```
L1 cache:      0.5 ns
RAM:           100 ns
SSD read:      100 μs
HDD read:      10 ms
Same DC RTT:   0.5 ms
Cross-US RTT:  40 ms
Cross-world:   150 ms
```

---

## Component Cheat Sheet

### When to Use What

```
CACHING: Redis/Memcached
• Read-heavy workloads
• Frequently accessed data
• Reduce database load

MESSAGE QUEUE: Kafka/SQS
• Async processing
• Decouple services
• Handle traffic spikes

LOAD BALANCER:
• Distribute traffic
• L4 (TCP) vs L7 (HTTP)
• Health checks

CDN:
• Static content
• Media files
• Geographic distribution

SEARCH: Elasticsearch
• Full-text search
• Log aggregation
• Analytics

DATABASE CHOICES:
• SQL: Transactions, joins, ACID
• NoSQL (DynamoDB): Key-value, scale
• NoSQL (Cassandra): Write-heavy, time-series
• NoSQL (MongoDB): Documents, flexibility
```

---

## Common Patterns

### Scaling Patterns
```
READ-HEAVY:   Cache + Read Replicas
WRITE-HEAVY:  Sharding + Message Queue
BOTH:         CQRS (separate read/write)
```

### Data Distribution
```
SHARDING:     Split data across DBs (by user_id, etc.)
REPLICATION:  Copy data for redundancy
PARTITIONING: Split tables (by time, etc.)
```

### Consistency
```
STRONG:       All reads see latest write
EVENTUAL:     Reads may be stale temporarily
CAP:          Pick 2 of Consistency, Availability, Partition tolerance
```

---

## Trade-off Phrases

Use these to sound professional:

```
"The trade-off here is..."
"We're optimizing for X at the cost of Y..."
"Given our requirements, I'd choose X because..."
"An alternative would be Y, but..."
"This gives us [benefit] but we sacrifice [cost]..."
```

---

## Red Flags to Avoid

```
❌ Jumping to solution without requirements
❌ No capacity estimation
❌ Single point of failure
❌ No trade-off discussion
❌ Over-engineering
❌ Ignoring interviewer hints
❌ Getting defensive
❌ Silent thinking
```

---

## Must-Discuss Topics

For any design, touch on:

```
□ Load balancing
□ Caching strategy
□ Database choice (+ why)
□ How it scales
□ What happens on failure
□ Data consistency model
```

---

## Day-Before Checklist

```
□ Review this sheet
□ Re-read 2-3 case studies
□ Practice one question out loud
□ Prepare your setup (whiteboard, markers)
□ Get good sleep
□ Know your interview time + link/location
```

---

## Day-Of Checklist

```
□ Arrive/log in 5 min early
□ Have water nearby
□ Have paper for notes
□ Deep breath, you're prepared!
```

---

## Key Mantras

```
┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│  "Ask questions before designing"                              │
│                                                                 │
│  "Think out loud constantly"                                   │
│                                                                 │
│  "Every decision has a trade-off"                              │
│                                                                 │
│  "Breadth first, then depth"                                   │
│                                                                 │
│  "It's okay to not know everything"                            │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

**You've prepared well. Trust your preparation. Good luck!** 🎯
