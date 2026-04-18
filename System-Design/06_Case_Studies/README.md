# Case Studies

> "The best way to learn system design is to study real systems."

This section contains complete, interview-style system designs for popular applications. Each case study follows the exact format you'd use in a FAANG system design interview.

## What You'll Learn

```
┌─────────────────────────────────────────────────────────────────┐
│                      CASE STUDIES                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  01. URL Shortener (TinyURL)                                    │
│      └── Entry-level classic, great for learning the process   │
│                                                                  │
│  02. Twitter/X Timeline                                          │
│      └── Fan-out problem, caching at scale                      │
│                                                                  │
│  03. WhatsApp Chat System                                       │
│      └── Real-time messaging, presence, delivery receipts       │
│                                                                  │
│  04. Netflix Streaming                                          │
│      └── Video delivery, CDN, adaptive streaming                │
│                                                                  │
│  05. Uber Ride Matching                                         │
│      └── Geospatial indexing, real-time matching                │
│                                                                  │
│  06. News Feed System                                           │
│      └── Ranking, personalization, infinite scroll              │
│                                                                  │
│  07. Google Drive (Distributed Storage)                         │
│      └── File sync, conflict resolution, sharing                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Case Study Format

Each case study follows this interview-proven structure:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CASE STUDY STRUCTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. PROBLEM STATEMENT                                           │
│     └── What are we building? Clear scope definition            │
│                                                                  │
│  2. REQUIREMENTS                                                │
│     ├── Functional: What the system does                        │
│     └── Non-functional: Scale, latency, availability            │
│                                                                  │
│  3. CAPACITY ESTIMATION                                         │
│     └── Math for storage, bandwidth, QPS                        │
│                                                                  │
│  4. HIGH-LEVEL ARCHITECTURE                                     │
│     └── Component diagram showing major pieces                  │
│                                                                  │
│  5. API DESIGN                                                  │
│     └── Key endpoints and contracts                             │
│                                                                  │
│  6. DATA MODEL                                                  │
│     └── Database schema and storage choices                     │
│                                                                  │
│  7. COMPONENT DEEP DIVE                                         │
│     └── Detailed design of critical components                  │
│                                                                  │
│  8. SCALING & BOTTLENECKS                                       │
│     └── How to handle growth, identify limits                   │
│                                                                  │
│  9. TRADE-OFFS                                                  │
│     └── Decisions made and alternatives                         │
│                                                                  │
│  10. FOLLOW-UP QUESTIONS                                        │
│      └── What interviewers might ask next                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Study Order

### Beginner (Start Here)
1. **URL Shortener** - Learn the framework
2. **News Feed** - Understand fan-out

### Intermediate
3. **Twitter Timeline** - Complex caching
4. **WhatsApp** - Real-time systems

### Advanced
5. **Netflix** - Content delivery
6. **Uber** - Geospatial systems
7. **Google Drive** - Distributed storage

## How to Use These Case Studies

### For Learning
1. Read the problem statement
2. Try designing it yourself first (30-45 min)
3. Compare with the solution
4. Note what you missed
5. Practice explaining it out loud

### For Interview Prep
1. Time yourself (45 min)
2. Draw diagrams on paper
3. Practice talking through trade-offs
4. Have someone ask follow-up questions

## Interview Evaluation Criteria

```
┌─────────────────────────────────────────────────────────────────┐
│              WHAT INTERVIEWERS LOOK FOR                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  REQUIREMENTS (15%)                                             │
│  ├── Asked clarifying questions                                 │
│  ├── Identified functional requirements                         │
│  └── Considered non-functional requirements                     │
│                                                                  │
│  HIGH-LEVEL DESIGN (25%)                                        │
│  ├── Reasonable component breakdown                             │
│  ├── Correct data flow                                          │
│  └── Identified major challenges                                │
│                                                                  │
│  DETAILED DESIGN (30%)                                          │
│  ├── Dove deep on critical components                           │
│  ├── Made reasonable technology choices                         │
│  └── Addressed edge cases                                       │
│                                                                  │
│  TRADE-OFFS & ALTERNATIVES (20%)                                │
│  ├── Discussed pros/cons of decisions                           │
│  ├── Knew alternative approaches                                │
│  └── Justified choices                                          │
│                                                                  │
│  COMMUNICATION (10%)                                            │
│  ├── Clear explanation                                          │
│  ├── Organized approach                                         │
│  └── Responded well to feedback                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Common Mistakes to Avoid

| Mistake | Why It's Bad | What to Do Instead |
|---------|--------------|-------------------|
| Jumping into solution | Missed requirements | Ask questions first |
| No capacity estimation | Can't make informed decisions | Do back-of-envelope math |
| Single point of failure | System isn't reliable | Add redundancy |
| Ignoring trade-offs | Seems like you don't understand | Discuss alternatives |
| Going too deep too early | Run out of time | Cover breadth first |

---

## Quick Reference: Key Numbers

| Metric | Value | Context |
|--------|-------|---------|
| 1 day | 86,400 seconds | Time calculations |
| 1 month | ~2.5 million seconds | Storage planning |
| 1 year | ~31 million seconds | Long-term planning |
| 1 KB | 1,000 bytes | Text, small records |
| 1 MB | 1,000 KB | Images, small files |
| 1 GB | 1,000 MB | Videos, databases |
| 1 TB | 1,000 GB | Large databases |
| 1 PB | 1,000 TB | Big data, archives |

### Latency Numbers

| Operation | Time |
|-----------|------|
| L1 cache | 0.5 ns |
| L2 cache | 7 ns |
| RAM | 100 ns |
| SSD random read | 150 μs |
| HDD random read | 10 ms |
| Same datacenter RTT | 0.5 ms |
| Cross-region RTT | 150 ms |

---

**Ready? Start with the [URL Shortener](01_url_shortener.md) case study.**
