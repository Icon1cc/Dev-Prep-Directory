# Strong Answer Template

A proven framework for structuring your system design answers.

---

## The RESHADED Framework

```
┌────────────────────────────────────────────────────────────────┐
│                    RESHADED FRAMEWORK                           │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  R - Requirements      Define what we're building              │
│  E - Estimation        Back-of-envelope math                   │
│  S - Storage           Data model and database choice          │
│  H - High-level        Architecture diagram                    │
│  A - API               Key endpoints                           │
│  D - Detailed          Deep dive on components                 │
│  E - Evaluate          Trade-offs and alternatives             │
│  D - Discuss           Bottlenecks and improvements            │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Template

### Step 1: Requirements (3-5 minutes)

```
TEMPLATE:

"Let me start by clarifying the requirements.

CLARIFYING QUESTIONS:
1. [Scope question] - What are the core features?
2. [Scale question] - How many users/requests?
3. [Priority question] - Availability vs consistency?
4. [Constraint question] - Any latency requirements?

Based on this, here are the requirements:

FUNCTIONAL REQUIREMENTS:
1. [Feature 1]
2. [Feature 2]
3. [Feature 3]

NON-FUNCTIONAL REQUIREMENTS:
1. Scale: [X users, Y requests/sec]
2. Latency: [< Z ms]
3. Availability: [99.X%]

Let me write these down so we can reference them."
```

**Example (Twitter):**
```
"FUNCTIONAL: Users can post tweets, follow users, view timeline
NON-FUNCTIONAL: 500M users, 200M DAU, <200ms latency, 99.9% uptime"
```

---

### Step 2: Estimation (2-5 minutes)

```
TEMPLATE:

"Let me do some quick capacity estimation.

TRAFFIC:
- [X] users × [Y] actions/day = [Z] total/day
- [Z] / 86,400 seconds = [W] requests/second
- Peak (3x): [W × 3] requests/second

STORAGE:
- Each [entity] = ~[X] bytes
- [Y] entities/day × [X] bytes = [Z] GB/day
- [N] years: [Z × 365 × N] = [Total] TB

BANDWIDTH:
- [Calculation based on traffic and data size]

These numbers will inform our design decisions."
```

**Example (Twitter):**
```
"TRAFFIC: 400M tweets/day = 5K tweets/second, 50K reads/second
STORAGE: 400M × 500 bytes = 200GB/day, ~70TB/year
This tells me we need a distributed database and heavy caching."
```

---

### Step 3: API Design (2-3 minutes)

```
TEMPLATE:

"Here are the key APIs:

[Primary operation]:
  [METHOD] [endpoint]
  Request: { [fields] }
  Response: { [fields] }

[Secondary operation]:
  [METHOD] [endpoint]
  Request: { [fields] }
  Response: { [fields] }

[Tertiary operation]:
  [METHOD] [endpoint]
  ..."
```

**Example (Twitter):**
```
"POST /tweets        - Create tweet, returns tweet_id
GET  /timeline       - Get home timeline, paginated
POST /follow/{id}    - Follow a user
GET  /users/{id}     - Get user profile"
```

---

### Step 4: Data Model (2-3 minutes)

```
TEMPLATE:

"The main entities are:

[Entity 1]: [key fields]
[Entity 2]: [key fields]
[Entity 3]: [key fields]

For storage, I'll use [database] because:
- [Reason 1]
- [Reason 2]

The trade-off is [downside], which is acceptable because [reason]."
```

**Example (Twitter):**
```
"USERS: user_id, username, email, follower_count
TWEETS: tweet_id, user_id, content, created_at, media_urls
FOLLOWS: follower_id, followee_id, created_at

I'll use Cassandra for tweets (write-heavy, time-series)
and PostgreSQL for users (relational, less scale-critical)."
```

---

### Step 5: High-Level Design (5-7 minutes)

```
TEMPLATE:

"Let me draw the high-level architecture.

[Draw while explaining]

'Starting from the client:
1. Requests go through [Load Balancer] for distribution
2. [Service A] handles [responsibility]
3. [Service B] handles [responsibility]
4. Data is stored in [Database]
5. [Cache] sits in front for [reason]
6. [Queue] decouples [X] from [Y]

Here's how the main flow works:
[Walk through primary use case on diagram]'"
```

---

### Step 6: Deep Dive (10-15 minutes)

```
TEMPLATE:

"Let me dive deeper into [component].

THE CHALLENGE:
[Explain the specific problem]

OPTIONS CONSIDERED:
1. [Option A]: [pros/cons]
2. [Option B]: [pros/cons]

MY CHOICE: [Option X] because [reasons]

IMPLEMENTATION DETAILS:
- [Detail 1]
- [Detail 2]
- [Detail 3]

EDGE CASES:
- [Edge case 1] → [How we handle it]
- [Edge case 2] → [How we handle it]"
```

---

### Step 7: Trade-offs & Alternatives (2-3 minutes)

```
TEMPLATE:

"Let me summarize the key trade-offs in this design:

1. [Decision 1]:
   - We chose: [Choice]
   - Trade-off: [What we gave up]
   - Alternative: [What we could have done]
   - Why this choice: [Justification]

2. [Decision 2]:
   ...

If our requirements were different (e.g., [scenario]),
I would change [X] to [Y]."
```

---

### Step 8: Wrap-up (2-3 minutes)

```
TEMPLATE:

"To summarize the design:

KEY COMPONENTS:
- [Component 1]: [Purpose]
- [Component 2]: [Purpose]
- [Component 3]: [Purpose]

POTENTIAL BOTTLENECKS:
- [Bottleneck 1]: Would address by [solution]
- [Bottleneck 2]: Would address by [solution]

FUTURE IMPROVEMENTS:
- [Improvement 1]
- [Improvement 2]

Any questions about the design?"
```

---

## Complete Example: URL Shortener

```
┌────────────────────────────────────────────────────────────────┐
│                   URL SHORTENER - FULL ANSWER                   │
├────────────────────────────────────────────────────────────────┤

1. REQUIREMENTS (3 min)
───────────────────────
"Let me clarify: What's our scale? Do we need custom URLs?
Analytics? Expiration?

Functional: Shorten URLs, redirect, optional custom alias
Non-functional: 100M URLs/month, <100ms redirect, 99.9% uptime"

2. ESTIMATION (2 min)
─────────────────────
"100M URLs/month = 40 URLs/second writes
100:1 read ratio = 4,000 redirects/second
Storage: 100M × 500 bytes = 50GB/month, 3TB for 5 years"

3. API (1 min)
──────────────
"POST /urls - create short URL
GET /{code} - redirect to long URL"

4. DATA MODEL (2 min)
─────────────────────
"urls: short_code (PK), long_url, created_at, expires_at
Using key-value store (DynamoDB) - simple lookups, scales well"

5. HIGH-LEVEL DESIGN (5 min)
────────────────────────────
[Draw architecture]
"LB → API Servers → Cache (Redis) → Database
Short code generation via counter service with range allocation"

6. DEEP DIVE: Code Generation (8 min)
─────────────────────────────────────
"Challenge: Generate unique 7-char codes without collision

Options:
- Random: Risk collisions, need uniqueness check
- Hash: Collisions possible, deterministic
- Counter + Base62: No collisions, predictable

Choice: Counter with range allocation
- Zookeeper assigns ranges to servers
- Each server generates from its range
- Base62 encode: 62^7 = 3.5 trillion codes"

7. TRADE-OFFS (2 min)
─────────────────────
"Chose NoSQL over SQL: Better for simple key-value, scales easier
Trade-off: No complex queries, but we don't need them

Chose counter over hash: More predictable, no collision handling
Trade-off: Requires coordination service"

8. WRAP-UP (2 min)
──────────────────
"Summary: Counter-based generation, Redis cache, DynamoDB storage
Bottleneck: Counter service - mitigate with large ranges
Future: Analytics pipeline, abuse detection"

└────────────────────────────────────────────────────────────────┘
```

---

## Checklist Before Moving to Next Step

```
□ REQUIREMENTS: Did I write them down? Did interviewer confirm?
□ ESTIMATION: Did I show my math? Did I use the numbers?
□ API: Did I cover the main operations?
□ DATA MODEL: Did I explain database choice?
□ ARCHITECTURE: Is the diagram clear? Did I explain data flow?
□ DEEP DIVE: Did I discuss trade-offs? Edge cases?
□ WRAP-UP: Did I mention bottlenecks and improvements?
```

---

*Next: [Weak vs Strong Answers](06_weak_vs_strong.md) →*
