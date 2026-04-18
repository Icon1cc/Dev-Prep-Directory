# Circuit Breakers

## What is a Circuit Breaker?

**Simple explanation**: A circuit breaker stops calling a failing service, preventing wasted resources and allowing the service time to recover. Like an electrical circuit breaker that trips to prevent fires, it protects your system from cascading failures.

**Technical definition**: The Circuit Breaker pattern prevents an application from repeatedly trying to execute an operation that's likely to fail, allowing it to continue without waiting for the fault to be fixed.

```
WITHOUT CIRCUIT BREAKER:
┌──────────┐         ┌──────────────────────┐
│  Client  │────────►│  Failing Service     │
│          │  wait   │  (Down or Slow)      │
│          │◄────────│                      │
│          │ timeout │  Every request waits │
│          │────────►│  for timeout         │
│          │  wait   │                      │
│          │◄────────│  Resources exhausted!│
└──────────┘         └──────────────────────┘

WITH CIRCUIT BREAKER:
┌──────────┐    ┌─────────────┐    ┌──────────────────────┐
│  Client  │───►│   Circuit   │───►│  Failing Service     │
│          │    │   Breaker   │    │  (Down or Slow)      │
│          │◄───│             │    │                      │
│          │    │ OPEN: Fail  │    │                      │
│          │    │ fast, don't │    │                      │
│          │    │ even try!   │    │                      │
└──────────┘    └─────────────┘    └──────────────────────┘
```

## Why Circuit Breakers?

### The Cascade Failure Problem

```
┌─────────────────────────────────────────────────────────────────┐
│                   CASCADE FAILURE                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Service A ──► Service B ──► Service C ──► Database             │
│                                              │                   │
│                                              ▼                   │
│                                         DATABASE DOWN            │
│                                              │                   │
│  What happens:                               │                   │
│  1. Service C waits for DB timeout          ◄┘                  │
│  2. Service C threads exhausted                                 │
│  3. Service B waits for Service C                               │
│  4. Service B threads exhausted                                 │
│  5. Service A waits for Service B                               │
│  6. Service A threads exhausted                                 │
│  7. ENTIRE SYSTEM DOWN!                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Circuit Breaker Prevents This

```
┌─────────────────────────────────────────────────────────────────┐
│                 WITH CIRCUIT BREAKER                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Service A ──► Service B ──► [CB] ──► Service C ──► Database   │
│                               │                      │          │
│                               │                      ▼          │
│                          OPEN!               DATABASE DOWN      │
│                               │                                  │
│  What happens:                │                                  │
│  1. Service C fails a few times                                 │
│  2. Circuit breaker OPENS                                       │
│  3. Subsequent calls fail FAST (no waiting)                     │
│  4. Service B handles error gracefully                          │
│  5. System stays healthy!                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Circuit Breaker States

```
┌─────────────────────────────────────────────────────────────────┐
│                 CIRCUIT BREAKER STATES                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────┐         ┌────────────────┐                  │
│  │     CLOSED     │         │      OPEN      │                  │
│  │  (Normal)      │         │  (Fail Fast)   │                  │
│  │                │         │                │                  │
│  │ Requests pass  │         │ Requests fail  │                  │
│  │ through        │         │ immediately    │                  │
│  └───────┬────────┘         └───────┬────────┘                  │
│          │                          │                           │
│          │ Failure threshold        │ Timeout expires           │
│          │ exceeded                 │                           │
│          ▼                          ▼                           │
│          └──────────┐    ┌──────────┘                          │
│                     │    │                                      │
│                     ▼    ▼                                      │
│              ┌────────────────┐                                 │
│              │   HALF-OPEN    │                                 │
│              │  (Testing)     │                                 │
│              │                │                                 │
│              │ Allow ONE test │                                 │
│              │ request        │                                 │
│              └───────┬────────┘                                 │
│                      │                                          │
│          ┌───────────┴───────────┐                             │
│          │                       │                              │
│      Success                  Failure                          │
│          │                       │                              │
│          ▼                       ▼                              │
│      CLOSED                    OPEN                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### State Transitions

| From State | Trigger | To State |
|------------|---------|----------|
| CLOSED | Failure threshold exceeded | OPEN |
| OPEN | Timeout expires | HALF-OPEN |
| HALF-OPEN | Test request succeeds | CLOSED |
| HALF-OPEN | Test request fails | OPEN |

## Implementation

### Basic Circuit Breaker

```python
from enum import Enum
from time import time
from threading import Lock

class State(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception

        self.state = State.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.lock = Lock()

    def call(self, func, *args, **kwargs):
        with self.lock:
            if self.state == State.OPEN:
                if self._should_attempt_reset():
                    self.state = State.HALF_OPEN
                else:
                    raise CircuitOpenError("Circuit is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        with self.lock:
            self.failure_count = 0
            self.state = State.CLOSED

    def _on_failure(self):
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time()

            if self.failure_count >= self.failure_threshold:
                self.state = State.OPEN

    def _should_attempt_reset(self) -> bool:
        return time() - self.last_failure_time >= self.recovery_timeout


# Usage
cb = CircuitBreaker(failure_threshold=5, recovery_timeout=30)

def get_user(user_id):
    return cb.call(external_service.get_user, user_id)
```

### With Fallback

```python
def get_user_with_fallback(user_id):
    try:
        return cb.call(external_service.get_user, user_id)
    except CircuitOpenError:
        # Return cached data or default
        return cache.get(f"user:{user_id}") or DEFAULT_USER
```

## Configuration Best Practices

```
┌─────────────────────────────────────────────────────────────────┐
│                  CONFIGURATION GUIDE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Failure Threshold:                                             │
│  ├── Too low (1-2): Opens on transient errors                   │
│  ├── Too high (50+): Takes too long to open                     │
│  └── Good: 5-10 failures                                        │
│                                                                  │
│  Recovery Timeout:                                              │
│  ├── Too short (1-5s): Hammers recovering service               │
│  ├── Too long (5min+): Slow recovery                            │
│  └── Good: 30-60 seconds                                        │
│                                                                  │
│  Monitoring Window:                                             │
│  └── Count failures within window (e.g., last 60 seconds)       │
│  └── Prevents old failures from keeping circuit open            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Popular Libraries

| Language | Library | Example |
|----------|---------|---------|
| Java | Resilience4j | `CircuitBreaker.ofDefaults("name")` |
| Python | pybreaker | `@circuit(failure_threshold=5)` |
| Go | sony/gobreaker | `gobreaker.NewCircuitBreaker(settings)` |
| .NET | Polly | `Policy.Handle<Exception>().CircuitBreaker()` |

## Interview Questions

1. "What is a circuit breaker and why would you use it?"
2. "Explain the three states of a circuit breaker."
3. "How would you configure a circuit breaker for a payment service?"

## Key Takeaways

```
┌────────────────────────────────────────────────────────────────┐
│                 CIRCUIT BREAKER SUMMARY                         │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PURPOSE:                                                      │
│  └── Prevent cascade failures by failing fast                 │
│  └── Give failing services time to recover                    │
│                                                                 │
│  STATES:                                                       │
│  ├── CLOSED: Normal operation, requests pass through          │
│  ├── OPEN: Fail fast, don't call downstream                   │
│  └── HALF-OPEN: Test if service has recovered                 │
│                                                                 │
│  BEST PRACTICES:                                               │
│  ├── Always have a fallback strategy                          │
│  ├── Monitor circuit state as a health metric                 │
│  ├── Tune thresholds based on service characteristics         │
│  └── Combine with timeouts and retries                        │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

*Next: [Bulkhead Pattern](10_bulkheads.md) →*
