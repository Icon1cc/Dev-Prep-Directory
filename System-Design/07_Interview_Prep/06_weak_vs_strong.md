# Weak vs Strong Answers

Side-by-side comparisons showing what separates passing from failing answers.

---

## Example 1: Requirements Phase

**Question: "Design a chat application"**

### Weak Answer ❌

```
"Okay, so for a chat app we need to send messages. I'll start
with the architecture. We'll have some servers and a database..."

[Immediately jumps to solution]
```

**Why it's weak:**
- No clarifying questions
- Didn't define scope
- May design wrong thing

### Strong Answer ✓

```
"Before I start, I'd like to clarify a few things:

1. Is this 1-on-1 chat, group chat, or both?
2. What's our expected scale - users and messages per day?
3. Do we need features like read receipts and typing indicators?
4. Is message history persistence required? How long?
5. Mobile, web, or both?

[Waits for answers]

Based on your responses, let me define the requirements:

FUNCTIONAL:
- 1-on-1 and group chat (up to 100 members)
- Text messages with image/file sharing
- Read receipts and online status
- Message history (90 days retention)

NON-FUNCTIONAL:
- 50M DAU, 1B messages/day
- < 100ms message delivery
- 99.99% availability
- Messages must be delivered in order

Does this capture what we need?"
```

**Why it's strong:**
- Clarifies scope before designing
- Prioritizes requirements
- Gets interviewer buy-in

---

## Example 2: Capacity Estimation

**Question: "Design Twitter"**

### Weak Answer ❌

```
"Twitter has lots of users, so we'll need to scale. Let's use
some big servers and a distributed database."
```

**Why it's weak:**
- No actual numbers
- Vague "lots of users"
- Can't make informed decisions

### Strong Answer ✓

```
"Let me estimate the capacity we'll need.

USERS:
- 500M total users, 200M daily active
- Average user follows 200 accounts

TWEETS:
- 200M DAU × 2 tweets/day = 400M tweets/day
- 400M / 86,400 = ~5,000 tweets/second
- Peak (3x average) = 15,000 tweets/second

TIMELINE READS:
- 200M DAU × 10 timeline views/day = 2B reads/day
- 2B / 86,400 = ~25,000 reads/second
- This is 5:1 read-to-write ratio

STORAGE:
- Tweet: 280 chars + metadata ≈ 500 bytes
- 400M tweets × 500 bytes = 200 GB/day
- 5 years: 200 GB × 365 × 5 = ~350 TB

This tells me:
1. We're read-heavy → need caching
2. High write volume → need to handle fan-out efficiently
3. Large storage → need distributed database"
```

**Why it's strong:**
- Concrete numbers
- Shows calculation process
- Uses numbers to inform design decisions

---

## Example 3: Architecture Explanation

**Question: "Walk me through your architecture"**

### Weak Answer ❌

```
"So here's a load balancer, and these are the servers,
and this is the database. The servers talk to the database."

[Points at boxes without explanation]
```

**Why it's weak:**
- No explanation of WHY
- Doesn't describe data flow
- Anyone could draw boxes

### Strong Answer ✓

```
"Let me walk through the architecture, explaining each component:

[Points to diagram while speaking]

STARTING WITH THE CLIENT:
User requests hit our load balancer first. I'm using an L7
load balancer because we need to route based on URL paths -
reads go to read replicas, writes to primary.

API LAYER:
These stateless API servers handle request validation and
routing. They're stateless so we can auto-scale easily.
I'd run 10-20 instances based on our 25K QPS.

CACHING LAYER:
Before hitting the database, we check Redis. With our 5:1
read-write ratio, I expect 80%+ cache hit rate. This reduces
database load from 25K to ~5K QPS.

DATABASE:
I'm using Cassandra because:
- Write-heavy workload (5K tweets/sec)
- Need horizontal scaling
- Time-series nature of tweets

The data flows like this:
1. User posts tweet → API server
2. API validates → writes to Cassandra
3. Triggers async job to Kafka
4. Fan-out workers push to followers' timeline caches
5. User reads timeline → API checks cache → returns tweets"
```

**Why it's strong:**
- Explains WHY each component exists
- Connects to capacity numbers
- Describes complete data flow

---

## Example 4: Handling Deep Dive

**Interviewer: "Tell me more about how you'd handle the fan-out"**

### Weak Answer ❌

```
"We'd push the tweet to all followers. We could use a
message queue for that."
```

**Why it's weak:**
- Surface-level only
- No discussion of challenges
- No trade-offs

### Strong Answer ✓

```
"Fan-out is the core challenge here. Let me break it down.

THE PROBLEM:
When a user with 10M followers tweets, we need to update
10M timeline caches. Doing this synchronously would:
- Take too long (seconds)
- Block the API response
- Create hot spots in our system

MY APPROACH - HYBRID FAN-OUT:

For normal users (< 10K followers):
- Fan-out on WRITE
- When they tweet, push tweet_id to followers' caches
- This is fast because followers count is small
- Timeline reads are O(1) - just read the cache

For celebrities (> 10K followers):
- Fan-out on READ
- Store tweet, but don't push to followers
- When follower loads timeline, merge celebrity tweets in
- Avoids massive write amplification

IMPLEMENTATION:
1. Tweet comes in → save to Tweet DB
2. Check user's follower count
3. If < 10K: Send to Kafka fan-out topic
4. Fan-out workers (100+ instances) process in parallel
5. Each worker: get follower batch, update their Redis caches
6. For celebrities: maintain a separate 'celebrity tweets' cache

TRADE-OFFS:
- Pro: Scales for celebrities without massive write cost
- Con: Timeline read is slightly more complex (merge step)
- Con: Celebrity tweets may have slight delay for followers

I'd also implement batching in the fan-out workers to reduce
Redis round trips - update 100 follower caches per batch."
```

**Why it's strong:**
- Identifies the core challenge
- Discusses multiple approaches
- Explains trade-offs
- Goes into implementation details

---

## Example 5: Handling Unknown Questions

**Interviewer: "How would you implement end-to-end encryption?"**

### Weak Answer ❌

```
"I'm not really sure about encryption. We could use SSL?"
```

**Why it's weak:**
- Gives up immediately
- Confuses transport encryption with E2E
- Doesn't try to reason through it

### Strong Answer ✓

```
"I haven't implemented E2E encryption directly, but let me
reason through how I'd approach it.

MY UNDERSTANDING:
End-to-end encryption means only the communicating users can
read messages - not even our servers. This is different from
transport encryption (HTTPS), which protects data in transit
but allows servers to read it.

HOW I'D APPROACH IT:

Key Exchange:
- Each user generates a public/private key pair
- Public keys are stored on our servers
- Private keys stay on user's device only

Message Flow:
1. Sender fetches recipient's public key
2. Encrypts message with recipient's public key
3. Sends encrypted blob to server
4. Server stores/relays encrypted blob
5. Recipient decrypts with their private key

CHALLENGES I'D NEED TO SOLVE:
- Multi-device support (how to share private keys securely?)
- Group chats (key management for multiple recipients)
- Key rotation when user gets new device
- Backup/restore of message history

I'd want to research Signal Protocol, which WhatsApp uses,
for a proven approach to these challenges.

Does this align with what you were looking for?"
```

**Why it's strong:**
- Honest about knowledge limits
- Reasons from first principles
- Shows problem-solving process
- Acknowledges gaps

---

## Quick Comparison Table

| Aspect | Weak Answer | Strong Answer |
|--------|-------------|---------------|
| Requirements | Skips or asks 1 question | 4-5 targeted questions |
| Estimation | "Lots of data" | Concrete numbers + math |
| Architecture | Lists components | Explains WHY + data flow |
| Deep dive | Surface level | Trade-offs + implementation |
| Unknown topics | "I don't know" | Reason from principles |
| Trade-offs | None mentioned | For every major decision |

---

## Key Insight

```
┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│  WEAK ANSWERS describe WHAT the system looks like              │
│                                                                 │
│  STRONG ANSWERS explain WHY it's designed that way             │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

*Next: [Question Bank](07_question_bank.md) →*
