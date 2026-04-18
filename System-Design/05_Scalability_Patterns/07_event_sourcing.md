# Event Sourcing

## What is Event Sourcing?

**Simple explanation**: Instead of storing just the current state of your data, you store all the events (changes) that led to that state. Think of it like a bank statement—you don't just see your balance, you see every transaction that created it.

**Technical definition**: Event Sourcing is a pattern where application state is stored as a sequence of immutable events. The current state is derived by replaying these events from the beginning.

```
TRADITIONAL (Store current state):
┌─────────────────────────────────────────────┐
│ Account: acc_123                            │
│ Balance: $500                               │  ← Only current value
│ Last updated: 2024-03-15                    │
└─────────────────────────────────────────────┘
                    │
    "How did we get to $500?"  →  "No idea! 🤷"


EVENT SOURCING (Store all events):
┌─────────────────────────────────────────────────────────┐
│ Event 1: AccountOpened    { initial_balance: $0 }       │
│ Event 2: MoneyDeposited   { amount: $1000 }             │
│ Event 3: MoneyWithdrawn   { amount: $300 }              │
│ Event 4: MoneyWithdrawn   { amount: $200 }              │
├─────────────────────────────────────────────────────────┤
│ Current Balance: $0 + $1000 - $300 - $200 = $500        │
│ (Computed from events)                                  │
└─────────────────────────────────────────────────────────┘
                    │
    "How did we get to $500?"  →  "Here's every transaction!"
```

## Why Event Sourcing?

### Problems with Traditional State Storage

```
TRADITIONAL DATABASE:
┌────────────────────────────────────────────┐
│ UPDATE accounts SET balance = 500          │
│ WHERE account_id = 'acc_123'               │
└────────────────────────────────────────────┘

Problems:
1. Lost history - Can't see what happened before
2. Audit difficulty - "Who changed this? When? Why?"
3. Hard to debug - "How did this invalid state occur?"
4. No temporal queries - "What was the balance last Tuesday?"
```

### Event Sourcing Solves These

```
EVENT STORE:
┌─────────────────────────────────────────────────────────────────┐
│ seq │ event_type      │ data              │ timestamp           │
├─────┼─────────────────┼───────────────────┼─────────────────────┤
│  1  │ AccountOpened   │ {initial: $0}     │ 2024-01-01 10:00   │
│  2  │ MoneyDeposited  │ {amount: $1000}   │ 2024-01-15 14:30   │
│  3  │ MoneyWithdrawn  │ {amount: $300}    │ 2024-02-01 09:15   │
│  4  │ MoneyWithdrawn  │ {amount: $200}    │ 2024-03-15 16:45   │
└─────┴─────────────────┴───────────────────┴─────────────────────┘

✓ Complete history preserved
✓ Natural audit trail
✓ Can debug by replaying events
✓ Can query any point in time
```

## Core Concepts

### Events

Events are immutable facts about what happened.

```python
# Events are past-tense, immutable facts
@dataclass(frozen=True)
class AccountOpened:
    account_id: str
    owner_id: str
    initial_balance: Decimal
    timestamp: datetime

@dataclass(frozen=True)
class MoneyDeposited:
    account_id: str
    amount: Decimal
    source: str
    timestamp: datetime

@dataclass(frozen=True)
class MoneyWithdrawn:
    account_id: str
    amount: Decimal
    destination: str
    timestamp: datetime
```

### Event Store

The event store is an append-only log of events.

```
┌─────────────────────────────────────────────────────────────────┐
│                        EVENT STORE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Stream: account-acc_123                                        │
│  ┌───────┬───────┬───────┬───────┬───────┐                     │
│  │ Evt 1 │ Evt 2 │ Evt 3 │ Evt 4 │       │ ──► Append only     │
│  └───────┴───────┴───────┴───────┴───────┘                     │
│                                                                  │
│  Properties:                                                    │
│  - Append only (never update or delete)                        │
│  - Ordered (events have sequence numbers)                      │
│  - Partitioned by aggregate (account, order, etc.)            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Aggregates

Aggregates are rebuilt by replaying events.

```python
class BankAccount:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = Decimal('0')
        self.is_open = False
        self.version = 0

    # Replay events to rebuild state
    def apply(self, event):
        if isinstance(event, AccountOpened):
            self.is_open = True
            self.balance = event.initial_balance
        elif isinstance(event, MoneyDeposited):
            self.balance += event.amount
        elif isinstance(event, MoneyWithdrawn):
            self.balance -= event.amount
        self.version += 1

    @classmethod
    def load(cls, account_id: str, events: list):
        account = cls(account_id)
        for event in events:
            account.apply(event)
        return account
```

## Event Sourcing Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    EVENT SOURCING FLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. COMMAND RECEIVED                                            │
│     ┌──────────────────────┐                                    │
│     │ WithdrawMoney        │                                    │
│     │ account_id: acc_123  │                                    │
│     │ amount: $200         │                                    │
│     └──────────┬───────────┘                                    │
│                │                                                 │
│  2. LOAD AGGREGATE (Replay events)                              │
│                ▼                                                 │
│     ┌──────────────────────┐     ┌─────────────────────┐       │
│     │ Event Store          │────►│ BankAccount         │       │
│     │ Events 1, 2, 3...    │     │ balance: $500       │       │
│     └──────────────────────┘     └──────────┬──────────┘       │
│                                             │                   │
│  3. VALIDATE & EXECUTE                      │                   │
│                                             ▼                   │
│     ┌─────────────────────────────────────────────────────┐    │
│     │ if balance >= amount:                               │    │
│     │     create MoneyWithdrawn event                     │    │
│     │ else:                                               │    │
│     │     reject command                                  │    │
│     └────────────────────────────┬────────────────────────┘    │
│                                  │                              │
│  4. APPEND EVENT                 │                              │
│                                  ▼                              │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ Event Store                                          │   │
│     │ Events 1, 2, 3, [NEW: MoneyWithdrawn]               │   │
│     └──────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Snapshots

Replaying thousands of events is slow. Snapshots help.

```
WITHOUT SNAPSHOTS:
Load account with 10,000 events
├── Read all 10,000 events
├── Apply each event
└── Time: 500ms 😰

WITH SNAPSHOTS:
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Events:  [1][2][3]...[9000][SNAPSHOT][9001][9002]...[10000]   │
│                              │                                   │
│                              ▼                                   │
│                       balance: $45,000                          │
│                       version: 9000                             │
│                                                                  │
│  Load process:                                                  │
│  1. Load snapshot (version 9000, balance $45,000)              │
│  2. Replay only events 9001-10000 (1,000 events)               │
│  3. Time: 50ms 🚀                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Snapshot Strategy

```python
class BankAccountRepository:
    SNAPSHOT_FREQUENCY = 1000

    def save(self, account: BankAccount, new_events: list):
        # Append new events
        self.event_store.append(account.account_id, new_events)

        # Create snapshot periodically
        if account.version % self.SNAPSHOT_FREQUENCY == 0:
            self.snapshot_store.save(
                account_id=account.account_id,
                version=account.version,
                state={'balance': account.balance, 'is_open': account.is_open}
            )

    def load(self, account_id: str) -> BankAccount:
        # Try to load from snapshot
        snapshot = self.snapshot_store.get_latest(account_id)

        if snapshot:
            account = BankAccount.from_snapshot(snapshot)
            events = self.event_store.get_after(account_id, snapshot.version)
        else:
            account = BankAccount(account_id)
            events = self.event_store.get_all(account_id)

        for event in events:
            account.apply(event)

        return account
```

## Projections (Read Models)

Events are optimized for writes. Projections optimize for reads.

```
┌─────────────────────────────────────────────────────────────────┐
│                      PROJECTIONS                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Event Store (Write optimized)                                  │
│  ┌───────┬───────┬───────┬───────┐                              │
│  │ Evt 1 │ Evt 2 │ Evt 3 │ Evt 4 │                              │
│  └───┬───┴───┬───┴───┬───┴───┬───┘                              │
│      │       │       │       │                                   │
│      └───────┼───────┼───────┘                                   │
│              │                                                   │
│              ▼                                                   │
│      Event Handler (Projects events to read models)             │
│              │                                                   │
│      ┌───────┴───────┐                                          │
│      │               │                                           │
│      ▼               ▼                                           │
│  ┌─────────┐    ┌─────────────────┐                             │
│  │ Account │    │ Transaction     │                             │
│  │ Balance │    │ History         │                             │
│  │ View    │    │ View            │                             │
│  └─────────┘    └─────────────────┘                             │
│                                                                  │
│  Projection 1:           Projection 2:                          │
│  - Current balance       - All transactions                     │
│  - Quick lookup          - Searchable                           │
│  - Single row            - Many rows                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Benefits and Tradeoffs

### Benefits

| Benefit | Explanation |
|---------|-------------|
| **Complete audit trail** | Every change is recorded |
| **Temporal queries** | Query state at any point in time |
| **Debug-friendly** | Replay events to understand bugs |
| **Rebuild views** | Create new projections from events |
| **Event replay** | Fix bugs by replaying corrected logic |

### Tradeoffs

| Tradeoff | Explanation |
|----------|-------------|
| **Complexity** | More concepts to understand |
| **Eventual consistency** | Projections may lag behind |
| **Event evolution** | Changing event schema is tricky |
| **Storage growth** | Events accumulate forever |
| **Query complexity** | Can't query events directly |

## When to Use Event Sourcing

### Good Fit

```
✓ Audit requirements (finance, healthcare, legal)
✓ Need to understand "how we got here"
✓ Complex domain with many state transitions
✓ Need to rebuild state at any point in time
✓ Already using CQRS
✓ Domain experts think in events
```

### Bad Fit

```
✗ Simple CRUD applications
✗ No audit requirements
✗ Team unfamiliar with pattern
✗ Strong consistency required
✗ Simple state with few transitions
```

## Interview Questions

1. "What is event sourcing and when would you use it?"
2. "How do you handle event schema evolution?"
3. "What are projections in event sourcing?"
4. "How do snapshots improve performance?"

## Key Takeaways

```
┌────────────────────────────────────────────────────────────────┐
│                EVENT SOURCING SUMMARY                           │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CORE IDEA:                                                    │
│  └── Store events, not state. Derive state from events.        │
│                                                                 │
│  KEY COMPONENTS:                                               │
│  ├── Events: Immutable facts about what happened              │
│  ├── Event Store: Append-only log of events                   │
│  ├── Aggregates: Rebuilt by replaying events                  │
│  ├── Projections: Read-optimized views of events              │
│  └── Snapshots: Optimization for long event streams           │
│                                                                 │
│  USE WHEN:                                                     │
│  └── Audit trail is critical                                   │
│  └── Need temporal queries                                     │
│  └── Complex state transitions                                 │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

*Next: [Backpressure Handling](08_backpressure.md) →*
