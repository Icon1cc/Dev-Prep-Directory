# Structural Design Patterns

## What are Structural Patterns?

Structural patterns deal with **object composition**—how classes and objects are composed to form larger structures. They help ensure that when parts of a system change, the entire structure doesn't need to change.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   Structural Patterns Overview                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Pattern    │ Purpose                        │ Real-World Analogy       │
│  ───────────┼────────────────────────────────┼───────────────────────── │
│  Adapter    │ Convert incompatible interfaces│ Power plug adapter       │
│  Decorator  │ Add behavior dynamically       │ Coffee with toppings     │
│  Proxy      │ Control access to object       │ Credit card for cash     │
│  Facade     │ Simplify complex subsystem     │ Hotel concierge          │
│  Composite  │ Tree structures                │ File/folder hierarchy    │
│  Bridge     │ Separate abstraction from impl │ Remote + TV brands       │
│  Flyweight  │ Share common state             │ Character fonts          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Adapter Pattern

### Intent
Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces.

### Real-World Analogy
When you travel to a country with different electrical outlets, you use a **power adapter**. The adapter doesn't change the electricity—it just makes your plug compatible with the foreign socket.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Adapter Pattern Structure                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌────────────┐         ┌─────────────┐         ┌─────────────┐       │
│   │   Client   │────────►│   Target    │         │   Adaptee   │       │
│   └────────────┘         │  Interface  │         ├─────────────┤       │
│                          ├─────────────┤         │ + specificOp│       │
│                          │ + request() │         └─────────────┘       │
│                          └─────────────┘                ▲              │
│                                 ▲                       │              │
│                                 │                       │              │
│                          ┌─────────────┐               │              │
│                          │   Adapter   │───────────────┘              │
│                          ├─────────────┤   (wraps adaptee)            │
│                          │ + request() │                               │
│                          └─────────────┘                               │
│                                                                         │
│   How it works:                                                         │
│   1. Client calls adapter.request()                                     │
│   2. Adapter translates to adaptee.specificOperation()                  │
│   3. Result is translated back and returned                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### When to Use
- Integrating legacy code with new systems
- Using third-party libraries with incompatible interfaces
- Unifying interfaces of similar classes from different sources
- Wrapping external APIs to match your internal interface

### When NOT to Use
- When interfaces are similar enough to use directly
- When you can modify the original class
- When adapting too many methods (consider redesign)

### Python Implementation

```python
from abc import ABC, abstractmethod

# Target Interface - what the client expects
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float, currency: str) -> bool:
        pass

    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        pass

# Adaptee - Third-party payment service with different interface
class StripeAPI:
    """Legacy/third-party service with incompatible interface"""

    def create_charge(self, amount_cents: int, currency_code: str) -> dict:
        print(f"Stripe: Charging {amount_cents} cents in {currency_code}")
        return {"id": "ch_123", "status": "succeeded"}

    def create_refund(self, charge_id: str, amount_cents: int = None) -> dict:
        print(f"Stripe: Refunding charge {charge_id}")
        return {"id": "re_456", "status": "succeeded"}

# Another Adaptee - Different payment service
class PayPalAPI:
    """Another service with its own interface"""

    def send_payment(self, value: float, currency: str) -> str:
        print(f"PayPal: Sending ${value} {currency}")
        return "PAYID-123456"

    def reverse_payment(self, payment_id: str) -> bool:
        print(f"PayPal: Reversing payment {payment_id}")
        return True

# Adapter for Stripe
class StripeAdapter(PaymentProcessor):
    """Adapts Stripe API to PaymentProcessor interface"""

    def __init__(self):
        self._stripe = StripeAPI()
        self._transactions = {}  # Store transaction mappings

    def process_payment(self, amount: float, currency: str) -> bool:
        # Convert dollars to cents (Stripe uses cents)
        amount_cents = int(amount * 100)
        currency_code = currency.lower()

        result = self._stripe.create_charge(amount_cents, currency_code)

        if result["status"] == "succeeded":
            self._transactions[result["id"]] = result
            return True
        return False

    def refund(self, transaction_id: str) -> bool:
        result = self._stripe.create_refund(transaction_id)
        return result["status"] == "succeeded"

# Adapter for PayPal
class PayPalAdapter(PaymentProcessor):
    """Adapts PayPal API to PaymentProcessor interface"""

    def __init__(self):
        self._paypal = PayPalAPI()
        self._transactions = {}

    def process_payment(self, amount: float, currency: str) -> bool:
        payment_id = self._paypal.send_payment(amount, currency)

        if payment_id:
            self._transactions[payment_id] = True
            return True
        return False

    def refund(self, transaction_id: str) -> bool:
        return self._paypal.reverse_payment(transaction_id)

# Client code - works with any PaymentProcessor
class CheckoutService:
    def __init__(self, payment_processor: PaymentProcessor):
        self._processor = payment_processor

    def checkout(self, cart_total: float, currency: str = "USD") -> bool:
        print(f"\n--- Processing ${cart_total} {currency} ---")
        return self._processor.process_payment(cart_total, currency)

# Usage
if __name__ == "__main__":
    # Client code is identical regardless of payment provider

    # Using Stripe
    stripe_checkout = CheckoutService(StripeAdapter())
    stripe_checkout.checkout(99.99, "USD")

    # Using PayPal
    paypal_checkout = CheckoutService(PayPalAdapter())
    paypal_checkout.checkout(49.99, "USD")
```

### Java Implementation

```java
// Target Interface
interface PaymentProcessor {
    boolean processPayment(double amount, String currency);
    boolean refund(String transactionId);
}

// Adaptee - Legacy/Third-party service
class StripeAPI {
    public Map<String, Object> createCharge(int amountCents, String currencyCode) {
        System.out.println("Stripe: Charging " + amountCents + " cents in " + currencyCode);
        Map<String, Object> result = new HashMap<>();
        result.put("id", "ch_123");
        result.put("status", "succeeded");
        return result;
    }

    public Map<String, Object> createRefund(String chargeId) {
        System.out.println("Stripe: Refunding charge " + chargeId);
        Map<String, Object> result = new HashMap<>();
        result.put("id", "re_456");
        result.put("status", "succeeded");
        return result;
    }
}

// Adapter
class StripeAdapter implements PaymentProcessor {
    private StripeAPI stripe;
    private Map<String, Map<String, Object>> transactions;

    public StripeAdapter() {
        this.stripe = new StripeAPI();
        this.transactions = new HashMap<>();
    }

    @Override
    public boolean processPayment(double amount, String currency) {
        // Convert dollars to cents
        int amountCents = (int) (amount * 100);
        String currencyCode = currency.toLowerCase();

        Map<String, Object> result = stripe.createCharge(amountCents, currencyCode);

        if ("succeeded".equals(result.get("status"))) {
            transactions.put((String) result.get("id"), result);
            return true;
        }
        return false;
    }

    @Override
    public boolean refund(String transactionId) {
        Map<String, Object> result = stripe.createRefund(transactionId);
        return "succeeded".equals(result.get("status"));
    }
}

// Client
class CheckoutService {
    private PaymentProcessor processor;

    public CheckoutService(PaymentProcessor processor) {
        this.processor = processor;
    }

    public boolean checkout(double cartTotal, String currency) {
        System.out.println("\n--- Processing $" + cartTotal + " " + currency + " ---");
        return processor.processPayment(cartTotal, currency);
    }
}
```

### Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "Why not just modify the original class?" | Understanding when adapter is appropriate | Can't modify third-party code; don't want to change stable interfaces |
| "Adapter vs Facade?" | Pattern distinction | Adapter converts interface; Facade simplifies multiple interfaces |
| "Object adapter vs Class adapter?" | Implementation approaches | Object uses composition (flexible); Class uses inheritance (compile-time) |

---

## 2. Decorator Pattern

### Intent
Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.

### Real-World Analogy
Think of ordering coffee. You start with a base coffee, then add decorations: milk, sugar, whipped cream, etc. Each addition wraps the previous order and adds its own cost and description.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Decorator Pattern Structure                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌────────────────┐                                                    │
│   │   Component    │◄─────────────────────────────────────┐            │
│   │   (interface)  │                                       │            │
│   ├────────────────┤                                       │            │
│   │ + operation()  │                                       │            │
│   └────────────────┘                                       │            │
│          ▲                                                 │            │
│          │                                                 │            │
│    ┌─────┴─────────────────────┐                          │            │
│    │                           │                          │            │
│   ┌┴────────────────┐    ┌─────┴──────────┐              │            │
│   │ConcreteComponent│    │   Decorator    │──────────────┘            │
│   ├─────────────────┤    ├────────────────┤  (wraps component)         │
│   │ + operation()   │    │ - component    │                            │
│   └─────────────────┘    │ + operation()  │                            │
│                          └────────────────┘                            │
│                                  ▲                                      │
│                    ┌─────────────┴─────────────┐                       │
│               ┌────┴───────┐            ┌──────┴─────┐                 │
│               │DecoratorA  │            │DecoratorB  │                 │
│               ├────────────┤            ├────────────┤                 │
│               │+operation()│            │+operation()│                 │
│               └────────────┘            └────────────┘                 │
│                                                                         │
│   Wrapping Chain:                                                       │
│   DecoratorB( DecoratorA( ConcreteComponent ) )                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### When to Use
- Adding features to objects without changing their class
- When extension by subclassing is impractical (explosion of subclasses)
- When you need to add/remove features at runtime
- Implementing cross-cutting concerns (logging, caching, validation)

### When NOT to Use
- When you need to change the object's core behavior (not just add to it)
- When the order of decoration doesn't matter and all are always applied
- When component interface has many methods (decorator becomes verbose)

### Python Implementation

```python
from abc import ABC, abstractmethod
from typing import List

# Component Interface
class DataSource(ABC):
    @abstractmethod
    def write_data(self, data: str) -> None:
        pass

    @abstractmethod
    def read_data(self) -> str:
        pass

# Concrete Component
class FileDataSource(DataSource):
    def __init__(self, filename: str):
        self._filename = filename
        self._data = ""

    def write_data(self, data: str) -> None:
        print(f"Writing to file: {self._filename}")
        self._data = data

    def read_data(self) -> str:
        print(f"Reading from file: {self._filename}")
        return self._data

# Base Decorator
class DataSourceDecorator(DataSource):
    def __init__(self, source: DataSource):
        self._wrapped = source

    def write_data(self, data: str) -> None:
        self._wrapped.write_data(data)

    def read_data(self) -> str:
        return self._wrapped.read_data()

# Concrete Decorators
class EncryptionDecorator(DataSourceDecorator):
    """Adds encryption capability"""

    def __init__(self, source: DataSource, key: str = "secret"):
        super().__init__(source)
        self._key = key

    def write_data(self, data: str) -> None:
        encrypted = self._encrypt(data)
        print(f"Encrypting data with key: {self._key}")
        super().write_data(encrypted)

    def read_data(self) -> str:
        data = super().read_data()
        print(f"Decrypting data with key: {self._key}")
        return self._decrypt(data)

    def _encrypt(self, data: str) -> str:
        # Simple XOR encryption for demo
        return ''.join(chr(ord(c) ^ ord(self._key[i % len(self._key)]))
                       for i, c in enumerate(data))

    def _decrypt(self, data: str) -> str:
        # XOR is symmetric
        return self._encrypt(data)

class CompressionDecorator(DataSourceDecorator):
    """Adds compression capability"""

    def write_data(self, data: str) -> None:
        compressed = self._compress(data)
        print(f"Compressing data: {len(data)} -> {len(compressed)} chars")
        super().write_data(compressed)

    def read_data(self) -> str:
        data = super().read_data()
        print("Decompressing data")
        return self._decompress(data)

    def _compress(self, data: str) -> str:
        # Simple run-length encoding for demo
        import zlib
        import base64
        compressed = zlib.compress(data.encode())
        return base64.b64encode(compressed).decode()

    def _decompress(self, data: str) -> str:
        import zlib
        import base64
        decompressed = zlib.decompress(base64.b64decode(data.encode()))
        return decompressed.decode()

class LoggingDecorator(DataSourceDecorator):
    """Adds logging capability"""

    def write_data(self, data: str) -> None:
        print(f"[LOG] Writing {len(data)} characters")
        super().write_data(data)

    def read_data(self) -> str:
        print("[LOG] Reading data")
        data = super().read_data()
        print(f"[LOG] Read {len(data)} characters")
        return data

# Usage - decorators can be stacked in any order
if __name__ == "__main__":
    # Basic file source
    source = FileDataSource("data.txt")

    # Add logging
    source = LoggingDecorator(source)

    # Add compression
    source = CompressionDecorator(source)

    # Add encryption (outermost layer)
    source = EncryptionDecorator(source, key="mykey")

    # Client uses same interface regardless of decorations
    print("\n=== Writing Data ===")
    source.write_data("Hello, World! This is sensitive data.")

    print("\n=== Reading Data ===")
    result = source.read_data()
    print(f"Final result: {result}")
```

### Java Implementation

```java
import java.util.Base64;
import java.util.zip.*;

// Component Interface
interface DataSource {
    void writeData(String data);
    String readData();
}

// Concrete Component
class FileDataSource implements DataSource {
    private String filename;
    private String data = "";

    public FileDataSource(String filename) {
        this.filename = filename;
    }

    @Override
    public void writeData(String data) {
        System.out.println("Writing to file: " + filename);
        this.data = data;
    }

    @Override
    public String readData() {
        System.out.println("Reading from file: " + filename);
        return data;
    }
}

// Base Decorator
abstract class DataSourceDecorator implements DataSource {
    protected DataSource wrapped;

    public DataSourceDecorator(DataSource source) {
        this.wrapped = source;
    }

    @Override
    public void writeData(String data) {
        wrapped.writeData(data);
    }

    @Override
    public String readData() {
        return wrapped.readData();
    }
}

// Concrete Decorator - Encryption
class EncryptionDecorator extends DataSourceDecorator {
    public EncryptionDecorator(DataSource source) {
        super(source);
    }

    @Override
    public void writeData(String data) {
        System.out.println("Encrypting data");
        String encrypted = Base64.getEncoder().encodeToString(data.getBytes());
        super.writeData(encrypted);
    }

    @Override
    public String readData() {
        String data = super.readData();
        System.out.println("Decrypting data");
        return new String(Base64.getDecoder().decode(data));
    }
}

// Concrete Decorator - Compression
class CompressionDecorator extends DataSourceDecorator {
    public CompressionDecorator(DataSource source) {
        super(source);
    }

    @Override
    public void writeData(String data) {
        System.out.println("Compressing data: " + data.length() + " chars");
        // Compression logic here
        super.writeData(data);  // Simplified
    }

    @Override
    public String readData() {
        System.out.println("Decompressing data");
        return super.readData();  // Simplified
    }
}

// Client
public class DecoratorDemo {
    public static void main(String[] args) {
        // Stack decorators
        DataSource source = new FileDataSource("data.txt");
        source = new CompressionDecorator(source);
        source = new EncryptionDecorator(source);

        source.writeData("Sensitive information");
        System.out.println("Result: " + source.readData());
    }
}
```

### Decorator vs Inheritance

```
┌─────────────────────────────────────────────────────────────────────────┐
│              Inheritance vs Decorator Comparison                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Inheritance (Static)                 Decorator (Dynamic)              │
│   ────────────────────                 ────────────────────             │
│                                                                         │
│   • Behavior set at compile time       • Behavior set at runtime        │
│   • Subclass explosion problem         • Compose behaviors flexibly     │
│   • Cannot change at runtime           • Can add/remove at runtime      │
│   • Breaks encapsulation               • Preserves encapsulation        │
│                                                                         │
│   Example: Coffee with 3 addons × 2 sizes = 6 subclasses               │
│   With Decorator: 1 base + 3 decorators = 4 classes                    │
│                                                                         │
│   Inheritance Tree:                    Decorator Chain:                 │
│                                                                         │
│         Coffee                              Coffee                      │
│         /    \                                │                         │
│      Small  Large                        MilkDecorator                  │
│      / \    / \                               │                         │
│   +Milk +Sugar...   (explosion!)        SugarDecorator                  │
│                                               │                         │
│                                          (flexible!)                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "Decorator vs Proxy?" | Pattern distinction | Decorator adds behavior; Proxy controls access |
| "Can decorators modify the interface?" | Understanding constraints | No, decorators preserve the interface—that's the point |
| "Order matters?" | Implementation understanding | Yes, decoration order affects behavior (encryption before compression ≠ compression before encryption) |

---

## 3. Proxy Pattern

### Intent
Provide a surrogate or placeholder for another object to control access to it.

### Real-World Analogy
A **credit card** is a proxy for a bank account. It provides the same interface (paying for things) but adds access control (credit limit), lazy loading (doesn't need cash upfront), and logging (transaction history).

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       Proxy Pattern Structure                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌────────────┐         ┌─────────────────┐                           │
│   │   Client   │────────►│    Subject      │                           │
│   └────────────┘         │   (interface)   │                           │
│                          ├─────────────────┤                           │
│                          │ + request()     │                           │
│                          └─────────────────┘                           │
│                                  ▲                                      │
│                    ┌─────────────┴─────────────┐                       │
│                    │                           │                       │
│              ┌─────┴─────┐              ┌──────┴──────┐                │
│              │   Proxy   │─────────────►│ RealSubject │                │
│              ├───────────┤  (reference)  ├─────────────┤                │
│              │+ request()│              │ + request() │                │
│              └───────────┘              └─────────────┘                │
│                                                                         │
│   Types of Proxies:                                                     │
│   ─────────────────                                                     │
│   • Virtual Proxy:    Lazy initialization, load on demand              │
│   • Protection Proxy: Access control, permission checking              │
│   • Remote Proxy:     Local representative for remote object           │
│   • Logging Proxy:    Log all operations                               │
│   • Caching Proxy:    Cache expensive operations                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### When to Use
- **Lazy initialization** (virtual proxy): Delay creating expensive objects
- **Access control** (protection proxy): Check permissions before access
- **Remote objects** (remote proxy): Represent objects in different address space
- **Logging/auditing**: Track all operations
- **Caching**: Cache results of expensive operations

### When NOT to Use
- When the overhead of proxy isn't worth the benefit
- When you need to intercept and modify the interface (use Adapter)
- When you need to add behavior dynamically (use Decorator)

### Python Implementation

```python
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import datetime
import time

# Subject Interface
class Database(ABC):
    @abstractmethod
    def query(self, sql: str) -> list:
        pass

    @abstractmethod
    def execute(self, sql: str) -> bool:
        pass

# Real Subject - Heavy object
class RealDatabase(Database):
    def __init__(self, connection_string: str):
        print(f"Connecting to database: {connection_string}")
        # Simulate expensive connection
        time.sleep(1)
        self._connection_string = connection_string
        self._connected = True
        print("Database connection established!")

    def query(self, sql: str) -> list:
        print(f"Executing query: {sql}")
        # Simulate query
        time.sleep(0.5)
        return [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]

    def execute(self, sql: str) -> bool:
        print(f"Executing: {sql}")
        time.sleep(0.3)
        return True

# Virtual Proxy - Lazy initialization
class LazyDatabaseProxy(Database):
    """Delays database connection until first use"""

    def __init__(self, connection_string: str):
        self._connection_string = connection_string
        self._database: Optional[RealDatabase] = None

    def _get_database(self) -> RealDatabase:
        if self._database is None:
            print("Lazy loading database connection...")
            self._database = RealDatabase(self._connection_string)
        return self._database

    def query(self, sql: str) -> list:
        return self._get_database().query(sql)

    def execute(self, sql: str) -> bool:
        return self._get_database().execute(sql)

# Protection Proxy - Access control
class SecureDatabaseProxy(Database):
    """Controls access based on user permissions"""

    def __init__(self, database: Database, user_role: str):
        self._database = database
        self._user_role = user_role
        self._permissions = {
            "admin": ["SELECT", "INSERT", "UPDATE", "DELETE", "DROP"],
            "user": ["SELECT", "INSERT", "UPDATE"],
            "readonly": ["SELECT"]
        }

    def _check_permission(self, sql: str) -> bool:
        operation = sql.strip().split()[0].upper()
        allowed = self._permissions.get(self._user_role, [])

        if operation not in allowed:
            raise PermissionError(
                f"User role '{self._user_role}' cannot perform {operation}"
            )
        return True

    def query(self, sql: str) -> list:
        self._check_permission(sql)
        return self._database.query(sql)

    def execute(self, sql: str) -> bool:
        self._check_permission(sql)
        return self._database.execute(sql)

# Caching Proxy
class CachingDatabaseProxy(Database):
    """Caches query results"""

    def __init__(self, database: Database, ttl_seconds: int = 60):
        self._database = database
        self._cache: Dict[str, tuple] = {}  # sql -> (result, timestamp)
        self._ttl = ttl_seconds

    def query(self, sql: str) -> list:
        # Check cache
        if sql in self._cache:
            result, timestamp = self._cache[sql]
            age = (datetime.now() - timestamp).total_seconds()

            if age < self._ttl:
                print(f"Cache HIT for: {sql[:30]}... (age: {age:.1f}s)")
                return result
            else:
                print(f"Cache EXPIRED for: {sql[:30]}...")
                del self._cache[sql]

        # Cache miss - query database
        print(f"Cache MISS for: {sql[:30]}...")
        result = self._database.query(sql)
        self._cache[sql] = (result, datetime.now())
        return result

    def execute(self, sql: str) -> bool:
        # Invalidate cache on write operations
        self._cache.clear()
        print("Cache invalidated due to write operation")
        return self._database.execute(sql)

# Logging Proxy
class LoggingDatabaseProxy(Database):
    """Logs all database operations"""

    def __init__(self, database: Database):
        self._database = database
        self._log: list = []

    def _log_operation(self, operation: str, sql: str, duration: float):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "sql": sql,
            "duration_ms": duration * 1000
        }
        self._log.append(entry)
        print(f"[LOG] {operation} ({duration*1000:.1f}ms): {sql[:50]}...")

    def query(self, sql: str) -> list:
        start = time.time()
        result = self._database.query(sql)
        self._log_operation("QUERY", sql, time.time() - start)
        return result

    def execute(self, sql: str) -> bool:
        start = time.time()
        result = self._database.execute(sql)
        self._log_operation("EXECUTE", sql, time.time() - start)
        return result

    def get_audit_log(self) -> list:
        return self._log.copy()

# Usage - combining proxies
if __name__ == "__main__":
    # Create layered proxies
    print("=== Creating Proxy Chain ===\n")

    # Start with lazy loading
    db = LazyDatabaseProxy("postgresql://localhost/mydb")

    # Add caching
    db = CachingDatabaseProxy(db, ttl_seconds=30)

    # Add logging
    db = LoggingDatabaseProxy(db)

    # Add security (outermost)
    db = SecureDatabaseProxy(db, user_role="user")

    print("\n=== Database Created (Not Connected Yet) ===\n")

    # First query triggers connection
    print("=== First Query ===")
    result = db.query("SELECT * FROM users")
    print(f"Result: {result}\n")

    # Second query hits cache
    print("=== Second Query (Same) ===")
    result = db.query("SELECT * FROM users")
    print(f"Result: {result}\n")

    # Write operation
    print("=== Write Operation ===")
    db.execute("INSERT INTO users VALUES (3, 'Bob')")

    # This would fail - user role can't DROP
    print("\n=== Attempting Forbidden Operation ===")
    try:
        db.execute("DROP TABLE users")
    except PermissionError as e:
        print(f"Access denied: {e}")
```

### Java Implementation

```java
import java.util.*;
import java.time.*;

// Subject Interface
interface ImageLoader {
    void display();
    String getFilename();
}

// Real Subject - Heavy object
class RealImage implements ImageLoader {
    private String filename;
    private byte[] imageData;

    public RealImage(String filename) {
        this.filename = filename;
        loadFromDisk();
    }

    private void loadFromDisk() {
        System.out.println("Loading image from disk: " + filename);
        // Simulate heavy loading
        try { Thread.sleep(2000); } catch (InterruptedException e) {}
        this.imageData = new byte[1024 * 1024]; // 1MB placeholder
        System.out.println("Image loaded!");
    }

    @Override
    public void display() {
        System.out.println("Displaying image: " + filename);
    }

    @Override
    public String getFilename() {
        return filename;
    }
}

// Virtual Proxy - Lazy Loading
class LazyImageProxy implements ImageLoader {
    private String filename;
    private RealImage realImage;

    public LazyImageProxy(String filename) {
        this.filename = filename;
        // NOT loading the image yet!
    }

    @Override
    public void display() {
        if (realImage == null) {
            System.out.println("Lazy loading image...");
            realImage = new RealImage(filename);
        }
        realImage.display();
    }

    @Override
    public String getFilename() {
        return filename; // No need to load for metadata
    }
}

// Protection Proxy
class SecureImageProxy implements ImageLoader {
    private ImageLoader image;
    private Set<String> allowedUsers;
    private String currentUser;

    public SecureImageProxy(ImageLoader image, String currentUser) {
        this.image = image;
        this.currentUser = currentUser;
        this.allowedUsers = new HashSet<>(Arrays.asList("admin", "editor"));
    }

    @Override
    public void display() {
        if (!allowedUsers.contains(currentUser)) {
            throw new SecurityException("User " + currentUser + " cannot access this image");
        }
        image.display();
    }

    @Override
    public String getFilename() {
        return image.getFilename();
    }
}

// Demo
public class ProxyDemo {
    public static void main(String[] args) {
        // Without proxy - loads immediately
        System.out.println("=== Without Proxy ===");
        ImageLoader heavyImage = new RealImage("photo.jpg");

        System.out.println("\n=== With Proxy ===");
        // With proxy - doesn't load until display() called
        ImageLoader lazyImage = new LazyImageProxy("large_photo.jpg");
        System.out.println("Proxy created, image NOT loaded yet");
        System.out.println("Getting filename: " + lazyImage.getFilename());
        System.out.println("Now displaying (will load):");
        lazyImage.display();
    }
}
```

### Proxy vs Decorator vs Adapter

```
┌─────────────────────────────────────────────────────────────────────────┐
│              Pattern Comparison: Proxy vs Decorator vs Adapter          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Pattern   │ Interface  │ Purpose                │ Relationship        │
│   ──────────┼────────────┼────────────────────────┼──────────────────── │
│   Proxy     │ Same       │ Control access         │ Often creates object│
│   Decorator │ Same       │ Add behavior           │ Never creates object│
│   Adapter   │ Different  │ Convert interface      │ Wraps existing obj  │
│                                                                         │
│   Mental Models:                                                        │
│   ─────────────                                                         │
│   Proxy:     "I'll handle this on behalf of the real object"           │
│   Decorator: "I'll do what you do, plus something extra"               │
│   Adapter:   "I'll translate your language to theirs"                  │
│                                                                         │
│   Example - Database Access:                                            │
│   ─────────────────────────                                             │
│   Proxy:     LazyDatabaseProxy (delays connection until needed)         │
│   Decorator: LoggingDatabase (adds logging to any database)             │
│   Adapter:   MySQLToPostgresAdapter (converts MySQL calls to Postgres)  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "When would you use virtual proxy?" | Practical application | Expensive objects that might not be used; images in a gallery, reports in a list |
| "Proxy vs Facade?" | Pattern distinction | Proxy has same interface; Facade simplifies multiple interfaces |
| "Can you combine proxies?" | Implementation flexibility | Yes, chain like decorators: Logging(Caching(Security(RealDB))) |

---

## 4. Facade Pattern

### Intent
Provide a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use.

### Real-World Analogy
A **hotel concierge** is a facade. Instead of calling the restaurant, taxi service, theater box office, and tour guide separately, you just tell the concierge what you want. They handle all the complex coordination.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Facade Pattern Structure                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Before Facade:                     After Facade:                      │
│   ──────────────                     ─────────────                      │
│                                                                         │
│   ┌────────┐                        ┌────────┐                         │
│   │ Client │                        │ Client │                         │
│   └────────┘                        └────────┘                         │
│       │                                  │                              │
│       ├───────┬───────┬───────┐         │                              │
│       ▼       ▼       ▼       ▼         ▼                              │
│   ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   ┌────────┐                        │
│   │  A  │ │  B  │ │  C  │ │  D  │   │ Facade │                        │
│   └─────┘ └─────┘ └─────┘ └─────┘   └────────┘                        │
│                                          │                              │
│   Complex coupling!                      ├───────┬───────┬───────┐     │
│                                          ▼       ▼       ▼       ▼     │
│                                      ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │
│                                      │  A  │ │  B  │ │  C  │ │  D  │  │
│                                      └─────┘ └─────┘ └─────┘ └─────┘  │
│                                                                         │
│                                      Simple interface!                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### When to Use
- Simplifying complex subsystem interactions
- Layered architecture (facade for each layer)
- Reducing coupling between clients and subsystems
- Providing a simple default for common operations

### When NOT to Use
- When clients need fine-grained control over subsystems
- When the facade becomes a "god class" with too many methods

### Python Implementation

```python
# Complex Subsystem Classes
class VideoFile:
    def __init__(self, filename: str):
        self.filename = filename
        self.codec_type = filename.split('.')[-1]

    def get_codec(self) -> str:
        return self.codec_type

class CodecFactory:
    @staticmethod
    def extract(file: VideoFile) -> 'Codec':
        codec_type = file.get_codec()
        if codec_type == "mp4":
            return MPEG4Codec()
        elif codec_type == "ogg":
            return OggCodec()
        else:
            raise ValueError(f"Unknown codec: {codec_type}")

class Codec:
    pass

class MPEG4Codec(Codec):
    def __init__(self):
        print("MPEG4Codec initialized")

class OggCodec(Codec):
    def __init__(self):
        print("OggCodec initialized")

class BitrateReader:
    @staticmethod
    def read(file: VideoFile, codec: Codec) -> bytes:
        print(f"Reading bitrate from {file.filename}")
        return b"video_buffer_data"

    @staticmethod
    def convert(buffer: bytes, codec: Codec) -> bytes:
        print("Converting bitrate")
        return b"converted_video_data"

class AudioMixer:
    def fix(self, result: bytes) -> bytes:
        print("Fixing audio...")
        return b"final_video_with_audio"

# FACADE - Simplifies the complex video conversion process
class VideoConverter:
    """
    Facade that hides the complexity of video conversion.
    Client just calls convert() with filename and format.
    """

    def convert(self, filename: str, target_format: str) -> bytes:
        print(f"\n=== Converting {filename} to {target_format} ===\n")

        # Step 1: Load the file
        file = VideoFile(filename)

        # Step 2: Extract appropriate codec
        source_codec = CodecFactory.extract(file)

        # Step 3: Determine target codec
        if target_format == "mp4":
            target_codec = MPEG4Codec()
        else:
            target_codec = OggCodec()

        # Step 4: Read and convert bitrate
        buffer = BitrateReader.read(file, source_codec)
        result = BitrateReader.convert(buffer, target_codec)

        # Step 5: Fix audio
        mixer = AudioMixer()
        final_result = mixer.fix(result)

        print(f"\n=== Conversion complete! ===")
        return final_result

# Client code is now simple
if __name__ == "__main__":
    converter = VideoConverter()

    # Convert a video - one simple call!
    mp4_video = converter.convert("movie.ogg", "mp4")
```

### Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "Facade vs Adapter?" | Pattern distinction | Facade simplifies; Adapter converts interfaces |
| "Does Facade break OCP?" | Design principles | No, clients can still access subsystems directly if needed |
| "Facade vs API Gateway?" | System design connection | API Gateway is a facade for microservices |

---

## 5. Composite Pattern

### Intent
Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions uniformly.

### Real-World Analogy
A **file system**: both files and folders implement a common interface (getSize, delete). A folder contains files and other folders. Operations work uniformly on both.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Composite Pattern Structure                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌───────────────────┐                                                 │
│   │     Component     │◄──────────────────────────────┐                │
│   │    (interface)    │                               │                │
│   ├───────────────────┤                               │                │
│   │ + operation()     │                               │                │
│   │ + add(Component)  │                               │ children       │
│   │ + remove(c)       │                               │                │
│   │ + getChild(i)     │                               │                │
│   └───────────────────┘                               │                │
│            ▲                                          │                │
│      ┌─────┴─────────────────┐                       │                │
│      │                       │                       │                │
│   ┌──┴───────────┐    ┌──────┴───────┐              │                │
│   │     Leaf     │    │   Composite  │──────────────┘                │
│   ├──────────────┤    ├──────────────┤                                │
│   │ + operation()│    │ - children   │                                │
│   └──────────────┘    │ + operation()│ ──► delegates to children      │
│                       │ + add()      │                                │
│                       │ + remove()   │                                │
│                       └──────────────┘                                │
│                                                                         │
│   Example Tree:                                                         │
│                        ┌───────────┐                                   │
│                        │ Composite │                                   │
│                        │  (root)   │                                   │
│                        └─────┬─────┘                                   │
│                    ┌─────────┼─────────┐                               │
│                    ▼         ▼         ▼                               │
│               ┌───────┐ ┌───────┐ ┌────────┐                          │
│               │ Leaf  │ │ Leaf  │ │Composit│                          │
│               └───────┘ └───────┘ └────┬───┘                          │
│                                    ┌───┴───┐                           │
│                                    ▼       ▼                           │
│                               ┌───────┐ ┌───────┐                      │
│                               │ Leaf  │ │ Leaf  │                      │
│                               └───────┘ └───────┘                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Python Implementation

```python
from abc import ABC, abstractmethod
from typing import List

# Component
class FileSystemItem(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> None:
        pass

# Leaf
class File(FileSystemItem):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size

    def get_size(self) -> int:
        return self._size

    def display(self, indent: int = 0) -> None:
        print(" " * indent + f"📄 {self.name} ({self._size} bytes)")

# Composite
class Directory(FileSystemItem):
    def __init__(self, name: str):
        super().__init__(name)
        self._children: List[FileSystemItem] = []

    def add(self, item: FileSystemItem) -> None:
        self._children.append(item)

    def remove(self, item: FileSystemItem) -> None:
        self._children.remove(item)

    def get_size(self) -> int:
        # Recursively sum sizes of all children
        return sum(child.get_size() for child in self._children)

    def display(self, indent: int = 0) -> None:
        print(" " * indent + f"📁 {self.name}/ ({self.get_size()} bytes)")
        for child in self._children:
            child.display(indent + 4)

# Usage
if __name__ == "__main__":
    # Build tree structure
    root = Directory("root")

    documents = Directory("documents")
    documents.add(File("resume.pdf", 1024))
    documents.add(File("cover_letter.docx", 512))

    pictures = Directory("pictures")
    pictures.add(File("photo1.jpg", 2048))
    pictures.add(File("photo2.jpg", 3072))

    vacation = Directory("vacation")
    vacation.add(File("beach.jpg", 4096))
    pictures.add(vacation)

    root.add(documents)
    root.add(pictures)
    root.add(File("notes.txt", 256))

    # Operations work uniformly
    print("=== File System ===")
    root.display()

    print(f"\nTotal size: {root.get_size()} bytes")
```

---

## Summary: Structural Patterns Cheat Sheet

```
┌─────────────────────────────────────────────────────────────────────────┐
│              Structural Patterns Quick Reference                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Pattern    │ Key Question to Ask                                       │
│  ───────────┼───────────────────────────────────────────────────────── │
│  Adapter    │ "Do I need to use a class with an incompatible interface?"│
│  Decorator  │ "Do I need to add responsibilities dynamically?"          │
│  Proxy      │ "Do I need to control access to an object?"              │
│  Facade     │ "Do I need to simplify a complex subsystem?"             │
│  Composite  │ "Do I need to treat single and composed objects alike?"  │
│                                                                         │
│  Interview Red Flags:                                                   │
│  ─────────────────────                                                  │
│  ✗ Confusing Proxy and Decorator (both wrap, different purposes)       │
│  ✗ Using inheritance when composition (Decorator) is better            │
│  ✗ Creating adapters for interfaces you control (just change them!)    │
│  ✗ Making Facade mandatory (clients should still access subsystems)    │
│                                                                         │
│  Interview Green Flags:                                                 │
│  ─────────────────────                                                  │
│  ✓ Explaining when NOT to use each pattern                             │
│  ✓ Discussing real-world examples from your experience                 │
│  ✓ Combining patterns appropriately (Proxy + Decorator chain)          │
│  ✓ Connecting patterns to SOLID principles                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

**Next:** Continue to [05_design_patterns_behavioral.md](./05_design_patterns_behavioral.md) for Strategy, Observer, and State patterns.
