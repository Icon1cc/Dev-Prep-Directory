# Design Google Drive (Distributed File Storage)

## Problem Statement

Design a cloud file storage service like Google Drive or Dropbox. Users should be able to upload, download, sync files across devices, and share files with others.

---

## 1. Requirements

### Functional Requirements

| Requirement | Description |
|-------------|-------------|
| **Upload/Download** | Store and retrieve files |
| **Sync** | Sync files across multiple devices |
| **Share** | Share files/folders with other users |
| **Versioning** | Keep version history of files |
| **Offline access** | Work offline, sync when online |

### Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| **Reliability** | 99.999% (no data loss) |
| **Availability** | 99.9% uptime |
| **Scale** | 500M users, 1 billion files/day |
| **Latency** | < 200ms for metadata operations |

---

## 2. Capacity Estimation

```
STORAGE:
- 500M users × 5 GB average = 2.5 exabytes
- With replication (3x): ~7.5 EB

UPLOADS:
- 1 billion files/day
- Average file size: 500 KB
- 500 TB uploaded daily

SYNC OPERATIONS:
- 500M users × 5 devices × 10 syncs/day = 25 billion sync events/day
```

---

## 3. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  GOOGLE DRIVE ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Desktop Client        Web Client         Mobile Client        │
│   ┌──────────┐         ┌──────────┐       ┌──────────┐         │
│   │ Sync     │         │ Browser  │       │   App    │         │
│   │ Engine   │         │          │       │          │         │
│   └────┬─────┘         └────┬─────┘       └────┬─────┘         │
│        │                    │                   │                │
│        └────────────────────┼───────────────────┘                │
│                             │                                    │
│                      ┌──────▼──────┐                            │
│                      │ API Gateway │                            │
│                      └──────┬──────┘                            │
│                             │                                    │
│      ┌──────────────────────┼──────────────────────┐            │
│      │                      │                      │             │
│ ┌────▼─────┐         ┌──────▼──────┐        ┌─────▼─────┐      │
│ │ Metadata │         │   Upload    │        │   Sync    │      │
│ │ Service  │         │   Service   │        │  Service  │      │
│ └────┬─────┘         └──────┬──────┘        └─────┬─────┘      │
│      │                      │                     │              │
│ ┌────▼─────┐         ┌──────▼──────┐        ┌─────▼─────┐      │
│ │ Metadata │         │   Block     │        │  Message  │      │
│ │    DB    │         │   Storage   │        │   Queue   │      │
│ │(Postgres)│         │    (S3)     │        │  (Kafka)  │      │
│ └──────────┘         └─────────────┘        └───────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Core Concept: Block Storage

### Why Chunking?

```
┌─────────────────────────────────────────────────────────────────┐
│                       FILE CHUNKING                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Problem: Large files are hard to handle                        │
│  - 1 GB file: Single failure = re-upload entire file           │
│  - Network interruption = start over                            │
│  - Small change = re-upload entire file                         │
│                                                                  │
│  Solution: Split into fixed-size blocks (4 MB)                  │
│                                                                  │
│  1 GB File → Split into 256 blocks                              │
│  ┌──────┬──────┬──────┬──────┬─────┬──────┐                    │
│  │Block1│Block2│Block3│Block4│ ... │Block256                   │
│  │ 4MB  │ 4MB  │ 4MB  │ 4MB  │     │ 4MB  │                    │
│  └──────┴──────┴──────┴──────┴─────┴──────┘                    │
│                                                                  │
│  Benefits:                                                      │
│  ✓ Resume interrupted uploads                                  │
│  ✓ Deduplicate common blocks                                   │
│  ✓ Sync only changed blocks                                    │
│  ✓ Parallel upload/download                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Block Deduplication

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEDUPLICATION                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Each block has a hash: SHA-256(block_content)                 │
│                                                                  │
│  User A uploads report.docx:                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Block 1: hash_abc │ Block 2: hash_def │ Block 3: hash_ghi│  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  User B uploads same report.docx:                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Block 1: hash_abc │ Block 2: hash_def │ Block 3: hash_ghi│  │
│  └──────────────────────────────────────────────────────────┘  │
│                         │                                       │
│                         ▼                                       │
│  Server: "I already have these blocks!"                        │
│          → No upload needed, just link to existing blocks      │
│                                                                  │
│  Storage savings: 30-50% in enterprise (shared documents)      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Data Model

### File Metadata

```sql
CREATE TABLE files (
    file_id         UUID PRIMARY KEY,
    name            VARCHAR(255),
    user_id         UUID,
    parent_folder   UUID,
    size            BIGINT,
    mime_type       VARCHAR(100),
    version         INT,
    checksum        VARCHAR(64),
    created_at      TIMESTAMP,
    modified_at     TIMESTAMP,
    is_deleted      BOOLEAN DEFAULT FALSE
);

CREATE TABLE file_blocks (
    file_id         UUID,
    version         INT,
    block_index     INT,
    block_hash      VARCHAR(64),
    block_size      INT,

    PRIMARY KEY (file_id, version, block_index)
);

CREATE TABLE blocks (
    block_hash      VARCHAR(64) PRIMARY KEY,
    storage_path    VARCHAR(255),   -- S3 path
    reference_count INT,            -- For dedup
    created_at      TIMESTAMP
);
```

### Sharing

```sql
CREATE TABLE shares (
    share_id        UUID PRIMARY KEY,
    file_id         UUID,
    shared_by       UUID,
    shared_with     UUID,   -- NULL for link sharing
    permission      VARCHAR(20),  -- view, edit
    link_token      VARCHAR(64),
    expires_at      TIMESTAMP
);
```

---

## 6. Upload Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      UPLOAD FLOW                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Client prepares upload                                      │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ - Split file into 4 MB blocks                        │   │
│     │ - Calculate hash for each block                      │   │
│     │ - Send block hashes to server                        │   │
│     └──────────────────────────────────────────────────────┘   │
│                         │                                       │
│                         ▼                                       │
│  2. Server checks which blocks exist                            │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ Request: [hash_1, hash_2, hash_3, hash_4]            │   │
│     │ Response: {                                          │   │
│     │   "need_upload": [hash_2, hash_4],                  │   │
│     │   "already_have": [hash_1, hash_3]                  │   │
│     │ }                                                    │   │
│     └──────────────────────────────────────────────────────┘   │
│                         │                                       │
│                         ▼                                       │
│  3. Client uploads only needed blocks                          │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ POST /blocks                                         │   │
│     │ - Upload block_2 and block_4                        │   │
│     │ - Parallel uploads for speed                        │   │
│     └──────────────────────────────────────────────────────┘   │
│                         │                                       │
│                         ▼                                       │
│  4. Client commits file with block list                        │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ POST /files                                          │   │
│     │ {                                                    │   │
│     │   "name": "report.docx",                            │   │
│     │   "blocks": [hash_1, hash_2, hash_3, hash_4]        │   │
│     │ }                                                    │   │
│     └──────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Sync Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        SYNC FLOW                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Client maintains:                                              │
│  - Local state: { file_id → (version, modified_at) }           │
│  - Server cursor: Last sync position                            │
│                                                                  │
│  Sync process:                                                  │
│                                                                  │
│  1. ┌─────────────────────────────────────────────────────────┐│
│     │ Client → Server: "Changes since cursor_abc?"            ││
│     │                                                         ││
│     │ GET /sync?cursor=cursor_abc                             ││
│     └─────────────────────────────────────────────────────────┘│
│                         │                                       │
│                         ▼                                       │
│  2. ┌─────────────────────────────────────────────────────────┐│
│     │ Server → Client: List of changes                        ││
│     │                                                         ││
│     │ {                                                       ││
│     │   "changes": [                                          ││
│     │     { "type": "add", "file_id": "x", "version": 3 },   ││
│     │     { "type": "modify", "file_id": "y", "version": 2 },││
│     │     { "type": "delete", "file_id": "z" }               ││
│     │   ],                                                    ││
│     │   "new_cursor": "cursor_xyz"                            ││
│     │ }                                                       ││
│     └─────────────────────────────────────────────────────────┘│
│                         │                                       │
│                         ▼                                       │
│  3. ┌─────────────────────────────────────────────────────────┐│
│     │ Client applies changes locally                          ││
│     │                                                         ││
│     │ - Download new/modified files                           ││
│     │ - Delete locally removed files                          ││
│     │ - Resolve conflicts if needed                           ││
│     └─────────────────────────────────────────────────────────┘│
│                                                                  │
│  Long polling for real-time updates:                           │
│  GET /sync?cursor=cursor_xyz&timeout=60                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Conflict Resolution

```
┌─────────────────────────────────────────────────────────────────┐
│                  CONFLICT RESOLUTION                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Scenario: Same file edited on two offline devices             │
│                                                                  │
│  Device A (offline):    Device B (offline):                    │
│  report.docx v1         report.docx v1                         │
│       │                      │                                  │
│   Edit: "Hello"          Edit: "World"                         │
│       │                      │                                  │
│       ▼                      ▼                                  │
│  report.docx v2         report.docx v2                         │
│                                                                  │
│  Both go online → Conflict!                                    │
│                                                                  │
│  Resolution strategies:                                        │
│                                                                  │
│  1. LAST-WRITE-WINS (LWW):                                     │
│     - Simpler, may lose data                                   │
│     - Use when data loss is acceptable                         │
│                                                                  │
│  2. COPY-ON-CONFLICT (Dropbox style):                          │
│     - Keep both versions                                       │
│     - report.docx (Device A's conflicted copy)                │
│     - report.docx (Device B's version)                        │
│     - User manually resolves                                   │
│                                                                  │
│  3. OPERATIONAL TRANSFORM:                                      │
│     - Merge changes automatically (like Google Docs)           │
│     - Complex to implement                                     │
│                                                                  │
│  Recommendation: Copy-on-conflict for files                    │
│                  (Let user decide what to keep)                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. Storage Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   STORAGE ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Block Storage (S3-compatible):                                 │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    S3 STORAGE                           │   │
│  │                                                         │   │
│  │  Bucket: drive-blocks                                   │   │
│  │                                                         │   │
│  │  Path structure:                                        │   │
│  │  /blocks/{hash_prefix}/{block_hash}                    │   │
│  │                                                         │   │
│  │  Example:                                               │   │
│  │  /blocks/ab/abcdef1234567890...                        │   │
│  │  /blocks/cd/cdef9876543210...                          │   │
│  │                                                         │   │
│  │  Hash prefix for distribution across storage nodes      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Replication:                                                   │
│  - 3 replicas minimum                                          │
│  - Cross-region for disaster recovery                          │
│  - Different storage classes (hot/cold) based on access       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Version History

```
┌─────────────────────────────────────────────────────────────────┐
│                    VERSION HISTORY                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  File: report.docx                                              │
│                                                                  │
│  Version 1 (2024-01-01):                                       │
│  ┌────────────────────────────────────────────────────┐        │
│  │ Blocks: [hash_a, hash_b, hash_c]                   │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                  │
│  Version 2 (2024-01-15): User edited page 1                    │
│  ┌────────────────────────────────────────────────────┐        │
│  │ Blocks: [hash_d, hash_b, hash_c]  ← Only first changed    │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                  │
│  Version 3 (2024-02-01): User added page 4                     │
│  ┌────────────────────────────────────────────────────┐        │
│  │ Blocks: [hash_d, hash_b, hash_c, hash_e] ← New block      │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                  │
│  Storage efficiency:                                           │
│  - Blocks hash_b and hash_c reused across versions            │
│  - Only changed blocks stored                                  │
│                                                                  │
│  Restore version: Reconstruct from version's block list       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 11. Trade-offs

| Decision | Choice | Alternative | Reason |
|----------|--------|-------------|--------|
| Block size | 4 MB | 1 MB, 16 MB | Balance dedup vs overhead |
| Conflict | Copy-on-conflict | LWW, OT | Simple, user control |
| Sync | Polling + long-poll | WebSocket | Simpler, reliable |
| Storage | S3 | Custom | Cost-effective at scale |

---

## 12. Follow-up Questions

1. "How would you handle files larger than 100 GB?"
2. "How do you implement real-time collaboration (Google Docs)?"
3. "How do you handle folder sharing with nested permissions?"
4. "How would you implement search across all user files?"
5. "How do you handle quota management?"

---

## Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                   GOOGLE DRIVE SUMMARY                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  KEY COMPONENTS:                                                │
│  ├── Block storage (4 MB chunks)                               │
│  ├── Deduplication via content hashing                         │
│  ├── Cursor-based sync                                         │
│  └── Version history via block references                      │
│                                                                  │
│  KEY INSIGHTS:                                                  │
│  ├── Chunking enables resume, dedup, delta sync                │
│  ├── Only upload/download changed blocks                       │
│  ├── Conflict resolution: copy-on-conflict                     │
│  └── Long polling for near-real-time sync                      │
│                                                                  │
│  SCALE:                                                         │
│  ├── 500M users, 2.5 EB storage                               │
│  ├── 1B files uploaded daily                                   │
│  └── 25B sync events daily                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

*Congratulations! You've completed the Case Studies section. Continue to [Interview Prep](../07_Interview_Prep/README.md) for final preparation tips.*
