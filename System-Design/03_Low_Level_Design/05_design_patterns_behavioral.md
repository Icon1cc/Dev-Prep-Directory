# Behavioral Design Patterns

## What are Behavioral Patterns?

Behavioral patterns focus on **communication between objects**—how objects interact and distribute responsibilities. They help make complex control flows easier to understand and maintain.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   Behavioral Patterns Overview                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Pattern      │ Purpose                       │ Real-World Analogy      │
│  ─────────────┼───────────────────────────────┼──────────────────────── │
│  Strategy     │ Swap algorithms at runtime    │ Different routes on GPS │
│  Observer     │ Notify on state changes       │ Newsletter subscription │
│  State        │ Change behavior with state    │ Vending machine states  │
│  Command      │ Encapsulate requests          │ Restaurant order slip   │
│  Template     │ Define algorithm skeleton     │ Recipe with variations  │
│  Iterator     │ Traverse collections          │ TV remote channel surf  │
│  Chain of Resp│ Pass request along chain      │ Tech support escalation │
│  Mediator     │ Centralize communications     │ Air traffic controller  │
│  Visitor      │ Add operations to classes     │ Tax accountant visiting │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Strategy Pattern

### Intent
Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it.

### Real-World Analogy
**GPS Navigation**: You can choose different routing strategies (fastest, shortest, avoid highways, scenic route) without changing the navigation app itself. Each strategy is a different algorithm for the same task.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Strategy Pattern Structure                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌────────────────────┐         ┌─────────────────────┐               │
│   │      Context       │────────►│     Strategy        │               │
│   ├────────────────────┤         │    (interface)      │               │
│   │ - strategy         │         ├─────────────────────┤               │
│   │ + setStrategy(s)   │         │ + execute(data)     │               │
│   │ + doWork()         │         └─────────────────────┘               │
│   └────────────────────┘                   ▲                            │
│                                            │                            │
│                              ┌─────────────┼─────────────┐             │
│                              │             │             │             │
│                        ┌─────┴─────┐ ┌─────┴─────┐ ┌─────┴─────┐      │
│                        │StrategyA  │ │StrategyB  │ │ StrategyC │      │
│                        ├───────────┤ ├───────────┤ ├───────────┤      │
│                        │+ execute()│ │+ execute()│ │+ execute()│      │
│                        └───────────┘ └───────────┘ └───────────┘      │
│                                                                         │
│   Key Insight:                                                          │
│   ────────────                                                          │
│   Context.doWork() delegates to strategy.execute()                      │
│   Strategy can be changed at runtime without modifying Context          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### When to Use
- Multiple algorithms for the same task
- Need to switch algorithms at runtime
- Avoid conditional statements for algorithm selection
- Isolate algorithm-specific data from client

### When NOT to Use
- Only one or two algorithms (overkill)
- Algorithms rarely change
- Clients need to know which strategy to use (leaky abstraction)

### Python Implementation

```python
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass

# Strategy Interface
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

# Concrete Strategies
class CreditCardStrategy(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str, expiry: str):
        self._card_number = card_number
        self._cvv = cvv
        self._expiry = expiry

    def pay(self, amount: float) -> bool:
        # Simulate credit card processing
        masked_card = f"****{self._card_number[-4:]}"
        print(f"Paid ${amount:.2f} using Credit Card {masked_card}")
        return True

    def get_name(self) -> str:
        return "Credit Card"

class PayPalStrategy(PaymentStrategy):
    def __init__(self, email: str):
        self._email = email

    def pay(self, amount: float) -> bool:
        print(f"Paid ${amount:.2f} using PayPal ({self._email})")
        return True

    def get_name(self) -> str:
        return "PayPal"

class CryptoStrategy(PaymentStrategy):
    def __init__(self, wallet_address: str):
        self._wallet = wallet_address

    def pay(self, amount: float) -> bool:
        # Convert to crypto equivalent
        btc_amount = amount / 50000  # Simplified conversion
        print(f"Paid {btc_amount:.6f} BTC from wallet {self._wallet[:10]}...")
        return True

    def get_name(self) -> str:
        return "Cryptocurrency"

# Context
@dataclass
class CartItem:
    name: str
    price: float
    quantity: int

class ShoppingCart:
    def __init__(self):
        self._items: List[CartItem] = []
        self._payment_strategy: PaymentStrategy = None

    def add_item(self, item: CartItem) -> None:
        self._items.append(item)

    def get_total(self) -> float:
        return sum(item.price * item.quantity for item in self._items)

    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        """Strategy can be changed at runtime"""
        self._payment_strategy = strategy
        print(f"Payment method set to: {strategy.get_name()}")

    def checkout(self) -> bool:
        if not self._payment_strategy:
            raise ValueError("Payment strategy not set!")

        total = self.get_total()
        print(f"\n=== Checkout: ${total:.2f} ===")

        # Delegate to strategy
        return self._payment_strategy.pay(total)

# Usage
if __name__ == "__main__":
    # Create cart and add items
    cart = ShoppingCart()
    cart.add_item(CartItem("Laptop", 999.99, 1))
    cart.add_item(CartItem("Mouse", 29.99, 2))

    print(f"Cart Total: ${cart.get_total():.2f}\n")

    # Strategy can be selected at runtime based on user choice
    print("=== Using Credit Card ===")
    cart.set_payment_strategy(
        CreditCardStrategy("4111111111111111", "123", "12/25")
    )
    cart.checkout()

    print("\n=== Switching to PayPal ===")
    cart.set_payment_strategy(PayPalStrategy("user@example.com"))
    cart.checkout()

    print("\n=== Switching to Crypto ===")
    cart.set_payment_strategy(CryptoStrategy("0x742d35Cc6634C0532925a3b844Bc9e"))
    cart.checkout()
```

### Java Implementation

```java
import java.util.ArrayList;
import java.util.List;

// Strategy Interface
interface SortingStrategy {
    void sort(int[] array);
    String getName();
}

// Concrete Strategies
class BubbleSortStrategy implements SortingStrategy {
    @Override
    public void sort(int[] array) {
        int n = array.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (array[j] > array[j + 1]) {
                    int temp = array[j];
                    array[j] = array[j + 1];
                    array[j + 1] = temp;
                }
            }
        }
        System.out.println("Sorted using Bubble Sort");
    }

    @Override
    public String getName() {
        return "Bubble Sort - O(n²)";
    }
}

class QuickSortStrategy implements SortingStrategy {
    @Override
    public void sort(int[] array) {
        quickSort(array, 0, array.length - 1);
        System.out.println("Sorted using Quick Sort");
    }

    private void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }

    private int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++;
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
        int temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;
        return i + 1;
    }

    @Override
    public String getName() {
        return "Quick Sort - O(n log n)";
    }
}

class MergeSortStrategy implements SortingStrategy {
    @Override
    public void sort(int[] array) {
        mergeSort(array, 0, array.length - 1);
        System.out.println("Sorted using Merge Sort");
    }

    private void mergeSort(int[] arr, int l, int r) {
        if (l < r) {
            int m = l + (r - l) / 2;
            mergeSort(arr, l, m);
            mergeSort(arr, m + 1, r);
            merge(arr, l, m, r);
        }
    }

    private void merge(int[] arr, int l, int m, int r) {
        // Standard merge implementation
        int n1 = m - l + 1, n2 = r - m;
        int[] L = new int[n1], R = new int[n2];
        System.arraycopy(arr, l, L, 0, n1);
        System.arraycopy(arr, m + 1, R, 0, n2);

        int i = 0, j = 0, k = l;
        while (i < n1 && j < n2) {
            arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];
        }
        while (i < n1) arr[k++] = L[i++];
        while (j < n2) arr[k++] = R[j++];
    }

    @Override
    public String getName() {
        return "Merge Sort - O(n log n)";
    }
}

// Context
class Sorter {
    private SortingStrategy strategy;

    public void setStrategy(SortingStrategy strategy) {
        this.strategy = strategy;
        System.out.println("Strategy set to: " + strategy.getName());
    }

    public void sort(int[] array) {
        if (strategy == null) {
            throw new IllegalStateException("Sorting strategy not set!");
        }

        // Automatically select strategy based on array size
        // This is an example of dynamic strategy selection
        strategy.sort(array);
    }

    // Smart strategy selection
    public void sortSmart(int[] array) {
        if (array.length < 10) {
            setStrategy(new BubbleSortStrategy());  // Simple for small arrays
        } else if (array.length < 1000) {
            setStrategy(new QuickSortStrategy());   // Fast for medium arrays
        } else {
            setStrategy(new MergeSortStrategy());   // Stable for large arrays
        }
        strategy.sort(array);
    }
}

// Demo
public class StrategyDemo {
    public static void main(String[] args) {
        Sorter sorter = new Sorter();
        int[] data = {64, 34, 25, 12, 22, 11, 90};

        // Manual strategy selection
        sorter.setStrategy(new QuickSortStrategy());
        sorter.sort(data.clone());

        // Smart auto-selection
        System.out.println("\n--- Smart Selection ---");
        sorter.sortSmart(new int[5]);      // Will use Bubble
        sorter.sortSmart(new int[100]);    // Will use Quick
        sorter.sortSmart(new int[10000]);  // Will use Merge
    }
}
```

### Strategy vs if/else

```
┌─────────────────────────────────────────────────────────────────────────┐
│              Strategy Pattern vs Conditional Logic                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   WITHOUT Strategy (Bad):              WITH Strategy (Good):            │
│   ───────────────────────              ─────────────────────            │
│                                                                         │
│   def process_payment(type, amount):   cart.set_strategy(              │
│       if type == "credit":                 CreditCardStrategy(...)     │
│           # 50 lines of code           )                               │
│       elif type == "paypal":           cart.checkout()                 │
│           # 50 lines of code                                           │
│       elif type == "crypto":                                           │
│           # 50 lines of code           # Each strategy is a separate   │
│       elif type == "bank":             # class with single responsibility
│           # 50 lines of code                                           │
│       # Adding new type = modify       # Adding new type = new class   │
│       # this function (violates OCP)   # (follows OCP)                 │
│                                                                         │
│   Problems with if/else:               Benefits of Strategy:           │
│   • Violates Open/Closed Principle     • Each algorithm isolated       │
│   • Single class becomes huge          • Easy to add new strategies    │
│   • Hard to test individual paths      • Easy to test strategies       │
│   • Modifications risk breaking others • Runtime flexibility           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "Strategy vs State?" | Pattern distinction | Strategy: interchangeable algorithms; State: behavior changes with internal state |
| "When is Strategy overkill?" | Practical judgment | When there's only 1-2 algorithms that won't change |
| "How does client choose strategy?" | Design completeness | Factory, config, user input, or context-based auto-selection |

---

## 2. Observer Pattern

### Intent
Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

### Real-World Analogy
**YouTube Subscriptions**: When you subscribe to a channel (subject), you (observer) get notified whenever new content is posted. The channel doesn't need to know who's subscribed—it just broadcasts to all subscribers.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Observer Pattern Structure                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────────┐              ┌────────────────────┐             │
│   │     Subject      │              │     Observer       │             │
│   │   (Observable)   │◄─────────────│    (interface)     │             │
│   ├──────────────────┤   observes   ├────────────────────┤             │
│   │ - observers[]    │              │ + update(data)     │             │
│   │ + attach(o)      │              └────────────────────┘             │
│   │ + detach(o)      │                       ▲                         │
│   │ + notify()       │                       │                         │
│   └──────────────────┘           ┌───────────┼───────────┐            │
│           │                      │           │           │            │
│           │ notifies       ┌─────┴────┐ ┌────┴─────┐ ┌───┴──────┐    │
│           └───────────────►│ObserverA │ │ObserverB │ │ObserverC │    │
│                            ├──────────┤ ├──────────┤ ├──────────┤    │
│                            │+ update()│ │+ update()│ │+ update()│    │
│                            └──────────┘ └──────────┘ └──────────┘    │
│                                                                         │
│   Flow:                                                                 │
│   ─────                                                                 │
│   1. Observers register with Subject (attach)                          │
│   2. Subject state changes                                             │
│   3. Subject calls notify()                                            │
│   4. Each Observer's update() is called                                │
│   5. Observers can unregister anytime (detach)                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### When to Use
- When changes in one object require changing others
- When you don't know how many objects need to change
- When an object should notify others without tight coupling
- Event handling systems, pub/sub systems, MVC architecture

### When NOT to Use
- When notification order matters (undefined order)
- When updates are very frequent (performance overhead)
- When circular dependencies might occur

### Python Implementation

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum

# Observer Interface
class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, data: Any) -> None:
        pass

# Subject (Observable)
class Subject(ABC):
    def __init__(self):
        self._observers: Dict[str, List[Observer]] = {}

    def attach(self, event_type: str, observer: Observer) -> None:
        if event_type not in self._observers:
            self._observers[event_type] = []
        self._observers[event_type].append(observer)
        print(f"Observer attached to '{event_type}' events")

    def detach(self, event_type: str, observer: Observer) -> None:
        if event_type in self._observers:
            self._observers[event_type].remove(observer)
            print(f"Observer detached from '{event_type}' events")

    def notify(self, event_type: str, data: Any = None) -> None:
        if event_type in self._observers:
            for observer in self._observers[event_type]:
                observer.update(event_type, data)

# Concrete Subject
@dataclass
class StockData:
    symbol: str
    price: float
    change: float

class StockMarket(Subject):
    def __init__(self):
        super().__init__()
        self._stocks: Dict[str, StockData] = {}

    def update_stock(self, symbol: str, price: float) -> None:
        old_price = self._stocks.get(symbol, StockData(symbol, price, 0)).price
        change = ((price - old_price) / old_price * 100) if old_price else 0

        self._stocks[symbol] = StockData(symbol, price, change)

        print(f"\n📈 Stock Update: {symbol} = ${price:.2f} ({change:+.2f}%)")

        # Notify observers
        self.notify("price_update", self._stocks[symbol])

        # Special notifications for significant changes
        if abs(change) > 5:
            self.notify("significant_change", self._stocks[symbol])

        if price < 10:
            self.notify("low_price_alert", self._stocks[symbol])

# Concrete Observers
class PriceDisplay(Observer):
    """Displays all price updates in real-time"""

    def __init__(self, name: str):
        self._name = name

    def update(self, event_type: str, data: StockData) -> None:
        print(f"  [{self._name}] {data.symbol}: ${data.price:.2f}")

class AlertSystem(Observer):
    """Sends alerts for significant changes"""

    def update(self, event_type: str, data: StockData) -> None:
        if event_type == "significant_change":
            direction = "📈 SURGE" if data.change > 0 else "📉 DROP"
            print(f"  🚨 ALERT: {data.symbol} {direction} {abs(data.change):.1f}%!")
        elif event_type == "low_price_alert":
            print(f"  💰 BUY SIGNAL: {data.symbol} is below $10!")

class TradingBot(Observer):
    """Automated trading based on signals"""

    def __init__(self, name: str):
        self._name = name
        self._portfolio: Dict[str, int] = {}

    def update(self, event_type: str, data: StockData) -> None:
        if event_type == "significant_change":
            if data.change < -5:
                # Buy on dip
                self._portfolio[data.symbol] = self._portfolio.get(data.symbol, 0) + 100
                print(f"  🤖 [{self._name}] AUTO-BUY: 100 shares of {data.symbol}")
            elif data.change > 5:
                # Sell on surge
                if self._portfolio.get(data.symbol, 0) > 0:
                    print(f"  🤖 [{self._name}] AUTO-SELL: {data.symbol}")
                    self._portfolio[data.symbol] = 0

class Logger(Observer):
    """Logs all events for audit"""

    def __init__(self):
        self._log: List[str] = []

    def update(self, event_type: str, data: StockData) -> None:
        entry = f"{event_type}: {data.symbol}=${data.price:.2f} ({data.change:+.2f}%)"
        self._log.append(entry)
        print(f"  📝 Logged: {event_type}")

    def get_log(self) -> List[str]:
        return self._log.copy()

# Usage
if __name__ == "__main__":
    # Create subject
    market = StockMarket()

    # Create observers
    display = PriceDisplay("Main Display")
    alerts = AlertSystem()
    bot = TradingBot("AlphaBot")
    logger = Logger()

    # Attach observers to relevant events
    market.attach("price_update", display)
    market.attach("price_update", logger)
    market.attach("significant_change", alerts)
    market.attach("significant_change", bot)
    market.attach("low_price_alert", alerts)

    print("\n" + "="*50)
    print("Stock Market Simulation")
    print("="*50)

    # Simulate stock updates
    market.update_stock("AAPL", 150.00)  # Initial price
    market.update_stock("AAPL", 152.00)  # Small change
    market.update_stock("AAPL", 165.00)  # Big surge (+8.5%)
    market.update_stock("TSLA", 200.00)  # Initial
    market.update_stock("TSLA", 180.00)  # Big drop (-10%)
    market.update_stock("PENNY", 8.50)   # Low price alert

    # Unsubscribe from some events
    print("\n--- Unsubscribing display from price updates ---")
    market.detach("price_update", display)

    market.update_stock("AAPL", 170.00)  # Display won't show this
```

### Java Implementation

```java
import java.util.*;

// Observer Interface
interface EventListener {
    void update(String eventType, Object data);
}

// Subject
class EventManager {
    private Map<String, List<EventListener>> listeners = new HashMap<>();

    public void subscribe(String eventType, EventListener listener) {
        listeners.computeIfAbsent(eventType, k -> new ArrayList<>()).add(listener);
    }

    public void unsubscribe(String eventType, EventListener listener) {
        List<EventListener> users = listeners.get(eventType);
        if (users != null) {
            users.remove(listener);
        }
    }

    public void notify(String eventType, Object data) {
        List<EventListener> users = listeners.get(eventType);
        if (users != null) {
            for (EventListener listener : users) {
                listener.update(eventType, data);
            }
        }
    }
}

// Concrete Subject
class Editor {
    public EventManager events;
    private String content = "";

    public Editor() {
        this.events = new EventManager();
    }

    public void openFile(String filename) {
        content = "Content of " + filename;
        events.notify("open", filename);
    }

    public void saveFile(String filename) {
        events.notify("save", filename);
    }

    public void edit(String newContent) {
        content = newContent;
        events.notify("edit", content);
    }
}

// Concrete Observers
class LoggingListener implements EventListener {
    private String logFile;

    public LoggingListener(String logFile) {
        this.logFile = logFile;
    }

    @Override
    public void update(String eventType, Object data) {
        System.out.println("Log to " + logFile + ": " + eventType + " - " + data);
    }
}

class EmailAlertsListener implements EventListener {
    private String email;

    public EmailAlertsListener(String email) {
        this.email = email;
    }

    @Override
    public void update(String eventType, Object data) {
        System.out.println("Email to " + email + ": File was " + eventType + " - " + data);
    }
}

class AutoSaveListener implements EventListener {
    @Override
    public void update(String eventType, Object data) {
        if ("edit".equals(eventType)) {
            System.out.println("Auto-saving draft...");
        }
    }
}

// Demo
public class ObserverDemo {
    public static void main(String[] args) {
        Editor editor = new Editor();

        // Subscribe listeners
        LoggingListener logger = new LoggingListener("editor.log");
        EmailAlertsListener emailer = new EmailAlertsListener("admin@example.com");
        AutoSaveListener autoSave = new AutoSaveListener();

        editor.events.subscribe("open", logger);
        editor.events.subscribe("save", logger);
        editor.events.subscribe("save", emailer);
        editor.events.subscribe("edit", autoSave);

        // Perform operations
        System.out.println("--- Opening file ---");
        editor.openFile("document.txt");

        System.out.println("\n--- Editing ---");
        editor.edit("New content here");

        System.out.println("\n--- Saving ---");
        editor.saveFile("document.txt");
    }
}
```

### Push vs Pull Model

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Push vs Pull Observer Models                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   PUSH Model:                          PULL Model:                      │
│   ───────────                          ───────────                      │
│                                                                         │
│   Subject sends data to observers      Subject notifies, observers      │
│                                        pull data they need              │
│                                                                         │
│   notify(data) ───────►                notify() ───────►                │
│                  │                              │                       │
│              ┌───┴───┐                      ┌───┴───┐                  │
│              │ data  │                      │       │                  │
│              └───────┘                      └───────┘                  │
│                                                 │                       │
│                                       observer.getState() ◄────┐       │
│                                                                 │       │
│   Pros:                                Pros:                    │       │
│   • Observers get exactly what        • Observers get only     │       │
│     they need immediately               what they need          │       │
│   • No extra round-trip               • Subject interface      │       │
│                                         is simpler              │       │
│   Cons:                                                         │       │
│   • May send unnecessary data         Cons:                     │       │
│   • Subject must know what            • Extra call to get data  │       │
│     observers need                    • May cause race conditions│      │
│                                                                         │
│   Use Push when:                       Use Pull when:                   │
│   • Data is small                      • Different observers need       │
│   • All observers need same data         different data                 │
│   • Performance critical               • State is complex               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "How to avoid memory leaks?" | Practical knowledge | Weak references, or explicit unsubscribe in lifecycle methods |
| "Observer vs Pub/Sub?" | Architectural understanding | Observer: direct coupling; Pub/Sub: message broker decouples completely |
| "Thread safety concerns?" | Concurrency awareness | ConcurrentHashMap for observers, or notify copy of list |

---

## 3. State Pattern

### Intent
Allow an object to alter its behavior when its internal state changes. The object will appear to change its class.

### Real-World Analogy
**Vending Machine**: Its behavior depends on its state: waiting for money, has money, dispensing, out of stock. Same button press (select item) does different things in different states.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       State Pattern Structure                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────┐         ┌──────────────────────┐             │
│   │      Context        │────────►│       State          │             │
│   ├─────────────────────┤         │     (interface)      │             │
│   │ - state             │         ├──────────────────────┤             │
│   │ + request()         │         │ + handle(context)    │             │
│   │ + setState(state)   │         └──────────────────────┘             │
│   └─────────────────────┘                   ▲                          │
│           │                                 │                          │
│           │                    ┌────────────┼────────────┐            │
│   Context.request() calls     │            │            │            │
│   state.handle(this)          │            │            │            │
│                          ┌────┴────┐  ┌────┴────┐  ┌────┴────┐       │
│                          │ StateA  │  │ StateB  │  │ StateC  │       │
│                          ├─────────┤  ├─────────┤  ├─────────┤       │
│                          │+handle()│  │+handle()│  │+handle()│       │
│                          └─────────┘  └─────────┘  └─────────┘       │
│                                                                         │
│   State Transitions:                                                    │
│   ──────────────────                                                    │
│            ┌───────┐    event    ┌───────┐    event    ┌───────┐      │
│            │StateA │───────────► │StateB │───────────► │StateC │      │
│            └───────┘             └───────┘             └───────┘      │
│                                                                         │
│   Each state knows which state comes next                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### When to Use
- Object behavior depends on its state
- Operations have large conditional statements based on state
- States have clear transitions
- Need to add new states without modifying existing code

### When NOT to Use
- Only a few states with simple behavior
- State transitions are not well-defined
- State-specific behavior is minimal

### Python Implementation

```python
from abc import ABC, abstractmethod
from typing import Optional

# State Interface
class OrderState(ABC):
    @abstractmethod
    def proceed(self, order: 'Order') -> None:
        pass

    @abstractmethod
    def cancel(self, order: 'Order') -> None:
        pass

    @abstractmethod
    def get_status(self) -> str:
        pass

# Concrete States
class DraftState(OrderState):
    """Initial state - order is being created"""

    def proceed(self, order: 'Order') -> None:
        print("Order submitted! Moving to Pending state.")
        order.set_state(PendingState())

    def cancel(self, order: 'Order') -> None:
        print("Draft discarded.")
        order.set_state(CancelledState())

    def get_status(self) -> str:
        return "DRAFT"

class PendingState(OrderState):
    """Waiting for payment"""

    def proceed(self, order: 'Order') -> None:
        print("Payment received! Moving to Processing state.")
        order.set_state(ProcessingState())

    def cancel(self, order: 'Order') -> None:
        print("Order cancelled. Refund initiated if applicable.")
        order.set_state(CancelledState())

    def get_status(self) -> str:
        return "PENDING PAYMENT"

class ProcessingState(OrderState):
    """Being prepared/packed"""

    def proceed(self, order: 'Order') -> None:
        print("Order shipped! Moving to Shipped state.")
        order.set_state(ShippedState())

    def cancel(self, order: 'Order') -> None:
        print("Too late to cancel - order is being processed.")
        print("Please wait for delivery and return if needed.")

    def get_status(self) -> str:
        return "PROCESSING"

class ShippedState(OrderState):
    """In transit"""

    def proceed(self, order: 'Order') -> None:
        print("Order delivered! Moving to Delivered state.")
        order.set_state(DeliveredState())

    def cancel(self, order: 'Order') -> None:
        print("Cannot cancel - package is in transit.")
        print("Please refuse delivery or return after receiving.")

    def get_status(self) -> str:
        return "SHIPPED"

class DeliveredState(OrderState):
    """Final successful state"""

    def proceed(self, order: 'Order') -> None:
        print("Order already delivered. No further action needed.")

    def cancel(self, order: 'Order') -> None:
        print("Cannot cancel delivered order. Please initiate a return.")

    def get_status(self) -> str:
        return "DELIVERED"

class CancelledState(OrderState):
    """Final cancelled state"""

    def proceed(self, order: 'Order') -> None:
        print("Cannot proceed - order has been cancelled.")

    def cancel(self, order: 'Order') -> None:
        print("Order is already cancelled.")

    def get_status(self) -> str:
        return "CANCELLED"

# Context
class Order:
    def __init__(self, order_id: str, items: list):
        self._order_id = order_id
        self._items = items
        self._state: OrderState = DraftState()

    def set_state(self, state: OrderState) -> None:
        self._state = state

    def proceed(self) -> None:
        """Move to next state"""
        print(f"\n[Order {self._order_id}] Current: {self._state.get_status()}")
        self._state.proceed(self)
        print(f"[Order {self._order_id}] New: {self._state.get_status()}")

    def cancel(self) -> None:
        """Attempt to cancel"""
        print(f"\n[Order {self._order_id}] Attempting to cancel...")
        self._state.cancel(self)
        print(f"[Order {self._order_id}] Status: {self._state.get_status()}")

    def get_status(self) -> str:
        return self._state.get_status()

    def __str__(self) -> str:
        return f"Order({self._order_id}, items={self._items}, status={self.get_status()})"

# Usage
if __name__ == "__main__":
    # Create order
    order = Order("ORD-001", ["Laptop", "Mouse", "Keyboard"])
    print(order)

    # Normal flow
    print("\n" + "="*50)
    print("NORMAL ORDER FLOW")
    print("="*50)

    order.proceed()  # Draft -> Pending
    order.proceed()  # Pending -> Processing
    order.proceed()  # Processing -> Shipped
    order.proceed()  # Shipped -> Delivered
    order.proceed()  # Already delivered

    # Test cancellation at different stages
    print("\n" + "="*50)
    print("CANCELLATION SCENARIOS")
    print("="*50)

    # Cancel from draft
    order2 = Order("ORD-002", ["Phone"])
    order2.cancel()  # Can cancel from draft

    # Cancel from pending
    order3 = Order("ORD-003", ["Tablet"])
    order3.proceed()  # Draft -> Pending
    order3.cancel()   # Can cancel from pending

    # Cancel from processing
    order4 = Order("ORD-004", ["Watch"])
    order4.proceed()  # Draft -> Pending
    order4.proceed()  # Pending -> Processing
    order4.cancel()   # Cannot cancel - too late!
```

### Java Implementation

```java
// State Interface
interface DocumentState {
    void edit(Document doc);
    void review(Document doc);
    void publish(Document doc);
    String getStatus();
}

// Concrete States
class DraftState implements DocumentState {
    @Override
    public void edit(Document doc) {
        System.out.println("Editing document...");
    }

    @Override
    public void review(Document doc) {
        System.out.println("Submitting for review...");
        doc.setState(new ReviewState());
    }

    @Override
    public void publish(Document doc) {
        System.out.println("Cannot publish - document must be reviewed first!");
    }

    @Override
    public String getStatus() {
        return "DRAFT";
    }
}

class ReviewState implements DocumentState {
    @Override
    public void edit(Document doc) {
        System.out.println("Changes requested - moving back to draft...");
        doc.setState(new DraftState());
    }

    @Override
    public void review(Document doc) {
        System.out.println("Already in review.");
    }

    @Override
    public void publish(Document doc) {
        System.out.println("Review approved - publishing...");
        doc.setState(new PublishedState());
    }

    @Override
    public String getStatus() {
        return "IN REVIEW";
    }
}

class PublishedState implements DocumentState {
    @Override
    public void edit(Document doc) {
        System.out.println("Creating new draft from published version...");
        doc.setState(new DraftState());
    }

    @Override
    public void review(Document doc) {
        System.out.println("Already published - cannot review.");
    }

    @Override
    public void publish(Document doc) {
        System.out.println("Already published.");
    }

    @Override
    public String getStatus() {
        return "PUBLISHED";
    }
}

// Context
class Document {
    private DocumentState state;
    private String content;

    public Document() {
        this.state = new DraftState();
        this.content = "";
    }

    public void setState(DocumentState state) {
        this.state = state;
    }

    public void edit() {
        state.edit(this);
    }

    public void review() {
        state.review(this);
    }

    public void publish() {
        state.publish(this);
    }

    public String getStatus() {
        return state.getStatus();
    }
}

// Demo
public class StateDemo {
    public static void main(String[] args) {
        Document doc = new Document();

        System.out.println("Status: " + doc.getStatus());

        doc.edit();      // Can edit in draft
        doc.publish();   // Can't publish from draft!

        doc.review();    // Submit for review
        System.out.println("Status: " + doc.getStatus());

        doc.publish();   // Approve and publish
        System.out.println("Status: " + doc.getStatus());

        doc.edit();      // Creates new draft
        System.out.println("Status: " + doc.getStatus());
    }
}
```

### State vs Strategy

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     State vs Strategy Comparison                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Aspect          │ State                    │ Strategy                 │
│   ────────────────┼──────────────────────────┼───────────────────────── │
│   Purpose         │ Change behavior based    │ Choose algorithm         │
│                   │ on internal state        │                          │
│                                                                         │
│   Who controls?   │ State objects control    │ Client controls          │
│                   │ transitions              │ which strategy to use    │
│                                                                         │
│   Awareness       │ States know about        │ Strategies are           │
│                   │ each other               │ independent              │
│                                                                         │
│   Transitions     │ Many transitions         │ Usually set once         │
│                   │ during lifetime          │ or rarely changed        │
│                                                                         │
│   Example         │ Order: Draft→Pending     │ Sorting: Pick            │
│                   │ →Processing→Shipped      │ QuickSort or MergeSort   │
│                                                                         │
│   Mental Model:                                                         │
│   ─────────────                                                         │
│   State:    "I behave differently because I AM different now"          │
│   Strategy: "I behave differently because I USE a different algorithm" │
│                                                                         │
│   Code Smell Detection:                                                 │
│   ─────────────────────                                                 │
│   If you have: switch(state) { case A:... case B:... }                 │
│   → Consider State pattern                                              │
│                                                                         │
│   If you have: switch(algorithmType) { case QUICK:... case MERGE:... } │
│   → Consider Strategy pattern                                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "Who manages transitions?" | Pattern understanding | State objects manage their own transitions to other states |
| "State vs FSM?" | Conceptual depth | State pattern is OOP implementation of FSM concept |
| "What if too many states?" | Practical limits | Consider if State pattern is overkill; maybe enums + switch is simpler |

---

## 4. Command Pattern

### Intent
Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.

### Real-World Analogy
**Restaurant Order**: A waiter writes your order on a slip (command object). The slip goes to the kitchen (invoker calls execute). The slip contains all info needed to prepare the dish (receiver + parameters).

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Command Pattern Structure                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌────────┐      ┌──────────┐      ┌───────────────┐                  │
│   │ Client │─────►│ Invoker  │─────►│    Command    │                  │
│   └────────┘      ├──────────┤      │  (interface)  │                  │
│                   │+execute()│      ├───────────────┤                  │
│                   │+undo()   │      │ + execute()   │                  │
│                   └──────────┘      │ + undo()      │                  │
│                                     └───────────────┘                  │
│                                            ▲                            │
│                                            │                            │
│                              ┌─────────────┼─────────────┐             │
│                              │             │             │             │
│                        ┌─────┴─────┐ ┌─────┴─────┐ ┌─────┴─────┐      │
│                        │ CommandA  │ │ CommandB  │ │ CommandC  │      │
│                        ├───────────┤ ├───────────┤ ├───────────┤      │
│                        │- receiver │ │- receiver │ │- receiver │      │
│                        │- params   │ │- params   │ │- params   │      │
│                        │+execute() │ │+execute() │ │+execute() │      │
│                        │+undo()    │ │+undo()    │ │+undo()    │      │
│                        └─────┬─────┘ └───────────┘ └───────────┘      │
│                              │                                          │
│                              ▼                                          │
│                        ┌───────────┐                                   │
│                        │ Receiver  │ ◄── Knows how to do the work     │
│                        └───────────┘                                   │
│                                                                         │
│   Key Benefits:                                                         │
│   • Decouple invoker from receiver                                     │
│   • Commands can be queued, logged, undone                             │
│   • Commands are first-class objects                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### When to Use
- Need to parameterize objects with operations
- Need to queue operations, schedule execution, or execute remotely
- Need undo/redo functionality
- Need to log changes for crash recovery

### Python Implementation

```python
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass

# Command Interface
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

# Receiver
class TextEditor:
    def __init__(self):
        self._text = ""

    @property
    def text(self) -> str:
        return self._text

    def insert(self, text: str, position: int) -> None:
        self._text = self._text[:position] + text + self._text[position:]

    def delete(self, start: int, end: int) -> str:
        deleted = self._text[start:end]
        self._text = self._text[:start] + self._text[end:]
        return deleted

    def replace(self, start: int, end: int, new_text: str) -> str:
        old_text = self._text[start:end]
        self._text = self._text[:start] + new_text + self._text[end:]
        return old_text

# Concrete Commands
class InsertCommand(Command):
    def __init__(self, editor: TextEditor, text: str, position: int):
        self._editor = editor
        self._text = text
        self._position = position

    def execute(self) -> None:
        self._editor.insert(self._text, self._position)
        print(f"Inserted '{self._text}' at position {self._position}")

    def undo(self) -> None:
        self._editor.delete(self._position, self._position + len(self._text))
        print(f"Undid insert of '{self._text}'")

class DeleteCommand(Command):
    def __init__(self, editor: TextEditor, start: int, end: int):
        self._editor = editor
        self._start = start
        self._end = end
        self._deleted_text = ""

    def execute(self) -> None:
        self._deleted_text = self._editor.delete(self._start, self._end)
        print(f"Deleted '{self._deleted_text}'")

    def undo(self) -> None:
        self._editor.insert(self._deleted_text, self._start)
        print(f"Undid delete, restored '{self._deleted_text}'")

class ReplaceCommand(Command):
    def __init__(self, editor: TextEditor, start: int, end: int, new_text: str):
        self._editor = editor
        self._start = start
        self._end = end
        self._new_text = new_text
        self._old_text = ""

    def execute(self) -> None:
        self._old_text = self._editor.replace(self._start, self._end, self._new_text)
        print(f"Replaced '{self._old_text}' with '{self._new_text}'")

    def undo(self) -> None:
        self._editor.replace(self._start, self._start + len(self._new_text), self._old_text)
        print(f"Undid replace, restored '{self._old_text}'")

# Invoker with undo/redo support
class EditorHistory:
    def __init__(self):
        self._history: List[Command] = []
        self._redo_stack: List[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()  # Clear redo stack on new command

    def undo(self) -> None:
        if not self._history:
            print("Nothing to undo!")
            return

        command = self._history.pop()
        command.undo()
        self._redo_stack.append(command)

    def redo(self) -> None:
        if not self._redo_stack:
            print("Nothing to redo!")
            return

        command = self._redo_stack.pop()
        command.execute()
        self._history.append(command)

# Macro Command - composite of commands
class MacroCommand(Command):
    def __init__(self):
        self._commands: List[Command] = []

    def add(self, command: Command) -> None:
        self._commands.append(command)

    def execute(self) -> None:
        print("--- Executing Macro ---")
        for command in self._commands:
            command.execute()

    def undo(self) -> None:
        print("--- Undoing Macro ---")
        for command in reversed(self._commands):
            command.undo()

# Usage
if __name__ == "__main__":
    editor = TextEditor()
    history = EditorHistory()

    print("=== Text Editor Demo ===\n")

    # Execute commands
    history.execute(InsertCommand(editor, "Hello", 0))
    print(f"Text: '{editor.text}'")

    history.execute(InsertCommand(editor, " World", 5))
    print(f"Text: '{editor.text}'")

    history.execute(InsertCommand(editor, "!", 11))
    print(f"Text: '{editor.text}'")

    # Undo
    print("\n--- Undoing ---")
    history.undo()
    print(f"Text: '{editor.text}'")

    history.undo()
    print(f"Text: '{editor.text}'")

    # Redo
    print("\n--- Redoing ---")
    history.redo()
    print(f"Text: '{editor.text}'")

    # Replace
    print("\n--- Replace ---")
    history.execute(ReplaceCommand(editor, 0, 5, "Hi"))
    print(f"Text: '{editor.text}'")

    history.undo()
    print(f"Text: '{editor.text}'")

    # Macro command
    print("\n--- Macro Command ---")
    editor2 = TextEditor()
    macro = MacroCommand()
    macro.add(InsertCommand(editor2, "function ", 0))
    macro.add(InsertCommand(editor2, "hello", 9))
    macro.add(InsertCommand(editor2, "() {}", 14))

    macro.execute()
    print(f"Text: '{editor2.text}'")

    macro.undo()
    print(f"Text: '{editor2.text}'")
```

### Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "Command vs Strategy?" | Pattern distinction | Command encapsulates action + receiver; Strategy encapsulates algorithm |
| "How to implement undo for database changes?" | Practical application | Store inverse operations or use memento pattern for state snapshots |
| "Command in distributed systems?" | Architecture connection | Commands can be serialized, queued (message queue), replayed (event sourcing) |

---

## 5. Template Method Pattern

### Intent
Define the skeleton of an algorithm in an operation, deferring some steps to subclasses. Template Method lets subclasses redefine certain steps of an algorithm without changing the algorithm's structure.

### Real-World Analogy
**Recipe Template**: "Make Beverage" has steps: boil water, brew, pour, add condiments. Coffee and Tea follow the same template but implement brew() and addCondiments() differently.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   Template Method Pattern Structure                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────┐                                  │
│   │       AbstractClass             │                                  │
│   ├─────────────────────────────────┤                                  │
│   │ + templateMethod()  ─────────┐  │  ◄── Final - can't override     │
│   │                              │  │                                  │
│   │     ┌────────────────────────┘  │                                  │
│   │     │  step1()                  │  ◄── Concrete steps              │
│   │     │  step2()     // abstract  │                                  │
│   │     │  step3()     // abstract  │  ◄── Abstract steps for subclass │
│   │     │  hook()      // optional  │  ◄── Hook - optional override    │
│   │     │  step4()                  │                                  │
│   │     └────────────────────────   │                                  │
│   │                                 │                                  │
│   │ # step2()  // abstract          │                                  │
│   │ # step3()  // abstract          │                                  │
│   │ # hook()   // empty default     │                                  │
│   └─────────────────────────────────┘                                  │
│                    ▲                                                    │
│          ┌─────────┴─────────┐                                         │
│          │                   │                                         │
│   ┌──────┴────────┐   ┌──────┴────────┐                               │
│   │ ConcreteA     │   │ ConcreteB     │                               │
│   ├───────────────┤   ├───────────────┤                               │
│   │ # step2()     │   │ # step2()     │  ◄── Implement abstract steps │
│   │ # step3()     │   │ # step3()     │                               │
│   │ # hook()      │   │               │  ◄── May override hook        │
│   └───────────────┘   └───────────────┘                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Python Implementation

```python
from abc import ABC, abstractmethod

# Abstract Class with Template Method
class DataMiner(ABC):
    """Template for data mining operations"""

    def mine(self, path: str) -> str:
        """
        Template method - defines the algorithm skeleton.
        Marked as final (by convention) - subclasses shouldn't override.
        """
        file_data = self.open_file(path)
        raw_data = self.extract_data(file_data)
        parsed_data = self.parse_data(raw_data)

        # Hook - optional step
        if self.should_analyze():
            analysis = self.analyze_data(parsed_data)
        else:
            analysis = parsed_data

        report = self.generate_report(analysis)
        self.send_report(report)

        return report

    # Concrete steps - same for all subclasses
    def open_file(self, path: str) -> str:
        print(f"Opening file: {path}")
        return f"<file_content:{path}>"

    def send_report(self, report: str) -> None:
        print(f"Sending report ({len(report)} chars)...")

    # Abstract steps - must be implemented by subclasses
    @abstractmethod
    def extract_data(self, file_data: str) -> str:
        """Extract raw data from file"""
        pass

    @abstractmethod
    def parse_data(self, raw_data: str) -> dict:
        """Parse raw data into structured format"""
        pass

    # Hook methods - optional override points
    def should_analyze(self) -> bool:
        """Hook: override to skip analysis step"""
        return True

    def analyze_data(self, data: dict) -> dict:
        """Hook: override to customize analysis"""
        print("Performing default analysis...")
        return {"analyzed": True, "data": data}

    def generate_report(self, data: dict) -> str:
        """Hook: override to customize report format"""
        return f"Report: {data}"

# Concrete implementations
class PDFDataMiner(DataMiner):
    def extract_data(self, file_data: str) -> str:
        print("Extracting text from PDF...")
        return "PDF extracted text content"

    def parse_data(self, raw_data: str) -> dict:
        print("Parsing PDF data...")
        return {"type": "pdf", "content": raw_data, "pages": 10}

class CSVDataMiner(DataMiner):
    def extract_data(self, file_data: str) -> str:
        print("Reading CSV rows...")
        return "col1,col2,col3\nval1,val2,val3"

    def parse_data(self, raw_data: str) -> dict:
        print("Parsing CSV into records...")
        rows = raw_data.split('\n')
        return {"type": "csv", "headers": rows[0], "rows": len(rows) - 1}

    # Override hook to customize report
    def generate_report(self, data: dict) -> str:
        return f"CSV Report: {data['rows']} rows with headers: {data['headers']}"

class JSONDataMiner(DataMiner):
    def extract_data(self, file_data: str) -> str:
        print("Reading JSON structure...")
        return '{"key": "value", "items": [1, 2, 3]}'

    def parse_data(self, raw_data: str) -> dict:
        print("Parsing JSON...")
        import json
        return {"type": "json", "data": json.loads(raw_data)}

    # Override hook to skip analysis
    def should_analyze(self) -> bool:
        return False

# Usage
if __name__ == "__main__":
    print("=== PDF Mining ===")
    pdf_miner = PDFDataMiner()
    pdf_miner.mine("document.pdf")

    print("\n=== CSV Mining ===")
    csv_miner = CSVDataMiner()
    csv_miner.mine("data.csv")

    print("\n=== JSON Mining (no analysis) ===")
    json_miner = JSONDataMiner()
    json_miner.mine("config.json")
```

### Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "Template Method vs Strategy?" | Pattern comparison | Template uses inheritance (is-a); Strategy uses composition (has-a) |
| "What's a hook?" | Pattern details | Empty method that subclasses can optionally override |
| "When to use hooks vs abstract?" | Design judgment | Abstract = must implement; Hook = optional customization point |

---

## Summary: Behavioral Patterns Cheat Sheet

```
┌─────────────────────────────────────────────────────────────────────────┐
│              Behavioral Patterns Quick Reference                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Pattern      │ Use When...                                             │
│  ─────────────┼──────────────────────────────────────────────────────── │
│  Strategy     │ You need interchangeable algorithms                     │
│  Observer     │ Objects need to be notified of state changes            │
│  State        │ Object behavior depends on its state                    │
│  Command      │ You need undoable operations or request queuing         │
│  Template     │ Algorithm skeleton is fixed, but steps vary             │
│  Chain of Resp│ Request can be handled by multiple handlers             │
│  Iterator     │ You need uniform traversal of collections               │
│  Mediator     │ Objects communicate through a central hub               │
│                                                                         │
│  Interview Quick Tests:                                                 │
│  ──────────────────────                                                 │
│  "I want to switch algorithms at runtime" → Strategy                   │
│  "I want to notify multiple objects" → Observer                        │
│  "Behavior changes based on state" → State                             │
│  "I need undo/redo" → Command                                          │
│  "Same algorithm, different steps" → Template Method                   │
│                                                                         │
│  Common Combinations:                                                   │
│  ────────────────────                                                   │
│  • Command + Memento = Undoable operations                             │
│  • Observer + Mediator = Event bus                                     │
│  • State + Strategy = Context-aware algorithms                         │
│  • Template + Factory = Framework construction                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

**Next:** Continue to [06_uml_basics.md](./06_uml_basics.md) to learn how to draw and read UML diagrams.
