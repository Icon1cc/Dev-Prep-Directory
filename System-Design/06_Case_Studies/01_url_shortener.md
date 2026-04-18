# Design a URL Shortener (TinyURL)

## Problem Statement

Design a URL shortening service like TinyURL or bit.ly. Users should be able to submit a long URL and receive a short URL that redirects to the original.

```
Input:  https://www.example.com/very/long/path/to/resource?query=param
Output: https://tinyurl.com/abc123
```

---

## 1. Requirements

### Functional Requirements

| Requirement | Description |
|-------------|-------------|
| **Shorten URL** | Given a long URL, generate a unique short URL |
| **Redirect** | Given a short URL, redirect to the original long URL |
| **Custom alias** | (Optional) Allow users to pick custom short URLs |
| **Expiration** | (Optional) URLs can have expiration dates |
| **Analytics** | (Optional) Track click counts |

### Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| **Availability** | 99.9% uptime |
| **Latency** | < 100ms for redirects |
| **Scale** | 100 million URLs created per month |
| **Durability** | URLs should never be lost |

### Out of Scope
- User accounts and authentication
- Rate limiting (mentioned but not designed)
- Spam/abuse prevention

---

## 2. Capacity Estimation

### Traffic Estimates

```
URL CREATION:
- 100 million new URLs per month
- 100M / (30 days × 24 hours × 3600 sec) ≈ 40 URLs/second

REDIRECTS (assume 100:1 read:write ratio):
- 40 URLs/sec × 100 = 4,000 redirects/second
- Peak: 4,000 × 3 = 12,000 redirects/second
```

### Storage Estimates

```
STORAGE PER URL:
- Short URL: 7 characters = 7 bytes
- Long URL: average 200 bytes
- Created timestamp: 8 bytes
- Expiration: 8 bytes
- Total: ~250 bytes per record

TOTAL STORAGE (5 years):
- 100M URLs/month × 12 months × 5 years = 6 billion URLs
- 6B × 250 bytes = 1.5 TB

With replication (3x): ~5 TB total
```

### Bandwidth Estimates

```
INCOMING (write):
- 40 URLs/sec × 250 bytes = 10 KB/second

OUTGOING (read):
- 4,000 redirects/sec × 250 bytes = 1 MB/second
```

---

## 3. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     URL SHORTENER ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                        ┌───────────────┐                        │
│                        │   Clients     │                        │
│                        │  (Web/Mobile) │                        │
│                        └───────┬───────┘                        │
│                                │                                 │
│                        ┌───────▼───────┐                        │
│                        │ Load Balancer │                        │
│                        └───────┬───────┘                        │
│                                │                                 │
│               ┌────────────────┼────────────────┐               │
│               │                │                │               │
│        ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐       │
│        │ App Server  │  │ App Server  │  │ App Server  │       │
│        └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │
│               │                │                │               │
│               └────────────────┼────────────────┘               │
│                                │                                 │
│                 ┌──────────────┴──────────────┐                 │
│                 │                             │                  │
│          ┌──────▼──────┐              ┌───────▼──────┐          │
│          │    Cache    │              │   Database   │          │
│          │   (Redis)   │              │   (NoSQL)    │          │
│          └─────────────┘              └──────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Component Overview

| Component | Purpose |
|-----------|---------|
| **Load Balancer** | Distribute traffic across app servers |
| **App Servers** | Handle URL creation and redirect logic |
| **Cache** | Store hot URLs for fast redirects |
| **Database** | Persistent storage for URL mappings |

---

## 4. API Design

### Create Short URL

```
POST /api/v1/urls

Request:
{
  "long_url": "https://www.example.com/very/long/path",
  "custom_alias": "mylink",     // optional
  "expiration": "2025-12-31"    // optional
}

Response (201 Created):
{
  "short_url": "https://tinyurl.com/abc123",
  "long_url": "https://www.example.com/very/long/path",
  "created_at": "2024-03-15T10:30:00Z",
  "expires_at": "2025-12-31T23:59:59Z"
}

Errors:
- 400: Invalid URL format
- 409: Custom alias already taken
```

### Redirect

```
GET /{short_code}

Response: 301 Redirect to long URL

Headers:
Location: https://www.example.com/very/long/path
```

### Get URL Info (Optional)

```
GET /api/v1/urls/{short_code}

Response (200 OK):
{
  "short_url": "https://tinyurl.com/abc123",
  "long_url": "https://www.example.com/very/long/path",
  "created_at": "2024-03-15T10:30:00Z",
  "click_count": 1542
}
```

---

## 5. Data Model

### URL Table

```
┌─────────────────────────────────────────────────────────────────┐
│                        URL TABLE                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Column          │ Type         │ Description                   │
│  ────────────────┼──────────────┼─────────────────────────────  │
│  short_code      │ VARCHAR(7)   │ Primary key, the short URL   │
│  long_url        │ VARCHAR(2048)│ Original URL                 │
│  created_at      │ TIMESTAMP    │ When URL was created         │
│  expires_at      │ TIMESTAMP    │ Expiration time (nullable)   │
│  click_count     │ BIGINT       │ Number of redirects          │
│                                                                  │
│  Indexes:                                                       │
│  - PRIMARY KEY (short_code)                                     │
│  - INDEX (expires_at) -- for cleanup jobs                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Database Choice: NoSQL (e.g., DynamoDB, Cassandra)

**Why NoSQL?**
- Simple key-value access pattern
- High read throughput needed
- No complex queries or joins
- Easy horizontal scaling

---

## 6. Short URL Generation

### Approach 1: Base62 Encoding

Convert a unique number to a short string using characters: `[a-z, A-Z, 0-9]`

```
62 characters available
7 characters = 62^7 = 3.5 trillion unique URLs

Example:
Number: 12345
Base62: "dnh"

Algorithm:
┌─────────────────────────────────────────────────────────────────┐
│  def encode_base62(num):                                        │
│      chars = "0123456789abcdefghijklmnopqrstuvwxyz"             │
│      chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"                      │
│      result = ""                                                 │
│      while num > 0:                                              │
│          result = chars[num % 62] + result                      │
│          num //= 62                                              │
│      return result.rjust(7, '0')                                │
└─────────────────────────────────────────────────────────────────┘
```

### Approach 2: Counter-Based (Recommended)

Use a distributed counter to generate unique IDs, then encode.

```
┌─────────────────────────────────────────────────────────────────┐
│                 COUNTER-BASED GENERATION                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Range Server (like ZooKeeper):                                 │
│  - Server 1 gets range: 1 - 1,000,000                           │
│  - Server 2 gets range: 1,000,001 - 2,000,000                   │
│  - Server 3 gets range: 2,000,001 - 3,000,000                   │
│                                                                  │
│  Each server:                                                   │
│  1. Takes next number from its range                            │
│  2. Encodes to base62                                           │
│  3. No coordination needed until range exhausted                │
│                                                                  │
│  Benefits:                                                      │
│  ✓ No collisions (each server has unique range)                │
│  ✓ Fast (no database lookup for uniqueness)                    │
│  ✓ Scalable (add more servers, assign new ranges)              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Approach 3: Hash-Based

Hash the long URL and take first 7 characters.

```
MD5(long_url) → first 7 chars → short_code

Problem: Collisions!
Solution: If collision, append counter and retry
```

### Comparison

| Approach | Pros | Cons |
|----------|------|------|
| **Counter** | Fast, no collisions | Need counter service |
| **Hash** | Stateless | Collisions possible |
| **Random** | Simple | Must check uniqueness |

**Recommendation**: Counter-based with range allocation

---

## 7. Redirect Flow (Deep Dive)

```
┌─────────────────────────────────────────────────────────────────┐
│                     REDIRECT FLOW                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. User visits: tinyurl.com/abc123                             │
│           │                                                      │
│           ▼                                                      │
│  2. ┌─────────────────┐                                         │
│     │  Load Balancer  │                                         │
│     └────────┬────────┘                                         │
│              │                                                   │
│              ▼                                                   │
│  3. ┌─────────────────┐                                         │
│     │   App Server    │                                         │
│     │                 │                                         │
│     │  Check Cache    │──── Hit ────► Return long_url          │
│     │       │         │                                         │
│     │      Miss       │                                         │
│     │       │         │                                         │
│     │       ▼         │                                         │
│     │  Query Database │                                         │
│     │       │         │                                         │
│     │      Found      │                                         │
│     │       │         │                                         │
│     │  Update Cache   │                                         │
│     │       │         │                                         │
│     │  Return long_url│                                         │
│     └────────┬────────┘                                         │
│              │                                                   │
│              ▼                                                   │
│  4. HTTP 301/302 Redirect to long_url                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 301 vs 302 Redirect

| Type | Meaning | Caching |
|------|---------|---------|
| **301** | Permanent redirect | Browser caches |
| **302** | Temporary redirect | No browser cache |

**Recommendation**: Use 302 if you want to track analytics (all requests hit your server)

---

## 8. Caching Strategy

```
CACHE CONFIGURATION:
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Cache: Redis Cluster                                           │
│  Key: short_code                                                │
│  Value: long_url                                                │
│  TTL: 24 hours (for most URLs)                                  │
│                                                                  │
│  Eviction: LRU (Least Recently Used)                            │
│  Size: ~20% of total URLs (hot data)                            │
│                                                                  │
│  Expected hit rate: 80%+                                        │
│  (Most traffic goes to small subset of popular URLs)            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. Scaling Considerations

### Database Scaling

```
SHARDING STRATEGY:
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Shard by: First character of short_code                        │
│                                                                  │
│  short_code starts with:                                        │
│  a-h  → Shard 1                                                 │
│  i-p  → Shard 2                                                 │
│  q-z  → Shard 3                                                 │
│  0-9, A-Z → Shard 4                                             │
│                                                                  │
│  Or use consistent hashing for more flexibility                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Read Replicas

```
REPLICATION:
┌─────────────┐     ┌─────────────┐
│   Primary   │────►│  Replica 1  │ (Reads)
│  (Writes)   │────►│  Replica 2  │ (Reads)
└─────────────┘────►│  Replica 3  │ (Reads)
                    └─────────────┘
```

---

## 10. Trade-offs and Alternatives

### Design Decisions

| Decision | Choice | Alternative | Why |
|----------|--------|-------------|-----|
| Short URL length | 7 chars | 6 or 8 | Balance uniqueness vs brevity |
| Database | NoSQL | SQL | Simple access pattern, scale |
| ID generation | Counter | Hash | No collision handling |
| Redirect type | 302 | 301 | Need analytics |
| Cache | Redis | Memcached | Persistence, replication |

### What If Questions

**Q: What if we need to support 1 trillion URLs?**
- Increase short code to 8 characters (62^8 = 218 trillion)
- Add more database shards

**Q: What if we need real-time analytics?**
- Stream clicks to Kafka → Analytics pipeline
- Async updates to avoid redirect latency

**Q: What if a popular URL goes viral?**
- Cache will absorb most traffic
- Consider CDN for static redirects

---

## 11. Follow-up Interview Questions

1. "How would you handle a custom alias that conflicts with a generated one?"
2. "How would you implement URL expiration?"
3. "How would you prevent abuse (spam URLs)?"
4. "How would you make this globally distributed?"
5. "How would you handle URL analytics at scale?"

---

## Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                    URL SHORTENER SUMMARY                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  KEY COMPONENTS:                                                │
│  ├── Counter service for unique ID generation                  │
│  ├── Base62 encoding for short URLs                            │
│  ├── NoSQL database for storage                                │
│  └── Redis cache for hot URLs                                  │
│                                                                  │
│  KEY NUMBERS:                                                   │
│  ├── 40 writes/sec, 4000 reads/sec                             │
│  ├── 1.5 TB storage for 5 years                                │
│  └── 7 characters = 3.5 trillion unique URLs                   │
│                                                                  │
│  KEY TRADE-OFFS:                                                │
│  ├── 301 vs 302 redirects (caching vs analytics)               │
│  ├── Counter vs hash for ID generation                         │
│  └── NoSQL vs SQL (scale vs features)                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

*Next: [Design Twitter Timeline](02_twitter_timeline.md) →*
