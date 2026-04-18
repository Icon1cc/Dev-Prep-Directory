# System Design Interview Flow

## The Standard Interview Structure

A typical system design interview follows this flow, regardless of company:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    45-MINUTE INTERVIEW FLOW                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  0:00 ─────────────────────────────────────────────────────────────│
│  │                                                                  │
│  │  PHASE 1: Problem & Requirements (5-7 min)                      │
│  │  ├── Interviewer states the problem                             │
│  │  ├── You ask clarifying questions                               │
│  │  ├── Define functional requirements                             │
│  │  └── Define non-functional requirements                         │
│  │                                                                  │
│  7:00 ─────────────────────────────────────────────────────────────│
│  │                                                                  │
│  │  PHASE 2: High-Level Design (15-20 min)                         │
│  │  ├── Capacity estimation (back-of-envelope)                     │
│  │  ├── API design (key endpoints)                                 │
│  │  ├── Data model (main entities)                                 │
│  │  └── Architecture diagram (components + flow)                   │
│  │                                                                  │
│  25:00 ────────────────────────────────────────────────────────────│
│  │                                                                  │
│  │  PHASE 3: Deep Dive (10-15 min)                                 │
│  │  ├── Interviewer picks area to explore                          │
│  │  ├── Detailed component design                                  │
│  │  ├── Discuss trade-offs                                         │
│  │  └── Handle edge cases                                          │
│  │                                                                  │
│  40:00 ────────────────────────────────────────────────────────────│
│  │                                                                  │
│  │  PHASE 4: Wrap-up (5 min)                                       │
│  │  ├── Summarize design                                           │
│  │  ├── Discuss bottlenecks                                        │
│  │  ├── Future improvements                                        │
│  │  └── Your questions for interviewer                             │
│  │                                                                  │
│  45:00 ─────────────────────────────────────────────────────────────│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Requirements (5-7 minutes)

### What the Interviewer Says

> "Design Twitter" or "Design a URL shortener"

### What You Should Do

**1. Clarify the scope:**
```
"Before I start, I'd like to ask a few questions to make sure
I understand the requirements..."

GOOD QUESTIONS:
- "What are the core features we need to support?"
- "How many users are we expecting?"
- "What's more important: consistency or availability?"
- "Do we need to support mobile, web, or both?"
- "Is this global or single region?"
```

**2. Define functional requirements:**
```
"Based on our discussion, here are the functional requirements:

1. Users can post tweets (text, images)
2. Users can follow other users
3. Users can view their home timeline
4. Users can search for tweets

Does this capture the core functionality?"
```

**3. Define non-functional requirements:**
```
"For non-functional requirements, I'll assume:

1. Scale: 500M users, 200M DAU
2. Availability: 99.9% uptime
3. Latency: < 200ms for timeline load
4. Consistency: Eventual consistency is acceptable

Does this align with your expectations?"
```

### Common Mistakes in Phase 1

| Mistake | Why It's Bad | What to Do |
|---------|--------------|------------|
| Skipping questions | Miss critical constraints | Always ask 3-5 questions |
| Asking too many | Wastes time | Focus on scope, scale, priorities |
| Not writing down | Forget later | Write requirements on board |

---

## Phase 2: High-Level Design (15-20 minutes)

### Step 1: Capacity Estimation (3-5 min)

```
"Let me do some back-of-envelope calculations...

USERS:
- 500M total users, 200M DAU
- Each user follows 200 people on average

TWEETS:
- 200M DAU × 2 tweets/day = 400M tweets/day
- 400M / 86400 sec ≈ 5,000 tweets/second

READS (Timeline):
- 200M DAU × 10 timeline loads/day = 2B reads/day
- 2B / 86400 ≈ 23,000 reads/second

STORAGE:
- Tweet: ~300 bytes (text + metadata)
- 400M tweets × 300 bytes = 120 GB/day
- 5 years: ~200 TB"
```

### Step 2: API Design (2-3 min)

```
"Here are the key APIs:

POST /tweets
- Body: { content, media_ids }
- Returns: tweet_id

GET /timeline
- Params: user_id, cursor, limit
- Returns: { tweets[], next_cursor }

POST /follow
- Body: { followee_id }
- Returns: success/failure"
```

### Step 3: Data Model (2-3 min)

```
"The main entities:

USERS: user_id, username, email, created_at
TWEETS: tweet_id, user_id, content, created_at
FOLLOWS: follower_id, followee_id, created_at
TIMELINE_CACHE: user_id → [tweet_ids]"
```

### Step 4: Architecture Diagram (5-7 min)

```
"Let me draw the high-level architecture..."

[Draw on whiteboard while explaining]

"1. Clients connect through a Load Balancer
2. API servers handle requests
3. For posting tweets:
   - Save to Tweet DB
   - Push to message queue for fan-out
4. Fan-out service pushes to followers' timeline caches
5. For reading timeline:
   - Check Timeline Cache (Redis)
   - If miss, build from Tweet DB"
```

---

## Phase 3: Deep Dive (10-15 minutes)

The interviewer will pick an area to explore. Common deep dives:

### Example: "Tell me more about the fan-out"

```
"Great question. For fan-out, I'd use a hybrid approach:

FOR NORMAL USERS (< 10K followers):
- Fan-out on write
- When they tweet, push tweet_id to all followers' caches
- Timeline reads are fast (pre-computed)

FOR CELEBRITIES (> 10K followers):
- Fan-out on read
- Don't push to followers' caches
- Merge celebrity tweets at read time

WHY HYBRID:
- Pure push: Celebrities would cause massive write amplification
- Pure pull: Slow reads for users following many people
- Hybrid: Best of both worlds

IMPLEMENTATION:
- Tweet creation triggers Kafka event
- Fan-out workers consume events
- Check follower count to decide push vs skip
- Timeline service merges at read time"
```

### How to Handle Deep Dives

1. **Explain your thought process**: "I'm considering two approaches..."
2. **Discuss trade-offs**: "The downside of this approach is..."
3. **Be specific**: Use concrete numbers and technologies
4. **Ask if you should go deeper**: "Should I dive into X?"

---

## Phase 4: Wrap-up (5 minutes)

### Summarize Your Design

```
"To summarize:
- We designed a Twitter-like system for 500M users
- Key components: Tweet Service, Timeline Service, Fan-out
- Used hybrid fan-out for scalability
- Redis for timeline caching
- Cassandra for tweet storage"
```

### Discuss Bottlenecks

```
"Potential bottlenecks:
1. Hot celebrities - mitigated by pull-based fan-out
2. Timeline cache size - use LRU eviction
3. Database writes at scale - sharding by user_id"
```

### Mention Future Improvements

```
"If I had more time, I'd add:
- Search functionality with Elasticsearch
- Trending topics with stream processing
- Direct messaging
- Analytics pipeline"
```

---

## The Interviewer's Perspective

### What They're Evaluating

```
┌────────────────────────────────────────────────────────────────┐
│                  EVALUATION CRITERIA                            │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROBLEM SOLVING (25%)                                         │
│  ├── Asked good clarifying questions                           │
│  ├── Broke down problem systematically                         │
│  └── Handled ambiguity well                                    │
│                                                                 │
│  TECHNICAL DESIGN (35%)                                        │
│  ├── Reasonable architecture                                   │
│  ├── Correct capacity estimation                               │
│  ├── Appropriate technology choices                            │
│  └── Addressed scalability                                     │
│                                                                 │
│  TRADE-OFF ANALYSIS (20%)                                      │
│  ├── Identified trade-offs                                     │
│  ├── Justified decisions                                       │
│  └── Knew alternatives                                         │
│                                                                 │
│  COMMUNICATION (20%)                                           │
│  ├── Clear explanation                                         │
│  ├── Good use of diagrams                                      │
│  ├── Organized approach                                        │
│  └── Responded to feedback                                     │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### Signals That Impress

- Asking about use cases before requirements
- Doing capacity estimation without being asked
- Proactively discussing failure scenarios
- Mentioning monitoring and observability
- Acknowledging limitations of your design

### Signals That Concern

- Jumping to solution immediately
- Not asking any clarifying questions
- Over-engineering simple problems
- Ignoring interviewer's hints
- Unable to explain trade-offs

---

## Key Takeaways

```
┌────────────────────────────────────────────────────────────────┐
│                    INTERVIEW FLOW SUMMARY                       │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. REQUIREMENTS (5-7 min)                                     │
│     └── Ask questions, define scope, write it down             │
│                                                                 │
│  2. HIGH-LEVEL DESIGN (15-20 min)                              │
│     └── Estimation → API → Data Model → Architecture           │
│                                                                 │
│  3. DEEP DIVE (10-15 min)                                      │
│     └── Follow interviewer's lead, explain trade-offs          │
│                                                                 │
│  4. WRAP-UP (5 min)                                            │
│     └── Summarize, bottlenecks, improvements                   │
│                                                                 │
│  REMEMBER:                                                     │
│  - You drive the interview                                     │
│  - Think out loud constantly                                   │
│  - Trade-offs are more important than "right" answers          │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

*Next: [Time Strategies](02_time_strategies.md) →*
