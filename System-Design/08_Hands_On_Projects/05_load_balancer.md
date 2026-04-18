# Project 5: Load Balancer Simulation

Build a simple load balancer with multiple algorithms.

## Problem Description

```
┌────────────────────────────────────────────────────────────────┐
│                     LOAD BALANCER                               │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Build a load balancer that distributes requests across        │
│  multiple backend servers using different algorithms:          │
│                                                                 │
│  1. Round Robin - Rotate through servers sequentially          │
│  2. Weighted Round Robin - Consider server capacity            │
│  3. Least Connections - Send to least busy server              │
│  4. Random - Random server selection                           │
│                                                                 │
│                    ┌─────────────┐                             │
│    Requests ──────►│Load Balancer│──────┬──► Server 1         │
│                    └─────────────┘      ├──► Server 2         │
│                                         └──► Server 3         │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Python Implementation

```python
import random
from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass
import threading
import time

@dataclass
class Server:
    """Represents a backend server."""
    name: str
    weight: int = 1
    active_connections: int = 0
    is_healthy: bool = True

    def connect(self):
        self.active_connections += 1

    def disconnect(self):
        self.active_connections = max(0, self.active_connections - 1)


class LoadBalancer(ABC):
    """Abstract base class for load balancers."""

    def __init__(self, servers: List[Server]):
        self.servers = servers
        self.lock = threading.Lock()

    @abstractmethod
    def get_server(self) -> Optional[Server]:
        """Select a server for the next request."""
        pass

    def get_healthy_servers(self) -> List[Server]:
        """Return only healthy servers."""
        return [s for s in self.servers if s.is_healthy]

    def add_server(self, server: Server):
        with self.lock:
            self.servers.append(server)

    def remove_server(self, server_name: str):
        with self.lock:
            self.servers = [s for s in self.servers if s.name != server_name]


class RoundRobinLB(LoadBalancer):
    """Round Robin: Rotate through servers sequentially."""

    def __init__(self, servers: List[Server]):
        super().__init__(servers)
        self.current_index = 0

    def get_server(self) -> Optional[Server]:
        healthy = self.get_healthy_servers()
        if not healthy:
            return None

        with self.lock:
            self.current_index = self.current_index % len(healthy)
            server = healthy[self.current_index]
            self.current_index += 1

        return server


class WeightedRoundRobinLB(LoadBalancer):
    """Weighted Round Robin: Consider server capacity."""

    def __init__(self, servers: List[Server]):
        super().__init__(servers)
        self.current_index = 0
        self.current_weight = 0

    def get_server(self) -> Optional[Server]:
        healthy = self.get_healthy_servers()
        if not healthy:
            return None

        with self.lock:
            while True:
                self.current_index = self.current_index % len(healthy)

                if self.current_index == 0:
                    self.current_weight -= 1
                    if self.current_weight <= 0:
                        self.current_weight = max(s.weight for s in healthy)

                server = healthy[self.current_index]
                self.current_index += 1

                if server.weight >= self.current_weight:
                    return server


class LeastConnectionsLB(LoadBalancer):
    """Least Connections: Send to server with fewest active connections."""

    def get_server(self) -> Optional[Server]:
        healthy = self.get_healthy_servers()
        if not healthy:
            return None

        with self.lock:
            # Find server with minimum connections
            return min(healthy, key=lambda s: s.active_connections)


class RandomLB(LoadBalancer):
    """Random: Select a random server."""

    def get_server(self) -> Optional[Server]:
        healthy = self.get_healthy_servers()
        if not healthy:
            return None

        return random.choice(healthy)


class IPHashLB(LoadBalancer):
    """IP Hash: Consistent mapping from client IP to server."""

    def get_server(self, client_ip: str = None) -> Optional[Server]:
        healthy = self.get_healthy_servers()
        if not healthy:
            return None

        if client_ip:
            # Hash IP to consistently select same server
            hash_value = hash(client_ip)
            index = hash_value % len(healthy)
            return healthy[index]
        else:
            # Fallback to random
            return random.choice(healthy)


# Demonstration
def simulate_requests(lb: LoadBalancer, num_requests: int, name: str):
    """Simulate requests and show distribution."""
    print(f"\n=== {name} ===")

    distribution = {}
    for server in lb.servers:
        distribution[server.name] = 0

    for _ in range(num_requests):
        server = lb.get_server()
        if server:
            distribution[server.name] += 1
            server.connect()

    print("Request distribution:")
    for server_name, count in distribution.items():
        bar = "█" * (count // 10)
        print(f"  {server_name}: {count:4d} {bar}")


def simulate_with_connections(lb: LoadBalancer, num_requests: int):
    """Simulate with connection tracking."""
    print(f"\n=== Least Connections Demo ===")

    # Simulate some existing connections
    lb.servers[0].active_connections = 10
    lb.servers[1].active_connections = 5
    lb.servers[2].active_connections = 2

    print("Initial connections:")
    for s in lb.servers:
        print(f"  {s.name}: {s.active_connections} connections")

    print("\nNext 5 requests go to:")
    for i in range(5):
        server = lb.get_server()
        print(f"  Request {i+1}: {server.name} (had {server.active_connections} conn)")
        server.connect()


if __name__ == "__main__":
    # Create servers
    servers = [
        Server("server1", weight=1),
        Server("server2", weight=2),
        Server("server3", weight=3),
    ]

    # Test Round Robin
    lb_rr = RoundRobinLB([Server(s.name, s.weight) for s in servers])
    simulate_requests(lb_rr, 100, "Round Robin")

    # Test Weighted Round Robin
    lb_wrr = WeightedRoundRobinLB([Server(s.name, s.weight) for s in servers])
    simulate_requests(lb_wrr, 100, "Weighted Round Robin (weights: 1, 2, 3)")

    # Test Random
    lb_rand = RandomLB([Server(s.name, s.weight) for s in servers])
    simulate_requests(lb_rand, 100, "Random")

    # Test Least Connections
    lb_lc = LeastConnectionsLB([Server(s.name, s.weight) for s in servers])
    simulate_with_connections(lb_lc, 5)

    # Test with health check
    print("\n=== Health Check Demo ===")
    servers_with_failure = [
        Server("server1"),
        Server("server2"),
        Server("server3", is_healthy=False),  # This one is down
    ]
    lb_health = RoundRobinLB(servers_with_failure)

    print("Server3 is unhealthy. Next 6 requests:")
    for i in range(6):
        server = lb_health.get_server()
        print(f"  Request {i+1}: {server.name}")
```

---

## Output Example

```
=== Round Robin ===
Request distribution:
  server1:   34 ███
  server2:   33 ███
  server3:   33 ███

=== Weighted Round Robin (weights: 1, 2, 3) ===
Request distribution:
  server1:   17 █
  server2:   33 ███
  server3:   50 █████

=== Random ===
Request distribution:
  server1:   31 ███
  server2:   35 ███
  server3:   34 ███

=== Least Connections Demo ===
Initial connections:
  server1: 10 connections
  server2: 5 connections
  server3: 2 connections

Next 5 requests go to:
  Request 1: server3 (had 2 conn)
  Request 2: server3 (had 3 conn)
  Request 3: server3 (had 4 conn)
  Request 4: server2 (had 5 conn)
  Request 5: server3 (had 5 conn)
```

---

## Algorithm Comparison

| Algorithm | Use Case | Pros | Cons |
|-----------|----------|------|------|
| Round Robin | Equal servers | Simple, fair | Ignores server capacity |
| Weighted RR | Different capacities | Respects weights | Static weights |
| Least Conn | Varying request times | Adaptive | More overhead |
| Random | Simple needs | No state needed | Not deterministic |
| IP Hash | Session affinity | Sticky sessions | Uneven if IPs cluster |

---

## Extensions

### 1. Health Checks
```python
def health_check(self):
    """Periodically check server health."""
    for server in self.servers:
        try:
            # Ping server or check /health endpoint
            response = requests.get(f"http://{server.name}/health", timeout=2)
            server.is_healthy = response.status_code == 200
        except:
            server.is_healthy = False
```

### 2. Circuit Breaker Integration
```python
def get_server_with_circuit_breaker(self):
    """Skip servers with open circuit breakers."""
    healthy = [s for s in self.servers
               if s.is_healthy and not s.circuit_breaker.is_open]
    # ... rest of selection logic
```

---

*Next: [Message Queue](06_message_queue.md) →*
