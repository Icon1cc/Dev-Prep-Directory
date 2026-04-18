# Design News Feed System

## Problem Statement

Design a social media news feed like Facebook's. Users should see posts from friends and pages they follow, ranked by relevance and recency.

---

## 1. Requirements

### Functional Requirements

| Requirement | Description |
|-------------|-------------|
| **Create post** | Users can create posts (text, images, videos) |
| **View feed** | See ranked posts from friends and followed pages |
| **Interact** | Like, comment, share posts |
| **Infinite scroll** | Load more posts as user scrolls |

### Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| **Latency** | < 500ms feed generation |
| **Availability** | 99.99% uptime |
| **Scale** | 1 billion users, 500M DAU |

---

## 2. Capacity Estimation

```
POSTS:
- 500M DAU × 2 posts/day average = 1 billion posts/day
- 1B / 86400 ≈ 11,500 posts/second

FEED READS:
- 500M DAU × 10 feed loads/day = 5 billion feed loads/day
- 5B / 86400 ≈ 58,000 feed loads/second
```

---

## 3. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    NEWS FEED ARCHITECTURE                        │
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
│         ┌─────────────────────┼─────────────────────┐           │
│         │                     │                     │            │
│  ┌──────▼──────┐       ┌──────▼──────┐      ┌──────▼──────┐    │
│  │    Post     │       │    Feed     │      │   Ranking   │    │
│  │   Service   │       │   Service   │      │   Service   │    │
│  └──────┬──────┘       └──────┬──────┘      └──────┬──────┘    │
│         │                     │                    │             │
│         │              ┌──────▼──────┐             │             │
│         │              │  Fan-Out    │◄────────────┘             │
│         │              │  Service    │                          │
│         │              └──────┬──────┘                          │
│         │                     │                                  │
│  ┌──────▼──────┐       ┌──────▼──────┐                          │
│  │  Post Store │       │ Feed Cache  │                          │
│  │ (Cassandra) │       │  (Redis)    │                          │
│  └─────────────┘       └─────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Feed Generation Strategy

### Hybrid Approach (Push + Pull)

```
┌─────────────────────────────────────────────────────────────────┐
│                   HYBRID FAN-OUT                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PUSH (for normal users):                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ User posts → Fan-out to all followers' feed caches      │   │
│  │                                                         │   │
│  │ Good for: Users with < 1000 followers                   │   │
│  │ Fast read: Pre-computed feed                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  PULL (for celebrities):                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Celebrity posts → Store but don't fan-out               │   │
│  │ At read time → Merge with pre-computed feed             │   │
│  │                                                         │   │
│  │ Good for: Users with millions of followers              │   │
│  │ Avoids massive write amplification                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  FEED LOAD:                                                     │
│  1. Get pre-computed feed from cache (pushed posts)            │
│  2. Get followed celebrities' recent posts (pulled)            │
│  3. Merge, rank, and return                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Feed Ranking

```
┌─────────────────────────────────────────────────────────────────┐
│                    FEED RANKING                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Ranking factors:                                               │
│                                                                  │
│  1. Affinity Score: How close is user to poster?               │
│     - Interaction history (likes, comments, messages)          │
│     - Profile views                                             │
│     - Tagged together                                           │
│                                                                  │
│  2. Post Quality: How engaging is this post?                   │
│     - Engagement rate (likes/views)                            │
│     - Comment count                                             │
│     - Share count                                               │
│                                                                  │
│  3. Time Decay: How recent is the post?                        │
│     - Newer posts score higher                                 │
│     - Decay function (exponential or linear)                   │
│                                                                  │
│  4. Content Type: User preferences                             │
│     - Videos vs photos vs text                                 │
│     - Topics/categories                                        │
│                                                                  │
│  Score = (Affinity × Weight_A) + (Quality × Weight_Q)          │
│          + (Recency × Weight_R) + (Type × Weight_T)            │
│                                                                  │
│  ML models continuously optimize these weights                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Data Model

### Posts Table

```sql
CREATE TABLE posts (
    post_id        UUID PRIMARY KEY,
    user_id        UUID,
    content        TEXT,
    media_urls     JSON,
    created_at     TIMESTAMP,
    like_count     INT,
    comment_count  INT,
    share_count    INT
);
```

### Feed Cache (Redis)

```
Key: feed:{user_id}
Value: Sorted set of post_ids by score

ZADD feed:user_123 0.95 "post_abc"
ZADD feed:user_123 0.87 "post_def"

# Get top 20 posts
ZREVRANGE feed:user_123 0 19
```

---

## 7. Post Creation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   POST CREATION FLOW                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. User creates post                                           │
│     ┌──────────┐     ┌──────────────┐                          │
│     │  Client  │────►│ Post Service │                          │
│     └──────────┘     └──────┬───────┘                          │
│                             │                                   │
│  2. Store post              │                                   │
│                      ┌──────▼───────┐                          │
│                      │  Post Store  │                          │
│                      │ (Cassandra)  │                          │
│                      └──────┬───────┘                          │
│                             │                                   │
│  3. Send to fan-out queue   │                                   │
│                      ┌──────▼───────┐                          │
│                      │    Kafka     │                          │
│                      │ (post-events)│                          │
│                      └──────┬───────┘                          │
│                             │                                   │
│  4. Fan-out workers process │                                   │
│                      ┌──────▼───────┐                          │
│                      │  Fan-Out     │                          │
│                      │  Workers     │                          │
│                      └──────┬───────┘                          │
│                             │                                   │
│  5. Push to followers' feeds│                                   │
│                      ┌──────▼───────┐                          │
│                      │ Feed Caches  │                          │
│                      │   (Redis)    │                          │
│                      └─────────────┘                           │
│                                                                  │
│  Async: Return to user immediately after step 2                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Feed Load Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    FEED LOAD FLOW                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Client requests feed                                        │
│     ┌──────────┐     ┌──────────────┐                          │
│     │  Client  │────►│ Feed Service │                          │
│     └──────────┘     └──────┬───────┘                          │
│                             │                                   │
│  2. Get pre-computed feed from cache                           │
│                      ┌──────▼───────┐                          │
│                      │ Feed Cache   │  post_ids for user       │
│                      │   (Redis)    │                          │
│                      └──────┬───────┘                          │
│                             │                                   │
│  3. Get celebrity posts (pull)                                 │
│                      ┌──────▼───────┐                          │
│                      │ Post Store   │  Recent posts from       │
│                      │              │  followed celebrities    │
│                      └──────┬───────┘                          │
│                             │                                   │
│  4. Merge and rank          │                                   │
│                      ┌──────▼───────┐                          │
│                      │   Ranking    │                          │
│                      │   Service    │                          │
│                      └──────┬───────┘                          │
│                             │                                   │
│  5. Hydrate posts (get full data)                              │
│                      ┌──────▼───────┐                          │
│                      │ Post Store   │  Full post objects       │
│                      │ (multiget)   │                          │
│                      └──────┬───────┘                          │
│                             │                                   │
│  6. Return to client        │                                   │
│     { posts: [...], next_cursor: "..." }                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. Pagination (Infinite Scroll)

```
CURSOR-BASED PAGINATION:
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Initial request:                                               │
│  GET /feed?limit=20                                             │
│  Response: { posts: [...], next_cursor: "score_0.87_post_xyz" }│
│                                                                  │
│  Load more:                                                     │
│  GET /feed?limit=20&cursor=score_0.87_post_xyz                 │
│  Response: { posts: [...], next_cursor: "score_0.65_post_abc" }│
│                                                                  │
│  Cursor encodes:                                                │
│  - Score of last post (for continuing sort)                    │
│  - Post ID (for uniqueness)                                    │
│                                                                  │
│  Benefits:                                                      │
│  - Works with real-time updates (new posts don't shift pages)  │
│  - Efficient (no OFFSET)                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Trade-offs

| Decision | Choice | Alternative | Reason |
|----------|--------|-------------|--------|
| Fan-out | Hybrid | Pure push/pull | Balance speed and cost |
| Feed storage | Redis | Database | Speed for hot data |
| Ranking | ML-based | Chronological | Better engagement |
| Pagination | Cursor | Offset | Handles real-time updates |

---

## 11. Follow-up Questions

1. "How would you handle posts with millions of likes?"
2. "How do you prevent showing the same post twice?"
3. "How would you implement a 'close friends' feature?"
4. "How do you handle feed for inactive users?"
5. "How would you add support for stories (ephemeral content)?"

---

## Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                   NEWS FEED SUMMARY                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  KEY COMPONENTS:                                                │
│  ├── Hybrid fan-out (push + pull)                              │
│  ├── Feed cache (Redis) for pre-computed feeds                 │
│  ├── ML-based ranking                                          │
│  └── Cursor-based pagination                                   │
│                                                                  │
│  KEY INSIGHTS:                                                  │
│  ├── Push for normal users, pull for celebrities               │
│  ├── Async fan-out via message queue                           │
│  ├── Ranking considers affinity, quality, recency              │
│  └── Pre-compute feeds, hydrate on read                        │
│                                                                  │
│  SCALE:                                                         │
│  ├── 58K feed loads/second                                     │
│  ├── 11.5K posts/second                                        │
│  └── Sub-second feed generation                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

*Next: [Design Google Drive](07_google_drive.md) →*
