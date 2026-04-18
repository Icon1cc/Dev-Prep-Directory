# Dependency Injection (DI)

## What is Dependency Injection?

**Dependency Injection** is a design technique where an object receives its dependencies from external sources rather than creating them itself. It's a specific form of **Inversion of Control (IoC)**.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                  Dependency Injection Concept                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   WITHOUT DI (Tight Coupling):                                         │
│   ────────────────────────────                                          │
│                                                                         │
│   class OrderService {                                                  │
│       private db = new MySQLDatabase();  ← Creates its own dependency  │
│       private email = new SMTPEmailer(); ← Hard to test/change         │
│   }                                                                     │
│                                                                         │
│   Problems:                                                             │
│   • OrderService tied to specific implementations                      │
│   • Can't easily swap MySQL for PostgreSQL                             │
│   • Can't test without real database and email server                  │
│   • Violates Single Responsibility (knows how to create dependencies)  │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   WITH DI (Loose Coupling):                                            │
│   ─────────────────────────                                             │
│                                                                         │
│   class OrderService {                                                  │
│       constructor(db: Database, email: Emailer) {  ← Receives deps     │
│           this.db = db;                                                 │
│           this.email = email;                                           │
│       }                                                                 │
│   }                                                                     │
│                                                                         │
│   Benefits:                                                             │
│   • OrderService works with ANY Database implementation                │
│   • Easy to swap implementations                                       │
│   • Easy to test with mocks                                            │
│   • Single Responsibility maintained                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## The DI Principle

```
┌─────────────────────────────────────────────────────────────────────────┐
│            Dependency Inversion Principle (the "D" in SOLID)           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   "Depend on abstractions, not concretions"                            │
│                                                                         │
│   Before DI:                              After DI:                     │
│   ──────────                              ─────────                     │
│                                                                         │
│   ┌────────────────┐                 ┌────────────────┐                │
│   │  OrderService  │                 │  OrderService  │                │
│   └───────┬────────┘                 └───────┬────────┘                │
│           │                                  │                          │
│           │ depends on                       │ depends on               │
│           ▼                                  ▼                          │
│   ┌────────────────┐                 ┌────────────────┐                │
│   │ MySQLDatabase  │                 │ <<interface>>  │                │
│   └────────────────┘                 │   Database     │                │
│                                      └───────▲────────┘                │
│   High-level module                          │                          │
│   depends on low-level                       │ implements               │
│   module (BAD!)                       ┌──────┴──────┐                  │
│                                       │             │                  │
│                                  ┌────┴────┐  ┌────┴────┐             │
│                                  │ MySQL   │  │ Postgres│             │
│                                  │Database │  │Database │             │
│                                  └─────────┘  └─────────┘             │
│                                                                         │
│                                  Both depend on abstraction (GOOD!)    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Types of Dependency Injection

### 1. Constructor Injection (Preferred)

Dependencies are provided through the constructor.

```python
# Python Example

from abc import ABC, abstractmethod

# Abstractions
class Database(ABC):
    @abstractmethod
    def save(self, data: dict) -> bool:
        pass

    @abstractmethod
    def find(self, id: str) -> dict:
        pass

class NotificationService(ABC):
    @abstractmethod
    def send(self, to: str, message: str) -> bool:
        pass

# Concrete implementations
class PostgresDatabase(Database):
    def save(self, data: dict) -> bool:
        print(f"PostgreSQL: Saving {data}")
        return True

    def find(self, id: str) -> dict:
        print(f"PostgreSQL: Finding {id}")
        return {"id": id, "name": "Found Item"}

class EmailNotification(NotificationService):
    def send(self, to: str, message: str) -> bool:
        print(f"Email to {to}: {message}")
        return True

# Service using Constructor Injection
class OrderService:
    """
    OrderService doesn't know or care about concrete implementations.
    It works with ANY Database and ANY NotificationService.
    """

    def __init__(self, db: Database, notifier: NotificationService):
        # Dependencies are INJECTED through constructor
        self._db = db
        self._notifier = notifier

    def create_order(self, customer_email: str, items: list) -> dict:
        order = {
            "id": "ORD-001",
            "items": items,
            "status": "created"
        }

        # Use injected dependencies
        self._db.save(order)
        self._notifier.send(customer_email, f"Order {order['id']} created!")

        return order

# Composition Root - where we wire everything together
if __name__ == "__main__":
    # Create concrete implementations
    database = PostgresDatabase()
    emailer = EmailNotification()

    # Inject dependencies
    order_service = OrderService(db=database, notifier=emailer)

    # Use the service
    order_service.create_order("user@example.com", ["item1", "item2"])
```

### 2. Setter Injection

Dependencies are provided through setter methods. Useful when dependencies are optional.

```python
class ReportGenerator:
    def __init__(self):
        self._exporter = None  # Optional dependency
        self._logger = None    # Optional dependency

    # Setter injection
    def set_exporter(self, exporter):
        self._exporter = exporter

    def set_logger(self, logger):
        self._logger = logger

    def generate(self, data: dict) -> str:
        report = f"Report: {data}"

        if self._logger:
            self._logger.log(f"Generated report")

        if self._exporter:
            self._exporter.export(report)

        return report

# Usage
generator = ReportGenerator()
generator.set_logger(FileLogger())  # Optional
generator.set_exporter(PDFExporter())  # Optional
generator.generate({"sales": 1000})
```

### 3. Interface Injection

The dependency provides an injector method that injects the dependency into any client passed to it.

```python
from abc import ABC, abstractmethod

class DatabaseAware(ABC):
    """Interface that clients implement to receive database"""
    @abstractmethod
    def set_database(self, db: 'Database') -> None:
        pass

class Database:
    """Database that can inject itself into aware objects"""
    def inject_into(self, client: DatabaseAware) -> None:
        client.set_database(self)

class UserRepository(DatabaseAware):
    def __init__(self):
        self._db = None

    def set_database(self, db: Database) -> None:
        self._db = db

# Usage
db = Database()
repo = UserRepository()
db.inject_into(repo)  # Database injects itself
```

---

## Java Implementation

```java
// Interfaces (Abstractions)
interface PaymentGateway {
    boolean charge(String cardNumber, double amount);
    boolean refund(String transactionId);
}

interface InventoryService {
    boolean reserve(String productId, int quantity);
    void release(String productId, int quantity);
}

interface OrderRepository {
    void save(Order order);
    Order findById(String id);
}

// Concrete Implementations
class StripeGateway implements PaymentGateway {
    @Override
    public boolean charge(String cardNumber, double amount) {
        System.out.println("Stripe: Charging $" + amount);
        return true;
    }

    @Override
    public boolean refund(String transactionId) {
        System.out.println("Stripe: Refunding " + transactionId);
        return true;
    }
}

class WarehouseInventory implements InventoryService {
    @Override
    public boolean reserve(String productId, int quantity) {
        System.out.println("Reserving " + quantity + " of " + productId);
        return true;
    }

    @Override
    public void release(String productId, int quantity) {
        System.out.println("Releasing " + quantity + " of " + productId);
    }
}

class MySQLOrderRepository implements OrderRepository {
    @Override
    public void save(Order order) {
        System.out.println("MySQL: Saving order " + order.getId());
    }

    @Override
    public Order findById(String id) {
        return new Order(id);
    }
}

// Service with Constructor Injection
class OrderService {
    private final PaymentGateway paymentGateway;
    private final InventoryService inventoryService;
    private final OrderRepository orderRepository;

    // Constructor Injection - all dependencies required
    public OrderService(
            PaymentGateway paymentGateway,
            InventoryService inventoryService,
            OrderRepository orderRepository) {
        this.paymentGateway = paymentGateway;
        this.inventoryService = inventoryService;
        this.orderRepository = orderRepository;
    }

    public Order placeOrder(String customerId, String productId,
                           int quantity, String cardNumber) {

        // Reserve inventory
        if (!inventoryService.reserve(productId, quantity)) {
            throw new RuntimeException("Out of stock");
        }

        // Calculate total (simplified)
        double total = quantity * 10.0;

        // Charge payment
        if (!paymentGateway.charge(cardNumber, total)) {
            inventoryService.release(productId, quantity);
            throw new RuntimeException("Payment failed");
        }

        // Create and save order
        Order order = new Order(customerId, productId, quantity);
        orderRepository.save(order);

        return order;
    }
}

// Composition Root / Main
public class Application {
    public static void main(String[] args) {
        // Create dependencies
        PaymentGateway payment = new StripeGateway();
        InventoryService inventory = new WarehouseInventory();
        OrderRepository repository = new MySQLOrderRepository();

        // Inject into service
        OrderService orderService = new OrderService(
            payment, inventory, repository
        );

        // Use service
        orderService.placeOrder("CUST-1", "PROD-1", 2, "4111111111111111");
    }
}
```

---

## DI Containers / Frameworks

In real applications, you typically use a **DI Container** (IoC Container) to manage dependencies automatically.

### Python with dependency-injector

```python
from dependency_injector import containers, providers

# Container configuration
class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    # Singleton - same instance everywhere
    database = providers.Singleton(
        PostgresDatabase,
        connection_string=config.db.connection_string
    )

    # Factory - new instance each time
    email_service = providers.Factory(
        EmailNotification,
        smtp_host=config.email.smtp_host
    )

    # Wire dependencies automatically
    order_service = providers.Factory(
        OrderService,
        db=database,
        notifier=email_service
    )

# Usage
container = Container()
container.config.from_yaml('config.yml')

order_service = container.order_service()
order_service.create_order("user@example.com", ["item1"])
```

### Java with Spring

```java
import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;

// Spring automatically creates and injects dependencies
@Service
public class OrderService {

    private final PaymentGateway paymentGateway;
    private final InventoryService inventoryService;

    // Spring injects implementations automatically
    @Autowired
    public OrderService(PaymentGateway paymentGateway,
                       InventoryService inventoryService) {
        this.paymentGateway = paymentGateway;
        this.inventoryService = inventoryService;
    }

    // ...
}

// Mark implementations as Spring beans
@Service
public class StripeGateway implements PaymentGateway {
    // ...
}

@Service
public class WarehouseInventory implements InventoryService {
    // ...
}
```

---

## Benefits of Dependency Injection

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Benefits of DI                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. TESTABILITY                                                        │
│   ──────────────                                                        │
│   # Without DI - Hard to test                                          │
│   class OrderService:                                                   │
│       def __init__(self):                                              │
│           self.db = RealDatabase()  # Can't mock!                      │
│                                                                         │
│   # With DI - Easy to test                                             │
│   class OrderService:                                                   │
│       def __init__(self, db: Database):                                │
│           self.db = db  # Can inject mock!                             │
│                                                                         │
│   # Test with mock                                                      │
│   def test_create_order():                                             │
│       mock_db = Mock(spec=Database)                                    │
│       service = OrderService(db=mock_db)                               │
│       service.create_order(...)                                        │
│       mock_db.save.assert_called_once()                                │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   2. FLEXIBILITY                                                        │
│   ──────────────                                                        │
│   # Switch implementations without changing OrderService               │
│   order_service = OrderService(                                        │
│       db=PostgresDatabase(),  # Production                             │
│       notifier=EmailNotifier()                                         │
│   )                                                                     │
│                                                                         │
│   order_service = OrderService(                                        │
│       db=InMemoryDatabase(),  # Testing                                │
│       notifier=MockNotifier()                                          │
│   )                                                                     │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   3. SINGLE RESPONSIBILITY                                             │
│   ────────────────────────                                              │
│   OrderService only handles orders                                     │
│   It doesn't know HOW to create a database connection                  │
│   It doesn't know WHICH email provider to use                          │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   4. EXPLICIT DEPENDENCIES                                             │
│   ────────────────────────                                              │
│   Constructor clearly shows what a class needs:                        │
│                                                                         │
│   class OrderService:                                                   │
│       def __init__(self,                                               │
│                    db: Database,        # Needs database               │
│                    payment: PaymentGW,  # Needs payment                │
│                    notifier: Notifier): # Needs notifications          │
│                                                                         │
│   vs hidden dependencies:                                              │
│                                                                         │
│   class OrderService:                                                   │
│       def __init__(self):                                              │
│           # What does this class need? Mystery!                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Testing with DI

```python
import unittest
from unittest.mock import Mock, MagicMock

# The class under test
class PaymentProcessor:
    def __init__(self, gateway: 'PaymentGateway', logger: 'Logger'):
        self._gateway = gateway
        self._logger = logger

    def process(self, amount: float, card: str) -> bool:
        self._logger.info(f"Processing ${amount}")

        try:
            result = self._gateway.charge(card, amount)
            if result.success:
                self._logger.info("Payment successful")
                return True
            else:
                self._logger.error(f"Payment failed: {result.error}")
                return False
        except Exception as e:
            self._logger.error(f"Gateway error: {e}")
            raise

# Tests using mocks
class TestPaymentProcessor(unittest.TestCase):

    def setUp(self):
        # Create mock dependencies
        self.mock_gateway = Mock()
        self.mock_logger = Mock()

        # Inject mocks
        self.processor = PaymentProcessor(
            gateway=self.mock_gateway,
            logger=self.mock_logger
        )

    def test_successful_payment(self):
        # Arrange - configure mock to return success
        self.mock_gateway.charge.return_value = Mock(success=True)

        # Act
        result = self.processor.process(100.0, "4111111111111111")

        # Assert
        self.assertTrue(result)
        self.mock_gateway.charge.assert_called_once_with("4111111111111111", 100.0)
        self.mock_logger.info.assert_called()

    def test_failed_payment(self):
        # Arrange - configure mock to return failure
        self.mock_gateway.charge.return_value = Mock(
            success=False,
            error="Insufficient funds"
        )

        # Act
        result = self.processor.process(1000.0, "4111111111111111")

        # Assert
        self.assertFalse(result)
        self.mock_logger.error.assert_called()

    def test_gateway_exception(self):
        # Arrange - configure mock to raise exception
        self.mock_gateway.charge.side_effect = ConnectionError("Network error")

        # Act & Assert
        with self.assertRaises(ConnectionError):
            self.processor.process(100.0, "4111111111111111")

        self.mock_logger.error.assert_called()

if __name__ == '__main__':
    unittest.main()
```

---

## Common DI Patterns

### 1. Factory Pattern with DI

```python
from abc import ABC, abstractmethod
from enum import Enum

class DatabaseType(Enum):
    MYSQL = "mysql"
    POSTGRES = "postgres"
    SQLITE = "sqlite"

class Database(ABC):
    @abstractmethod
    def connect(self): pass

class DatabaseFactory:
    """Factory that can be injected and creates appropriate database"""

    def __init__(self, config: dict):
        self._config = config

    def create(self, db_type: DatabaseType) -> Database:
        if db_type == DatabaseType.MYSQL:
            return MySQLDatabase(self._config['mysql'])
        elif db_type == DatabaseType.POSTGRES:
            return PostgresDatabase(self._config['postgres'])
        elif db_type == DatabaseType.SQLITE:
            return SQLiteDatabase(self._config['sqlite'])
        raise ValueError(f"Unknown database type: {db_type}")

# Service receives factory, not concrete database
class DataService:
    def __init__(self, db_factory: DatabaseFactory):
        self._db_factory = db_factory
        self._db = None

    def connect(self, db_type: DatabaseType):
        self._db = self._db_factory.create(db_type)
        self._db.connect()
```

### 2. Strategy Pattern with DI

```python
class ShippingCalculator:
    """Calculator with injected shipping strategy"""

    def __init__(self, strategy: 'ShippingStrategy'):
        self._strategy = strategy

    def calculate(self, order) -> float:
        return self._strategy.calculate_cost(order)

# Can inject different strategies
calculator = ShippingCalculator(StandardShipping())
calculator = ShippingCalculator(ExpressShipping())
calculator = ShippingCalculator(FreeShipping())
```

---

## Interview Tips

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DI Interview Points                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   COMMON QUESTIONS:                                                     │
│   ─────────────────                                                     │
│                                                                         │
│   Q: "What is Dependency Injection?"                                   │
│   A: A technique where objects receive dependencies from external      │
│      sources rather than creating them. It inverts control of          │
│      dependency creation.                                              │
│                                                                         │
│   Q: "Why use DI?"                                                     │
│   A: Testability (inject mocks), Flexibility (swap implementations),   │
│      Single Responsibility (class doesn't create its dependencies),    │
│      Explicit dependencies (constructor shows what's needed).          │
│                                                                         │
│   Q: "Constructor vs Setter injection?"                                │
│   A: Constructor for required dependencies (fails fast if missing).    │
│      Setter for optional dependencies. Constructor is preferred.       │
│                                                                         │
│   Q: "DI vs Service Locator?"                                          │
│   A: Both achieve loose coupling. DI pushes dependencies in,           │
│      Service Locator pulls them. DI makes dependencies explicit.       │
│                                                                         │
│   RED FLAGS:                                                           │
│   ──────────                                                            │
│   • Using `new` for services inside classes                            │
│   • Static methods that are hard to mock                               │
│   • God classes with many dependencies                                 │
│   • Hidden dependencies (not in constructor)                           │
│                                                                         │
│   GREEN FLAGS:                                                         │
│   ────────────                                                          │
│   • Constructor injection for required deps                            │
│   • Programming to interfaces                                          │
│   • Small, focused classes                                             │
│   • Easy to write unit tests                                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

**Next:** Continue to [08_thread_safety.md](./08_thread_safety.md) to learn about writing concurrent-safe code.
