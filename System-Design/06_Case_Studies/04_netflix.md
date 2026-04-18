# Design Netflix Streaming

## Problem Statement

Design a video streaming service like Netflix. Users should be able to browse content, play videos with minimal buffering, and receive personalized recommendations.

---

## 1. Requirements

### Functional Requirements

| Requirement | Description |
|-------------|-------------|
| **Browse catalog** | Search and browse videos by genre, title |
| **Play video** | Stream video with adaptive quality |
| **Resume playback** | Continue from where user left off |
| **Multiple devices** | Support TV, mobile, web, tablet |
| **User profiles** | Multiple profiles per account |

### Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| **Availability** | 99.99% uptime |
| **Latency** | < 2 sec to start playback |
| **Scale** | 200M subscribers globally |
| **Bandwidth** | Handle peak streaming hours |

---

## 2. Capacity Estimation

### Users and Viewing

```
USERS:
- 200M paid subscribers
- 100M concurrent viewers at peak

VIEWING:
- Average 2 hours/day per active user
- 100M × 2 hours = 200M hours streamed daily
```

### Bandwidth

```
VIDEO QUALITY:
- SD: 3 Mbps
- HD: 5 Mbps
- 4K: 25 Mbps
- Average: 5 Mbps

PEAK BANDWIDTH:
- 100M concurrent × 5 Mbps = 500 Petabits/second (distributed via CDN)
```

### Storage

```
CONTENT:
- 15,000 titles
- Average 2 hours = 7,200 seconds per video
- Each video in 10 quality levels
- Each quality: ~2 GB average
- Total: 15,000 × 10 × 2 GB = 300 PB (before replication)
```

---

## 3. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    NETFLIX ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                         ┌──────────────┐                        │
│                         │   Clients    │                        │
│                         │ TV/Mobile/Web│                        │
│                         └──────┬───────┘                        │
│                                │                                 │
│           ┌────────────────────┼────────────────────┐           │
│           │                    │                    │            │
│    ┌──────▼──────┐      ┌──────▼──────┐     ┌──────▼──────┐    │
│    │ API Gateway │      │     CDN     │     │    OCA      │    │
│    │  (Control)  │      │  (Content)  │     │  (Netflix   │    │
│    │             │      │             │     │  Appliances)│    │
│    └──────┬──────┘      └─────────────┘     └─────────────┘    │
│           │                                                     │
│    ┌──────▼──────────────────────────────────────────────┐     │
│    │                 BACKEND SERVICES                      │     │
│    │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐│     │
│    │  │  User    │ │ Content  │ │ Playback │ │ Recom-  ││     │
│    │  │ Service  │ │ Catalog  │ │ Service  │ │mendation││     │
│    │  └──────────┘ └──────────┘ └──────────┘ └─────────┘│     │
│    └──────────────────────────────────────────────────────┘     │
│           │                                                     │
│    ┌──────▼──────────────────────────────────────────────┐     │
│    │                   DATA STORES                         │     │
│    │  ┌──────────┐ ┌──────────┐ ┌──────────┐             │     │
│    │  │ User DB  │ │ Content  │ │ Viewing  │             │     │
│    │  │(Cassandra)│ │ Metadata │ │ History  │             │     │
│    │  └──────────┘ └──────────┘ └──────────┘             │     │
│    └──────────────────────────────────────────────────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Video Streaming Pipeline

### Video Encoding (Offline Process)

```
┌─────────────────────────────────────────────────────────────────┐
│                    VIDEO ENCODING PIPELINE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Original Video (Master)                                        │
│  ┌─────────────────┐                                            │
│  │  4K HDR Master  │  Source file from content provider        │
│  │  ~100 GB        │                                            │
│  └────────┬────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────┐                                            │
│  │  Transcoding    │  Encode to multiple resolutions/bitrates  │
│  │   Farm          │  Parallel encoding on 1000s of servers    │
│  └────────┬────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  Output: Multiple versions                                      │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Resolution │ Bitrate  │ Use Case                          │ │
│  │────────────┼──────────┼────────────────────────────────── │ │
│  │ 4K (2160p) │ 25 Mbps  │ 4K TVs, fiber connections        │ │
│  │ 1080p     │ 8 Mbps   │ HD TVs, fast connections         │ │
│  │ 720p      │ 5 Mbps   │ Laptops, tablets                 │ │
│  │ 480p      │ 3 Mbps   │ Mobile, slow connections         │ │
│  │ 360p      │ 1.5 Mbps │ Very slow connections            │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                  │
│  + Chunking: Split into 2-4 second segments                    │
│  + Manifest: Index file listing all chunks and qualities       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Adaptive Bitrate Streaming (ABR)

```
┌─────────────────────────────────────────────────────────────────┐
│               ADAPTIVE BITRATE STREAMING                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Player monitors bandwidth and adapts quality in real-time:    │
│                                                                  │
│  Time ────────────────────────────────────────────────────────► │
│                                                                  │
│  Bandwidth:                                                     │
│  25Mbps │         ████                                         │
│  10Mbps │    █████    █████████                                │
│   5Mbps │████              ████████████                        │
│   2Mbps │                              ████████████            │
│         ────────────────────────────────────────────────────── │
│                                                                  │
│  Video Quality:                                                 │
│  4K     │         ████                                         │
│  1080p  │    █████    █████████                                │
│  720p   │████              ████████████                        │
│  480p   │                              ████████████            │
│         ────────────────────────────────────────────────────── │
│                                                                  │
│  Player automatically switches quality based on:                │
│  - Available bandwidth                                          │
│  - Buffer level                                                 │
│  - Device capabilities                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Content Delivery Network (CDN)

```
┌─────────────────────────────────────────────────────────────────┐
│                    NETFLIX CDN (OPEN CONNECT)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Architecture:                                                  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    ORIGIN (AWS S3)                       │   │
│  │              All content stored here                     │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│           ┌───────────────┼───────────────┐                    │
│           │               │               │                     │
│  ┌────────▼─────┐ ┌───────▼──────┐ ┌──────▼───────┐           │
│  │  Regional    │ │  Regional    │ │  Regional    │           │
│  │  POP (US)    │ │  POP (EU)    │ │  POP (Asia)  │           │
│  └────────┬─────┘ └───────┬──────┘ └──────┬───────┘           │
│           │               │               │                     │
│  ┌────────▼─────┐ ┌───────▼──────┐ ┌──────▼───────┐           │
│  │  ISP Edge    │ │  ISP Edge    │ │  ISP Edge    │           │
│  │  OCAs        │ │  OCAs        │ │  OCAs        │           │
│  │  (In ISP     │ │              │ │              │           │
│  │  Data Center)│ │              │ │              │           │
│  └────────┬─────┘ └───────┬──────┘ └──────┬───────┘           │
│           │               │               │                     │
│       ┌───▼───┐       ┌───▼───┐       ┌───▼───┐               │
│       │ Users │       │ Users │       │ Users │               │
│       └───────┘       └───────┘       └───────┘               │
│                                                                  │
│  OCA (Open Connect Appliance):                                  │
│  - Custom Netflix servers placed at ISPs                        │
│  - Pre-loaded with popular content during off-peak              │
│  - Serves 90%+ of traffic                                       │
│  - Reduces ISP bandwidth costs                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Content Placement Strategy

```
POPULARITY-BASED PLACEMENT:
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Hot Content (Top 100):                                         │
│  - Cached on ALL edge servers                                   │
│  - 90% of views                                                 │
│                                                                  │
│  Warm Content (Top 1000):                                       │
│  - Cached on regional POPs                                      │
│  - 8% of views                                                  │
│                                                                  │
│  Cold Content (Long tail):                                      │
│  - Stored at origin (S3)                                        │
│  - Fetched on demand                                            │
│  - 2% of views                                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Playback Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    VIDEO PLAYBACK FLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. User clicks "Play" on a title                               │
│                                                                  │
│  2. ┌─────────────────────────────────────────────────────────┐│
│     │ Client → Playback Service                               ││
│     │ Request: "I want to play title_123"                     ││
│     │                                                         ││
│     │ Playback Service:                                       ││
│     │ - Verify subscription status                            ││
│     │ - Get resume position (if any)                          ││
│     │ - Determine best CDN server for user                    ││
│     │ - Generate secure URL with token                        ││
│     └─────────────────────────────────────────────────────────┘│
│                         │                                       │
│                         ▼                                       │
│  3. ┌─────────────────────────────────────────────────────────┐│
│     │ Return manifest URL:                                    ││
│     │ https://cdn.netflix.com/video/123/manifest.mpd?token=xyz││
│     └─────────────────────────────────────────────────────────┘│
│                         │                                       │
│                         ▼                                       │
│  4. ┌─────────────────────────────────────────────────────────┐│
│     │ Client fetches manifest from CDN                        ││
│     │ Manifest contains:                                      ││
│     │ - List of available qualities                           ││
│     │ - Chunk URLs for each quality                           ││
│     │ - Audio track options                                   ││
│     │ - Subtitle options                                      ││
│     └─────────────────────────────────────────────────────────┘│
│                         │                                       │
│                         ▼                                       │
│  5. ┌─────────────────────────────────────────────────────────┐│
│     │ Client starts fetching video chunks                     ││
│     │                                                         ││
│     │ GET chunk_001_1080p.m4s                                ││
│     │ GET chunk_002_1080p.m4s                                ││
│     │ ...                                                     ││
│     │                                                         ││
│     │ Playback begins after initial buffer filled             ││
│     └─────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Key Data Models

### Content Metadata

```json
{
  "content_id": "title_123",
  "title": "Stranger Things",
  "type": "series",
  "seasons": [
    {
      "season_number": 1,
      "episodes": [
        {
          "episode_id": "ep_001",
          "title": "The Vanishing of Will Byers",
          "duration": 2940,
          "manifest_url": "s3://content/title_123/s01e01/manifest.mpd"
        }
      ]
    }
  ],
  "genres": ["sci-fi", "drama"],
  "maturity_rating": "TV-14"
}
```

### User Viewing History

```sql
CREATE TABLE viewing_history (
    user_id         UUID,
    content_id      TEXT,
    episode_id      TEXT,
    watch_position  INT,      -- seconds
    watch_duration  INT,
    completed       BOOLEAN,
    watched_at      TIMESTAMP,

    PRIMARY KEY (user_id, watched_at)
);
```

---

## 8. Recommendations System

```
┌─────────────────────────────────────────────────────────────────┐
│              RECOMMENDATION ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Data Sources:                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Viewing History │ Search History │ Ratings │ Demographics│   │
│  └──────────┬─────────────┬───────────┬─────────┬──────────┘   │
│             │             │           │         │               │
│             └─────────────┴───────────┴─────────┘               │
│                           │                                     │
│                    ┌──────▼──────┐                              │
│                    │   ML Models │                              │
│                    │             │                              │
│                    │- Collaborative filtering                  │
│                    │- Content-based filtering                  │
│                    │- Deep learning (personalization)          │
│                    └──────┬──────┘                              │
│                           │                                     │
│                    ┌──────▼──────┐                              │
│                    │ Recommendations                           │
│                    │             │                              │
│                    │"Because you watched..."                   │
│                    │"Top picks for you"                        │
│                    │"Trending now"                             │
│                    └─────────────┘                              │
│                                                                  │
│  Pre-computed daily, cached in Redis                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. Trade-offs

| Decision | Choice | Alternative | Reason |
|----------|--------|-------------|--------|
| CDN | Custom (Open Connect) | Third-party | Control, cost at scale |
| Streaming | DASH/HLS | Progressive | Adaptive quality |
| Storage | S3 + Edge | Central only | Global performance |
| Encoding | Per-title optimization | Fixed profiles | Bandwidth efficiency |

---

## 10. Follow-up Questions

1. "How would you handle a new season release of a popular show?"
2. "How do you ensure playback works on low-bandwidth connections?"
3. "How would you implement parental controls?"
4. "How do you handle DRM (Digital Rights Management)?"
5. "How would you design the search feature?"

---

## Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                     NETFLIX SUMMARY                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  KEY COMPONENTS:                                                │
│  ├── CDN (Open Connect) for video delivery                     │
│  ├── Adaptive bitrate streaming (ABR)                          │
│  ├── Pre-transcoded video in multiple qualities                │
│  └── ML-based recommendations                                  │
│                                                                  │
│  KEY INSIGHTS:                                                  │
│  ├── Content delivered from edge servers at ISPs               │
│  ├── Hot content pre-positioned during off-peak                │
│  ├── Client-side ABR adapts to network conditions              │
│  └── Playback service just provides URLs + tokens              │
│                                                                  │
│  SCALE:                                                         │
│  ├── 100M concurrent viewers                                   │
│  ├── 500 Pbps total bandwidth (via CDN)                        │
│  └── 300 PB content storage                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

*Next: [Design Uber](05_uber.md) →*
