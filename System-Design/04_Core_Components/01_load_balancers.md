# Load Balancers

## What is a Load Balancer?

A **Load Balancer** distributes incoming network traffic across multiple servers to ensure no single server bears too much load. It improves availability, reliability, and performance.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Load Balancer Concept                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Without Load Balancer:             With Load Balancer:                │
│   ──────────────────────             ─────────────────────              │
│                                                                         │
│   Clients                            Clients                            │
│     │ │ │ │ │                          │ │ │ │ │                        │
│     │ │ │ │ │                          ▼ ▼ ▼ ▼ ▼                        │
│     ▼ ▼ ▼ ▼ ▼                      ┌───────────────┐                   │
│   ┌───────────┐                    │ Load Balancer │                   │
│   │  Server   │                    └───────┬───────┘                   │
│   │(overloaded)│                       ┌───┼───┐                       │
│   └───────────┘                        ▼   ▼   ▼                       │
│                                    ┌───┐ ┌───┐ ┌───┐                   │
│   Single point of failure!         │ S │ │ S │ │ S │                   │
│                                    └───┘ └───┘ └───┘                   │
│                                                                         │
│                                    Distributed load!                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Types of Load Balancers

### Layer 4 (L4) - Transport Layer

Operates at TCP/UDP level. Makes routing decisions based on IP address and port.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Layer 4 Load Balancer                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   What it sees:                                                         │
│   ─────────────                                                         │
│   • Source IP: 192.168.1.100                                           │
│   • Destination IP: 10.0.0.50                                          │
│   • Source Port: 54321                                                 │
│   • Destination Port: 443                                              │
│   • Protocol: TCP                                                      │
│                                                                         │
│   What it CANNOT see:                                                  │
│   ───────────────────                                                   │
│   • HTTP headers                                                       │
│   • URLs/paths                                                         │
│   • Cookies                                                            │
│   • Request body                                                       │
│                                                                         │
│   Pros:                          Cons:                                 │
│   ─────                          ─────                                 │
│   • Very fast (no parsing)       • Can't route by URL/content          │
│   • Low latency                  • No application awareness            │
│   • Works with any protocol      • Limited health checks               │
│                                                                         │
│   Use cases:                                                           │
│   ──────────                                                            │
│   • TCP/UDP services             • Database connections                │
│   • Real-time gaming             • Simple distribution                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Layer 7 (L7) - Application Layer

Operates at HTTP/HTTPS level. Can make intelligent routing decisions based on content.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Layer 7 Load Balancer                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   What it sees (in addition to L4):                                    │
│   ─────────────────────────────────                                     │
│   • HTTP Method: GET, POST, etc.                                       │
│   • URL Path: /api/users/123                                           │
│   • Query params: ?page=1&limit=10                                     │
│   • Headers: Host, Cookie, User-Agent                                  │
│   • Request body (for routing)                                         │
│                                                                         │
│   Capabilities:                                                         │
│   ─────────────                                                         │
│   • Route /api/* to API servers                                        │
│   • Route /static/* to CDN                                             │
│   • Route by cookie (session affinity)                                 │
│   • SSL termination                                                    │
│   • Request/response modification                                      │
│   • Content caching                                                    │
│                                                                         │
│   Pros:                          Cons:                                 │
│   ─────                          ─────                                 │
│   • Smart routing                • Higher latency (parsing)            │
│   • Content-based decisions      • More CPU intensive                  │
│   • Better health checks         • Must understand protocol            │
│   • SSL offloading               • More complex configuration          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Comparison

| Feature | Layer 4 | Layer 7 |
|---------|---------|---------|
| Speed | Faster | Slower |
| Intelligence | Low | High |
| SSL Termination | No | Yes |
| URL-based routing | No | Yes |
| Cookie stickiness | No | Yes |
| Request modification | No | Yes |
| Health checks | TCP/port | HTTP/content |
| Use case | Any protocol | HTTP/HTTPS |

---

## Load Balancing Algorithms

### 1. Round Robin

Distributes requests sequentially across servers.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Round Robin Algorithm                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Request 1 ──► Server A                                               │
│   Request 2 ──► Server B                                               │
│   Request 3 ──► Server C                                               │
│   Request 4 ──► Server A  (back to start)                              │
│   Request 5 ──► Server B                                               │
│   ...                                                                   │
│                                                                         │
│   Pros:                          Cons:                                 │
│   ─────                          ─────                                 │
│   • Simple to implement          • Ignores server capacity             │
│   • Fair distribution            • Ignores current load                │
│   • No state needed              • Bad if servers are different        │
│                                                                         │
│   Best for: Homogeneous servers with similar capacity                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2. Weighted Round Robin

Servers receive traffic proportional to their weight.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Weighted Round Robin                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Server A (weight=3): 3 requests out of every 6                       │
│   Server B (weight=2): 2 requests out of every 6                       │
│   Server C (weight=1): 1 request out of every 6                        │
│                                                                         │
│   Pattern: A, A, A, B, B, C, A, A, A, B, B, C, ...                     │
│                                                                         │
│   Use case: Different server capacities                                │
│   • Powerful server: weight=10                                         │
│   • Standard server: weight=5                                          │
│   • Small server: weight=1                                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3. Least Connections

Routes to server with fewest active connections.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Least Connections                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Current State:                                                        │
│   ──────────────                                                        │
│   Server A: 45 connections                                             │
│   Server B: 23 connections ◄── New request goes here                   │
│   Server C: 67 connections                                             │
│                                                                         │
│   Pros:                          Cons:                                 │
│   ─────                          ─────                                 │
│   • Adapts to server load        • Requires connection tracking        │
│   • Handles slow requests        • More overhead                       │
│   • Better for long connections  • May thrash on fast requests         │
│                                                                         │
│   Best for: Requests with varying processing times                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4. Weighted Least Connections

Combines connection count with server capacity weights.

```
Score = Active Connections / Weight
Route to server with lowest score

Server A: 30 connections / weight 3 = 10
Server B: 25 connections / weight 2 = 12.5
Server C: 5 connections / weight 1 = 5 ◄── Winner
```

### 5. IP Hash

Uses client IP to determine server (provides session persistence).

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    IP Hash Algorithm                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   hash(client_ip) % number_of_servers = server_index                   │
│                                                                         │
│   Client 192.168.1.1 ──► hash() % 3 = 0 ──► Server A                  │
│   Client 192.168.1.2 ──► hash() % 3 = 2 ──► Server C                  │
│   Client 192.168.1.3 ──► hash() % 3 = 1 ──► Server B                  │
│                                                                         │
│   Same client ALWAYS goes to same server                               │
│                                                                         │
│   Pros:                          Cons:                                 │
│   ─────                          ─────                                 │
│   • Session persistence          • Uneven distribution possible        │
│   • No sticky session config     • Breaks when servers change          │
│   • Predictable routing          • Can overload popular servers        │
│                                                                         │
│   Best for: Stateful applications, caching                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6. Least Response Time

Routes to server with fastest response time + fewest connections.

### 7. Random

Randomly selects a server. Simple but effective at scale.

---

## Health Checks

Load balancers must detect unhealthy servers to avoid routing traffic to them.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Health Check Types                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. TCP Health Check (L4)                                             │
│      ─────────────────────                                              │
│      LB ──► Try TCP connection to port 80                              │
│         ◄── Connection successful = healthy                            │
│                                                                         │
│   2. HTTP Health Check (L7)                                            │
│      ─────────────────────                                              │
│      LB ──► GET /health                                                │
│         ◄── 200 OK = healthy                                           │
│         ◄── 503 = unhealthy                                            │
│                                                                         │
│   3. Custom Health Check                                               │
│      ─────────────────────                                              │
│      LB ──► GET /health                                                │
│         ◄── {"status": "ok", "db": "connected", "cache": "connected"} │
│                                                                         │
│   Health Check Configuration:                                          │
│   ───────────────────────────                                           │
│   • Interval: How often to check (e.g., 30 seconds)                    │
│   • Timeout: Max wait for response (e.g., 5 seconds)                   │
│   • Healthy threshold: Successes to mark healthy (e.g., 2)             │
│   • Unhealthy threshold: Failures to mark unhealthy (e.g., 3)          │
│                                                                         │
│   Example timeline:                                                    │
│   ─────────────────                                                     │
│   Server A: ✓ ✓ ✓ ✗ ✗ ✗ [UNHEALTHY] ✓ ✓ [HEALTHY]                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Session Persistence (Sticky Sessions)

Ensures a user's requests go to the same backend server.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Sticky Sessions                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Methods:                                                              │
│   ────────                                                              │
│                                                                         │
│   1. Cookie-based (Application Cookie)                                 │
│      LB inserts cookie: SERVERID=server-a                              │
│      Subsequent requests with cookie → Server A                        │
│                                                                         │
│   2. IP-based                                                          │
│      Source IP hashed to determine server                              │
│      Problem: Users behind NAT share IP                                │
│                                                                         │
│   3. Session-aware (L7)                                                │
│      Read application session cookie                                   │
│      Map session ID to server                                          │
│                                                                         │
│   When to use:                    When to avoid:                       │
│   ────────────                    ──────────────                       │
│   • Stateful applications         • Stateless microservices            │
│   • Legacy systems                • When possible (better HA)          │
│   • WebSocket connections         • If using external session store    │
│                                                                         │
│   Problems with sticky sessions:                                       │
│   ──────────────────────────────                                        │
│   • Uneven load distribution                                           │
│   • Server failure loses sessions                                      │
│   • Harder to scale                                                    │
│   • Harder to deploy updates                                           │
│                                                                         │
│   Better alternative: External session store (Redis)                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Load Balancer Deployment Patterns

### Single Load Balancer

```
            Clients
               │
               ▼
        ┌──────────────┐
        │      LB      │ ◄── Single point of failure!
        └──────┬───────┘
          ┌────┴────┐
          ▼         ▼
      ┌──────┐  ┌──────┐
      │ Srv1 │  │ Srv2 │
      └──────┘  └──────┘
```

### Active-Passive (HA Pair)

```
            Clients
               │
               ▼
        ┌──────────────┐
        │   Active LB  │◄────┐
        └──────┬───────┘     │ Heartbeat
               │             │
        ┌──────┴───────┐     │
        │  Passive LB  │─────┘
        │  (standby)   │
        └──────────────┘

If Active fails → Passive takes over (failover)
```

### Active-Active

```
            Clients
          ┌────┴────┐
          ▼         ▼
      ┌──────┐  ┌──────┐
      │ LB 1 │  │ LB 2 │  Both handle traffic
      └──┬───┘  └──┬───┘
         └────┬────┘
              ▼
        ┌──────────┐
        │ Servers  │
        └──────────┘

DNS returns multiple LB IPs
Traffic distributed across both LBs
```

### Global Load Balancing (GSLB)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Global Server Load Balancing                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                          User in Europe                                │
│                               │                                         │
│                               ▼                                         │
│                        ┌──────────────┐                                │
│                        │     DNS      │                                │
│                        │    (GSLB)    │                                │
│                        └──────┬───────┘                                │
│               ┌───────────────┼───────────────┐                        │
│               │               │               │                        │
│               ▼               ▼               ▼                        │
│          ┌────────┐      ┌────────┐      ┌────────┐                   │
│          │ US-East│      │  EU    │      │ APAC   │                   │
│          │ Region │      │ Region │      │ Region │                   │
│          └────────┘      └───┬────┘      └────────┘                   │
│                              │                                         │
│                              ▼                                         │
│                    Routes to closest/healthiest                        │
│                                                                         │
│   GSLB Routing Methods:                                                │
│   • Geographic (closest region)                                        │
│   • Latency-based (fastest response)                                   │
│   • Weighted (traffic splitting)                                       │
│   • Failover (primary/secondary regions)                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## When to Use / When NOT to Use

### When to Use Load Balancers

✅ Multiple servers handling same traffic
✅ Need high availability (failover)
✅ Traffic exceeds single server capacity
✅ Geographic distribution needed
✅ Zero-downtime deployments required
✅ SSL termination needed
✅ Need to route by URL/content

### When NOT to Use

❌ Single server is sufficient
❌ Cost-sensitive with low traffic
❌ Peer-to-peer applications
❌ When complexity outweighs benefits

---

## Failure Modes and Mitigations

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Load Balancer Failure Modes                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Failure Mode              │ Impact           │ Mitigation            │
│   ──────────────────────────┼──────────────────┼────────────────────── │
│   LB itself fails           │ Total outage     │ Active-passive HA     │
│   Health check false pos.   │ Good server      │ Multiple checks,      │
│                             │ marked down      │ higher threshold      │
│   All backends unhealthy    │ No routing       │ Graceful degradation, │
│                             │ possible         │ backup servers        │
│   Thundering herd after     │ New servers      │ Slow start,           │
│   recovery                  │ overloaded       │ gradual ramp-up       │
│   Connection draining       │ In-flight reqs   │ Graceful shutdown,    │
│   during server removal     │ dropped          │ drain timeout         │
│   SSL/TLS issues            │ Connection       │ Cert monitoring,      │
│                             │ failures         │ auto-renewal          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Popular Implementations

| Type | Examples |
|------|----------|
| Hardware | F5 BIG-IP, Citrix ADC, A10 |
| Software | HAProxy, NGINX, Envoy, Traefik |
| Cloud | AWS ALB/NLB/ELB, GCP Load Balancing, Azure Load Balancer |
| DNS-based | AWS Route 53, Cloudflare, NS1 |

---

## Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "L4 vs L7?" | Understanding trade-offs | L4 is faster but dumber; L7 can route by content but adds latency |
| "How to handle sticky sessions at scale?" | Architecture thinking | External session store (Redis) > sticky sessions |
| "What if LB is single point of failure?" | HA awareness | HA pair (active-passive) or active-active with DNS |
| "How to do zero-downtime deployment?" | Operational knowledge | Rolling deployment with connection draining |

---

**Next:** Continue to [02_caching_systems.md](./02_caching_systems.md) to learn about caching fundamentals.
