# Must-Read Books for System Design

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     ESSENTIAL BOOKS                                           ║
║              Curated Reading List for System Design Mastery                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Tier 1: Essential (Must Read)

### Designing Data-Intensive Applications (DDIA)
**Author**: Martin Kleppmann
**Why It's Essential**: The bible of system design. Covers everything from storage engines to distributed systems with incredible depth and clarity.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  DDIA READING GUIDE                                                          │
│                                                                              │
│  Part 1: Foundations of Data Systems (Interview Critical)                   │
│  ├── Ch 1: Reliable, Scalable, Maintainable Applications                   │
│  ├── Ch 2: Data Models and Query Languages                                 │
│  ├── Ch 3: Storage and Retrieval ⭐                                        │
│  └── Ch 4: Encoding and Evolution                                          │
│                                                                              │
│  Part 2: Distributed Data (Interview Critical)                              │
│  ├── Ch 5: Replication ⭐⭐                                                 │
│  ├── Ch 6: Partitioning ⭐⭐                                                │
│  ├── Ch 7: Transactions ⭐                                                  │
│  ├── Ch 8: Trouble with Distributed Systems ⭐                             │
│  └── Ch 9: Consistency and Consensus ⭐⭐                                   │
│                                                                              │
│  Part 3: Derived Data (Good to Know)                                        │
│  ├── Ch 10: Batch Processing                                                │
│  ├── Ch 11: Stream Processing                                               │
│  └── Ch 12: Future of Data Systems                                          │
│                                                                              │
│  ⭐ = High interview relevance                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Time Investment**: 4-6 weeks (thorough), 2 weeks (chapters 1-9)
**Best For**: Everyone preparing for system design interviews

---

### System Design Interview (Alex Xu) - Volume 1 & 2
**Author**: Alex Xu
**Why It's Essential**: Interview-focused with real design problems. Great for understanding what interviewers expect.

**Volume 1 Covers**:
- Rate limiter, URL shortener
- Web crawler, notification system
- News feed, chat system
- Search autocomplete

**Volume 2 Covers**:
- Payment system, hotel reservation
- Proximity service, nearby friends
- Google Maps, distributed message queue
- S3-like object storage

**Time Investment**: 1-2 weeks per volume
**Best For**: Interview preparation, structured approach

---

## Tier 2: Highly Recommended

### Web Scalability for Startup Engineers
**Author**: Artur Ejsmont
**Why Read It**: Practical, covers the journey from single server to distributed system. Great for understanding the "why" behind scaling decisions.

**Key Chapters**:
- Principles of good software design
- Front-end layer (DNS, CDN, load balancers)
- Web services layer
- Data layer (caching, databases)
- Searching and logging

**Time Investment**: 1-2 weeks
**Best For**: Developers building scalable systems

---

### Building Microservices (2nd Edition)
**Author**: Sam Newman
**Why Read It**: Definitive guide on microservices architecture, deployment, and operations.

**Key Topics**:
- Microservices decomposition
- Communication patterns
- Security, testing, monitoring
- Deployment strategies

**Time Investment**: 2-3 weeks
**Best For**: Understanding microservices trade-offs

---

### Database Internals
**Author**: Alex Petrov
**Why Read It**: Deep dive into how databases work internally. Essential for understanding performance characteristics.

**Key Topics**:
- B-Trees and LSM-Trees
- Transaction processing
- Distributed systems components
- Consensus algorithms

**Time Investment**: 3-4 weeks
**Best For**: Senior roles, database-heavy systems

---

## Tier 3: Specialized Topics

### Kafka: The Definitive Guide (2nd Edition)
**Authors**: Gwen Shapira, Todd Palino, Rajini Sivaram, Krit Petty
**Focus**: Message queues, event streaming, real-time data pipelines

**Time Investment**: 2 weeks
**Best For**: Event-driven architectures

---

### Redis in Action
**Author**: Josiah Carlson
**Focus**: Caching patterns, data structures, use cases

**Time Investment**: 1-2 weeks
**Best For**: Understanding caching deeply

---

### Site Reliability Engineering (SRE Book)
**Authors**: Google SRE Team
**Focus**: Operations, reliability, incident response

**Available Free**: https://sre.google/sre-book/table-of-contents/

**Time Investment**: Selective reading (2-3 chapters)
**Best For**: Operations focus, senior roles

---

### Clean Architecture
**Author**: Robert C. Martin
**Focus**: Software architecture principles, dependency management

**Time Investment**: 1-2 weeks
**Best For**: Low-level design, code architecture

---

## Reading Priority Guide

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    READING PRIORITY BY GOAL                                  │
│                                                                              │
│  INTERVIEW PREP (4 weeks):                                                  │
│  ────────────────────────                                                   │
│  1. Alex Xu Vol 1 (1 week)                                                 │
│  2. DDIA Chapters 1-9 (2 weeks)                                            │
│  3. Alex Xu Vol 2 (1 week)                                                 │
│                                                                              │
│  DEEP LEARNING (3 months):                                                  │
│  ─────────────────────────                                                  │
│  1. DDIA full book (6 weeks)                                               │
│  2. Building Microservices (2 weeks)                                       │
│  3. Database Internals (3 weeks)                                           │
│  4. Alex Xu books (2 weeks)                                                │
│                                                                              │
│  SPECIFIC TECHNOLOGIES:                                                     │
│  ──────────────────────                                                     │
│  Caching focus: Redis in Action                                            │
│  Message queues: Kafka Definitive Guide                                    │
│  Operations: SRE Book                                                      │
│  Code design: Clean Architecture                                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Reading Tips

### For Maximum Retention

1. **Active reading**: Take notes, draw diagrams
2. **Connect to systems**: "How does Twitter use this?"
3. **Implement concepts**: Build mini-projects
4. **Teach others**: Explain concepts out loud

### Time-Boxing

```
If you have 2 weeks:
├── DDIA Ch 5, 6, 9 (replication, partitioning, consensus)
├── Alex Xu: 4-5 case studies
└── Skip the rest

If you have 4 weeks:
├── DDIA Part 1 + Part 2
├── Alex Xu Vol 1 complete
└── Selected chapters from Vol 2

If you have 3 months:
├── Read everything in Tier 1 and 2
├── Implement hands-on projects
└── Do mock interviews
```

## Free Resources

Some books and chapters available free:

- **SRE Book**: https://sre.google/sre-book/table-of-contents/
- **High Scalability Blog**: http://highscalability.com/ (not a book, but equivalent content)
- **System Design Primer**: https://github.com/donnemartin/system-design-primer

---

**Next**: [Engineering Blogs](./blogs.md) - Learn from real production systems
