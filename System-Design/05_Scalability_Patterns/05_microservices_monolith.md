# Microservices vs Monolith

## Overview

This is one of the most frequently asked architecture questions in system design interviews. Understanding when to use each approach—and the tradeoffs involved—is essential.

```
MONOLITH:                              MICROSERVICES:
┌─────────────────────────────┐       ┌─────────┐ ┌─────────┐ ┌─────────┐
│                             │       │  User   │ │  Order  │ │ Payment │
│    Single Application       │       │ Service │ │ Service │ │ Service │
│                             │       └────┬────┘ └────┬────┘ └────┬────┘
│  ┌───────┐ ┌───────┐       │             │          │          │
│  │ Users │ │Orders │       │             └──────────┼──────────┘
│  └───────┘ └───────┘       │                        │
│  ┌───────┐ ┌───────┐       │             ┌──────────▼──────────┐
│  │Payment│ │Notif. │       │             │    Message Bus /    │
│  └───────┘ └───────┘       │             │     API Gateway     │
│                             │             └─────────────────────┘
│     One Codebase            │             Independent Services
│     One Database            │             Own Databases
│     One Deployment          │             Separate Deployments
└─────────────────────────────┘
```

## Monolithic Architecture

### What is a Monolith?

A monolith is a single, unified application where all functionality is packaged and deployed together.

```
┌─────────────────────────────────────────────────────────────┐
│                    MONOLITHIC APP                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│   │ User Module  │  │ Order Module │  │Payment Module│     │
│   │              │  │              │  │              │     │
│   │ - Register   │  │ - Create     │  │ - Process    │     │
│   │ - Login      │  │ - Cancel     │  │ - Refund     │     │
│   │ - Profile    │  │ - History    │  │ - Validate   │     │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│          │                 │                  │              │
│          └─────────────────┼──────────────────┘              │
│                            │                                 │
│                   ┌────────▼────────┐                       │
│                   │ Shared Database │                       │
│                   └─────────────────┘                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Advantages of Monoliths

| Advantage | Explanation |
|-----------|-------------|
| **Simpler development** | One codebase, one IDE, familiar tooling |
| **Easier debugging** | Single process, stack traces make sense |
| **Simpler deployment** | One artifact to deploy |
| **No network latency** | In-process function calls |
| **Simpler transactions** | ACID across the whole application |
| **Lower operational cost** | Less infrastructure to manage |

### Disadvantages of Monoliths

| Disadvantage | Explanation |
|--------------|-------------|
| **Scaling limitations** | Must scale entire app, not just hot spots |
| **Deployment risk** | Small change = redeploy everything |
| **Technology lock-in** | Hard to adopt new languages/frameworks |
| **Team coordination** | Everyone works in same codebase |
| **Long build times** | As codebase grows, builds slow down |
| **Single point of failure** | Bug in one module can crash everything |

### When to Use a Monolith

```
┌─────────────────────────────────────────────────────────────┐
│  MONOLITH IS RIGHT WHEN:                                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✓ Small team (< 10 developers)                             │
│  ✓ New product with unclear requirements                    │
│  ✓ Simple domain with clear boundaries                      │
│  ✓ Need to move fast and iterate quickly                    │
│  ✓ Limited DevOps expertise                                 │
│  ✓ Tight budget / limited infrastructure                    │
│  ✓ Strong consistency requirements                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Microservices Architecture

### What are Microservices?

Microservices is an architectural style where an application is composed of small, independent services that communicate over a network.

```
┌─────────────────────────────────────────────────────────────────┐
│                    MICROSERVICES ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐        │
│  │ User Service │   │Order Service │   │Payment Svc   │        │
│  │              │   │              │   │              │        │
│  │ Own DB: Users│   │ Own DB: Orders│  │ Own DB: Pay  │        │
│  │ Own Team     │   │ Own Team     │   │ Own Team     │        │
│  │ Own Deploy   │   │ Own Deploy   │   │ Own Deploy   │        │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘        │
│         │                  │                   │                 │
│         │    ┌─────────────┴───────────────┐   │                │
│         └────┤       API Gateway /          ├───┘                │
│              │       Service Mesh           │                    │
│              └──────────────────────────────┘                    │
│                          │                                       │
│                    ┌─────▼─────┐                                │
│                    │  Clients  │                                │
│                    └───────────┘                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Characteristics of Microservices

| Characteristic | Description |
|---------------|-------------|
| **Single responsibility** | Each service does one thing well |
| **Independent deployment** | Deploy services without affecting others |
| **Decentralized data** | Each service owns its data |
| **Smart endpoints** | Services contain business logic |
| **Failure isolation** | One service failure doesn't crash all |
| **Technology diversity** | Each service can use different tech |

### Advantages of Microservices

| Advantage | Explanation |
|-----------|-------------|
| **Independent scaling** | Scale only what needs scaling |
| **Independent deployment** | Deploy frequently, lower risk |
| **Technology freedom** | Use best tool for each job |
| **Team autonomy** | Teams own their services end-to-end |
| **Fault isolation** | Failures are contained |
| **Easier to understand** | Smaller codebases per service |

### Disadvantages of Microservices

| Disadvantage | Explanation |
|--------------|-------------|
| **Distributed complexity** | Network failures, latency, debugging |
| **Operational overhead** | Many services to deploy, monitor |
| **Data consistency** | Eventual consistency, no ACID across services |
| **Testing complexity** | Integration tests are harder |
| **Initial development slower** | More infrastructure needed upfront |
| **Network latency** | Every call is a network call |

### When to Use Microservices

```
┌─────────────────────────────────────────────────────────────┐
│  MICROSERVICES ARE RIGHT WHEN:                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✓ Large team (> 20 developers)                             │
│  ✓ Clear domain boundaries                                  │
│  ✓ Different parts need different scaling                   │
│  ✓ Need technology flexibility                              │
│  ✓ Organization has DevOps maturity                         │
│  ✓ High availability requirements                           │
│  ✓ Frequent, independent releases needed                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Head-to-Head Comparison

| Aspect | Monolith | Microservices |
|--------|----------|---------------|
| **Deployment** | All or nothing | Independent per service |
| **Scaling** | Scale everything together | Scale what's needed |
| **Data** | Single shared database | Database per service |
| **Consistency** | Strong (ACID) | Eventual |
| **Debugging** | Single process, easier | Distributed, harder |
| **Latency** | In-process calls | Network calls |
| **Team Structure** | Central team | Autonomous teams |
| **Technology** | Single stack | Polyglot |
| **Testing** | Simpler | More complex |
| **Initial Speed** | Faster | Slower |
| **Long-term Speed** | Slows down | Maintains velocity |

---

## The Middle Ground: Modular Monolith

A modular monolith combines the deployment simplicity of a monolith with the logical separation of microservices.

```
┌─────────────────────────────────────────────────────────────┐
│                    MODULAR MONOLITH                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │                  Single Deployment                  │    │
│  │                                                     │    │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐      │    │
│  │  │   User    │  │   Order   │  │  Payment  │      │    │
│  │  │  Module   │  │  Module   │  │  Module   │      │    │
│  │  │           │  │           │  │           │      │    │
│  │  │ Clear API │  │ Clear API │  │ Clear API │      │    │
│  │  │ Boundary  │  │ Boundary  │  │ Boundary  │      │    │
│  │  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘      │    │
│  │        │              │              │             │    │
│  │  ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐      │    │
│  │  │ User DB   │  │ Order DB  │  │Payment DB │      │    │
│  │  │ (Schema)  │  │ (Schema)  │  │ (Schema)  │      │    │
│  │  └───────────┘  └───────────┘  └───────────┘      │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Benefits:                                                  │
│  - Simple deployment (like monolith)                        │
│  - Clear boundaries (like microservices)                    │
│  - Easier to extract services later                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Migration Strategies

### Monolith to Microservices

```
STRANGLER FIG PATTERN:
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  Phase 1: Identify boundaries                               │
│  ┌─────────────────────────────┐                            │
│  │         MONOLITH            │                            │
│  │  [User] [Order] [Payment]   │                            │
│  └─────────────────────────────┘                            │
│                                                              │
│  Phase 2: Extract one service                               │
│  ┌──────────────────────┐     ┌────────────┐               │
│  │      MONOLITH        │ ◄─► │   User     │               │
│  │  [Order] [Payment]   │     │  Service   │               │
│  └──────────────────────┘     └────────────┘               │
│                                                              │
│  Phase 3: Continue extraction                               │
│  ┌──────────────┐  ┌────────────┐  ┌────────────┐          │
│  │   MONOLITH   │  │   User     │  │   Order    │          │
│  │  [Payment]   │  │  Service   │  │  Service   │          │
│  └──────────────┘  └────────────┘  └────────────┘          │
│                                                              │
│  Phase 4: Complete migration                                │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │   User     │  │   Order    │  │  Payment   │            │
│  │  Service   │  │  Service   │  │  Service   │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Key Migration Steps

1. **Identify seams**: Find natural boundaries in the monolith
2. **Define APIs**: Create clear interfaces between modules
3. **Extract database**: Separate data for the module
4. **Create service**: Build the new microservice
5. **Redirect traffic**: Route requests to new service
6. **Remove old code**: Delete the code from monolith
7. **Repeat**: Continue with next service

---

## Interview Questions

### Basic
1. "What is the difference between monolith and microservices?"
2. "What are the advantages of microservices?"
3. "When would you choose a monolith over microservices?"

### Intermediate
4. "How do you handle transactions across microservices?"
5. "What is the strangler fig pattern?"
6. "How do microservices communicate?"

### Advanced
7. "You're building a new startup. Would you start with monolith or microservices? Why?"
8. "How would you migrate a 10-year-old monolith to microservices?"
9. "What are the challenges of data consistency in microservices?"

---

## Sample Interview Answer

**Q: "For a new e-commerce platform startup, would you recommend monolith or microservices?"**

**Strong Answer**:
"For a new startup, I'd strongly recommend starting with a **modular monolith** and migrating to microservices later if needed.

**Why not microservices from day one:**
1. **Speed to market**: Startups need to validate quickly. Microservices add operational overhead that slows initial development.
2. **Team size**: A small team (3-10 people) can't effectively manage multiple services.
3. **Unclear boundaries**: We don't know yet which parts will need independent scaling.
4. **Operational maturity**: Microservices require mature DevOps practices.

**How I'd structure the monolith:**
- Clear module boundaries (Users, Orders, Products, Payments)
- Clean interfaces between modules
- Separate database schemas per module
- This makes future extraction easier

**When to consider microservices:**
- When team grows past 20+ developers
- When specific components need independent scaling
- When different parts need different technology stacks
- When deployment conflicts become frequent

This approach gives us startup speed now while preserving the option to scale later."

---

## Key Takeaways

```
┌────────────────────────────────────────────────────────────────┐
│                 ARCHITECTURE DECISION FRAMEWORK                 │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  START with Monolith when:                                     │
│  └── Small team, new product, speed matters most               │
│                                                                 │
│  MOVE to Microservices when:                                   │
│  └── Large team, clear domains, scaling needs differ           │
│                                                                 │
│  CONSIDER Modular Monolith when:                               │
│  └── Want microservices benefits without operational cost      │
│                                                                 │
│  REMEMBER:                                                      │
│  └── "Microservices" is not automatically better               │
│  └── Start simple, add complexity only when needed             │
│  └── Organizational structure often dictates architecture      │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

*Next: [CQRS Pattern](06_cqrs.md) →*
