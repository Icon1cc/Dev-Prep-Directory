# Engineering Blogs

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      ENGINEERING BLOGS                                        ║
║             Learn How Top Companies Build Systems                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Why Engineering Blogs?

```
Books teach theory. Blogs teach reality.

Engineering blogs show you:
├── Real production challenges
├── Actual scale numbers
├── Trade-offs they made
├── Failures and lessons learned
└── Technologies in practice
```

## Tier 1: Must-Follow

### Netflix Tech Blog
**URL**: https://netflixtechblog.com/
**Focus**: Streaming, microservices, chaos engineering, data

**Must-Read Posts**:
- "Scaling Time Series Data Storage"
- "Building and Scaling Data Lineage at Netflix"
- "Zuul 2: The Netflix Journey to Asynchronous, Non-Blocking Systems"
- "Chaos Engineering Upgraded"

**Why Follow**: Netflix handles massive scale with sophisticated systems. Their posts are detailed and practical.

---

### Uber Engineering
**URL**: https://www.uber.com/blog/engineering/
**Focus**: Geospatial, real-time, microservices, data platforms

**Must-Read Posts**:
- "How Uber Serves Over 40 Million Reads Per Second"
- "Schemaless: Uber's Scalable Datastore"
- "Rethinking Uber's Payment System"
- "H3: Uber's Hexagonal Hierarchical Spatial Index"

**Why Follow**: Excellent posts on scaling, real-time systems, and handling complexity.

---

### Stripe Engineering
**URL**: https://stripe.com/blog/engineering
**Focus**: Payments, reliability, API design, infrastructure

**Must-Read Posts**:
- "Designing robust and predictable APIs with idempotency"
- "Online migrations at scale"
- "Scaling your API with rate limiters"

**Why Follow**: Payment systems require extreme reliability. Great for understanding correctness.

---

### AWS Architecture Blog
**URL**: https://aws.amazon.com/blogs/architecture/
**Focus**: Cloud architecture patterns, best practices

**Must-Read Posts**:
- "Exponential Backoff And Jitter"
- "Caching Best Practices"
- Various Well-Architected Framework posts

**Why Follow**: Authoritative source on cloud architecture patterns.

---

### Google Cloud Blog
**URL**: https://cloud.google.com/blog/
**Focus**: Infrastructure, data, ML systems

**Must-Read Posts**:
- Spanner-related posts
- BigQuery architecture posts
- SRE practices

**Why Follow**: Google builds at massive scale with innovative approaches.

---

## Tier 2: Highly Recommended

### LinkedIn Engineering
**URL**: https://engineering.linkedin.com/blog
**Focus**: Data infrastructure, feed systems, search

**Notable Posts**:
- "How LinkedIn Handles 5M+ Kafka Messages Per Second"
- "Building LinkedIn's Real-time Activity Data Pipeline"

---

### Airbnb Engineering
**URL**: https://medium.com/airbnb-engineering
**Focus**: Search, ML systems, data pipelines

**Notable Posts**:
- "Airflow: Workflow Management Platform"
- "Building a Scalable ML Feature Store"

---

### Spotify Engineering
**URL**: https://engineering.atspotify.com/
**Focus**: Data pipelines, recommendation systems, developer experience

**Notable Posts**:
- "How Spotify Organizes Teams"
- "Tracking Interactions in Real-Time"

---

### Dropbox Tech Blog
**URL**: https://dropbox.tech/
**Focus**: Storage systems, sync, infrastructure

**Notable Posts**:
- "How Dropbox Stores and Syncs Exabytes of Data"
- "Building Dropbox's Edge API Gateway"

---

### Meta Engineering
**URL**: https://engineering.fb.com/
**Focus**: Social graph, news feed, messaging, infrastructure

**Notable Posts**:
- "Scaling the Facebook data warehouse to 300 PB"
- "TAO: Facebook's Distributed Data Store"
- "Building Mobile-First Infrastructure for Messenger"

---

### Pinterest Engineering
**URL**: https://medium.com/pinterest-engineering
**Focus**: Recommendation systems, image processing, search

**Notable Posts**:
- "How Pinterest Powers a Healthy Discovery Engine"
- "Building a Real-time Feature Store"

---

## Tier 3: Specialized

### Cloudflare Blog
**URL**: https://blog.cloudflare.com/
**Focus**: CDN, DDoS, edge computing, network

**Why Read**: Excellent technical depth on networking and edge systems.

---

### Discord Engineering
**URL**: https://discord.com/blog/engineering-and-developers
**Focus**: Real-time communication, gaming scale

**Notable Post**: "How Discord Stores Billions of Messages"

---

### Slack Engineering
**URL**: https://slack.engineering/
**Focus**: Real-time messaging, search, infrastructure

**Notable Posts**: Architecture evolution posts

---

### GitHub Engineering
**URL**: https://github.blog/category/engineering/
**Focus**: Git internals, code hosting at scale

---

### Shopify Engineering
**URL**: https://shopify.engineering/
**Focus**: E-commerce, Rails at scale, checkout systems

---

## Reading Strategy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BLOG READING STRATEGY                                     │
│                                                                              │
│  FOR INTERVIEW PREP:                                                        │
│  ───────────────────                                                        │
│  Focus on posts about systems you might design:                             │
│  ├── Chat system → Discord, Slack blogs                                    │
│  ├── Feed system → LinkedIn, Facebook, Twitter                             │
│  ├── Streaming → Netflix, Spotify                                          │
│  ├── E-commerce → Stripe, Shopify                                          │
│  └── Storage → Dropbox, Google                                             │
│                                                                              │
│  FOR STAYING CURRENT:                                                       │
│  ────────────────────                                                       │
│  1. Set up RSS reader                                                       │
│  2. Follow 5-10 blogs                                                       │
│  3. Read 2-3 posts per week                                                │
│  4. Take notes on interesting patterns                                     │
│                                                                              │
│  FOR DEEP LEARNING:                                                         │
│  ──────────────────                                                         │
│  Pick one company, read their entire engineering blog                      │
│  (Netflix or Uber are best for this)                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## How to Read Engineering Posts

### Extract Key Information

1. **The Problem**: What were they trying to solve?
2. **The Scale**: How many users/requests/data?
3. **The Solution**: What architecture did they choose?
4. **The Trade-offs**: What did they sacrifice?
5. **The Learnings**: What would they do differently?

### Example Analysis

```
POST: "How Discord Stores Billions of Messages"

PROBLEM: Store chat messages at massive scale
SCALE: Billions of messages, real-time reads/writes
SOLUTION: Cassandra with careful data modeling
TRADE-OFFS: Eventual consistency, no complex queries
LEARNINGS: Partition key design is critical

INTERVIEW APPLICATION:
"When designing a chat system, I'd consider using
 Cassandra with message_id as partition key,
 similar to how Discord handles billions of messages..."
```

## Best Posts for Interviews

### By Topic

**Databases/Storage**:
- Uber: "Schemaless"
- Discord: "Billions of Messages"
- Dropbox: "Exabytes of Data"

**Caching**:
- Netflix: "EVCache"
- Pinterest: "Building a Real-time Feature Store"

**Message Queues**:
- LinkedIn: "Kafka at Scale"
- Uber: "Real-time Data Infrastructure"

**API Design**:
- Stripe: "Idempotency"
- Stripe: "Rate Limiters"

**Microservices**:
- Netflix: "Zuul"
- Uber: "Domain-Oriented Microservice Architecture"

---

**Next**: [YouTube Channels](./youtube.md) - Visual learning resources
