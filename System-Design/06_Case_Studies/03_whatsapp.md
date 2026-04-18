# Design WhatsApp Chat System

## Problem Statement

Design a real-time messaging system like WhatsApp. Users should be able to send text messages to individuals or groups, with features like delivery receipts, read receipts, and presence indicators (online status).

---

## 1. Requirements

### Functional Requirements

| Requirement | Description |
|-------------|-------------|
| **One-on-one chat** | Send/receive messages between two users |
| **Group chat** | Send messages to groups (up to 256 members) |
| **Delivery status** | Sent, delivered, read indicators |
| **Online status** | Show when users are online/last seen |
| **Media sharing** | Send images, videos, documents |
| **Push notifications** | Notify offline users |

### Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| **Latency** | < 100ms message delivery |
| **Availability** | 99.99% uptime |
| **Scale** | 2 billion users, 100 billion messages/day |
| **Ordering** | Messages in order within a conversation |

### Out of Scope
- End-to-end encryption (mentioned but not detailed)
- Voice/video calls
- Stories/Status feature
- Payment features

---

## 2. Capacity Estimation

### Traffic

```
MESSAGES:
- 100 billion messages per day
- 100B / 86400 sec ≈ 1.15 million messages/second
- Peak: ~2 million messages/second

CONNECTIONS:
- 2 billion users
- ~500 million concurrent connections at peak
```

### Storage

```
MESSAGE STORAGE:
- Average message: 100 bytes
- 100B messages/day × 100 bytes = 10 TB/day
- Keep 30 days: 300 TB
- With replication: ~1 PB

MEDIA STORAGE:
- 10% of messages have media
- Average media: 200 KB
- 10B × 200 KB = 2 PB/day
```

---

## 3. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   WHATSAPP ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Mobile Apps                                                   │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│   │  User A  │    │  User B  │    │  User C  │                 │
│   └────┬─────┘    └────┬─────┘    └────┬─────┘                 │
│        │               │               │                        │
│        │   WebSocket Connections       │                        │
│        └───────────────┼───────────────┘                        │
│                        │                                         │
│                 ┌──────▼──────┐                                 │
│                 │   Gateway   │   (Load Balancer)               │
│                 │   Servers   │                                 │
│                 └──────┬──────┘                                 │
│                        │                                         │
│         ┌──────────────┼──────────────┐                         │
│         │              │              │                          │
│   ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐                  │
│   │  Chat     │  │ Presence  │  │  Group    │                  │
│   │  Server   │  │  Server   │  │  Service  │                  │
│   └─────┬─────┘  └─────┬─────┘  └─────┬─────┘                  │
│         │              │              │                          │
│   ┌─────▼──────────────▼──────────────▼─────┐                  │
│   │              Message Queue               │                  │
│   │               (Kafka)                    │                  │
│   └─────────────────────┬────────────────────┘                  │
│                         │                                        │
│         ┌───────────────┼───────────────┐                       │
│         │               │               │                        │
│   ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐                │
│   │  Message  │   │  Session  │   │   Media   │                │
│   │    DB     │   │   Store   │   │   Store   │                │
│   │(Cassandra)│   │  (Redis)  │   │   (S3)    │                │
│   └───────────┘   └───────────┘   └───────────┘                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Core Components

### WebSocket Connection Management

```
┌─────────────────────────────────────────────────────────────────┐
│               WEBSOCKET CONNECTION MANAGEMENT                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Why WebSocket?                                                 │
│  - Full-duplex communication                                    │
│  - Low latency (no HTTP overhead)                               │
│  - Server can push messages instantly                           │
│                                                                  │
│  Connection Flow:                                               │
│                                                                  │
│  ┌────────┐   1. Connect    ┌─────────────┐                    │
│  │ Client │ ───────────────► │   Gateway   │                    │
│  │        │                  │   Server    │                    │
│  │        │ ◄─────────────── │             │                    │
│  └────────┘   2. Connected   └──────┬──────┘                    │
│                                     │                            │
│                              3. Register session                │
│                                     │                            │
│                              ┌──────▼──────┐                    │
│                              │   Session   │                    │
│                              │    Store    │                    │
│                              │             │                    │
│                              │ user_123:   │                    │
│                              │  server: gw5│                    │
│                              │  socket: ws9│                    │
│                              └─────────────┘                    │
│                                                                  │
│  Session Store (Redis):                                         │
│  - Maps user_id → gateway server                                │
│  - Enables routing messages to correct server                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Message Delivery Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  MESSAGE DELIVERY FLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User A sends message to User B:                                │
│                                                                  │
│  ┌────────┐  1. Send msg   ┌─────────────┐                     │
│  │ User A │ ─────────────► │  Gateway 1  │                     │
│  │        │                │ (WebSocket) │                     │
│  └────────┘                └──────┬──────┘                     │
│                                   │                             │
│                            2. Publish to queue                  │
│                                   │                             │
│                            ┌──────▼──────┐                     │
│                            │   Kafka     │                     │
│                            │ msg-queue   │                     │
│                            └──────┬──────┘                     │
│                                   │                             │
│                            3. Persist message                   │
│                                   │                             │
│                            ┌──────▼──────┐                     │
│                            │  Cassandra  │                     │
│                            └──────┬──────┘                     │
│                                   │                             │
│                            4. Lookup User B's server            │
│                                   │                             │
│                            ┌──────▼──────┐                     │
│                            │ Session DB  │ user_B → gateway_2  │
│                            └──────┬──────┘                     │
│                                   │                             │
│               ┌───────────────────┴────────────────┐           │
│               │                                    │            │
│         User B online?                       User B offline?   │
│               │                                    │            │
│        ┌──────▼──────┐                     ┌──────▼──────┐     │
│        │  Gateway 2  │                     │    Push     │     │
│        │ Push to WS  │                     │Notification │     │
│        └──────┬──────┘                     └─────────────┘     │
│               │                                                 │
│        ┌──────▼──────┐                                         │
│        │   User B    │ Receives message instantly              │
│        └─────────────┘                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Data Model

### Messages Table (Cassandra)

```sql
CREATE TABLE messages (
    conversation_id  UUID,
    message_id       TIMEUUID,     -- Sortable by time
    sender_id        BIGINT,
    content          TEXT,
    media_url        TEXT,
    message_type     TEXT,         -- text, image, video
    created_at       TIMESTAMP,

    PRIMARY KEY (conversation_id, message_id)
) WITH CLUSTERING ORDER BY (message_id DESC);
```

**Why Cassandra?**
- Write-heavy workload (100B messages/day)
- Time-series data (messages ordered by time)
- Horizontal scaling
- Tunable consistency

### Conversation Participants

```sql
CREATE TABLE conversation_participants (
    user_id          BIGINT,
    conversation_id  UUID,
    last_read_msg    TIMEUUID,
    muted            BOOLEAN,

    PRIMARY KEY (user_id, conversation_id)
);
```

### User Sessions (Redis)

```
Key: session:{user_id}
Value: {
    gateway_id: "gateway-5",
    connected_at: 1615000000,
    device_id: "device_abc"
}
TTL: Connection duration + buffer
```

---

## 6. Message Status and Receipts

```
┌─────────────────────────────────────────────────────────────────┐
│                  MESSAGE STATUS FLOW                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Status progression:                                            │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐            │
│  │  SENT  │ → │DELIVERED│ → │  READ  │                         │
│  │   ✓    │   │   ✓✓   │   │  ✓✓   │ (blue)                  │
│  └────────┘   └────────┘   └────────┘                          │
│                                                                  │
│  Flow:                                                          │
│                                                                  │
│  1. SENT: Message reaches server                                │
│     ┌────────┐     ┌────────┐                                  │
│     │ Sender │────►│ Server │  Server ACKs receipt             │
│     │   ✓    │◄────│        │                                  │
│     └────────┘     └────────┘                                  │
│                                                                  │
│  2. DELIVERED: Message reaches recipient's device               │
│     ┌────────┐     ┌────────┐     ┌──────────┐                │
│     │ Server │────►│Receiver│────►│ Receiver │                │
│     │        │◄────│ Device │     │   App    │                │
│     │        │ ACK │        │     │          │                │
│     └────────┘     └────────┘     └──────────┘                │
│           │                                                     │
│           ▼                                                     │
│     ┌────────┐                                                 │
│     │ Sender │  Update status to ✓✓                            │
│     │   ✓✓   │                                                 │
│     └────────┘                                                 │
│                                                                  │
│  3. READ: Recipient opens conversation                          │
│     Same flow, triggered when user views message               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Group Messaging

```
┌─────────────────────────────────────────────────────────────────┐
│                    GROUP MESSAGE FLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Group: "Family" (4 members: A, B, C, D)                        │
│  User A sends: "Hello everyone!"                                │
│                                                                  │
│  1. ┌─────────────────────────────────────────────────────────┐│
│     │ User A → Chat Server                                    ││
│     │ Message: { group_id: "family", content: "Hello..." }   ││
│     └─────────────────────────────────────────────────────────┘│
│                         │                                       │
│                         ▼                                       │
│  2. ┌─────────────────────────────────────────────────────────┐│
│     │ Store message once (group_id as conversation_id)       ││
│     │                                                         ││
│     │ INSERT INTO messages (conversation_id, ...) VALUES     ││
│     │ ("family", ..., "Hello everyone!")                     ││
│     └─────────────────────────────────────────────────────────┘│
│                         │                                       │
│                         ▼                                       │
│  3. ┌─────────────────────────────────────────────────────────┐│
│     │ Fan-out to group members                                ││
│     │                                                         ││
│     │ Get members: SELECT user_id FROM group_members         ││
│     │              WHERE group_id = "family"                  ││
│     │ Returns: [B, C, D] (exclude sender A)                  ││
│     └─────────────────────────────────────────────────────────┘│
│                         │                                       │
│        ┌────────────────┼────────────────┐                     │
│        │                │                │                      │
│        ▼                ▼                ▼                      │
│   ┌─────────┐      ┌─────────┐      ┌─────────┐               │
│   │  User B │      │  User C │      │  User D │               │
│   │ (online)│      │ (online)│      │(offline)│               │
│   └─────────┘      └─────────┘      └─────────┘               │
│   Push via WS      Push via WS      Push notification         │
│                                                                  │
│  Note: Message stored ONCE, delivered to MANY                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Group Metadata

```sql
CREATE TABLE groups (
    group_id         UUID PRIMARY KEY,
    name             TEXT,
    created_by       BIGINT,
    created_at       TIMESTAMP,
    member_count     INT
);

CREATE TABLE group_members (
    group_id         UUID,
    user_id          BIGINT,
    role             TEXT,    -- admin, member
    joined_at        TIMESTAMP,

    PRIMARY KEY (group_id, user_id)
);
```

---

## 8. Presence (Online Status)

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENCE SYSTEM                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Presence States:                                               │
│  - Online (connected)                                           │
│  - Last seen at [timestamp]                                     │
│  - Typing...                                                    │
│                                                                  │
│  Implementation:                                                │
│                                                                  │
│  1. Heartbeat:                                                  │
│     Client sends ping every 30 seconds                          │
│     Server updates presence in Redis                            │
│                                                                  │
│     ┌────────┐  heartbeat   ┌─────────┐                        │
│     │ Client │ ───────────► │ Server  │                        │
│     │        │  (30s)       │         │                        │
│     └────────┘              └────┬────┘                        │
│                                  │                              │
│                           ┌──────▼──────┐                      │
│                           │   Redis     │                      │
│                           │             │                      │
│                           │ presence:123│                      │
│                           │ online: true│                      │
│                           │ TTL: 60s    │                      │
│                           └─────────────┘                      │
│                                                                  │
│  2. Subscribing to presence:                                    │
│     When User A opens chat with User B:                         │
│     - Subscribe to presence:B channel                           │
│     - Get notified of online/offline changes                    │
│                                                                  │
│  3. Typing indicator:                                           │
│     Client sends "typing" event → Server broadcasts to chat    │
│     Auto-expires after 3 seconds                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. Scaling Considerations

### Gateway Server Scaling

```
HORIZONTAL SCALING:
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  500M concurrent connections ÷ 100K connections/server         │
│  = 5,000 gateway servers                                        │
│                                                                  │
│  Load balancing by:                                             │
│  - Geographic region (reduce latency)                           │
│  - Consistent hashing (sticky sessions)                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Message Database Sharding

```
SHARD BY CONVERSATION_ID:
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  All messages in a conversation on same shard                   │
│  Enables efficient conversation history queries                 │
│                                                                  │
│  conversation_abc → Shard 1                                     │
│  conversation_def → Shard 2                                     │
│  conversation_ghi → Shard 1                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Trade-offs

| Decision | Choice | Alternative | Reason |
|----------|--------|-------------|--------|
| Connection | WebSocket | Long polling | Real-time, efficient |
| Message DB | Cassandra | PostgreSQL | Write-heavy, scale |
| Session store | Redis | Database | Speed, TTL support |
| Message delivery | At-least-once | Exactly-once | Simpler, handle duplicates |

---

## 11. Follow-up Questions

1. "How would you implement end-to-end encryption?"
2. "How do you handle message sync across devices?"
3. "How would you implement voice/video calls?"
4. "How do you handle message ordering in unreliable networks?"
5. "How would you implement message search?"

---

## Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                    WHATSAPP SUMMARY                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CORE COMPONENTS:                                               │
│  ├── WebSocket for real-time messaging                         │
│  ├── Session store (Redis) for connection routing              │
│  ├── Cassandra for message storage                             │
│  └── Kafka for async processing                                │
│                                                                  │
│  KEY FLOWS:                                                     │
│  ├── Message delivery via session lookup                       │
│  ├── Push notifications for offline users                      │
│  └── Delivery/read receipts via reverse path                   │
│                                                                  │
│  SCALE:                                                         │
│  ├── 1M+ messages/second                                       │
│  ├── 500M concurrent connections                               │
│  └── ~1 PB message storage                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

*Next: [Design Netflix](04_netflix.md) →*
