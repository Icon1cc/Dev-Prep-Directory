# Core Components

## Overview

This section covers the essential building blocks used in distributed systems. Understanding these components deeply is critical for system design interviews—interviewers expect you to know not just **what** they do, but **when** to use them, **when NOT to** use them, and their **failure modes**.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Core Components Map                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                          ┌──────────────┐                               │
│                          │    Client    │                               │
│                          └──────┬───────┘                               │
│                                 │                                       │
│                                 ▼                                       │
│                          ┌──────────────┐                               │
│                          │     CDN      │ ◄── Static content           │
│                          └──────┬───────┘                               │
│                                 │                                       │
│                                 ▼                                       │
│                          ┌──────────────┐                               │
│                          │ API Gateway  │ ◄── Auth, rate limiting      │
│                          └──────┬───────┘                               │
│                                 │                                       │
│                                 ▼                                       │
│                          ┌──────────────┐                               │
│                          │Load Balancer │ ◄── Distribute traffic       │
│                          └──────┬───────┘                               │
│                    ┌────────────┼────────────┐                         │
│                    ▼            ▼            ▼                         │
│              ┌─────────┐  ┌─────────┐  ┌─────────┐                     │
│              │ Server  │  │ Server  │  │ Server  │                     │
│              └────┬────┘  └────┬────┘  └────┬────┘                     │
│                   │            │            │                          │
│              ┌────┴────────────┴────────────┴────┐                     │
│              │                                    │                     │
│              ▼                                    ▼                     │
│        ┌──────────┐                        ┌──────────┐                │
│        │  Cache   │                        │  Queue   │                │
│        │ (Redis)  │                        │ (Kafka)  │                │
│        └────┬─────┘                        └────┬─────┘                │
│             │                                   │                       │
│             ▼                                   ▼                       │
│        ┌──────────┐                        ┌──────────┐                │
│        │ Database │                        │ Workers  │                │
│        └──────────┘                        └──────────┘                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Study Order

1. **[01_load_balancers.md](./01_load_balancers.md)** - Traffic distribution fundamentals
2. **[02_caching_systems.md](./02_caching_systems.md)** - Speed up reads with caching
3. **[03_message_queues.md](./03_message_queues.md)** - Async processing and decoupling
4. **[04_cdn.md](./04_cdn.md)** - Content delivery at scale
5. **[05_api_gateway.md](./05_api_gateway.md)** - API management and security
6. **[06_distributed_databases.md](./06_distributed_databases.md)** - Data at scale
7. **[07_search_systems.md](./07_search_systems.md)** - Full-text search basics
8. **[08_bloom_filters.md](./08_bloom_filters.md)** - Probabilistic data structures
9. **[09_rate_limiters.md](./09_rate_limiters.md)** - Protecting your systems

## Component Selection Framework

```
┌─────────────────────────────────────────────────────────────────────────┐
│                 When to Use Which Component                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Problem                          │ Component                          │
│   ─────────────────────────────────┼─────────────────────────────────── │
│   Slow database reads              │ Cache (Redis, Memcached)           │
│   Traffic spikes overwhelming      │ Load Balancer + Auto-scaling       │
│   Need async processing            │ Message Queue (Kafka, RabbitMQ)    │
│   Slow static content delivery     │ CDN (CloudFront, Cloudflare)       │
│   Need auth/rate limiting at edge  │ API Gateway                        │
│   Full-text search needed          │ Search Engine (Elasticsearch)      │
│   Check membership in large set    │ Bloom Filter                       │
│   Protect from abuse               │ Rate Limiter                       │
│   Store huge amounts of data       │ Distributed Database               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Interview Expectations

For each component, you should be able to explain:

1. **What it does** (2-3 sentences)
2. **When to use it** (common use cases)
3. **When NOT to use it** (anti-patterns)
4. **How it works** (high-level internals)
5. **Trade-offs** (pros/cons)
6. **Failure modes** (what can go wrong)
7. **Popular implementations** (real-world examples)

---

**Start with:** [01_load_balancers.md](./01_load_balancers.md)
