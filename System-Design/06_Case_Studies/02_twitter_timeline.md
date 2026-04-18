# Design Twitter/X Timeline

## Problem Statement

Design Twitter's home timeline—the feed of tweets from people a user follows. When a user opens Twitter, they should see recent tweets from accounts they follow, sorted by time (or relevance).

---

## 1. Requirements

### Functional Requirements

| Requirement | Description |
|-------------|-------------|
| **Post tweet** | Users can post tweets (280 chars + media) |
| **Follow/Unfollow** | Users can follow other users |
| **Home timeline** | See tweets from followed users |
| **User timeline** | See tweets from a specific user |

### Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| **Availability** | 99.99% uptime |
| **Timeline latency** | < 200ms to load |
| **Post latency** | < 500ms to confirm |
| **Scale** | 500M users, 200M DAU |

### Out of Scope
- Likes, retweets, replies
- Search, hashtags, trends
- Direct messages
- Notifications

---

## 2. Capacity Estimation

### Users and Tweets

```
USERS:
- 500M total users
- 200M daily active users (DAU)
- Average user follows 200 accounts

TWEETS:
- 500M tweets per day
- 500M / 86400 sec ≈ 6,000 tweets/second
- Peak: 6,000 × 3 = 18,000 tweets/second
```

### Timeline Reads

```
TIMELINE READS:
- 200M DAU × 5 timeline loads/day = 1B timeline loads/day
- 1B / 86400 ≈ 12,000 timeline loads/second
- Peak: 12,000 × 3 = 36,000/second
```

### Storage

```
TWEET STORAGE:
- Tweet: 280 chars = 280 bytes (text)
- Metadata: 200 bytes (user_id, timestamp, etc.)
- Total: ~500 bytes per tweet
- 500M tweets/day × 500 bytes = 250 GB/day
- Per year: ~90 TB

TIMELINE CACHE:
- 200M active users × 800 tweets cached × 8 bytes (tweet_id)
- ≈ 1.3 TB for timeline cache
```

---

## 3. The Core Challenge: Fan-Out

### The Problem

```
USER A POSTS A TWEET:
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  User A has 10 million followers                                │
│  User A posts: "Hello World!"                                   │
│                                                                  │
│  How do 10 million users see this tweet in their timeline?     │
│                                                                  │
│  Option 1: PULL (Fan-out on read)                               │
│  - When user opens timeline, query all followed users' tweets  │
│  - 200 follows × query = SLOW at read time                     │
│                                                                  │
│  Option 2: PUSH (Fan-out on write)                              │
│  - When tweet posted, push to all followers' timelines         │
│  - 10M followers × push = SLOW at write time                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Fan-Out Strategies

#### Fan-Out on Read (Pull Model)

```
┌─────────────────────────────────────────────────────────────────┐
│                    FAN-OUT ON READ                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  When user loads timeline:                                      │
│                                                                  │
│  1. Get list of users I follow: [A, B, C, D, E...]             │
│  2. Query tweets from each user                                 │
│  3. Merge and sort by timestamp                                 │
│  4. Return top N tweets                                         │
│                                                                  │
│  User Timeline Request                                          │
│          │                                                       │
│          ▼                                                       │
│  ┌───────────────────────┐                                      │
│  │  Get Following List   │                                      │
│  │  (200 users)          │                                      │
│  └───────────┬───────────┘                                      │
│              │                                                   │
│  ┌───────────▼───────────┐                                      │
│  │  Query Tweets DB      │  200 queries!                        │
│  │  for each user        │                                      │
│  └───────────┬───────────┘                                      │
│              │                                                   │
│  ┌───────────▼───────────┐                                      │
│  │  Merge & Sort         │                                      │
│  └───────────┬───────────┘                                      │
│              │                                                   │
│              ▼                                                   │
│       Timeline Result                                           │
│                                                                  │
│  Pros: Simple, real-time, no write amplification               │
│  Cons: SLOW reads, high DB load                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### Fan-Out on Write (Push Model)

```
┌─────────────────────────────────────────────────────────────────┐
│                   FAN-OUT ON WRITE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  When user posts tweet:                                         │
│                                                                  │
│  1. Save tweet to database                                      │
│  2. Get all followers of this user                              │
│  3. Push tweet_id to each follower's timeline cache            │
│                                                                  │
│  Tweet Post                                                     │
│      │                                                          │
│      ▼                                                          │
│  ┌───────────────────────┐                                      │
│  │   Save Tweet to DB    │                                      │
│  └───────────┬───────────┘                                      │
│              │                                                   │
│  ┌───────────▼───────────┐                                      │
│  │  Get Followers List   │  (Could be millions!)               │
│  └───────────┬───────────┘                                      │
│              │                                                   │
│  ┌───────────▼───────────────────────────────────────────────┐ │
│  │  Push to Each Follower's Timeline Cache                   │ │
│  │                                                           │ │
│  │  Follower 1's Cache: [tweet_id, ...]                     │ │
│  │  Follower 2's Cache: [tweet_id, ...]                     │ │
│  │  ...                                                      │ │
│  │  Follower N's Cache: [tweet_id, ...]                     │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Reading timeline: Just read from cache! Fast!                 │
│                                                                  │
│  Pros: FAST reads (pre-computed)                               │
│  Cons: Slow writes for celebrities, storage cost               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### Hybrid Approach (Twitter's Solution)

```
┌─────────────────────────────────────────────────────────────────┐
│                    HYBRID APPROACH                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  For NORMAL users (< 10K followers):                            │
│  └── Fan-out on write (push to followers)                       │
│                                                                  │
│  For CELEBRITIES (> 10K followers):                             │
│  └── Fan-out on read (pull at read time)                        │
│                                                                  │
│  Timeline Load:                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  1. Get pre-computed timeline from cache (normal users) │   │
│  │  2. Query tweets from celebrities I follow              │   │
│  │  3. Merge and sort                                       │   │
│  │                                                          │   │
│  │  Pre-computed    +    Celebrity     =    Final          │   │
│  │  [tweet1,tweet2]     [celeb_tweet]      Timeline        │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  This balances:                                                 │
│  - Fast reads for most users                                   │
│  - Manageable write amplification                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   TWITTER TIMELINE ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                        ┌──────────────┐                         │
│                        │   Clients    │                         │
│                        └──────┬───────┘                         │
│                               │                                  │
│                        ┌──────▼───────┐                         │
│                        │ API Gateway  │                         │
│                        └──────┬───────┘                         │
│                               │                                  │
│            ┌──────────────────┼──────────────────┐              │
│            │                  │                  │               │
│     ┌──────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐      │
│     │   Tweet     │    │  Timeline   │    │    User     │      │
│     │   Service   │    │   Service   │    │   Service   │      │
│     └──────┬──────┘    └──────┬──────┘    └──────┬──────┘      │
│            │                  │                  │               │
│            │           ┌──────▼──────┐          │               │
│            │           │  Fan-Out    │          │               │
│            └──────────►│   Service   │◄─────────┘               │
│                        └──────┬──────┘                          │
│                               │                                  │
│         ┌─────────────────────┼─────────────────────┐           │
│         │                     │                     │            │
│  ┌──────▼──────┐       ┌──────▼──────┐      ┌──────▼──────┐    │
│  │   Tweet     │       │  Timeline   │      │  Social     │    │
│  │   Store     │       │   Cache     │      │   Graph     │    │
│  │  (Tweets)   │       │  (Redis)    │      │ (Followers) │    │
│  └─────────────┘       └─────────────┘      └─────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Purpose |
|-----------|---------|
| **Tweet Service** | CRUD operations for tweets |
| **Timeline Service** | Build and serve timelines |
| **User Service** | User profiles, follow relationships |
| **Fan-Out Service** | Distribute tweets to followers |
| **Timeline Cache** | Pre-computed timelines (Redis) |
| **Social Graph** | Follow/follower relationships |

---

## 5. Data Model

### Tweet Table

```sql
CREATE TABLE tweets (
    tweet_id       BIGINT PRIMARY KEY,
    user_id        BIGINT NOT NULL,
    content        VARCHAR(280),
    media_urls     JSON,
    created_at     TIMESTAMP,

    INDEX idx_user_time (user_id, created_at DESC)
);
```

### User Table

```sql
CREATE TABLE users (
    user_id        BIGINT PRIMARY KEY,
    username       VARCHAR(50) UNIQUE,
    follower_count BIGINT DEFAULT 0,
    is_celebrity   BOOLEAN DEFAULT FALSE
);
```

### Follow Table (Social Graph)

```sql
CREATE TABLE follows (
    follower_id    BIGINT,
    followee_id    BIGINT,
    created_at     TIMESTAMP,

    PRIMARY KEY (follower_id, followee_id),
    INDEX idx_followee (followee_id)
);
```

### Timeline Cache (Redis)

```
Key: timeline:{user_id}
Value: Sorted Set of tweet_ids by timestamp

ZADD timeline:123 1615000000 "tweet_abc"
ZADD timeline:123 1615000100 "tweet_def"

ZREVRANGE timeline:123 0 99  -- Get latest 100 tweets
```

---

## 6. Detailed Flow: Posting a Tweet

```
┌─────────────────────────────────────────────────────────────────┐
│                    POST TWEET FLOW                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User posts: "Hello Twitter!"                                   │
│                                                                  │
│  1. ┌─────────────────────────────────────────────────────────┐│
│     │ Tweet Service: Validate and save tweet                  ││
│     │                                                         ││
│     │ INSERT INTO tweets (tweet_id, user_id, content...)     ││
│     │ Return: tweet_id = "abc123"                            ││
│     └─────────────────────────────────────────────────────────┘│
│                         │                                       │
│                         ▼                                       │
│  2. ┌─────────────────────────────────────────────────────────┐│
│     │ Send to Message Queue (Kafka)                          ││
│     │                                                         ││
│     │ Topic: tweet-created                                    ││
│     │ Message: { tweet_id, user_id, timestamp }              ││
│     └─────────────────────────────────────────────────────────┘│
│                         │                                       │
│                         ▼                                       │
│  3. ┌─────────────────────────────────────────────────────────┐│
│     │ Fan-Out Service (async)                                 ││
│     │                                                         ││
│     │ IF user.follower_count < 10,000:                       ││
│     │   Get all followers from Social Graph                  ││
│     │   For each follower:                                   ││
│     │     ZADD timeline:{follower_id} {timestamp} {tweet_id} ││
│     │                                                         ││
│     │ ELSE (celebrity):                                       ││
│     │   Skip fan-out (will be pulled at read time)           ││
│     └─────────────────────────────────────────────────────────┘│
│                                                                  │
│  Response to user: 200 OK (fast, async fan-out)                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Detailed Flow: Loading Timeline

```
┌─────────────────────────────────────────────────────────────────┐
│                   LOAD TIMELINE FLOW                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User opens app, requests timeline                              │
│                                                                  │
│  1. ┌─────────────────────────────────────────────────────────┐│
│     │ Get pre-computed timeline from cache                    ││
│     │                                                         ││
│     │ ZREVRANGE timeline:123 0 99                            ││
│     │ Returns: [tweet_id_1, tweet_id_2, ...]                 ││
│     └─────────────────────────────────────────────────────────┘│
│                         │                                       │
│                         ▼                                       │
│  2. ┌─────────────────────────────────────────────────────────┐│
│     │ Get celebrities user follows                            ││
│     │                                                         ││
│     │ SELECT followee_id FROM follows                        ││
│     │ WHERE follower_id = 123 AND followee.is_celebrity      ││
│     │ Returns: [celeb_1, celeb_2]                            ││
│     └─────────────────────────────────────────────────────────┘│
│                         │                                       │
│                         ▼                                       │
│  3. ┌─────────────────────────────────────────────────────────┐│
│     │ Fetch celebrity tweets (fan-out on read)               ││
│     │                                                         ││
│     │ SELECT * FROM tweets                                    ││
│     │ WHERE user_id IN (celeb_1, celeb_2)                    ││
│     │ AND created_at > (now - 24 hours)                      ││
│     │ ORDER BY created_at DESC LIMIT 20                      ││
│     └─────────────────────────────────────────────────────────┘│
│                         │                                       │
│                         ▼                                       │
│  4. ┌─────────────────────────────────────────────────────────┐│
│     │ Merge and sort all tweets                               ││
│     │                                                         ││
│     │ Combined = precomputed_tweets + celebrity_tweets       ││
│     │ Sort by timestamp, take top 100                        ││
│     └─────────────────────────────────────────────────────────┘│
│                         │                                       │
│                         ▼                                       │
│  5. ┌─────────────────────────────────────────────────────────┐│
│     │ Hydrate tweet data                                      ││
│     │                                                         ││
│     │ Fetch full tweet objects from Tweet Store              ││
│     │ (using multiget for efficiency)                        ││
│     └─────────────────────────────────────────────────────────┘│
│                         │                                       │
│                         ▼                                       │
│     Return timeline to client                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Scaling Considerations

### Timeline Cache Sharding

```
SHARDING BY USER_ID:
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Redis Cluster with consistent hashing                          │
│                                                                  │
│  User 123 → hash(123) → Shard 2                                │
│  User 456 → hash(456) → Shard 5                                │
│  User 789 → hash(789) → Shard 1                                │
│                                                                  │
│  Each shard: ~2M users, ~200GB memory                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Database Sharding

```
TWEET DATABASE:
- Shard by user_id (tweets from same user on same shard)
- Range or hash-based sharding

SOCIAL GRAPH:
- Shard by follower_id (all follows for a user together)
- Enables efficient "who do I follow" queries
```

---

## 9. Trade-offs

| Decision | Choice | Alternative | Reason |
|----------|--------|-------------|--------|
| Fan-out | Hybrid | Pure push/pull | Balance speed and cost |
| Timeline storage | Redis | Memcached | Sorted sets, persistence |
| Tweet storage | MySQL sharded | Cassandra | Familiar, good enough |
| Celebrity threshold | 10K followers | Other values | Empirical tuning |

---

## 10. Follow-up Questions

1. "How would you handle tweet deletions?"
2. "How would you add a 'For You' algorithmic timeline?"
3. "How would you handle trending topics?"
4. "How do you ensure timeline consistency?"
5. "How would you add support for retweets?"

---

## Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                 TWITTER TIMELINE SUMMARY                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CORE INSIGHT: Hybrid fan-out                                   │
│  ├── Push for normal users (< 10K followers)                   │
│  └── Pull for celebrities (> 10K followers)                    │
│                                                                  │
│  KEY COMPONENTS:                                                │
│  ├── Timeline cache (Redis sorted sets)                        │
│  ├── Fan-out service (async via Kafka)                         │
│  └── Social graph for follow relationships                     │
│                                                                  │
│  KEY NUMBERS:                                                   │
│  ├── 6K tweets/sec, 12K timeline reads/sec                     │
│  ├── ~1.3 TB for timeline cache                                │
│  └── 200 follows average per user                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

*Next: [Design WhatsApp](03_whatsapp.md) →*
