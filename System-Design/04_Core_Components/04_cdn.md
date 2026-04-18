# Content Delivery Networks (CDN)

## What is a CDN?

A **Content Delivery Network** is a geographically distributed network of servers that deliver content to users from the nearest location, reducing latency and improving load times.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CDN Concept                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Without CDN:                                                         │
│   ────────────                                                          │
│                                                                         │
│   User in Tokyo ──────────────────────► Origin in New York             │
│                    12,000 km / ~200ms latency                          │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   With CDN:                                                            │
│   ─────────                                                             │
│                                                                         │
│                        ┌──────────┐                                    │
│                        │  Origin  │ (New York)                         │
│                        │  Server  │                                    │
│                        └────┬─────┘                                    │
│                             │ Replicated to                            │
│              ┌──────────────┼──────────────┐                          │
│              ▼              ▼              ▼                          │
│         ┌────────┐    ┌────────┐    ┌────────┐                       │
│         │ Edge   │    │ Edge   │    │ Edge   │                       │
│         │ Tokyo  │    │ London │    │ Sydney │                       │
│         └───┬────┘    └────────┘    └────────┘                       │
│             │                                                          │
│             │ 50km / ~10ms                                             │
│             ▼                                                          │
│        User in Tokyo                                                   │
│                                                                         │
│   Result: 95% reduction in latency!                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## How CDN Works

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CDN Request Flow                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. USER REQUEST                                                      │
│      ─────────────                                                      │
│      User requests: https://cdn.example.com/image.jpg                  │
│                                                                         │
│   2. DNS RESOLUTION                                                    │
│      ──────────────                                                     │
│      DNS returns IP of nearest edge server                             │
│      (Based on user's location via GeoDNS)                            │
│                                                                         │
│   3. EDGE SERVER CHECK (Cache Hit/Miss)                                │
│      ──────────────────────────────────                                 │
│                                                                         │
│      CACHE HIT:                      CACHE MISS:                       │
│      ──────────                      ───────────                        │
│      Content in edge cache           Edge fetches from origin          │
│            │                               │                            │
│            │ Return immediately            │                            │
│            ▼                               ▼                            │
│         ┌──────┐                      ┌─────────┐                      │
│         │ User │                      │  Origin │                      │
│         └──────┘                      └────┬────┘                      │
│                                            │                            │
│                                       Cache at edge                    │
│                                            │                            │
│                                            ▼                            │
│                                       ┌──────┐                         │
│                                       │ User │                         │
│                                       └──────┘                         │
│                                                                         │
│   Cache Hit Ratio Target: 90%+ for static content                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Types of Content

### Static Content (Ideal for CDN)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Static Content                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   • Images (JPEG, PNG, WebP, SVG)                                      │
│   • Videos (MP4, HLS/DASH streams)                                     │
│   • CSS stylesheets                                                    │
│   • JavaScript files                                                   │
│   • Fonts (WOFF, TTF)                                                 │
│   • PDFs and documents                                                 │
│   • Software downloads                                                 │
│                                                                         │
│   Characteristics:                                                      │
│   • Same content for all users                                         │
│   • Changes infrequently                                               │
│   • Large file sizes                                                   │
│   • High cache hit rate possible                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Dynamic Content

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Dynamic Content on CDN                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Can CDN cache dynamic content? Sometimes!                            │
│                                                                         │
│   1. SHORT-LIVED DYNAMIC                                               │
│      ─────────────────────                                              │
│      News articles, stock prices (cache 1-60 seconds)                  │
│      TTL: 30 seconds                                                   │
│                                                                         │
│   2. PERSONALIZED CONTENT                                              │
│      ────────────────────                                               │
│      API responses: Usually NOT cached                                 │
│      BUT: CDN can still help with:                                     │
│      • Connection pooling to origin                                    │
│      • TLS termination at edge                                         │
│      • DDoS protection                                                 │
│                                                                         │
│   3. EDGE COMPUTING                                                    │
│      ────────────────                                                   │
│      Run code at edge (Cloudflare Workers, Lambda@Edge)               │
│      Generate personalized content at edge server                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## CDN Architecture

### Push vs Pull CDN

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Push vs Pull CDN                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   PULL CDN (Most Common):                                              │
│   ───────────────────────                                               │
│                                                                         │
│   Origin uploads content as usual                                      │
│   CDN fetches content on first request (lazy loading)                  │
│                                                                         │
│   User ──► Edge ──────────────────► Origin                            │
│              │     (on cache miss)     │                               │
│              │                         │                               │
│              ◄─────────────────────────┘                               │
│              │  Cache content                                          │
│              ▼                                                         │
│           User                                                         │
│                                                                         │
│   Pros: Simple setup, automatic cache management                       │
│   Cons: First request slow (cold cache)                               │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   PUSH CDN:                                                            │
│   ──────────                                                            │
│                                                                         │
│   Origin proactively uploads content to CDN                            │
│   Content available at edge before first request                       │
│                                                                         │
│   Origin ──► Upload to all edges                                      │
│                    │                                                    │
│              ┌─────┴─────┐                                             │
│              ▼           ▼                                             │
│           Edge 1      Edge 2                                          │
│              │                                                         │
│   User ──────┘ (content already there)                                │
│                                                                         │
│   Pros: No cold cache problem                                          │
│   Cons: More complex, need to manage uploads                          │
│   Use: Large files, predictable high-demand content                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### CDN Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CDN Multi-Tier Architecture                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                          ┌─────────────┐                               │
│                          │   Origin    │                               │
│                          └──────┬──────┘                               │
│                                 │                                       │
│                    ┌────────────┴────────────┐                         │
│                    ▼                         ▼                         │
│              ┌───────────┐            ┌───────────┐                    │
│              │  Shield   │            │  Shield   │                    │
│              │ (US-East) │            │ (EU-West) │                    │
│              └─────┬─────┘            └─────┬─────┘                    │
│           ┌───────┴───────┐          ┌──────┴──────┐                  │
│           ▼               ▼          ▼             ▼                  │
│      ┌────────┐      ┌────────┐ ┌────────┐   ┌────────┐              │
│      │ Edge   │      │ Edge   │ │ Edge   │   │ Edge   │              │
│      │ NYC    │      │ Miami  │ │ London │   │ Paris  │              │
│      └────────┘      └────────┘ └────────┘   └────────┘              │
│                                                                         │
│   3-Tier Architecture:                                                 │
│   • Edge: Closest to users, highest cache volume                      │
│   • Shield: Regional cache, reduces origin load                       │
│   • Origin: Source of truth                                           │
│                                                                         │
│   Benefits:                                                            │
│   • Edge miss → Shield (not origin)                                   │
│   • Origin only queried once per region                               │
│   • 99%+ reduction in origin requests                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Cache Invalidation

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CDN Cache Invalidation                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. TTL (Time-To-Live)                                                │
│      ──────────────────                                                 │
│      Cache-Control: max-age=86400  (24 hours)                         │
│      Content automatically expires after TTL                           │
│                                                                         │
│   2. PURGE (Manual Invalidation)                                       │
│      ───────────────────────────                                        │
│      POST /purge { "url": "/image.jpg" }                              │
│      CDN removes from all edge caches                                  │
│      Warning: Can take 1-5 minutes globally                           │
│                                                                         │
│   3. VERSIONING (Best Practice)                                        │
│      ──────────────────────────                                         │
│      /static/app.v1.2.3.js                                            │
│      /static/app.v1.2.4.js  (new version = new URL)                   │
│                                                                         │
│      No invalidation needed! Old version naturally expires            │
│                                                                         │
│   4. CACHE TAGS (Advanced)                                             │
│      ─────────────────────                                              │
│      Tag content: "product-123", "category-electronics"               │
│      Purge by tag: Invalidate all product-123 related content         │
│                                                                         │
│   Best Practices:                                                       │
│   ───────────────                                                       │
│   • Use versioned URLs for static assets                               │
│   • Long TTL (1 year) for versioned content                           │
│   • Short TTL (minutes) for API responses                             │
│   • Purge only when absolutely necessary                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Security Features

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CDN Security Features                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. DDoS PROTECTION                                                   │
│      ──────────────────                                                 │
│      CDN absorbs attack traffic at edge                                │
│      Massive network capacity (Tbps)                                   │
│      Attack traffic never reaches origin                               │
│                                                                         │
│   2. WAF (Web Application Firewall)                                    │
│      ──────────────────────────────                                     │
│      Block SQL injection, XSS at edge                                  │
│      Rate limiting per IP                                              │
│      Geo-blocking                                                      │
│                                                                         │
│   3. TLS/SSL TERMINATION                                               │
│      ───────────────────────                                            │
│      HTTPS handled at edge (reduces origin CPU)                        │
│      Free certificates (Let's Encrypt integration)                     │
│      Modern protocols (TLS 1.3, HTTP/2, HTTP/3)                       │
│                                                                         │
│   4. TOKEN AUTHENTICATION                                              │
│      ────────────────────                                               │
│      Signed URLs for protected content                                 │
│      Time-limited access tokens                                        │
│      Prevent hotlinking                                                │
│                                                                         │
│   5. ORIGIN SHIELDING                                                  │
│      ────────────────────                                               │
│      Hide origin IP from public                                        │
│      Only CDN can access origin                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## CDN for Video Streaming

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Video Streaming Architecture                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Adaptive Bitrate Streaming (ABR):                                    │
│   ─────────────────────────────────                                     │
│                                                                         │
│   Original video → Transcoded to multiple qualities:                   │
│                                                                         │
│   video_1080p.m3u8  (4 Mbps)                                          │
│   video_720p.m3u8   (2 Mbps)                                          │
│   video_480p.m3u8   (1 Mbps)                                          │
│   video_240p.m3u8   (500 Kbps)                                        │
│                                                                         │
│   Player automatically switches based on bandwidth:                    │
│   ─────────────────────────────────────────────────                     │
│                                                                         │
│   Time:   0s    10s    20s    30s    40s                              │
│           │      │      │      │      │                               │
│   Quality: 720p → 1080p → 1080p → 480p → 720p                        │
│                            ↑                                           │
│                      (network congestion)                              │
│                                                                         │
│   CDN Role:                                                            │
│   • Cache video segments at edge                                       │
│   • Reduce buffering with low latency                                 │
│   • Handle millions of concurrent viewers                              │
│   • Multi-CDN for reliability                                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Popular CDN Providers

| Provider | Strengths | Best For |
|----------|-----------|----------|
| Cloudflare | Security, free tier, edge compute | General purpose, security |
| AWS CloudFront | AWS integration, Lambda@Edge | AWS users, serverless |
| Akamai | Enterprise, largest network | Large enterprise |
| Fastly | Real-time purge, edge compute | Media, real-time apps |
| Azure CDN | Azure integration | Microsoft ecosystem |
| Google Cloud CDN | GCP integration | Google Cloud users |

---

## When to Use / When NOT to Use

### When to Use CDN

✅ Global user base
✅ High traffic websites
✅ Static content heavy (images, videos, JS, CSS)
✅ Need DDoS protection
✅ Want to reduce origin load
✅ Improve SEO (Core Web Vitals)

### When NOT to Use

❌ Single region, low traffic
❌ Highly personalized content only
❌ Cost-sensitive with low volume
❌ Real-time data requirements (WebSocket heavy)
❌ Internal/private applications

---

## Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "Push vs Pull CDN?" | Understanding trade-offs | Pull is simpler; Push avoids cold cache for large files |
| "How to update cached content?" | Cache invalidation knowledge | Version URLs > Purge; TTL for API responses |
| "CDN for API responses?" | Dynamic content understanding | Yes with short TTL, or for edge compute/DDoS protection |
| "What if CDN goes down?" | Resilience thinking | Fallback to origin, multi-CDN strategy |

---

**Next:** Continue to [05_api_gateway.md](./05_api_gateway.md) to learn about API management.
