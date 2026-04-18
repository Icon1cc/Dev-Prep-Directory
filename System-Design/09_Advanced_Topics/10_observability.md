# Observability in Distributed Systems

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           OBSERVABILITY                                       ║
║              Understanding What's Happening in Production                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## What is Observability?

Observability is the ability to understand the internal state of a system by examining its outputs. In distributed systems, this is critical because you can't just attach a debugger or look at a single log file.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    THE THREE PILLARS OF OBSERVABILITY                        │
│                                                                              │
│                         OBSERVABILITY                                        │
│                              │                                               │
│              ┌───────────────┼───────────────┐                              │
│              │               │               │                              │
│              ▼               ▼               ▼                              │
│         ┌────────┐     ┌────────┐     ┌────────┐                           │
│         │ LOGS   │     │METRICS │     │TRACES  │                           │
│         └────────┘     └────────┘     └────────┘                           │
│              │               │               │                              │
│              ▼               ▼               ▼                              │
│         What        How well is     What path                              │
│         happened?   the system      did the                                │
│                     performing?     request take?                          │
│                                                                              │
│  ANALOGY:                                                                   │
│  ├── Logs: Diary entries (detailed events)                                 │
│  ├── Metrics: Dashboard gauges (aggregated numbers)                        │
│  └── Traces: GPS breadcrumbs (request journey)                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Pillar 1: Logging

### Structured Logging

```python
import json
import logging
import time
from typing import Any, Dict
import uuid

class StructuredLogger:
    """
    Structured logging for distributed systems
    """

    def __init__(self, service_name: str, version: str):
        self.service_name = service_name
        self.version = version
        self.logger = logging.getLogger(service_name)

    def log(self, level: str, message: str, **context):
        """
        Log with structured context
        """
        log_entry = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'level': level,
            'service': self.service_name,
            'version': self.version,
            'message': message,
            **context
        }

        # JSON format for easy parsing
        self.logger.log(
            getattr(logging, level.upper()),
            json.dumps(log_entry)
        )

    def info(self, message: str, **context):
        self.log('info', message, **context)

    def error(self, message: str, **context):
        self.log('error', message, **context)

    def with_context(self, **base_context):
        """Create a child logger with preset context"""
        return ContextualLogger(self, base_context)


class ContextualLogger:
    """Logger with preset context (e.g., request_id, user_id)"""

    def __init__(self, parent: StructuredLogger, context: Dict):
        self.parent = parent
        self.context = context

    def info(self, message: str, **extra_context):
        self.parent.info(message, **self.context, **extra_context)

    def error(self, message: str, **extra_context):
        self.parent.error(message, **self.context, **extra_context)


# Usage example
logger = StructuredLogger('order-service', 'v2.1.0')

def process_order(order_id: str, user_id: str):
    request_id = str(uuid.uuid4())

    # Create contextual logger for this request
    req_logger = logger.with_context(
        request_id=request_id,
        order_id=order_id,
        user_id=user_id
    )

    req_logger.info('Processing order started')

    try:
        # Process order...
        req_logger.info('Payment processed', amount=99.99, currency='USD')
        req_logger.info('Inventory reserved', items=['item1', 'item2'])
        req_logger.info('Order completed', status='success')

    except Exception as e:
        req_logger.error('Order failed',
                        error_type=type(e).__name__,
                        error_message=str(e))
        raise
```

### Log Levels and When to Use Them

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      LOG LEVELS GUIDE                                        │
│                                                                              │
│  LEVEL      │ WHEN TO USE                        │ EXAMPLE                  │
│  ═══════════╪════════════════════════════════════╪════════════════════════ │
│  DEBUG      │ Detailed diagnostic info           │ "Variable x = 42"        │
│             │ Usually disabled in production     │                          │
│  ───────────┼────────────────────────────────────┼────────────────────────│ │
│  INFO       │ Normal operations                  │ "Order 123 created"      │
│             │ Audit trail, business events       │ "User logged in"         │
│  ───────────┼────────────────────────────────────┼────────────────────────│ │
│  WARN       │ Potential issues, recoverable      │ "Retry attempt 2 of 3"  │
│             │ Degraded but working               │ "Cache miss, using DB"   │
│  ───────────┼────────────────────────────────────┼────────────────────────│ │
│  ERROR      │ Request failed, needs attention    │ "Payment declined"       │
│             │ Doesn't crash the service          │ "DB connection failed"   │
│  ───────────┼────────────────────────────────────┼────────────────────────│ │
│  FATAL      │ Service must stop                  │ "Out of memory"          │
│             │ Unrecoverable state                │ "Config file missing"    │
│                                                                              │
│  RULE OF THUMB:                                                             │
│  ├── DEBUG: 10-100x INFO volume (disabled in prod)                         │
│  ├── INFO: Normal operation audit trail                                    │
│  ├── WARN: 1-10% of INFO volume                                           │
│  ├── ERROR: <1% of requests                                                │
│  └── FATAL: Hopefully never                                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Pillar 2: Metrics

### Types of Metrics

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      METRIC TYPES                                            │
│                                                                              │
│  1. COUNTER                                                                 │
│     ─────────                                                               │
│     Monotonically increasing value                                          │
│     Example: Total requests, errors, bytes sent                             │
│                                                                              │
│     requests_total{service="api", endpoint="/users"} 142857                │
│                                                                              │
│  2. GAUGE                                                                   │
│     ─────                                                                   │
│     Value that goes up and down                                             │
│     Example: Current connections, queue size, memory                        │
│                                                                              │
│     active_connections{service="api"} 42                                   │
│                                                                              │
│  3. HISTOGRAM                                                               │
│     ─────────                                                               │
│     Distribution of values in buckets                                       │
│     Example: Request latency distribution                                   │
│                                                                              │
│     request_duration_bucket{le="0.1"} 24054                                │
│     request_duration_bucket{le="0.5"} 33025                                │
│     request_duration_bucket{le="1.0"} 34012                                │
│                                                                              │
│  4. SUMMARY                                                                 │
│     ───────                                                                 │
│     Calculated percentiles                                                  │
│     Example: P50, P95, P99 latencies                                       │
│                                                                              │
│     request_duration{quantile="0.5"} 0.042                                 │
│     request_duration{quantile="0.95"} 0.12                                 │
│     request_duration{quantile="0.99"} 0.31                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Implementing Metrics

```python
import time
from typing import Dict, List
from collections import defaultdict
import threading

class MetricsCollector:
    """
    Simple metrics collector (production: use Prometheus, StatsD, etc.)
    """

    def __init__(self):
        self.counters: Dict[str, float] = defaultdict(float)
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = defaultdict(list)
        self.lock = threading.Lock()

    def increment_counter(self, name: str, value: float = 1,
                          labels: Dict = None):
        """Increment a counter metric"""
        key = self._make_key(name, labels)
        with self.lock:
            self.counters[key] += value

    def set_gauge(self, name: str, value: float, labels: Dict = None):
        """Set a gauge metric"""
        key = self._make_key(name, labels)
        with self.lock:
            self.gauges[key] = value

    def observe_histogram(self, name: str, value: float,
                          labels: Dict = None):
        """Record a histogram observation"""
        key = self._make_key(name, labels)
        with self.lock:
            self.histograms[key].append(value)

    def _make_key(self, name: str, labels: Dict = None) -> str:
        if not labels:
            return name
        label_str = ','.join(f'{k}="{v}"' for k, v in sorted(labels.items()))
        return f'{name}{{{label_str}}}'

    def get_percentile(self, name: str, percentile: float,
                       labels: Dict = None) -> float:
        """Calculate percentile from histogram"""
        key = self._make_key(name, labels)
        with self.lock:
            values = sorted(self.histograms.get(key, []))

        if not values:
            return 0

        index = int(len(values) * percentile / 100)
        return values[min(index, len(values) - 1)]


class Timer:
    """Context manager for timing operations"""

    def __init__(self, metrics: MetricsCollector, name: str,
                 labels: Dict = None):
        self.metrics = metrics
        self.name = name
        self.labels = labels
        self.start = None

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        duration = time.time() - self.start
        self.metrics.observe_histogram(self.name, duration, self.labels)


# Usage example
metrics = MetricsCollector()

def handle_request(endpoint: str):
    labels = {'endpoint': endpoint, 'service': 'api'}

    # Count request
    metrics.increment_counter('http_requests_total', labels=labels)

    # Time the request
    with Timer(metrics, 'http_request_duration_seconds', labels):
        # Process request
        result = process_request()

    # Record response status
    metrics.increment_counter('http_responses_total',
                             labels={**labels, 'status': '200'})

    return result
```

### The RED Method (Request-focused)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        THE RED METHOD                                        │
│                   (For Request-Driven Services)                              │
│                                                                              │
│  R - RATE                                                                   │
│      The number of requests per second                                      │
│      http_requests_total / time                                             │
│                                                                              │
│  E - ERRORS                                                                 │
│      The number of failed requests per second                               │
│      http_errors_total / time                                               │
│      Error rate: errors / total requests                                    │
│                                                                              │
│  D - DURATION                                                               │
│      Distribution of request latencies                                      │
│      P50, P95, P99 of http_request_duration                                │
│                                                                              │
│  DASHBOARD EXAMPLE:                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Rate: 1,247 req/s    Errors: 0.3%    P99 Latency: 127ms          │   │
│  │                                                                     │   │
│  │  ████████████████████████████████████████                         │   │
│  │  Rate over time                                                    │   │
│  │                                                                     │   │
│  │  ─────────────────────────────────────────                         │   │
│  │  P99 latency over time                                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### The USE Method (Resource-focused)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        THE USE METHOD                                        │
│                   (For Resource Monitoring)                                  │
│                                                                              │
│  U - UTILIZATION                                                            │
│      Percentage of resource being used                                      │
│      CPU: 65%                                                               │
│      Memory: 78%                                                            │
│      Disk: 42%                                                              │
│                                                                              │
│  S - SATURATION                                                             │
│      How much extra work is queued                                          │
│      CPU run queue length                                                   │
│      Memory swap usage                                                      │
│      Network queue depth                                                    │
│                                                                              │
│  E - ERRORS                                                                 │
│      Error events for the resource                                          │
│      Disk I/O errors                                                        │
│      Network packet drops                                                   │
│      Memory allocation failures                                             │
│                                                                              │
│  COMBINE BOTH:                                                              │
│  ├── RED for service health                                                │
│  └── USE for infrastructure health                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Pillar 3: Distributed Tracing

### How Tracing Works

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DISTRIBUTED TRACING CONCEPTS                              │
│                                                                              │
│  TRACE: The entire journey of a request                                     │
│  SPAN: A single operation within a trace                                    │
│                                                                              │
│  Request: GET /user/123/orders                                              │
│                                                                              │
│  Trace ID: abc123                                                           │
│  │                                                                           │
│  ├── Span: API Gateway (50ms)                                              │
│  │   │   span_id: span1, parent: none                                      │
│  │   │                                                                      │
│  │   ├── Span: User Service (20ms)                                         │
│  │   │   │   span_id: span2, parent: span1                                 │
│  │   │   │                                                                  │
│  │   │   └── Span: User DB Query (15ms)                                    │
│  │   │       span_id: span3, parent: span2                                 │
│  │   │                                                                      │
│  │   └── Span: Order Service (25ms)                                        │
│  │       │   span_id: span4, parent: span1                                 │
│  │       │                                                                  │
│  │       └── Span: Order DB Query (20ms)                                   │
│  │           span_id: span5, parent: span4                                 │
│                                                                              │
│  Visual Timeline:                                                            │
│  ┌──────────────────────────────────────────────────────────┐              │
│  │ API Gateway  ████████████████████████████████████████████│ 0-50ms      │
│  │ User Service    ████████████                             │ 5-25ms      │
│  │ User DB              █████████                           │ 10-25ms     │
│  │ Order Service            █████████████████               │ 20-45ms     │
│  │ Order DB                     ████████████████            │ 25-45ms     │
│  └──────────────────────────────────────────────────────────┘              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Implementing Tracing

```python
import uuid
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from contextlib import contextmanager
import threading

@dataclass
class Span:
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    operation_name: str
    service_name: str
    start_time: float
    end_time: float = None
    tags: Dict[str, Any] = field(default_factory=dict)
    logs: list = field(default_factory=list)
    status: str = "OK"

    def finish(self):
        self.end_time = time.time()

    def set_tag(self, key: str, value: Any):
        self.tags[key] = value

    def log(self, message: str, **fields):
        self.logs.append({
            'timestamp': time.time(),
            'message': message,
            **fields
        })

    def duration_ms(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0


class Tracer:
    """
    Simple distributed tracer
    In production: use Jaeger, Zipkin, or cloud provider tracing
    """

    _current_span = threading.local()

    def __init__(self, service_name: str, exporter=None):
        self.service_name = service_name
        self.exporter = exporter or ConsoleExporter()

    @contextmanager
    def start_span(self, operation_name: str,
                   trace_id: str = None,
                   parent_span_id: str = None):
        """Start a new span"""
        # Get trace context from current span or parameters
        current = getattr(self._current_span, 'span', None)

        if trace_id is None:
            trace_id = current.trace_id if current else str(uuid.uuid4())

        if parent_span_id is None and current:
            parent_span_id = current.span_id

        span = Span(
            trace_id=trace_id,
            span_id=str(uuid.uuid4())[:16],
            parent_span_id=parent_span_id,
            operation_name=operation_name,
            service_name=self.service_name,
            start_time=time.time()
        )

        # Set as current span
        previous_span = current
        self._current_span.span = span

        try:
            yield span
        except Exception as e:
            span.status = "ERROR"
            span.set_tag('error', True)
            span.set_tag('error.message', str(e))
            raise
        finally:
            span.finish()
            self.exporter.export(span)
            self._current_span.span = previous_span

    def current_span(self) -> Optional[Span]:
        return getattr(self._current_span, 'span', None)

    def inject_headers(self) -> Dict[str, str]:
        """Get headers to propagate trace context"""
        span = self.current_span()
        if span:
            return {
                'X-Trace-ID': span.trace_id,
                'X-Span-ID': span.span_id
            }
        return {}

    def extract_headers(self, headers: Dict[str, str]) -> tuple:
        """Extract trace context from headers"""
        trace_id = headers.get('X-Trace-ID')
        parent_span_id = headers.get('X-Span-ID')
        return trace_id, parent_span_id


class ConsoleExporter:
    """Export spans to console (for debugging)"""

    def export(self, span: Span):
        print(f"[SPAN] {span.trace_id[:8]} | {span.operation_name} | "
              f"{span.duration_ms():.2f}ms | {span.status}")


# Usage example
tracer = Tracer('order-service')

def handle_order_request(order_id: str, headers: dict):
    # Extract trace context from incoming request
    trace_id, parent_span_id = tracer.extract_headers(headers)

    with tracer.start_span('handle_order', trace_id, parent_span_id) as span:
        span.set_tag('order_id', order_id)

        # Call user service
        with tracer.start_span('call_user_service') as user_span:
            user = call_user_service(tracer.inject_headers())
            user_span.set_tag('user_id', user['id'])

        # Call payment service
        with tracer.start_span('call_payment_service') as payment_span:
            payment = call_payment_service(tracer.inject_headers())
            payment_span.set_tag('payment_id', payment['id'])

        span.log('Order completed successfully')
        return {'status': 'completed'}
```

## Putting It All Together

### Correlation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CORRELATING THE THREE PILLARS                             │
│                                                                              │
│  The KEY is the TRACE ID (or REQUEST ID)                                   │
│                                                                              │
│  Trace ID: abc123                                                           │
│                                                                              │
│  METRICS:                                                                   │
│  http_request_duration{trace_id="abc123"} 0.127                            │
│                                                                              │
│  LOGS:                                                                      │
│  {"trace_id": "abc123", "message": "Order created", "order_id": "456"}     │
│  {"trace_id": "abc123", "message": "Payment processed", "amount": 99.99}   │
│                                                                              │
│  TRACE:                                                                     │
│  Trace abc123: API Gateway → User Service → Order Service → Payment        │
│                                                                              │
│  WORKFLOW:                                                                  │
│  1. Alert fires: "P99 latency > 200ms"                                     │
│  2. Look at metrics dashboard - see spike at 14:32                         │
│  3. Query logs: trace_id from slow requests                                │
│  4. Open trace: see which service is slow                                  │
│  5. Drill into that service's logs and metrics                            │
│  6. Find root cause                                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Alerting

```python
class AlertManager:
    """
    Alert based on metrics thresholds
    """

    def __init__(self, metrics: MetricsCollector, notifier):
        self.metrics = metrics
        self.notifier = notifier
        self.rules = []

    def add_rule(self, name: str, metric: str, condition: callable,
                 severity: str = 'warning', for_duration: int = 60):
        """Add alerting rule"""
        self.rules.append({
            'name': name,
            'metric': metric,
            'condition': condition,
            'severity': severity,
            'for_duration': for_duration,
            'triggered_at': None
        })

    def check_rules(self):
        """Check all rules and fire alerts"""
        for rule in self.rules:
            value = self.metrics.get_latest(rule['metric'])

            if rule['condition'](value):
                if rule['triggered_at'] is None:
                    rule['triggered_at'] = time.time()
                elif time.time() - rule['triggered_at'] > rule['for_duration']:
                    self._fire_alert(rule, value)
            else:
                rule['triggered_at'] = None

    def _fire_alert(self, rule: dict, value: float):
        self.notifier.send(
            severity=rule['severity'],
            title=rule['name'],
            message=f"Metric {rule['metric']} = {value}",
            runbook_url=f"https://runbooks.example.com/{rule['name']}"
        )


# Example rules
alert_manager = AlertManager(metrics, slack_notifier)

# Error rate > 1%
alert_manager.add_rule(
    name='high_error_rate',
    metric='http_error_rate',
    condition=lambda v: v > 0.01,
    severity='critical',
    for_duration=60
)

# P99 latency > 500ms
alert_manager.add_rule(
    name='high_latency',
    metric='http_request_duration_p99',
    condition=lambda v: v > 0.5,
    severity='warning',
    for_duration=300
)
```

## Interview Tips

### Common Questions

**Q: What's the difference between monitoring and observability?**
```
A: Monitoring: Tracking known metrics for known problems
   "Is the error rate above 1%?"

   Observability: Understanding unknown problems
   "Why is this specific request slow?"

   Observability = ability to ask arbitrary questions
```

**Q: How do you debug a slow request in microservices?**
```
A: 1. Start with metrics: Which service has high latency?
   2. Look at traces: What's the request path?
   3. Identify slow span: Which operation took long?
   4. Check that service's logs: What happened?
   5. Check resource metrics: CPU? Memory? DB?
```

**Q: What metrics would you collect for a distributed system?**
```
A: RED Method (for services):
   - Rate, Errors, Duration

   USE Method (for resources):
   - Utilization, Saturation, Errors

   Key metrics:
   - Request rate, error rate, latency (P50, P95, P99)
   - CPU, memory, disk, network utilization
   - Queue depths, connection pool usage
   - Downstream dependency latencies
```

### Red Flags

```
❌ "Just look at the logs"
   → Logs alone don't show request flow or aggregate health

❌ No trace ID / request ID correlation
   → Can't follow a request across services

❌ Only average latency (no percentiles)
   → Hides tail latency problems

❌ No alerting on key metrics
   → Reactive instead of proactive
```

## Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          KEY TAKEAWAYS                                       │
│                                                                              │
│  1. THREE PILLARS                                                           │
│     └── Logs: What happened (events)                                        │
│     └── Metrics: How well (numbers)                                         │
│     └── Traces: Request journey (path)                                      │
│                                                                              │
│  2. CORRELATION IS KEY                                                      │
│     └── Use trace_id / request_id everywhere                               │
│     └── Include in logs, metrics tags, traces                              │
│     └── Enables drill-down from alert to root cause                        │
│                                                                              │
│  3. RED + USE METHODS                                                       │
│     └── RED for service health (Rate, Errors, Duration)                   │
│     └── USE for resource health (Utilization, Saturation, Errors)         │
│                                                                              │
│  4. STRUCTURED EVERYTHING                                                   │
│     └── JSON logs for easy parsing                                         │
│     └── Consistent labels/tags                                             │
│     └── Standard trace propagation                                         │
│                                                                              │
│  5. FOR INTERVIEWS                                                          │
│     └── Know the three pillars                                             │
│     └── Explain debugging workflow                                         │
│     └── Mention specific tools (Prometheus, Jaeger, etc.)                 │
│     └── Discuss alerting strategy                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**Congratulations!** You've completed the Advanced Topics section. These concepts will help you stand out in senior/staff-level interviews and build truly robust distributed systems.

**Back to:** [README](./README.md) | **Resources:** [Curated Learning Materials](../resources/README.md)
