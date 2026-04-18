# Thread Safety Basics

## What is Thread Safety?

A piece of code is **thread-safe** if it functions correctly when accessed by multiple threads simultaneously, without causing data corruption, race conditions, or unexpected behavior.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Thread Safety Problem                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   NOT Thread-Safe:                                                     │
│   ────────────────                                                      │
│                                                                         │
│   class Counter:                                                        │
│       def __init__(self):                                              │
│           self.count = 0                                               │
│                                                                         │
│       def increment(self):                                             │
│           self.count = self.count + 1  # NOT ATOMIC!                   │
│                                                                         │
│   What can go wrong:                                                   │
│   ──────────────────                                                    │
│                                                                         │
│   Thread A                    Thread B                 Shared count    │
│   ─────────                   ─────────                ────────────    │
│   read count (0)                                           0           │
│                               read count (0)               0           │
│   compute 0+1                                              0           │
│                               compute 0+1                  0           │
│   write count (1)                                          1           │
│                               write count (1)              1  ← WRONG! │
│                                                                         │
│   Expected: 2                 Actual: 1                                │
│   This is called a RACE CONDITION                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Key Concepts

### 1. Race Condition
When program behavior depends on the relative timing of events (thread scheduling).

### 2. Critical Section
Code that accesses shared resources and must not be executed by more than one thread at a time.

### 3. Atomicity
An operation that completes entirely or not at all—no partial state is visible.

### 4. Mutual Exclusion (Mutex)
Ensuring only one thread can execute a critical section at a time.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Thread Safety Solutions                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. LOCKS / MUTEXES                                                   │
│      Ensure only one thread accesses critical section                  │
│                                                                         │
│   2. ATOMIC OPERATIONS                                                 │
│      Single indivisible operations (no lock needed)                    │
│                                                                         │
│   3. IMMUTABILITY                                                      │
│      If data can't change, no synchronization needed                   │
│                                                                         │
│   4. THREAD-LOCAL STORAGE                                              │
│      Each thread has its own copy of data                              │
│                                                                         │
│   5. CONCURRENT DATA STRUCTURES                                        │
│      Pre-built thread-safe collections                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Python Thread Safety

### Using Locks

```python
import threading
from threading import Lock, RLock
from typing import Dict

# NOT Thread-Safe
class UnsafeCounter:
    def __init__(self):
        self.count = 0

    def increment(self):
        # This is NOT atomic - race condition possible!
        self.count += 1

# Thread-Safe with Lock
class ThreadSafeCounter:
    def __init__(self):
        self._count = 0
        self._lock = Lock()

    def increment(self):
        with self._lock:  # Only one thread at a time
            self._count += 1

    def get_count(self):
        with self._lock:
            return self._count

# Thread-Safe Bank Account
class BankAccount:
    def __init__(self, balance: float = 0):
        self._balance = balance
        self._lock = Lock()

    def deposit(self, amount: float) -> float:
        with self._lock:
            self._balance += amount
            return self._balance

    def withdraw(self, amount: float) -> bool:
        with self._lock:
            if self._balance >= amount:
                self._balance -= amount
                return True
            return False

    def transfer_to(self, other: 'BankAccount', amount: float) -> bool:
        """
        Transfer money to another account.
        Need to lock BOTH accounts to prevent deadlock.
        """
        # Always acquire locks in consistent order to prevent deadlock
        first, second = sorted([self, other], key=id)

        with first._lock:
            with second._lock:
                if self._balance >= amount:
                    self._balance -= amount
                    other._balance += amount
                    return True
                return False

    @property
    def balance(self) -> float:
        with self._lock:
            return self._balance

# Demonstration
def test_thread_safety():
    counter = ThreadSafeCounter()
    threads = []

    def increment_many():
        for _ in range(10000):
            counter.increment()

    # Create 10 threads, each incrementing 10000 times
    for _ in range(10):
        t = threading.Thread(target=increment_many)
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print(f"Final count: {counter.get_count()}")  # Should be 100000

if __name__ == "__main__":
    test_thread_safety()
```

### Reentrant Locks (RLock)

```python
from threading import RLock

class RecursiveCounter:
    """
    RLock allows same thread to acquire lock multiple times.
    Regular Lock would deadlock on recursive calls.
    """

    def __init__(self):
        self._count = 0
        self._lock = RLock()  # Reentrant lock

    def increment(self):
        with self._lock:
            self._count += 1

    def add(self, n: int):
        with self._lock:  # Acquires lock
            for _ in range(n):
                self.increment()  # Can acquire same lock again

    def get_count(self):
        with self._lock:
            return self._count
```

### Read-Write Locks

```python
import threading
from typing import Dict, Any

class ReadWriteLock:
    """
    Allows multiple readers OR one writer, but not both.
    Useful when reads are much more frequent than writes.
    """

    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0

    def acquire_read(self):
        with self._read_ready:
            self._readers += 1

    def release_read(self):
        with self._read_ready:
            self._readers -= 1
            if self._readers == 0:
                self._read_ready.notify_all()

    def acquire_write(self):
        self._read_ready.acquire()
        while self._readers > 0:
            self._read_ready.wait()

    def release_write(self):
        self._read_ready.release()

class ThreadSafeCache:
    """Cache that allows concurrent reads but exclusive writes"""

    def __init__(self):
        self._data: Dict[str, Any] = {}
        self._lock = ReadWriteLock()

    def get(self, key: str) -> Any:
        self._lock.acquire_read()
        try:
            return self._data.get(key)
        finally:
            self._lock.release_read()

    def set(self, key: str, value: Any):
        self._lock.acquire_write()
        try:
            self._data[key] = value
        finally:
            self._lock.release_write()

    def delete(self, key: str):
        self._lock.acquire_write()
        try:
            self._data.pop(key, None)
        finally:
            self._lock.release_write()
```

---

## Java Thread Safety

### Synchronized Keyword

```java
public class ThreadSafeCounter {
    private int count = 0;

    // Method-level synchronization
    public synchronized void increment() {
        count++;
    }

    public synchronized int getCount() {
        return count;
    }
}

// Alternative: Synchronized block
public class BankAccount {
    private double balance;
    private final Object lock = new Object();

    public void deposit(double amount) {
        synchronized (lock) {
            balance += amount;
        }
    }

    public boolean withdraw(double amount) {
        synchronized (lock) {
            if (balance >= amount) {
                balance -= amount;
                return true;
            }
            return false;
        }
    }

    public double getBalance() {
        synchronized (lock) {
            return balance;
        }
    }
}
```

### ReentrantLock

```java
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.locks.Lock;

public class Counter {
    private int count = 0;
    private final Lock lock = new ReentrantLock();

    public void increment() {
        lock.lock();
        try {
            count++;
        } finally {
            lock.unlock();  // ALWAYS unlock in finally!
        }
    }

    // Try to acquire lock with timeout
    public boolean tryIncrement() {
        boolean acquired = false;
        try {
            acquired = lock.tryLock(100, TimeUnit.MILLISECONDS);
            if (acquired) {
                count++;
                return true;
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            if (acquired) {
                lock.unlock();
            }
        }
        return false;
    }
}
```

### ReadWriteLock

```java
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import java.util.HashMap;
import java.util.Map;

public class ThreadSafeCache<K, V> {
    private final Map<K, V> cache = new HashMap<>();
    private final ReadWriteLock lock = new ReentrantReadWriteLock();

    public V get(K key) {
        lock.readLock().lock();  // Multiple readers allowed
        try {
            return cache.get(key);
        } finally {
            lock.readLock().unlock();
        }
    }

    public void put(K key, V value) {
        lock.writeLock().lock();  // Exclusive access
        try {
            cache.put(key, value);
        } finally {
            lock.writeLock().unlock();
        }
    }

    public void remove(K key) {
        lock.writeLock().lock();
        try {
            cache.remove(key);
        } finally {
            lock.writeLock().unlock();
        }
    }
}
```

### Atomic Classes

```java
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.atomic.AtomicReference;

public class AtomicCounter {
    // No locks needed - uses CPU-level atomic operations
    private final AtomicInteger count = new AtomicInteger(0);

    public void increment() {
        count.incrementAndGet();  // Atomic!
    }

    public void add(int delta) {
        count.addAndGet(delta);
    }

    public int get() {
        return count.get();
    }

    // Compare-and-swap (CAS) pattern
    public boolean compareAndSet(int expected, int newValue) {
        return count.compareAndSet(expected, newValue);
    }
}

// Atomic reference for objects
public class AtomicConfig {
    private final AtomicReference<Config> config =
        new AtomicReference<>(new Config());

    public void updateConfig(Config newConfig) {
        config.set(newConfig);
    }

    public Config getConfig() {
        return config.get();
    }
}
```

### Volatile Keyword

```java
public class SharedFlag {
    // volatile ensures visibility across threads
    private volatile boolean running = true;

    public void stop() {
        running = false;  // Visible to other threads immediately
    }

    public void run() {
        while (running) {  // Always reads latest value
            // do work
        }
    }
}
```

---

## Concurrent Data Structures

### Python

```python
from queue import Queue, PriorityQueue
from collections import deque
import threading

# Thread-safe queue (built-in)
task_queue = Queue()

def producer():
    for i in range(10):
        task_queue.put(f"task-{i}")
        print(f"Produced task-{i}")

def consumer():
    while True:
        task = task_queue.get()  # Blocks until item available
        print(f"Consumed {task}")
        task_queue.task_done()

# Thread-safe dictionary (Python 3.7+)
# dict operations are atomic for single operations
# but NOT for check-then-act patterns

# For complex operations, use threading.Lock
class SafeDict:
    def __init__(self):
        self._data = {}
        self._lock = threading.Lock()

    def get_or_set(self, key, default_factory):
        with self._lock:
            if key not in self._data:
                self._data[key] = default_factory()
            return self._data[key]
```

### Java

```java
import java.util.concurrent.*;

public class ConcurrentCollectionsDemo {
    // Thread-safe HashMap
    ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

    // Thread-safe Queue
    BlockingQueue<String> queue = new LinkedBlockingQueue<>();

    // Thread-safe List
    CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();

    // Thread-safe Set
    ConcurrentSkipListSet<String> set = new ConcurrentSkipListSet<>();

    public void demo() {
        // ConcurrentHashMap - atomic operations
        map.put("key", 1);
        map.computeIfAbsent("key2", k -> 100);  // Atomic check-and-set
        map.merge("key", 1, Integer::sum);      // Atomic update

        // BlockingQueue - for producer-consumer
        try {
            queue.put("item");           // Blocks if full
            String item = queue.take();  // Blocks if empty
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

---

## Common Patterns

### Thread-Safe Singleton (Double-Checked Locking)

```java
public class Singleton {
    // volatile prevents instruction reordering
    private static volatile Singleton instance;

    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {  // First check (no lock)
            synchronized (Singleton.class) {
                if (instance == null) {  // Second check (with lock)
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}

// Better: Use enum (guaranteed thread-safe by JVM)
public enum SingletonEnum {
    INSTANCE;

    public void doSomething() {
        // ...
    }
}
```

### Python Thread-Safe Singleton

```python
import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Double-check inside lock
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

# Or using a module (Python modules are singletons)
# singleton.py
class _Singleton:
    def __init__(self):
        self.value = 0

instance = _Singleton()  # Created once on import
```

### Producer-Consumer Pattern

```python
import threading
from queue import Queue
from typing import Any

class ProducerConsumer:
    def __init__(self, num_consumers: int = 3):
        self._queue = Queue(maxsize=100)
        self._stop_event = threading.Event()
        self._consumers = []

        for i in range(num_consumers):
            t = threading.Thread(target=self._consumer_loop, args=(i,))
            t.daemon = True
            self._consumers.append(t)
            t.start()

    def produce(self, item: Any):
        """Add item to queue (blocks if full)"""
        self._queue.put(item)

    def _consumer_loop(self, consumer_id: int):
        """Consumer thread loop"""
        while not self._stop_event.is_set():
            try:
                item = self._queue.get(timeout=1)
                self._process(consumer_id, item)
                self._queue.task_done()
            except:
                pass  # Timeout, check stop event

    def _process(self, consumer_id: int, item: Any):
        print(f"Consumer {consumer_id} processing: {item}")

    def stop(self):
        """Stop all consumers after queue is empty"""
        self._queue.join()  # Wait for queue to empty
        self._stop_event.set()
        for t in self._consumers:
            t.join()
```

---

## Common Pitfalls

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Thread Safety Pitfalls                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. DEADLOCK                                                          │
│   ───────────                                                           │
│   Thread A holds Lock1, waiting for Lock2                              │
│   Thread B holds Lock2, waiting for Lock1                              │
│                                                                         │
│   Prevention:                                                          │
│   • Always acquire locks in same order                                 │
│   • Use timeout when acquiring locks                                   │
│   • Avoid nested locks when possible                                   │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   2. RACE CONDITION                                                    │
│   ─────────────────                                                     │
│   Check-then-act is NOT atomic:                                        │
│                                                                         │
│   if key not in dict:    # Thread A checks                             │
│                          # Thread B checks (same time)                 │
│       dict[key] = value  # Thread A sets                               │
│                          # Thread B sets (overwrites!)                 │
│                                                                         │
│   Fix: Use atomic operations or lock the entire block                  │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   3. LIVELOCK                                                          │
│   ───────────                                                           │
│   Threads keep changing state in response to each other                │
│   but make no progress (like two people in a hallway)                  │
│                                                                         │
│   Prevention:                                                          │
│   • Add randomness to retry delays                                     │
│   • Use proper synchronization                                         │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   4. STARVATION                                                        │
│   ────────────                                                          │
│   A thread never gets access to shared resource                        │
│   (other threads keep "cutting in line")                               │
│                                                                         │
│   Prevention:                                                          │
│   • Use fair locks (ReentrantLock(fair=true))                         │
│   • Use bounded waiting                                                │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   5. DOUBLE-CHECKED LOCKING BUG                                        │
│   ──────────────────────────────                                        │
│   Without volatile, partially constructed object may be visible        │
│                                                                         │
│   // WRONG                        // RIGHT                             │
│   if (instance == null) {         if (instance == null) {              │
│     synchronized {                  synchronized {                     │
│       if (instance == null)           if (instance == null)            │
│         instance = new Obj();           instance = new Obj();          │
│     }                               }                                  │
│   }                               }                                    │
│   // Missing volatile!            // instance must be volatile         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Interview Tips

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Thread Safety Interview Tips                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   COMMON QUESTIONS:                                                     │
│   ─────────────────                                                     │
│                                                                         │
│   Q: "How do you make a class thread-safe?"                            │
│   A: 1. Identify shared mutable state                                  │
│      2. Synchronize access (locks, atomic vars)                        │
│      3. Or make state immutable                                        │
│      4. Or use thread-local storage                                    │
│                                                                         │
│   Q: "What is a race condition?"                                       │
│   A: When correctness depends on timing/ordering of operations.        │
│      Common: check-then-act, read-modify-write without sync.           │
│                                                                         │
│   Q: "Difference between synchronized and ReentrantLock?"              │
│   A: ReentrantLock offers: tryLock with timeout, fairness option,      │
│      interruptible waiting, multiple conditions. synchronized is       │
│      simpler and auto-releases in finally.                             │
│                                                                         │
│   Q: "What is volatile?"                                               │
│   A: Ensures visibility of changes across threads. No caching in       │
│      CPU registers. NOT sufficient for compound operations.            │
│                                                                         │
│   Q: "How to avoid deadlock?"                                          │
│   A: Lock ordering, timeouts, avoid nested locks, use tryLock.         │
│                                                                         │
│   KEY POINTS TO MENTION:                                               │
│   ──────────────────────                                                │
│   • Prefer immutability when possible                                  │
│   • Use concurrent collections over manual synchronization             │
│   • Keep synchronized blocks small                                     │
│   • Always release locks in finally blocks                             │
│   • volatile is for visibility, not atomicity                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

**Next:** Continue to [09_lld_worked_examples.md](./09_lld_worked_examples.md) for complete LLD interview solutions.
