# Backpressure Handling

## What is Backpressure?

**Simple explanation**: Backpressure occurs when a system receives more data than it can process. It's like a traffic jam—cars (data) arrive faster than the road (system) can handle.

**Technical definition**: Backpressure is a flow control mechanism where a slower consumer signals to a faster producer to slow down, preventing system overload and data loss.

```
WITHOUT BACKPRESSURE:
┌──────────────┐         ┌──────────────┐
│   Producer   │ ══════► │   Consumer   │
│  1000 req/s  │         │  100 req/s   │  ← Can't keep up!
└──────────────┘         └──────────────┘
                                │
                                ▼
                         Overwhelmed → Crash or data loss

WITH BACKPRESSURE:
┌──────────────┐         ┌──────────────┐
│   Producer   │ ══════► │   Consumer   │
│  1000 req/s  │ ◄══════ │  100 req/s   │  ← "Slow down!"
│ → 100 req/s  │         │              │
└──────────────┘         └──────────────┘
                                │
                                ▼
                         Controlled flow → System survives
```

## Why Backpressure Matters

### The Problem

```
┌─────────────────────────────────────────────────────────────────┐
│                    WITHOUT BACKPRESSURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Time 0:     Producer ──► [Queue: ████        ] ──► Consumer   │
│                                                                  │
│  Time 1:     Producer ──► [Queue: ████████    ] ──► Consumer   │
│                                                                  │
│  Time 2:     Producer ──► [Queue: ████████████] ──► Consumer   │
│                                    FULL!                        │
│  Time 3:     What happens now?                                  │
│              ├── Drop messages? (Data loss!)                    │
│              ├── Block producer? (Upstream backup)              │
│              └── OOM crash? (System failure)                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Common Causes

| Cause | Example |
|-------|---------|
| **Traffic spikes** | Flash sale, viral content |
| **Slow consumers** | Database writes slower than API calls |
| **Resource constraints** | Limited memory, CPU, connections |
| **Cascade failures** | Downstream service slow/down |

## Backpressure Strategies

### 1. Dropping (Load Shedding)

When overwhelmed, drop excess requests.

```
┌─────────────────────────────────────────────────────────────────┐
│                        LOAD SHEDDING                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Incoming:  ────────────────────────────────────                │
│             ████████████████████████████████                    │
│             1000 requests/second                                │
│                                                                  │
│  Capacity:  100 req/s                                           │
│                                                                  │
│  Strategy:  Accept first 100, drop rest (900)                   │
│             ██████████ ╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳                   │
│             Accepted   Dropped (return 503)                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Implementation**:
```python
class LoadShedder:
    def __init__(self, max_concurrent: int):
        self.max_concurrent = max_concurrent
        self.current = 0
        self.lock = Lock()

    def try_acquire(self) -> bool:
        with self.lock:
            if self.current < self.max_concurrent:
                self.current += 1
                return True
            return False  # Shed load

    def release(self):
        with self.lock:
            self.current -= 1

# Usage
shedder = LoadShedder(max_concurrent=100)

def handle_request(request):
    if not shedder.try_acquire():
        return Response(status=503, body="Service overloaded")
    try:
        return process_request(request)
    finally:
        shedder.release()
```

**Pros**: Simple, protects system
**Cons**: Lost data/requests

---

### 2. Buffering

Store excess work in a queue for later processing.

```
┌─────────────────────────────────────────────────────────────────┐
│                         BUFFERING                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Producer           Buffer               Consumer               │
│  ┌────────┐    ┌─────────────────┐    ┌────────┐               │
│  │ 1000/s │───►│ ████████████    │───►│ 100/s  │               │
│  └────────┘    │ Bounded Queue   │    └────────┘               │
│                │ (Max 10,000)    │                              │
│                └─────────────────┘                              │
│                                                                  │
│  Behavior:                                                      │
│  - Accept requests into buffer                                  │
│  - Consumer processes at own pace                               │
│  - If buffer full → apply other strategy (drop/block)          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Implementation**:
```python
from queue import Queue, Full

class BufferedProcessor:
    def __init__(self, buffer_size: int):
        self.buffer = Queue(maxsize=buffer_size)

    def submit(self, item) -> bool:
        try:
            self.buffer.put_nowait(item)
            return True
        except Full:
            return False  # Buffer full

    def process_loop(self):
        while True:
            item = self.buffer.get()  # Blocks if empty
            self.process(item)
            self.buffer.task_done()
```

**Pros**: Handles bursts, no immediate data loss
**Cons**: Added latency, memory pressure

---

### 3. Throttling (Rate Limiting)

Limit the rate at which requests are accepted.

```
┌─────────────────────────────────────────────────────────────────┐
│                        THROTTLING                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Token Bucket Algorithm:                                        │
│                                                                  │
│  ┌─────────────────┐                                            │
│  │  Token Bucket   │  Tokens added at fixed rate (100/sec)     │
│  │  ○ ○ ○ ○ ○ ○   │                                            │
│  │  ○ ○ ○ ○       │  Max capacity: 100 tokens                  │
│  └────────┬────────┘                                            │
│           │                                                      │
│  Request arrives:                                               │
│  ├── Tokens available? → Take token, process request           │
│  └── No tokens? → Reject or wait                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Pros**: Predictable load, fair distribution
**Cons**: May reject valid requests during bursts

---

### 4. Blocking (Synchronous Backpressure)

Producer waits until consumer is ready.

```
┌─────────────────────────────────────────────────────────────────┐
│                         BLOCKING                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Time 1:  Producer ──(send)──► Consumer                        │
│                                     │                           │
│  Time 2:  Producer    (wait)   Consumer (processing)           │
│                │                    │                           │
│  Time 3:  Producer ◄──(ready)─ Consumer                        │
│                                     │                           │
│  Time 4:  Producer ──(send)──► Consumer                        │
│                                                                  │
│  Producer naturally slows to consumer's pace                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Pros**: Natural flow control, no data loss
**Cons**: Producer blocked, cascade slowdown

---

### 5. Reactive Streams / Pull-Based

Consumer requests data when ready.

```
┌─────────────────────────────────────────────────────────────────┐
│                    PULL-BASED (REACTIVE)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Traditional (Push):                                            │
│  Producer ══════════════════════════════════► Consumer          │
│           "Here's 1000 items, deal with it!"                    │
│                                                                  │
│  Reactive (Pull):                                               │
│  Producer ◄────────────────────────────────── Consumer          │
│           "I'm ready for 10 more items"                         │
│  Producer ──────────────────────────────────► Consumer          │
│           "Here are 10 items"                                   │
│                                                                  │
│  Consumer controls the pace!                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Implementation** (Reactive Streams):
```python
class ReactiveConsumer:
    def __init__(self, processor, batch_size: int = 10):
        self.processor = processor
        self.batch_size = batch_size

    def subscribe(self, publisher):
        self.subscription = publisher.subscribe(self)
        self.request_more()

    def on_next(self, items):
        for item in items:
            self.processor.process(item)
        self.request_more()  # Pull next batch

    def request_more(self):
        self.subscription.request(self.batch_size)
```

**Pros**: Consumer controls pace, efficient
**Cons**: More complex implementation

## Comparison

| Strategy | Data Loss | Latency | Complexity | Use Case |
|----------|-----------|---------|------------|----------|
| **Dropping** | Yes | Low | Low | Acceptable loss |
| **Buffering** | If full | Variable | Medium | Burst handling |
| **Throttling** | Rejected | Low | Medium | Rate limiting |
| **Blocking** | No | High | Low | Sync systems |
| **Reactive** | No | Low | High | Streaming |

## Interview Questions

1. "What is backpressure and why is it important?"
2. "How would you handle a traffic spike that's 10x normal load?"
3. "Compare different backpressure strategies."

## Key Takeaways

```
┌────────────────────────────────────────────────────────────────┐
│                  BACKPRESSURE SUMMARY                           │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  THE PROBLEM:                                                  │
│  └── Producer faster than consumer = system overload          │
│                                                                 │
│  STRATEGIES:                                                   │
│  ├── Drop: Shed load, accept loss                             │
│  ├── Buffer: Queue for later, bounded size                    │
│  ├── Throttle: Rate limit incoming requests                   │
│  ├── Block: Producer waits for consumer                       │
│  └── Pull: Consumer requests when ready                       │
│                                                                 │
│  BEST PRACTICE:                                                │
│  └── Combine strategies: Buffer + Drop when full              │
│  └── Monitor queue depths as health metric                    │
│  └── Set timeouts to prevent infinite waits                   │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

*Next: [Circuit Breakers](09_circuit_breakers.md) →*
