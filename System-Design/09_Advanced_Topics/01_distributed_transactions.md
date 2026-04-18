# Distributed Transactions

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      DISTRIBUTED TRANSACTIONS                                 ║
║             Maintaining Consistency Across Multiple Services                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## The Problem

In a monolithic application, a single database transaction can ensure all operations succeed or fail together (ACID). But what happens when your operation spans multiple services, each with its own database?

### Real-World Scenario: E-commerce Order

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ORDER PROCESSING FLOW                                │
│                                                                              │
│     User places order for $100                                               │
│            │                                                                 │
│            ▼                                                                 │
│   ┌─────────────────┐                                                       │
│   │  Order Service  │  1. Create order record                               │
│   │   (Database A)  │                                                       │
│   └────────┬────────┘                                                       │
│            │                                                                 │
│            ▼                                                                 │
│   ┌─────────────────┐                                                       │
│   │ Payment Service │  2. Charge $100                                       │
│   │   (Database B)  │                                                       │
│   └────────┬────────┘                                                       │
│            │                                                                 │
│            ▼                                                                 │
│   ┌─────────────────┐                                                       │
│   │Inventory Service│  3. Reserve items                                     │
│   │   (Database C)  │                                                       │
│   └────────┬────────┘                                                       │
│            │                                                                 │
│            ▼                                                                 │
│   ┌─────────────────┐                                                       │
│   │Shipping Service │  4. Create shipment                                   │
│   │   (Database D)  │                                                       │
│   └─────────────────┘                                                       │
│                                                                              │
│   What if step 3 fails? Payment is charged but items aren't reserved!       │
└─────────────────────────────────────────────────────────────────────────────┘
```

**The Challenge**: Each service has its own database. There's no single transaction that spans all of them.

## Solution 1: Two-Phase Commit (2PC)

### The Intuition

Think of 2PC like a wedding ceremony:

```
Phase 1 - "Prepare" (The Question)
├── Priest asks bride: "Do you take this person?"
├── Priest asks groom: "Do you take this person?"
└── Both must say "Yes" to proceed

Phase 2 - "Commit" (The Declaration)
├── If both said yes → "I now pronounce you married"
└── If anyone said no → Wedding cancelled
```

### How 2PC Works

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TWO-PHASE COMMIT PROTOCOL                                 │
│                                                                              │
│   PHASE 1: PREPARE                                                          │
│   ═══════════════                                                           │
│                                                                              │
│       Coordinator                                                            │
│            │                                                                 │
│            ├──────── "PREPARE" ────────┬──────────────┐                     │
│            │                           │              │                     │
│            ▼                           ▼              ▼                     │
│       Service A                   Service B      Service C                  │
│            │                           │              │                     │
│            │ (acquire locks)           │              │                     │
│            │ (validate)                │              │                     │
│            │                           │              │                     │
│            ├──────── "READY" ─────────┬┼──────────────┤                     │
│            │                          ││              │                     │
│            ▼                          ▼▼              ▼                     │
│       Coordinator receives all votes                                        │
│                                                                              │
│   PHASE 2: COMMIT (if all ready)                                            │
│   ══════════════════════════════                                            │
│                                                                              │
│       Coordinator                                                            │
│            │                                                                 │
│            ├──────── "COMMIT" ────────┬──────────────┐                      │
│            │                          │              │                      │
│            ▼                          ▼              ▼                      │
│       Service A                   Service B      Service C                  │
│            │                          │              │                      │
│            │ (apply changes)          │              │                      │
│            │ (release locks)          │              │                      │
│            │                          │              │                      │
│            ├──────── "ACK" ──────────┬┼──────────────┤                      │
│            ▼                         ▼▼              ▼                      │
│       Transaction Complete                                                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2PC State Machine

```
                    ┌─────────┐
                    │  INIT   │
                    └────┬────┘
                         │ send PREPARE
                         ▼
                    ┌─────────┐
                    │ WAITING │
                    └────┬────┘
                         │
           ┌─────────────┴─────────────┐
           │                           │
    all vote YES               any vote NO
           │                           │
           ▼                           ▼
    ┌─────────────┐            ┌─────────────┐
    │  COMMITTED  │            │  ABORTED    │
    └─────────────┘            └─────────────┘
```

### 2PC Code Example

```python
class TwoPhaseCommitCoordinator:
    def __init__(self, participants):
        self.participants = participants
        self.state = "INIT"

    def execute_transaction(self, operations):
        """
        Execute distributed transaction using 2PC
        """
        # PHASE 1: Prepare
        self.state = "PREPARING"
        votes = []

        for participant, operation in zip(self.participants, operations):
            try:
                # Ask participant to prepare
                vote = participant.prepare(operation)
                votes.append(vote)
            except Exception as e:
                votes.append("ABORT")

        # PHASE 2: Commit or Abort
        if all(v == "READY" for v in votes):
            self.state = "COMMITTING"
            return self._commit_all()
        else:
            self.state = "ABORTING"
            return self._abort_all()

    def _commit_all(self):
        for participant in self.participants:
            participant.commit()
        self.state = "COMMITTED"
        return True

    def _abort_all(self):
        for participant in self.participants:
            participant.rollback()
        self.state = "ABORTED"
        return False


class Participant:
    def __init__(self, name, database):
        self.name = name
        self.database = database
        self.prepared_data = None

    def prepare(self, operation):
        """
        Validate and acquire locks, but don't commit yet
        """
        try:
            # Validate the operation
            if not self._validate(operation):
                return "ABORT"

            # Acquire locks
            self._acquire_locks(operation)

            # Write to temporary storage
            self.prepared_data = operation

            # Write to WAL (Write-Ahead Log) for recovery
            self._write_to_wal("PREPARED", operation)

            return "READY"
        except Exception:
            return "ABORT"

    def commit(self):
        """
        Apply the prepared changes
        """
        self.database.apply(self.prepared_data)
        self._write_to_wal("COMMITTED", self.prepared_data)
        self._release_locks()
        self.prepared_data = None

    def rollback(self):
        """
        Discard prepared changes
        """
        self._write_to_wal("ABORTED", self.prepared_data)
        self._release_locks()
        self.prepared_data = None
```

### 2PC Problems

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PROBLEMS WITH 2PC                                       │
│                                                                              │
│  1. BLOCKING                                                                 │
│     ─────────                                                               │
│     If coordinator crashes after sending PREPARE but before COMMIT:         │
│                                                                              │
│     Coordinator ──────X (crashes)                                           │
│          │                                                                   │
│          └── PREPARE ──┬──────────┐                                         │
│                        │          │                                         │
│                        ▼          ▼                                         │
│                   Service A   Service B                                     │
│                   (WAITING)   (WAITING)                                     │
│                   (locked!)   (locked!)                                     │
│                                                                              │
│     Services are stuck holding locks indefinitely!                          │
│                                                                              │
│  2. SINGLE POINT OF FAILURE                                                 │
│     ──────────────────────────                                              │
│     Coordinator is critical - if it fails, entire system is stuck           │
│                                                                              │
│  3. LATENCY                                                                 │
│     ───────                                                                 │
│     Minimum 2 round-trips + lock holding time                               │
│     Network partitions can cause long waits                                 │
│                                                                              │
│  4. NOT PARTITION TOLERANT                                                  │
│     ──────────────────────                                                  │
│     Network partitions can leave system in uncertain state                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Solution 2: Saga Pattern

### The Intuition

Instead of one big transaction, Saga breaks it into a **sequence of local transactions**, each with a **compensating action** that can undo it.

Think of it like booking a vacation:
1. Book flight → Cancel flight (if hotel fails)
2. Book hotel → Cancel hotel (if car fails)
3. Book rental car → Cancel car (if payment fails)
4. Charge payment → Refund (if something fails)

### Saga Types

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SAGA PATTERNS                                       │
│                                                                              │
│  CHOREOGRAPHY (Event-Driven)                                                │
│  ═══════════════════════════                                                │
│                                                                              │
│  Each service publishes events, others react                                │
│                                                                              │
│  Order      Payment     Inventory     Shipping                              │
│    │           │            │            │                                  │
│    │──OrderCreated──►│      │            │                                  │
│    │           │            │            │                                  │
│    │           │──PaymentComplete──►│    │                                  │
│    │           │            │            │                                  │
│    │           │            │──InventoryReserved──►│                        │
│    │           │            │            │                                  │
│                                                                              │
│  ORCHESTRATION (Central Coordinator)                                        │
│  ═══════════════════════════════════                                        │
│                                                                              │
│                  Saga Orchestrator                                           │
│                        │                                                     │
│         ┌──────────────┼──────────────┐                                     │
│         │              │              │                                     │
│         ▼              ▼              ▼                                     │
│      Order ────► Payment ────► Inventory ────► Shipping                     │
│                                                                              │
│  Orchestrator controls the flow and handles failures                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Saga with Compensations

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SAGA COMPENSATION EXAMPLE                                 │
│                                                                              │
│  HAPPY PATH (all succeed):                                                  │
│  ═════════════════════════                                                  │
│                                                                              │
│  T1: Create Order ──► T2: Process Payment ──► T3: Reserve Inventory         │
│         │                    │                       │                      │
│         ▼                    ▼                       ▼                      │
│      Success              Success                 Success                   │
│                                                                              │
│  FAILURE SCENARIO (T3 fails):                                               │
│  ════════════════════════════                                               │
│                                                                              │
│  T1: Create Order ──► T2: Process Payment ──► T3: Reserve Inventory         │
│         │                    │                       │                      │
│         ▼                    ▼                       ▼                      │
│      Success              Success                 FAILED!                   │
│                                                       │                     │
│                                                       │ trigger             │
│                                                       │ compensation        │
│                                                       ▼                     │
│  C1: Cancel Order ◄── C2: Refund Payment ◄───────────┘                     │
│                                                                              │
│  Each Ti has a compensating action Ci that undoes it                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Saga Orchestrator Implementation

```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Callable, Any
import logging

class SagaStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"

@dataclass
class SagaStep:
    name: str
    action: Callable
    compensation: Callable

class SagaOrchestrator:
    """
    Coordinates a distributed transaction using the Saga pattern
    """

    def __init__(self, saga_id: str):
        self.saga_id = saga_id
        self.steps: List[SagaStep] = []
        self.completed_steps: List[SagaStep] = []
        self.status = SagaStatus.PENDING
        self.logger = logging.getLogger(f"Saga-{saga_id}")

    def add_step(self, name: str, action: Callable, compensation: Callable):
        """Add a step with its compensating action"""
        self.steps.append(SagaStep(name, action, compensation))

    def execute(self, context: dict) -> bool:
        """
        Execute the saga. On failure, run compensations.
        """
        self.status = SagaStatus.RUNNING

        for step in self.steps:
            try:
                self.logger.info(f"Executing step: {step.name}")

                # Execute the step
                result = step.action(context)
                context[f"{step.name}_result"] = result

                # Track completed steps for potential compensation
                self.completed_steps.append(step)

                self.logger.info(f"Step {step.name} completed successfully")

            except Exception as e:
                self.logger.error(f"Step {step.name} failed: {e}")

                # Trigger compensation
                self._compensate(context)
                return False

        self.status = SagaStatus.COMPLETED
        self.logger.info("Saga completed successfully")
        return True

    def _compensate(self, context: dict):
        """
        Run compensating actions in reverse order
        """
        self.status = SagaStatus.COMPENSATING
        self.logger.info("Starting compensation...")

        # Reverse order - undo most recent first
        for step in reversed(self.completed_steps):
            try:
                self.logger.info(f"Compensating step: {step.name}")
                step.compensation(context)
                self.logger.info(f"Compensation for {step.name} successful")
            except Exception as e:
                # Compensation failure is serious - needs manual intervention
                self.logger.error(
                    f"CRITICAL: Compensation for {step.name} failed: {e}"
                )
                # In production: alert, retry queue, or dead letter queue

        self.status = SagaStatus.FAILED


# Example Usage: E-commerce Order Saga
class OrderSaga:
    def __init__(self, order_service, payment_service,
                 inventory_service, shipping_service):
        self.order_service = order_service
        self.payment_service = payment_service
        self.inventory_service = inventory_service
        self.shipping_service = shipping_service

    def create_order(self, order_data: dict) -> bool:
        saga = SagaOrchestrator(f"order-{order_data['order_id']}")

        # Step 1: Create Order
        saga.add_step(
            name="create_order",
            action=lambda ctx: self.order_service.create(ctx['order_data']),
            compensation=lambda ctx: self.order_service.cancel(
                ctx['create_order_result']['order_id']
            )
        )

        # Step 2: Process Payment
        saga.add_step(
            name="process_payment",
            action=lambda ctx: self.payment_service.charge(
                ctx['order_data']['user_id'],
                ctx['order_data']['amount']
            ),
            compensation=lambda ctx: self.payment_service.refund(
                ctx['process_payment_result']['transaction_id']
            )
        )

        # Step 3: Reserve Inventory
        saga.add_step(
            name="reserve_inventory",
            action=lambda ctx: self.inventory_service.reserve(
                ctx['order_data']['items']
            ),
            compensation=lambda ctx: self.inventory_service.release(
                ctx['reserve_inventory_result']['reservation_id']
            )
        )

        # Step 4: Create Shipment
        saga.add_step(
            name="create_shipment",
            action=lambda ctx: self.shipping_service.create(
                ctx['create_order_result']['order_id'],
                ctx['order_data']['shipping_address']
            ),
            compensation=lambda ctx: self.shipping_service.cancel(
                ctx['create_shipment_result']['shipment_id']
            )
        )

        # Execute the saga
        context = {'order_data': order_data}
        return saga.execute(context)
```

```java
// Java Implementation
public class SagaOrchestrator<T> {
    private final String sagaId;
    private final List<SagaStep<T>> steps = new ArrayList<>();
    private final Deque<SagaStep<T>> completedSteps = new ArrayDeque<>();
    private SagaStatus status = SagaStatus.PENDING;

    public SagaOrchestrator(String sagaId) {
        this.sagaId = sagaId;
    }

    public SagaOrchestrator<T> addStep(
            String name,
            Function<T, T> action,
            Consumer<T> compensation) {
        steps.add(new SagaStep<>(name, action, compensation));
        return this;
    }

    public boolean execute(T context) {
        status = SagaStatus.RUNNING;

        for (SagaStep<T> step : steps) {
            try {
                log.info("Executing step: {}", step.getName());
                context = step.getAction().apply(context);
                completedSteps.push(step);
                log.info("Step {} completed", step.getName());
            } catch (Exception e) {
                log.error("Step {} failed: {}", step.getName(), e.getMessage());
                compensate(context);
                return false;
            }
        }

        status = SagaStatus.COMPLETED;
        return true;
    }

    private void compensate(T context) {
        status = SagaStatus.COMPENSATING;

        while (!completedSteps.isEmpty()) {
            SagaStep<T> step = completedSteps.pop();
            try {
                log.info("Compensating step: {}", step.getName());
                step.getCompensation().accept(context);
            } catch (Exception e) {
                log.error("CRITICAL: Compensation failed for {}: {}",
                    step.getName(), e.getMessage());
                // Alert, retry queue, manual intervention
            }
        }

        status = SagaStatus.FAILED;
    }
}
```

## 2PC vs Saga Comparison

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      2PC vs SAGA COMPARISON                                  │
│                                                                              │
│  Aspect           │ Two-Phase Commit       │ Saga                           │
│  ─────────────────┼────────────────────────┼────────────────────────────────│
│  Consistency      │ Strong (ACID)          │ Eventual                       │
│  Isolation        │ Yes (locks held)       │ No (intermediate visible)      │
│  Blocking         │ Yes (waiting for all)  │ No (async steps)               │
│  Availability     │ Lower (locks, coord)   │ Higher                         │
│  Complexity       │ Protocol complexity    │ Compensation complexity        │
│  Recovery         │ Coordinator recovery   │ Step-by-step rollback          │
│  Performance      │ Slower (2 round-trips) │ Faster (parallel possible)     │
│  Use Case         │ Need strong ACID       │ Can tolerate eventual          │
│                                                                              │
│  WHEN TO USE 2PC:                                                           │
│  ├── Financial systems requiring atomicity                                  │
│  ├── Inventory + payment must be atomic                                     │
│  └── Within a single datacenter (low latency)                               │
│                                                                              │
│  WHEN TO USE SAGA:                                                          │
│  ├── Long-running business processes                                        │
│  ├── Cross-datacenter transactions                                          │
│  ├── High availability requirement                                          │
│  └── Can design compensating actions                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Saga Isolation Problem

### The Issue

Saga doesn't provide isolation. Other transactions can see intermediate states:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SAGA ISOLATION PROBLEM                                    │
│                                                                              │
│  Timeline:                                                                   │
│  ═════════                                                                   │
│                                                                              │
│  Saga 1:   Create Order ──► Charge Payment ──► Reserve Items               │
│                                   │                                          │
│                                   │ $100 charged                            │
│                                   ▼                                          │
│  Query:              User balance reads $0 (but order not complete!)        │
│                                                                              │
│  Saga 1:                                          ──► FAILS!                │
│                                                                              │
│  Saga 1:                                   Refund $100                      │
│                                                                              │
│  Problem: Query saw inconsistent state during saga execution                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Solutions

```
1. SEMANTIC LOCKS
   ───────────────
   Add "status" field: PENDING → CONFIRMED
   Queries can filter on status

   Order:
   {
     id: 123,
     status: "PENDING",  // Not visible to normal queries
     amount: 100
   }

2. COMMUTATIVE UPDATES
   ────────────────────
   Design updates that can be applied in any order

   Instead of: balance = 100
   Use: balance += (-100)  // Can compensate with += 100

3. REREAD VALUE
   ─────────────
   Re-validate before compensation
   Ensure state hasn't changed

4. VERSION/SAGA_ID TRACKING
   ─────────────────────────
   Track which saga modified data
   Reject conflicting operations
```

## Interview Tips

### Common Questions

**Q: When would you use 2PC vs Saga?**
```
A: I'd use 2PC when:
   - Strong consistency is non-negotiable (e.g., financial ledger)
   - Operations are fast and within same datacenter
   - Can tolerate blocking during coordinator recovery

   I'd use Saga when:
   - High availability is priority
   - Operations span multiple datacenters
   - Long-running transactions
   - Can design meaningful compensations
```

**Q: How do you handle saga compensation failures?**
```
A: Multiple strategies:
   1. Retry with exponential backoff
   2. Dead letter queue for manual intervention
   3. Idempotent compensations (safe to retry)
   4. Forward recovery (complete instead of rollback)
   5. Alert and human intervention for critical paths
```

**Q: What about the "isolation" problem in Sagas?**
```
A: I'd use one or more of:
   1. Semantic locks (status fields like PENDING/CONFIRMED)
   2. Version numbers to detect concurrent modifications
   3. Saga ID tracking on records
   4. Eventual consistency in reads (may see in-progress)
```

### Red Flags to Avoid

```
❌ "Just use 2PC, it's simpler"
   → Shows lack of understanding of distributed systems challenges

❌ "Saga guarantees ACID"
   → Saga is eventually consistent, not ACID

❌ Forgetting about compensation failure handling
   → Real systems need this!

❌ Not considering the isolation problem
   → Shows lack of practical experience
```

### What Interviewers Want to Hear

```
✅ Clear understanding of trade-offs
✅ Awareness of failure modes
✅ Practical solutions to real problems
✅ "It depends" with good reasoning
✅ Discussion of monitoring/observability
```

## Advanced Patterns

### Semantic Lock Pattern

```python
class OrderWithSemanticLock:
    """
    Order that uses semantic lock for saga isolation
    """

    def create_pending_order(self, order_data):
        """Create order in PENDING state - not visible to normal queries"""
        return self.db.insert({
            **order_data,
            'status': 'PENDING',  # Semantic lock
            'saga_id': order_data['saga_id'],
            'created_at': datetime.now()
        })

    def confirm_order(self, order_id, saga_id):
        """Confirm order - only saga that created it can confirm"""
        result = self.db.update(
            {'_id': order_id, 'saga_id': saga_id, 'status': 'PENDING'},
            {'$set': {'status': 'CONFIRMED'}}
        )
        if result.modified_count == 0:
            raise ConcurrentModificationError("Order already modified")

    def cancel_order(self, order_id, saga_id):
        """Cancel order - compensation action"""
        self.db.update(
            {'_id': order_id, 'saga_id': saga_id},
            {'$set': {'status': 'CANCELLED'}}
        )

    def get_confirmed_orders(self, user_id):
        """Only returns confirmed orders - ignores pending"""
        return self.db.find({
            'user_id': user_id,
            'status': 'CONFIRMED'  # Filter semantic lock
        })
```

### Parallel Saga Execution

```python
class ParallelSagaOrchestrator:
    """
    Execute independent saga steps in parallel for better performance
    """

    async def execute_parallel_steps(self, steps, context):
        """
        Execute steps that can run in parallel
        """
        tasks = []
        for step in steps:
            task = asyncio.create_task(
                self._execute_step(step, context)
            )
            tasks.append((step, task))

        results = await asyncio.gather(
            *[t[1] for t in tasks],
            return_exceptions=True
        )

        # Check for failures
        failed_steps = []
        for (step, _), result in zip(tasks, results):
            if isinstance(result, Exception):
                failed_steps.append(step)

        if failed_steps:
            # Compensate all completed steps
            await self._compensate_parallel(
                [s for s, r in zip(steps, results)
                 if not isinstance(r, Exception)],
                context
            )
            return False

        return True
```

## Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         KEY TAKEAWAYS                                        │
│                                                                              │
│  1. Distributed transactions are HARD - no perfect solution                 │
│                                                                              │
│  2. 2PC provides strong consistency but:                                    │
│     - Blocking during failures                                              │
│     - Single point of failure (coordinator)                                 │
│     - Not partition tolerant                                                │
│                                                                              │
│  3. Saga provides availability and resilience but:                          │
│     - Eventually consistent                                                 │
│     - No isolation (intermediate states visible)                            │
│     - Requires careful compensation design                                  │
│                                                                              │
│  4. For most microservices: Prefer Saga                                     │
│     - Design for eventual consistency                                       │
│     - Use semantic locks for isolation                                      │
│     - Handle compensation failures gracefully                               │
│                                                                              │
│  5. Monitor everything:                                                     │
│     - Saga step success/failure rates                                       │
│     - Compensation invocations                                              │
│     - In-progress saga duration                                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**Next:** [Consensus Algorithms](./02_consensus.md) - How distributed nodes agree on shared state
