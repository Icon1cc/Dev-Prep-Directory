# Red Flags: What Interviewers Watch For

Avoid these common mistakes that signal "no hire" to interviewers.

---

## Critical Red Flags

### 1. Jumping to Solution Without Requirements

```
┌────────────────────────────────────────────────────────────────┐
│                      RED FLAG #1                                │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Interviewer: "Design a URL shortener"                         │
│                                                                 │
│  BAD:                                                          │
│  "Okay, so we'll have a load balancer, then some API          │
│   servers, then a database. We'll use base62 encoding..."     │
│                                                                 │
│  [Jumps straight to solution without asking anything]          │
│                                                                 │
│  WHY IT'S BAD:                                                 │
│  - Shows inability to gather requirements                      │
│  - May solve the wrong problem                                 │
│  - Misses chance to scope appropriately                        │
│                                                                 │
│  GOOD:                                                         │
│  "Before I start designing, I have a few questions:           │
│   - What's our expected scale?                                 │
│   - Do we need custom short URLs?                              │
│   - What's the read/write ratio we expect?"                   │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

### 2. Not Handling Ambiguity

```
┌────────────────────────────────────────────────────────────────┐
│                      RED FLAG #2                                │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Interviewer: "Design a messaging system"                      │
│                                                                 │
│  BAD:                                                          │
│  "What kind of messaging system? Like email? Or chat?         │
│   I need more details before I can start."                    │
│                                                                 │
│  [Waits for interviewer to provide everything]                 │
│                                                                 │
│  WHY IT'S BAD:                                                 │
│  - Shows inability to drive conversation                       │
│  - Real world problems are ambiguous                          │
│  - Waiting to be spoon-fed                                    │
│                                                                 │
│  GOOD:                                                         │
│  "I'll clarify a few things. For messaging, I'm thinking      │
│   real-time chat like WhatsApp. Should I design for that,     │
│   or did you have something else in mind?                     │
│                                                                 │
│   I'll assume we need: 1-1 chat, group chat, read receipts.   │
│   Does this scope sound right?"                                │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

### 3. Ignoring Scale

```
┌────────────────────────────────────────────────────────────────┐
│                      RED FLAG #3                                │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BAD DESIGN:                                                   │
│  "We'll have one server running our app and one database."    │
│                                                                 │
│  Interviewer: "What if we have 100 million users?"            │
│                                                                 │
│  BAD RESPONSE:                                                 │
│  "Oh... I guess we'd add more servers?"                       │
│                                                                 │
│  WHY IT'S BAD:                                                 │
│  - System design is ABOUT scale                               │
│  - Shows lack of distributed systems thinking                 │
│  - Basic architecture without scaling plan                    │
│                                                                 │
│  GOOD APPROACH:                                                │
│  "Given our 100M users and 10K QPS, we'll need:              │
│   - Load balancer to distribute traffic                       │
│   - Multiple API server instances (auto-scaling)              │
│   - Database sharding by user_id                              │
│   - Caching layer to reduce DB load                          │
│   Here's how data flows at scale..."                          │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

### 4. Single Point of Failure

```
┌────────────────────────────────────────────────────────────────┐
│                      RED FLAG #4                                │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BAD DESIGN:                                                   │
│                                                                 │
│  Users ──► Single Server ──► Single Database                  │
│                                                                 │
│  WHY IT'S BAD:                                                 │
│  - Server dies = entire system down                           │
│  - Database dies = data potentially lost                      │
│  - No redundancy = unacceptable for production               │
│                                                                 │
│  GOOD DESIGN:                                                  │
│                                                                 │
│  Users ──► Load Balancer ──┬──► Server 1 ──┐                  │
│                            ├──► Server 2 ──┼──► DB Primary    │
│                            └──► Server 3 ──┘        │         │
│                                                     ▼         │
│                                               DB Replica      │
│                                                               │
│  "Every component has redundancy. If any single              │
│   node fails, the system continues operating."               │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

### 5. No Trade-off Discussion

```
┌────────────────────────────────────────────────────────────────┐
│                      RED FLAG #5                                │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BAD:                                                          │
│  "We'll use Cassandra for the database."                      │
│  [No explanation of why or alternatives]                       │
│                                                                 │
│  WHY IT'S BAD:                                                 │
│  - Every decision has trade-offs                              │
│  - Shows shallow understanding                                 │
│  - Sounds like memorized solution                             │
│                                                                 │
│  GOOD:                                                         │
│  "For the database, I'm considering SQL vs NoSQL.             │
│                                                                 │
│   SQL (PostgreSQL):                                            │
│   + Strong consistency, ACID transactions                     │
│   - Harder to scale horizontally                              │
│                                                                 │
│   NoSQL (Cassandra):                                           │
│   + Excellent write scalability, high availability            │
│   - Eventual consistency, limited query patterns              │
│                                                                 │
│   Given our write-heavy workload and need for availability,   │
│   I'll go with Cassandra. The trade-off is we'll need to     │
│   design for eventual consistency."                           │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

### 6. Over-Engineering

```
┌────────────────────────────────────────────────────────────────┐
│                      RED FLAG #6                                │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Problem: "Design a URL shortener for a startup MVP"          │
│                                                                 │
│  BAD (Over-engineered):                                        │
│  "We'll need Kubernetes for orchestration, a service mesh     │
│   with Istio, multi-region deployment with global load        │
│   balancing, a data lake for analytics, machine learning      │
│   for spam detection, blockchain for URL verification..."     │
│                                                                 │
│  WHY IT'S BAD:                                                 │
│  - Doesn't match requirements (MVP = simple)                  │
│  - Shows poor judgment                                         │
│  - Overcomplicates needlessly                                  │
│                                                                 │
│  GOOD:                                                         │
│  "For an MVP, I'll keep it simple:                            │
│   - Single API service (can scale later)                      │
│   - PostgreSQL database                                        │
│   - Redis cache for hot URLs                                   │
│                                                                 │
│   This handles our initial scale. When we grow, we can add   │
│   [specific scaling measures]."                               │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

### 7. Not Listening to Hints

```
┌────────────────────────────────────────────────────────────────┐
│                      RED FLAG #7                                │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Interviewer: "What about the consistency model here?"        │
│                                                                 │
│  BAD:                                                          │
│  "Yeah, consistency. Anyway, moving on to the cache..."       │
│  [Ignores the hint completely]                                 │
│                                                                 │
│  WHY IT'S BAD:                                                 │
│  - Interviewer is trying to HELP you                          │
│  - Shows poor listening skills                                 │
│  - Misses chance to demonstrate knowledge                     │
│                                                                 │
│  GOOD:                                                         │
│  "Great point—I should address consistency.                   │
│                                                                 │
│   In this design, we have replication between database        │
│   nodes. I'd use asynchronous replication for performance,    │
│   which means we'll have eventual consistency.                │
│                                                                 │
│   For most read operations, that's acceptable. For critical   │
│   operations like account creation, I'd use synchronous       │
│   replication to ensure strong consistency.                   │
│                                                                 │
│   Is that the aspect you wanted me to explore?"               │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

### 8. Getting Defensive

```
┌────────────────────────────────────────────────────────────────┐
│                      RED FLAG #8                                │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Interviewer: "I'm not sure this approach will scale."        │
│                                                                 │
│  BAD:                                                          │
│  "Yes it will. This is how Netflix does it."                  │
│  [Defensive, dismissive]                                       │
│                                                                 │
│  WHY IT'S BAD:                                                 │
│  - Shows poor collaboration skills                            │
│  - Misses learning opportunity                                 │
│  - Red flag for team fit                                      │
│                                                                 │
│  GOOD:                                                         │
│  "That's a valid concern. Let me think about it...            │
│                                                                 │
│   At 10x our current scale, this component would need to      │
│   handle 100K requests/second. You're right, that could be    │
│   a bottleneck.                                                │
│                                                                 │
│   We could address this by:                                    │
│   1. Adding a caching layer here                              │
│   2. Sharding this database                                    │
│   3. Using async processing for non-critical paths            │
│                                                                 │
│   Would one of these address your concern?"                   │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Red Flag Summary Table

| Red Flag | What It Signals | How to Avoid |
|----------|----------------|--------------|
| No requirements gathering | Can't scope problems | Ask 3-5 questions first |
| Waiting for details | Can't handle ambiguity | Make assumptions, verify |
| Ignoring scale | Lacks distributed knowledge | Always discuss scale |
| Single points of failure | Doesn't think about reliability | Add redundancy |
| No trade-offs | Shallow understanding | Discuss alternatives |
| Over-engineering | Poor judgment | Match complexity to requirements |
| Ignoring hints | Poor listening | Thank and address hints |
| Getting defensive | Hard to work with | Stay curious and open |

---

## Self-Check Questions

Before your interview, ask yourself:

```
□ Did I ask clarifying questions before designing?
□ Did I estimate capacity and use it in my design?
□ Does every component have redundancy?
□ Did I discuss trade-offs for major decisions?
□ Is my design appropriate for the scale mentioned?
□ Did I respond positively to feedback?
□ Did I think about failure scenarios?
```

---

*Next: [Answer Template](05_answer_template.md) →*
