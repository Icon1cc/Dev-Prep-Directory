# API Gateway

## What is an API Gateway?

An **API Gateway** is a server that acts as the single entry point for all client requests. It handles cross-cutting concerns like authentication, rate limiting, routing, and protocol translation.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    API Gateway Concept                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Without API Gateway:                                                 │
│   ────────────────────                                                  │
│                                                                         │
│   Client must know every service:                                      │
│                                                                         │
│   Mobile App ───┬──► User Service (auth check)                        │
│                 ├──► Order Service (auth check)                       │
│                 ├──► Product Service (auth check)                     │
│                 └──► Payment Service (auth check)                     │
│                                                                         │
│   Problems:                                                            │
│   • Client complexity (multiple endpoints)                             │
│   • Duplicated auth logic                                              │
│   • No centralized rate limiting                                       │
│   • Hard to change services                                            │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   With API Gateway:                                                    │
│   ─────────────────                                                     │
│                                                                         │
│   Mobile App ──► API Gateway ──┬──► User Service                      │
│                     │          ├──► Order Service                      │
│                     │          ├──► Product Service                    │
│                     │          └──► Payment Service                    │
│                     │                                                   │
│                     ├── Authentication                                 │
│                     ├── Rate Limiting                                  │
│                     ├── Logging                                        │
│                     └── Protocol Translation                           │
│                                                                         │
│   Client only knows ONE endpoint!                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Core Responsibilities

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    API Gateway Functions                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. REQUEST ROUTING                                                   │
│      ─────────────────                                                  │
│      /api/users/*     → User Service                                   │
│      /api/orders/*    → Order Service                                  │
│      /api/products/*  → Product Service                                │
│                                                                         │
│   2. AUTHENTICATION & AUTHORIZATION                                    │
│      ─────────────────────────────────                                  │
│      Validate JWT tokens                                               │
│      Check API keys                                                    │
│      OAuth 2.0 flows                                                   │
│                                                                         │
│   3. RATE LIMITING & THROTTLING                                        │
│      ─────────────────────────────                                      │
│      100 requests/minute per user                                      │
│      1000 requests/minute per API key                                  │
│                                                                         │
│   4. REQUEST/RESPONSE TRANSFORMATION                                   │
│      ─────────────────────────────────                                  │
│      Add headers, modify payload                                       │
│      Protocol translation (REST → gRPC)                                │
│                                                                         │
│   5. LOAD BALANCING                                                    │
│      ────────────────                                                   │
│      Distribute requests across service instances                      │
│                                                                         │
│   6. CACHING                                                           │
│      ───────                                                            │
│      Cache responses at gateway level                                  │
│                                                                         │
│   7. CIRCUIT BREAKING                                                  │
│      ────────────────                                                   │
│      Prevent cascade failures                                          │
│                                                                         │
│   8. LOGGING & MONITORING                                              │
│      ─────────────────────                                              │
│      Centralized request logging                                       │
│      Metrics collection                                                │
│                                                                         │
│   9. SSL TERMINATION                                                   │
│      ────────────────                                                   │
│      Handle HTTPS at gateway                                           │
│      Internal traffic can be HTTP                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Request Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    API Gateway Request Flow                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Client Request                                                        │
│         │                                                               │
│         ▼                                                               │
│   ┌─────────────────┐                                                  │
│   │ 1. SSL/TLS      │ Terminate HTTPS                                  │
│   │    Termination  │                                                  │
│   └────────┬────────┘                                                  │
│            ▼                                                            │
│   ┌─────────────────┐                                                  │
│   │ 2. Rate         │ Check request limits                             │
│   │    Limiting     │ → 429 if exceeded                                │
│   └────────┬────────┘                                                  │
│            ▼                                                            │
│   ┌─────────────────┐                                                  │
│   │ 3. Authentication│ Validate token/key                              │
│   │                  │ → 401 if invalid                                │
│   └────────┬────────┘                                                  │
│            ▼                                                            │
│   ┌─────────────────┐                                                  │
│   │ 4. Authorization │ Check permissions                               │
│   │                  │ → 403 if forbidden                              │
│   └────────┬────────┘                                                  │
│            ▼                                                            │
│   ┌─────────────────┐                                                  │
│   │ 5. Request      │ Modify headers/body                              │
│   │    Transform    │ Add correlation ID                               │
│   └────────┬────────┘                                                  │
│            ▼                                                            │
│   ┌─────────────────┐                                                  │
│   │ 6. Routing      │ Select backend service                           │
│   │                 │ Load balance                                     │
│   └────────┬────────┘                                                  │
│            ▼                                                            │
│   ┌─────────────────┐                                                  │
│   │ 7. Backend      │ Forward to service                               │
│   │    Call         │ Circuit breaker check                            │
│   └────────┬────────┘                                                  │
│            ▼                                                            │
│   ┌─────────────────┐                                                  │
│   │ 8. Response     │ Modify response                                  │
│   │    Transform    │ Remove internal headers                          │
│   └────────┬────────┘                                                  │
│            ▼                                                            │
│   ┌─────────────────┐                                                  │
│   │ 9. Logging      │ Log request/response                             │
│   │                 │ Emit metrics                                     │
│   └────────┬────────┘                                                  │
│            ▼                                                            │
│      Client Response                                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## API Gateway Patterns

### 1. Backend for Frontend (BFF)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Backend for Frontend Pattern                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Problem: Different clients need different data formats               │
│                                                                         │
│   Mobile needs:              Web needs:                                │
│   • Compact responses        • Rich data                               │
│   • Different fields         • Different endpoints                     │
│   • Optimized for bandwidth  • Optimized for features                 │
│                                                                         │
│   Solution: Dedicated gateway per client type                          │
│                                                                         │
│   ┌──────────┐     ┌─────────────────┐                                │
│   │  Mobile  │────►│  Mobile BFF     │──┐                             │
│   │   App    │     │  (gateway)      │  │                             │
│   └──────────┘     └─────────────────┘  │                             │
│                                          │    ┌─────────────┐          │
│   ┌──────────┐     ┌─────────────────┐  ├───►│   Backend   │          │
│   │   Web    │────►│   Web BFF       │──┤    │  Services   │          │
│   │   App    │     │  (gateway)      │  │    └─────────────┘          │
│   └──────────┘     └─────────────────┘  │                             │
│                                          │                             │
│   ┌──────────┐     ┌─────────────────┐  │                             │
│   │   IoT    │────►│   IoT BFF       │──┘                             │
│   │ Devices  │     │  (gateway)      │                                │
│   └──────────┘     └─────────────────┘                                │
│                                                                         │
│   Each BFF is optimized for its client                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2. Gateway Aggregation

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Gateway Aggregation Pattern                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Problem: Client needs data from multiple services                    │
│                                                                         │
│   Without aggregation:                                                 │
│   Client → GET /users/123                                              │
│   Client → GET /orders?userId=123                                      │
│   Client → GET /recommendations?userId=123                             │
│   (3 round trips!)                                                     │
│                                                                         │
│   With aggregation:                                                    │
│   Client → GET /dashboard/123                                          │
│                                                                         │
│        API Gateway                                                      │
│             │                                                           │
│        ┌────┼────┐                                                     │
│        ▼    ▼    ▼  (parallel calls)                                  │
│   ┌──────┐┌──────┐┌──────────────┐                                    │
│   │Users ││Orders││Recommendations│                                    │
│   └──────┘└──────┘└──────────────┘                                    │
│        │    │    │                                                     │
│        └────┴────┘                                                     │
│             │                                                           │
│        Aggregated Response                                             │
│             │                                                           │
│        Client (1 round trip!)                                          │
│                                                                         │
│   Response:                                                            │
│   {                                                                    │
│     "user": { ... },                                                   │
│     "orders": [ ... ],                                                 │
│     "recommendations": [ ... ]                                         │
│   }                                                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3. Gateway Offloading

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Gateway Offloading                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Move cross-cutting concerns to gateway:                              │
│                                                                         │
│   BEFORE (each service handles):    AFTER (gateway handles):           │
│   ──────────────────────────────    ─────────────────────────          │
│                                                                         │
│   Service A:                        Gateway:                           │
│   ├── SSL termination               ├── SSL termination               │
│   ├── Authentication                ├── Authentication                │
│   ├── Rate limiting                 ├── Rate limiting                 │
│   ├── Logging                       ├── Logging                       │
│   └── Business logic                └── Routing                       │
│                                                                         │
│   Service B:                        Service A:                         │
│   ├── SSL termination               └── Business logic only           │
│   ├── Authentication                                                   │
│   ├── Rate limiting                 Service B:                         │
│   ├── Logging                       └── Business logic only           │
│   └── Business logic                                                   │
│                                                                         │
│   Benefits:                                                            │
│   • Services are simpler                                               │
│   • Consistent security policies                                       │
│   • Easier to update policies                                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Rate Limiting at Gateway

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Gateway Rate Limiting                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Rate Limit Types:                                                    │
│   ─────────────────                                                     │
│                                                                         │
│   1. Per User                                                          │
│      X-RateLimit-Limit: 100                                           │
│      X-RateLimit-Remaining: 45                                        │
│      X-RateLimit-Reset: 1609459200                                    │
│                                                                         │
│   2. Per API Key                                                       │
│      Free tier: 1000/day                                              │
│      Pro tier: 10000/day                                              │
│      Enterprise: Unlimited                                             │
│                                                                         │
│   3. Per Endpoint                                                      │
│      POST /login: 5/minute (prevent brute force)                      │
│      GET /search: 60/minute                                           │
│      POST /payments: 10/minute                                        │
│                                                                         │
│   4. Global                                                            │
│      Total API: 1M requests/minute                                    │
│                                                                         │
│   Response when exceeded:                                              │
│   ───────────────────────                                               │
│   HTTP 429 Too Many Requests                                          │
│   {                                                                    │
│     "error": "rate_limit_exceeded",                                   │
│     "retry_after": 30                                                  │
│   }                                                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Authentication Patterns

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    API Gateway Authentication                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. API KEY                                                           │
│      ───────                                                            │
│      Header: X-API-Key: sk_live_abc123                                │
│      Simple, for server-to-server                                      │
│                                                                         │
│   2. JWT (JSON Web Token)                                              │
│      ─────────────────────                                              │
│      Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIs...            │
│      Gateway validates signature, extracts claims                      │
│      No database lookup needed                                         │
│                                                                         │
│   3. OAuth 2.0                                                         │
│      ──────────                                                         │
│      Gateway acts as resource server                                   │
│      Validates access tokens with auth server                          │
│                                                                         │
│   JWT Validation Flow:                                                 │
│   ────────────────────                                                  │
│                                                                         │
│   Client ──► Gateway                                                   │
│              │                                                          │
│              ├── 1. Extract JWT from header                            │
│              ├── 2. Verify signature (no network call!)               │
│              ├── 3. Check expiration                                   │
│              ├── 4. Extract user ID, roles                            │
│              ├── 5. Add user context to request                       │
│              │                                                          │
│              └──► Backend Service (request includes user context)      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Popular API Gateways

| Gateway | Type | Best For |
|---------|------|----------|
| Kong | Open Source | Kubernetes, plugins |
| AWS API Gateway | Managed | AWS ecosystem, serverless |
| NGINX | Open Source | High performance, simple |
| Apigee | Managed | Enterprise, analytics |
| Envoy | Open Source | Service mesh, Kubernetes |
| Azure API Management | Managed | Azure ecosystem |
| Traefik | Open Source | Kubernetes, Docker |

---

## When to Use / When NOT to Use

### When to Use API Gateway

✅ Microservices architecture
✅ Multiple client types (web, mobile, IoT)
✅ Need centralized auth/rate limiting
✅ API versioning required
✅ Request/response transformation needed
✅ Multiple backend services

### When NOT to Use

❌ Simple monolith
❌ Single client type
❌ Low traffic (added latency not worth it)
❌ Internal services only
❌ When it becomes a bottleneck

---

## Failure Modes and Mitigations

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    API Gateway Failure Modes                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Failure Mode           │ Impact          │ Mitigation                │
│   ───────────────────────┼─────────────────┼────────────────────────── │
│   Gateway overloaded     │ All APIs slow   │ Horizontal scaling,       │
│                          │                 │ auto-scaling              │
│   Gateway crashes        │ Total outage    │ Multiple instances,       │
│                          │                 │ health checks             │
│   Backend timeout        │ Slow responses  │ Circuit breaker,          │
│                          │                 │ timeout settings          │
│   Auth service down      │ No new requests │ Token caching,            │
│                          │                 │ graceful degradation      │
│   Rate limiter issues    │ False positives │ Distributed rate limiting,│
│                          │                 │ Redis cluster             │
│                                                                         │
│   Gateway becomes single point of failure!                             │
│   ──────────────────────────────────────────                            │
│   Solution:                                                            │
│   • Multiple gateway instances behind load balancer                   │
│   • Geographic distribution                                            │
│   • Health checks at all layers                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "Gateway vs Load Balancer?" | Understanding scope | LB distributes traffic; Gateway adds auth, transformation, routing logic |
| "How to prevent gateway bottleneck?" | Scalability thinking | Horizontal scaling, keep gateway thin, offload to services |
| "Gateway for internal services?" | Architecture judgment | Usually no—adds latency; use service mesh instead |
| "JWT vs API Key?" | Security knowledge | JWT for user auth (stateless); API Key for service auth (simpler) |

---

**Next:** Continue to [06_distributed_databases.md](./06_distributed_databases.md) to learn about data at scale.
