# Practice Question Bank

25+ system design questions organized by difficulty and category.

---

## How to Use This Bank

```
┌────────────────────────────────────────────────────────────────┐
│                  PRACTICE RECOMMENDATIONS                       │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Time yourself (45 min per question)                        │
│  2. Draw on paper/whiteboard, not just think                   │
│  3. Explain out loud as if interviewing                        │
│  4. Compare with case studies after                            │
│  5. Practice each question 2-3 times                           │
│                                                                 │
│  START: Easy questions first                                   │
│  GOAL: Complete all hard questions confidently                 │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Beginner Level (Start Here)

### 1. URL Shortener (TinyURL)
```
Design a URL shortening service like bit.ly

Key areas:
- Short code generation
- Redirect mechanism
- Analytics (optional)

Estimated time: 30 min
```

### 2. Pastebin
```
Design a text sharing service like Pastebin

Key areas:
- Text storage and retrieval
- Expiration handling
- Unique URL generation

Estimated time: 30 min
```

### 3. Rate Limiter
```
Design a rate limiting system for an API

Key areas:
- Different algorithms (token bucket, sliding window)
- Distributed rate limiting
- Per-user vs global limits

Estimated time: 35 min
```

### 4. Key-Value Store
```
Design a distributed key-value store like Redis

Key areas:
- Data partitioning
- Replication
- Consistency model

Estimated time: 40 min
```

---

## Intermediate Level

### 5. Twitter/X
```
Design Twitter's core functionality

Key areas:
- Tweet posting and timeline
- Fan-out problem
- Following/followers

Focus: Fan-out on write vs read
Estimated time: 45 min
```

### 6. Instagram
```
Design Instagram's photo sharing system

Key areas:
- Photo upload and storage
- News feed generation
- Following system

Focus: Media storage and CDN
Estimated time: 45 min
```

### 7. Facebook Messenger / WhatsApp
```
Design a real-time chat system

Key areas:
- Real-time messaging
- Presence (online status)
- Group chats
- Read receipts

Focus: WebSocket connections, message delivery
Estimated time: 45 min
```

### 8. Dropbox / Google Drive
```
Design a file storage and sync system

Key areas:
- File upload/download
- Sync across devices
- Conflict resolution
- Sharing

Focus: Block storage, delta sync
Estimated time: 45 min
```

### 9. Web Crawler
```
Design a web crawler like Googlebot

Key areas:
- URL frontier management
- Politeness (rate limiting per domain)
- Deduplication
- Distributed crawling

Focus: Scale and politeness
Estimated time: 45 min
```

### 10. Notification System
```
Design a notification service (push, email, SMS)

Key areas:
- Multiple channels
- Priority handling
- Rate limiting
- Reliability

Focus: At-least-once delivery
Estimated time: 40 min
```

---

## Advanced Level

### 11. YouTube / Netflix
```
Design a video streaming platform

Key areas:
- Video upload and processing
- Adaptive bitrate streaming
- CDN architecture
- Recommendations

Focus: Video encoding, CDN
Estimated time: 50 min
```

### 12. Uber / Lyft
```
Design a ride-sharing service

Key areas:
- Driver-rider matching
- Real-time location tracking
- ETA calculation
- Surge pricing

Focus: Geospatial indexing
Estimated time: 50 min
```

### 13. Yelp / Google Maps
```
Design a location-based service

Key areas:
- Geospatial search
- Reviews and ratings
- Business listings

Focus: Geohash, proximity search
Estimated time: 45 min
```

### 14. Ticketmaster
```
Design a ticket booking system

Key areas:
- Inventory management
- Concurrent booking handling
- Seat selection
- Payment processing

Focus: Handling race conditions
Estimated time: 45 min
```

### 15. Amazon / E-commerce
```
Design an e-commerce platform

Key areas:
- Product catalog
- Shopping cart
- Order processing
- Inventory management

Focus: Eventual consistency, transactions
Estimated time: 50 min
```

### 16. Search Autocomplete
```
Design a typeahead/autocomplete system

Key areas:
- Trie data structure
- Ranking suggestions
- Real-time updates
- Personalization

Focus: Low latency, data structures
Estimated time: 40 min
```

### 17. Distributed Cache
```
Design a distributed caching system like Memcached

Key areas:
- Consistent hashing
- Cache invalidation
- Replication
- Hot keys

Focus: Consistency, partitioning
Estimated time: 45 min
```

---

## Expert Level

### 18. Google Search
```
Design a web search engine

Key areas:
- Inverted index
- PageRank
- Query processing
- Result ranking

Focus: Indexing at scale
Estimated time: 55 min
```

### 19. Slack
```
Design a team collaboration platform

Key areas:
- Real-time messaging
- Channels and workspaces
- Search
- Integrations

Focus: Multi-tenancy, real-time
Estimated time: 50 min
```

### 20. Distributed Task Scheduler
```
Design a job scheduling system like Airflow

Key areas:
- Task dependencies (DAG)
- Distributed execution
- Retry handling
- Monitoring

Focus: Exactly-once execution
Estimated time: 50 min
```

### 21. Stock Exchange
```
Design a stock trading platform

Key areas:
- Order matching engine
- Real-time quotes
- Transaction processing
- Regulatory compliance

Focus: Low latency, consistency
Estimated time: 55 min
```

### 22. Distributed Message Queue
```
Design a message queue like Kafka

Key areas:
- Partitioning
- Replication
- Consumer groups
- Message ordering

Focus: Durability, ordering guarantees
Estimated time: 50 min
```

### 23. Content Delivery Network
```
Design a CDN

Key areas:
- Global distribution
- Cache hierarchies
- Origin shielding
- Purging

Focus: Geographic distribution
Estimated time: 45 min
```

### 24. Ad Click Aggregator
```
Design a real-time ad click counting system

Key areas:
- High write throughput
- Real-time aggregation
- Deduplication
- Fraud detection

Focus: Stream processing
Estimated time: 45 min
```

### 25. Typeahead Search for Social Network
```
Design friend search with typeahead

Key areas:
- Personalized results
- Graph traversal
- Real-time indexing
- Ranking

Focus: Graph + text search
Estimated time: 45 min
```

---

## By Category

### Messaging & Real-time
- WhatsApp (#7)
- Slack (#19)
- Notification System (#10)

### Social Media
- Twitter (#5)
- Instagram (#6)
- News Feed

### Storage & Sync
- Dropbox (#8)
- Distributed Cache (#17)
- Key-Value Store (#4)

### Location-based
- Uber (#12)
- Yelp (#13)
- Google Maps

### Media & Streaming
- YouTube/Netflix (#11)
- Spotify (music streaming)

### E-commerce & Booking
- Amazon (#15)
- Ticketmaster (#14)
- Hotel booking

### Search & Discovery
- Google Search (#18)
- Autocomplete (#16)
- Web Crawler (#9)

### Infrastructure
- Rate Limiter (#3)
- Message Queue (#22)
- CDN (#23)
- Task Scheduler (#20)

---

## Practice Schedule

```
WEEK 1-2: Beginner (Questions 1-4)
- Do each question twice
- Focus on framework and communication

WEEK 3-4: Intermediate (Questions 5-10)
- Do each question once, review with case studies
- Focus on trade-offs

WEEK 5-6: Advanced (Questions 11-17)
- Time yourself strictly
- Focus on deep dives

WEEK 7-8: Expert + Review (Questions 18-25)
- Full mock interviews
- Revisit weak areas
```

---

## Self-Evaluation Checklist

After each practice session:

```
□ Did I ask clarifying questions first?
□ Did I define functional and non-functional requirements?
□ Did I do capacity estimation?
□ Did I draw a clear architecture diagram?
□ Did I explain the data model?
□ Did I discuss trade-offs?
□ Did I handle the deep dive well?
□ Did I mention potential bottlenecks?
□ Did I complete within time limit?
□ Did I communicate clearly throughout?
```

---

*Next: [Mock Interview Guide](08_mock_interview_guide.md) →*
