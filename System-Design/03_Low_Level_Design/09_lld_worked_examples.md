# LLD Worked Examples

This file contains complete Low Level Design solutions for common interview problems. Each example follows the LLD interview framework and includes class diagrams, code implementation, and discussion points.

---

## Example 1: Parking Lot System

### Problem Statement
Design a parking lot system that supports:
- Multiple floors with different spot types (compact, regular, large)
- Vehicle entry/exit with ticket generation
- Hourly rate calculation
- Display available spots per floor

### Requirements Clarification

```
Functional Requirements:
- Park different vehicle types (motorcycle, car, bus)
- Generate ticket on entry
- Calculate fee on exit
- Track available spots
- Support multiple floors

Non-Functional Requirements:
- Thread-safe operations
- Support concurrent entry/exit
```

### Class Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Parking Lot Class Diagram                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────┐                                                  │
│   │    ParkingLot   │                                                  │
│   ├─────────────────┤         1                                        │
│   │ - name          │◆────────────┐                                    │
│   │ - floors[]      │             │                                    │
│   │ - entryPanels[] │             │ *                                  │
│   │ - exitPanels[]  │    ┌────────┴────────┐                          │
│   ├─────────────────┤    │   ParkingFloor  │                          │
│   │ + getAvailable()│    ├─────────────────┤         1                 │
│   │ + isFull()      │    │ - floorNumber   │◆───────────┐             │
│   └─────────────────┘    │ - spots[]       │            │             │
│                          ├─────────────────┤            │ *           │
│                          │ + getAvailable()│    ┌───────┴───────┐     │
│                          └─────────────────┘    │  ParkingSpot  │     │
│                                                 ├───────────────┤     │
│   ┌─────────────────┐                          │ - spotNumber  │     │
│   │  <<enum>>       │                          │ - spotType    │     │
│   │  VehicleType    │                          │ - vehicle     │     │
│   ├─────────────────┤                          │ - isOccupied  │     │
│   │ MOTORCYCLE      │                          ├───────────────┤     │
│   │ CAR             │                          │ + park()      │     │
│   │ BUS             │                          │ + unpark()    │     │
│   └─────────────────┘                          │ + canFit()    │     │
│                                                └───────┬───────┘     │
│   ┌─────────────────┐                                  │             │
│   │  <<enum>>       │                          holds   │ 0..1        │
│   │  SpotType       │                                  ▼             │
│   ├─────────────────┤                          ┌───────────────┐     │
│   │ COMPACT         │                          │    Vehicle    │     │
│   │ REGULAR         │                          ├───────────────┤     │
│   │ LARGE           │                          │ - licensePlate│     │
│   └─────────────────┘                          │ - type        │     │
│                                                └───────────────┘     │
│                                                                       │
│   ┌─────────────────┐    creates    ┌─────────────────┐              │
│   │   EntryPanel    │──────────────►│    Ticket       │              │
│   ├─────────────────┤               ├─────────────────┤              │
│   │ + getTicket()   │               │ - ticketNumber  │              │
│   └─────────────────┘               │ - entryTime     │              │
│                                     │ - vehicle       │              │
│   ┌─────────────────┐               │ - parkingSpot   │              │
│   │   ExitPanel     │               │ - paymentStatus │              │
│   ├─────────────────┤               └─────────────────┘              │
│   │ + processExit() │                                                │
│   │ + calculateFee()│                                                │
│   └─────────────────┘                                                │
│                                                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

### Python Implementation

```python
from enum import Enum
from datetime import datetime
from typing import Optional, List, Dict
from threading import Lock
from abc import ABC, abstractmethod
import uuid

# Enums
class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    BUS = 3

class SpotType(Enum):
    COMPACT = 1
    REGULAR = 2
    LARGE = 3

class PaymentStatus(Enum):
    PENDING = 1
    COMPLETED = 2
    FAILED = 3

# Vehicle classes
class Vehicle:
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.ticket: Optional['Ticket'] = None

class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.MOTORCYCLE)

class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.CAR)

class Bus(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.BUS)

# Parking Spot
class ParkingSpot:
    def __init__(self, spot_number: str, spot_type: SpotType):
        self.spot_number = spot_number
        self.spot_type = spot_type
        self._vehicle: Optional[Vehicle] = None
        self._lock = Lock()

    @property
    def is_available(self) -> bool:
        return self._vehicle is None

    @property
    def vehicle(self) -> Optional[Vehicle]:
        return self._vehicle

    def can_fit(self, vehicle: Vehicle) -> bool:
        """Check if vehicle can fit in this spot type"""
        type_map = {
            VehicleType.MOTORCYCLE: [SpotType.COMPACT, SpotType.REGULAR, SpotType.LARGE],
            VehicleType.CAR: [SpotType.REGULAR, SpotType.LARGE],
            VehicleType.BUS: [SpotType.LARGE]
        }
        return self.spot_type in type_map[vehicle.vehicle_type]

    def park(self, vehicle: Vehicle) -> bool:
        with self._lock:
            if not self.is_available or not self.can_fit(vehicle):
                return False
            self._vehicle = vehicle
            return True

    def unpark(self) -> Optional[Vehicle]:
        with self._lock:
            vehicle = self._vehicle
            self._vehicle = None
            return vehicle

# Ticket
class Ticket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.ticket_number = str(uuid.uuid4())[:8].upper()
        self.entry_time = datetime.now()
        self.exit_time: Optional[datetime] = None
        self.vehicle = vehicle
        self.parking_spot = spot
        self.payment_status = PaymentStatus.PENDING

# Parking Floor
class ParkingFloor:
    def __init__(self, floor_number: int, spots: List[ParkingSpot]):
        self.floor_number = floor_number
        self.spots = spots
        self._display_board = DisplayBoard(floor_number)

    def get_available_spots(self, vehicle_type: VehicleType) -> List[ParkingSpot]:
        """Get available spots that can fit the vehicle type"""
        available = []
        for spot in self.spots:
            # Create temporary vehicle to check fit
            temp_vehicle = Vehicle("", vehicle_type)
            if spot.is_available and spot.can_fit(temp_vehicle):
                available.append(spot)
        return available

    def find_spot_for_vehicle(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """Find first available spot for a vehicle"""
        for spot in self.spots:
            if spot.is_available and spot.can_fit(vehicle):
                return spot
        return None

    def update_display(self):
        """Update the display board"""
        counts = {SpotType.COMPACT: 0, SpotType.REGULAR: 0, SpotType.LARGE: 0}
        for spot in self.spots:
            if spot.is_available:
                counts[spot.spot_type] += 1
        self._display_board.update(counts)

class DisplayBoard:
    def __init__(self, floor_number: int):
        self.floor_number = floor_number
        self._available = {}

    def update(self, available_counts: Dict[SpotType, int]):
        self._available = available_counts
        self._show()

    def _show(self):
        print(f"\n=== Floor {self.floor_number} Available Spots ===")
        for spot_type, count in self._available.items():
            print(f"  {spot_type.name}: {count}")

# Entry/Exit Panels
class EntryPanel:
    def __init__(self, panel_id: str, parking_lot: 'ParkingLot'):
        self.panel_id = panel_id
        self._parking_lot = parking_lot

    def get_ticket(self, vehicle: Vehicle) -> Optional[Ticket]:
        """Issue ticket and assign spot to vehicle"""
        spot = self._parking_lot.find_spot(vehicle)
        if not spot:
            print(f"No available spot for {vehicle.vehicle_type.name}")
            return None

        if spot.park(vehicle):
            ticket = Ticket(vehicle, spot)
            vehicle.ticket = ticket
            self._parking_lot._active_tickets[ticket.ticket_number] = ticket
            print(f"Ticket issued: {ticket.ticket_number}")
            print(f"Spot assigned: {spot.spot_number}")
            return ticket
        return None

class ExitPanel:
    def __init__(self, panel_id: str, parking_lot: 'ParkingLot'):
        self.panel_id = panel_id
        self._parking_lot = parking_lot
        self._hourly_rate = {
            VehicleType.MOTORCYCLE: 1.0,
            VehicleType.CAR: 2.0,
            VehicleType.BUS: 5.0
        }

    def calculate_fee(self, ticket: Ticket) -> float:
        """Calculate parking fee based on duration"""
        if not ticket.exit_time:
            ticket.exit_time = datetime.now()

        duration = ticket.exit_time - ticket.entry_time
        hours = max(1, duration.total_seconds() / 3600)  # Minimum 1 hour
        rate = self._hourly_rate[ticket.vehicle.vehicle_type]
        return round(hours * rate, 2)

    def process_exit(self, ticket_number: str) -> bool:
        """Process vehicle exit"""
        ticket = self._parking_lot._active_tickets.get(ticket_number)
        if not ticket:
            print(f"Invalid ticket: {ticket_number}")
            return False

        fee = self.calculate_fee(ticket)
        print(f"\nParking fee: ${fee}")

        # Simulate payment
        if self._process_payment(fee):
            ticket.payment_status = PaymentStatus.COMPLETED
            ticket.parking_spot.unpark()
            del self._parking_lot._active_tickets[ticket_number]
            print("Thank you! Have a nice day.")
            return True

        ticket.payment_status = PaymentStatus.FAILED
        return False

    def _process_payment(self, amount: float) -> bool:
        # Simulate payment processing
        print(f"Processing payment of ${amount}...")
        return True

# Main Parking Lot
class ParkingLot:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self, name: str, floors: List[ParkingFloor]):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.name = name
        self.floors = floors
        self.entry_panels: List[EntryPanel] = []
        self.exit_panels: List[ExitPanel] = []
        self._active_tickets: Dict[str, Ticket] = {}

    def add_entry_panel(self, panel_id: str) -> EntryPanel:
        panel = EntryPanel(panel_id, self)
        self.entry_panels.append(panel)
        return panel

    def add_exit_panel(self, panel_id: str) -> ExitPanel:
        panel = ExitPanel(panel_id, self)
        self.exit_panels.append(panel)
        return panel

    def find_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """Find available spot across all floors"""
        for floor in self.floors:
            spot = floor.find_spot_for_vehicle(vehicle)
            if spot:
                return spot
        return None

    def get_available_spots_count(self) -> Dict[SpotType, int]:
        """Get total available spots by type"""
        counts = {SpotType.COMPACT: 0, SpotType.REGULAR: 0, SpotType.LARGE: 0}
        for floor in self.floors:
            for spot in floor.spots:
                if spot.is_available:
                    counts[spot.spot_type] += 1
        return counts

    def is_full(self) -> bool:
        """Check if parking lot is full"""
        for floor in self.floors:
            for spot in floor.spots:
                if spot.is_available:
                    return False
        return True

    def update_all_displays(self):
        """Update display boards on all floors"""
        for floor in self.floors:
            floor.update_display()

# Demo
if __name__ == "__main__":
    # Create parking spots
    floor1_spots = [
        ParkingSpot("1-C1", SpotType.COMPACT),
        ParkingSpot("1-C2", SpotType.COMPACT),
        ParkingSpot("1-R1", SpotType.REGULAR),
        ParkingSpot("1-R2", SpotType.REGULAR),
        ParkingSpot("1-L1", SpotType.LARGE),
    ]

    floor2_spots = [
        ParkingSpot("2-R1", SpotType.REGULAR),
        ParkingSpot("2-R2", SpotType.REGULAR),
        ParkingSpot("2-L1", SpotType.LARGE),
    ]

    # Create floors
    floor1 = ParkingFloor(1, floor1_spots)
    floor2 = ParkingFloor(2, floor2_spots)

    # Create parking lot
    lot = ParkingLot("Downtown Parking", [floor1, floor2])
    entry = lot.add_entry_panel("E1")
    exit_panel = lot.add_exit_panel("X1")

    # Display initial state
    lot.update_all_displays()

    # Park some vehicles
    print("\n=== Parking Vehicles ===")
    car1 = Car("ABC-123")
    ticket1 = entry.get_ticket(car1)

    motorcycle = Motorcycle("MOTO-1")
    ticket2 = entry.get_ticket(motorcycle)

    bus = Bus("BUS-999")
    ticket3 = entry.get_ticket(bus)

    # Display updated state
    lot.update_all_displays()

    # Process exit
    print("\n=== Processing Exit ===")
    if ticket1:
        exit_panel.process_exit(ticket1.ticket_number)

    lot.update_all_displays()
```

### Discussion Points

1. **Scalability**: How would you handle multiple parking lots in a city?
2. **Payment Integration**: How would you integrate different payment methods?
3. **Reservations**: How would you add pre-booking functionality?
4. **Electric Vehicles**: How would you add EV charging spots?

---

## Example 2: LRU Cache

### Problem Statement
Design a Least Recently Used (LRU) cache with O(1) get and put operations.

### Class Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      LRU Cache Class Diagram                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────┐      1    * ┌──────────────────┐             │
│   │      LRUCache       │◆───────────│     CacheNode    │             │
│   ├─────────────────────┤            ├──────────────────┤             │
│   │ - capacity: int     │            │ - key: K         │             │
│   │ - cache: HashMap    │            │ - value: V       │             │
│   │ - head: CacheNode   │            │ - prev: CacheNode│             │
│   │ - tail: CacheNode   │            │ - next: CacheNode│             │
│   ├─────────────────────┤            └──────────────────┘             │
│   │ + get(key): V       │                                             │
│   │ + put(key, value)   │            Doubly Linked List:              │
│   │ - moveToHead(node)  │            ─────────────────────            │
│   │ - removeNode(node)  │                                             │
│   │ - addToHead(node)   │            head ←→ [A] ←→ [B] ←→ [C] ←→ tail│
│   │ - removeTail(): node│                                             │
│   └─────────────────────┘            Most recent → → → Least recent   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Python Implementation

```python
from typing import Optional, TypeVar, Generic
from collections import OrderedDict

K = TypeVar('K')
V = TypeVar('V')

# Custom Implementation
class CacheNode(Generic[K, V]):
    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value
        self.prev: Optional['CacheNode'] = None
        self.next: Optional['CacheNode'] = None

class LRUCache(Generic[K, V]):
    """
    LRU Cache with O(1) get and put operations.

    Uses:
    - HashMap for O(1) key lookup
    - Doubly Linked List for O(1) removal and insertion
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self._cache: dict[K, CacheNode[K, V]] = {}

        # Dummy head and tail for easier operations
        self._head = CacheNode(None, None)
        self._tail = CacheNode(None, None)
        self._head.next = self._tail
        self._tail.prev = self._head

    def get(self, key: K) -> Optional[V]:
        """
        Get value by key. Returns None if not found.
        Moves accessed node to front (most recently used).
        """
        if key not in self._cache:
            return None

        node = self._cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key: K, value: V) -> None:
        """
        Add or update key-value pair.
        If at capacity, evicts least recently used item.
        """
        if key in self._cache:
            # Update existing
            node = self._cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # Add new
            if len(self._cache) >= self.capacity:
                # Evict LRU (tail)
                lru = self._remove_tail()
                del self._cache[lru.key]

            node = CacheNode(key, value)
            self._cache[key] = node
            self._add_to_head(node)

    def _add_to_head(self, node: CacheNode) -> None:
        """Add node right after head (most recent position)"""
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node

    def _remove_node(self, node: CacheNode) -> None:
        """Remove node from its current position"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: CacheNode) -> None:
        """Move existing node to head (mark as most recent)"""
        self._remove_node(node)
        self._add_to_head(node)

    def _remove_tail(self) -> CacheNode:
        """Remove and return the LRU node (right before tail)"""
        lru = self._tail.prev
        self._remove_node(lru)
        return lru

    def __str__(self) -> str:
        """Display cache state for debugging"""
        items = []
        current = self._head.next
        while current != self._tail:
            items.append(f"{current.key}:{current.value}")
            current = current.next
        return f"LRUCache([{' -> '.join(items)}])"

# Simpler implementation using OrderedDict
class SimpleLRUCache(Generic[K, V]):
    """LRU Cache using Python's OrderedDict"""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self._cache = OrderedDict()

    def get(self, key: K) -> Optional[V]:
        if key not in self._cache:
            return None
        self._cache.move_to_end(key)  # Mark as recently used
        return self._cache[key]

    def put(self, key: K, value: V) -> None:
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if len(self._cache) > self.capacity:
            self._cache.popitem(last=False)  # Remove oldest

# Demo
if __name__ == "__main__":
    cache = LRUCache[str, int](3)

    print("=== LRU Cache Demo ===\n")

    cache.put("a", 1)
    print(f"put(a, 1): {cache}")

    cache.put("b", 2)
    print(f"put(b, 2): {cache}")

    cache.put("c", 3)
    print(f"put(c, 3): {cache}")

    print(f"\nget(a) = {cache.get('a')}")  # Moves 'a' to front
    print(f"After get(a): {cache}")

    cache.put("d", 4)  # Evicts 'b' (LRU)
    print(f"\nput(d, 4): {cache}")

    print(f"get(b) = {cache.get('b')}")  # None, was evicted
```

### Java Implementation

```java
import java.util.*;

class LRUCache<K, V> {
    private final int capacity;
    private final Map<K, Node<K, V>> cache;
    private final Node<K, V> head;
    private final Node<K, V> tail;

    static class Node<K, V> {
        K key;
        V value;
        Node<K, V> prev;
        Node<K, V> next;

        Node(K key, V value) {
            this.key = key;
            this.value = value;
        }
    }

    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.cache = new HashMap<>();
        this.head = new Node<>(null, null);
        this.tail = new Node<>(null, null);
        head.next = tail;
        tail.prev = head;
    }

    public V get(K key) {
        Node<K, V> node = cache.get(key);
        if (node == null) return null;
        moveToHead(node);
        return node.value;
    }

    public void put(K key, V value) {
        Node<K, V> node = cache.get(key);
        if (node != null) {
            node.value = value;
            moveToHead(node);
        } else {
            if (cache.size() >= capacity) {
                Node<K, V> lru = removeTail();
                cache.remove(lru.key);
            }
            node = new Node<>(key, value);
            cache.put(key, node);
            addToHead(node);
        }
    }

    private void addToHead(Node<K, V> node) {
        node.prev = head;
        node.next = head.next;
        head.next.prev = node;
        head.next = node;
    }

    private void removeNode(Node<K, V> node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void moveToHead(Node<K, V> node) {
        removeNode(node);
        addToHead(node);
    }

    private Node<K, V> removeTail() {
        Node<K, V> lru = tail.prev;
        removeNode(lru);
        return lru;
    }
}
```

---

## Example 3: Rate Limiter

### Problem Statement
Design a rate limiter that limits requests per time window (e.g., 100 requests per minute).

### Implementation: Token Bucket Algorithm

```python
import time
from threading import Lock
from typing import Dict

class TokenBucket:
    """
    Token Bucket Rate Limiter

    - Bucket holds tokens up to max capacity
    - Tokens are added at a fixed rate
    - Each request consumes one token
    - Request is rejected if no tokens available
    """

    def __init__(self, capacity: int, refill_rate: float):
        """
        Args:
            capacity: Maximum tokens in bucket
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = capacity
        self._last_refill = time.time()
        self._lock = Lock()

    def _refill(self):
        """Add tokens based on time elapsed"""
        now = time.time()
        elapsed = now - self._last_refill
        tokens_to_add = elapsed * self.refill_rate
        self._tokens = min(self.capacity, self._tokens + tokens_to_add)
        self._last_refill = now

    def allow_request(self, tokens: int = 1) -> bool:
        """
        Check if request is allowed.
        Returns True and consumes token if allowed.
        """
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

    @property
    def available_tokens(self) -> float:
        with self._lock:
            self._refill()
            return self._tokens

class RateLimiter:
    """Rate limiter supporting multiple clients"""

    def __init__(self, requests_per_minute: int):
        self._capacity = requests_per_minute
        self._refill_rate = requests_per_minute / 60.0  # per second
        self._buckets: Dict[str, TokenBucket] = {}
        self._lock = Lock()

    def _get_bucket(self, client_id: str) -> TokenBucket:
        """Get or create bucket for client"""
        if client_id not in self._buckets:
            with self._lock:
                if client_id not in self._buckets:
                    self._buckets[client_id] = TokenBucket(
                        self._capacity, self._refill_rate
                    )
        return self._buckets[client_id]

    def allow_request(self, client_id: str) -> bool:
        """Check if request from client is allowed"""
        bucket = self._get_bucket(client_id)
        return bucket.allow_request()

# Sliding Window Rate Limiter
class SlidingWindowRateLimiter:
    """
    Sliding Window Rate Limiter

    More accurate than fixed window but more memory intensive.
    Tracks timestamps of recent requests.
    """

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: Dict[str, list] = {}
        self._lock = Lock()

    def allow_request(self, client_id: str) -> bool:
        with self._lock:
            now = time.time()
            cutoff = now - self.window_seconds

            # Get or create request list
            if client_id not in self._requests:
                self._requests[client_id] = []

            # Remove old requests
            self._requests[client_id] = [
                ts for ts in self._requests[client_id] if ts > cutoff
            ]

            # Check limit
            if len(self._requests[client_id]) < self.max_requests:
                self._requests[client_id].append(now)
                return True

            return False

# Demo
if __name__ == "__main__":
    print("=== Token Bucket Rate Limiter ===\n")
    limiter = RateLimiter(requests_per_minute=10)

    for i in range(15):
        allowed = limiter.allow_request("user-1")
        print(f"Request {i+1}: {'✓ Allowed' if allowed else '✗ Denied'}")

    print("\nWaiting 7 seconds for refill...")
    time.sleep(7)

    for i in range(5):
        allowed = limiter.allow_request("user-1")
        print(f"Request {i+1}: {'✓ Allowed' if allowed else '✗ Denied'}")
```

---

## Example 4: Logger (Chain of Responsibility)

### Implementation

```python
from abc import ABC, abstractmethod
from enum import IntEnum
from datetime import datetime
from typing import Optional

class LogLevel(IntEnum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4

class Logger(ABC):
    """Abstract logger using Chain of Responsibility pattern"""

    def __init__(self, level: LogLevel):
        self._level = level
        self._next: Optional['Logger'] = None

    def set_next(self, logger: 'Logger') -> 'Logger':
        self._next = logger
        return logger

    def log(self, level: LogLevel, message: str):
        if level >= self._level:
            self._write(level, message)
        if self._next:
            self._next.log(level, message)

    @abstractmethod
    def _write(self, level: LogLevel, message: str):
        pass

class ConsoleLogger(Logger):
    def _write(self, level: LogLevel, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level.name}] {message}")

class FileLogger(Logger):
    def __init__(self, level: LogLevel, filename: str):
        super().__init__(level)
        self._filename = filename

    def _write(self, level: LogLevel, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self._filename, 'a') as f:
            f.write(f"[{timestamp}] [{level.name}] {message}\n")

class ErrorAlertLogger(Logger):
    def __init__(self, level: LogLevel = LogLevel.ERROR):
        super().__init__(level)

    def _write(self, level: LogLevel, message: str):
        print(f"🚨 ALERT: {message}")
        # In real system: send email, Slack, PagerDuty, etc.

# Usage
if __name__ == "__main__":
    # Build chain: Console -> File -> Alert
    console = ConsoleLogger(LogLevel.DEBUG)
    file_logger = FileLogger(LogLevel.WARNING, "app.log")
    alert = ErrorAlertLogger(LogLevel.ERROR)

    console.set_next(file_logger).set_next(alert)

    # Log messages
    console.log(LogLevel.DEBUG, "Debug message")
    console.log(LogLevel.INFO, "User logged in")
    console.log(LogLevel.WARNING, "High memory usage")
    console.log(LogLevel.ERROR, "Database connection failed")
```

---

## Interview Checklist

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    LLD Interview Checklist                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   BEFORE CODING:                                                        │
│   ☐ Clarify requirements                                               │
│   ☐ Identify main entities/nouns                                       │
│   ☐ Sketch class diagram                                               │
│   ☐ Discuss relationships (is-a vs has-a)                              │
│   ☐ Identify design patterns that fit                                  │
│                                                                         │
│   DURING CODING:                                                        │
│   ☐ Start with interfaces/abstractions                                 │
│   ☐ Apply SOLID principles                                             │
│   ☐ Consider thread safety                                             │
│   ☐ Handle edge cases                                                  │
│   ☐ Explain decisions as you code                                      │
│                                                                         │
│   AFTER CODING:                                                         │
│   ☐ Walk through a use case                                            │
│   ☐ Discuss trade-offs                                                 │
│   ☐ Mention testing approach                                           │
│   ☐ Suggest extensions/improvements                                    │
│                                                                         │
│   PATTERNS TO KNOW:                                                     │
│   • Singleton (for shared resources)                                   │
│   • Factory (for object creation)                                      │
│   • Strategy (for interchangeable algorithms)                          │
│   • Observer (for event handling)                                      │
│   • State (for state machines)                                         │
│   • Chain of Responsibility (for loggers, validators)                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

This completes the Low Level Design section. Practice implementing these examples from scratch and be ready to extend them based on interviewer's follow-up questions!
