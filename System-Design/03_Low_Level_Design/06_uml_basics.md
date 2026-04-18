# UML Basics for System Design Interviews

## What is UML?

**UML (Unified Modeling Language)** is a standardized way to visualize software design. In interviews, you'll primarily use **Class Diagrams** for LLD and **Sequence Diagrams** for showing interactions.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    UML Diagrams Overview                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Structural Diagrams              Behavioral Diagrams                  │
│   ───────────────────              ────────────────────                 │
│   • Class Diagram ★★★              • Sequence Diagram ★★★              │
│   • Object Diagram                 • Use Case Diagram ★★               │
│   • Component Diagram              • Activity Diagram ★                │
│   • Package Diagram                • State Diagram ★                   │
│                                                                         │
│   ★★★ = Most important for interviews                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Class Diagrams

### Basic Class Notation

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       Class Diagram Anatomy                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────┐                                  │
│   │         <<interface>>           │  ◄── Stereotype (optional)       │
│   │           ClassName             │  ◄── Class name (bold for class) │
│   ├─────────────────────────────────┤                                  │
│   │ - privateField: Type            │                                  │
│   │ # protectedField: Type          │  ◄── Attributes                  │
│   │ + publicField: Type             │      (visibility name: type)     │
│   │ ~ packageField: Type            │                                  │
│   │ staticField: Type {static}      │                                  │
│   ├─────────────────────────────────┤                                  │
│   │ + publicMethod(param): Return   │                                  │
│   │ - privateMethod(): void         │  ◄── Methods                     │
│   │ # protectedMethod()             │      (visibility name(params))   │
│   │ + abstractMethod() {abstract}   │                                  │
│   └─────────────────────────────────┘                                  │
│                                                                         │
│   Visibility Symbols:                                                   │
│   ───────────────────                                                   │
│   +  Public      (anyone can access)                                   │
│   -  Private     (only this class)                                     │
│   #  Protected   (this class + subclasses)                             │
│   ~  Package     (same package only)                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Relationship Types

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    UML Relationship Types                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ASSOCIATION (knows-about)                                             │
│   ─────────────────────────                                             │
│   ┌─────────┐         ┌─────────┐                                      │
│   │ Teacher │─────────│ Student │    Teacher knows about Student       │
│   └─────────┘         └─────────┘                                      │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   AGGREGATION (has-a, weak ownership)                                   │
│   ───────────────────────────────────                                   │
│   ┌─────────┐         ┌─────────┐                                      │
│   │Department│◇───────│Professor│    Department has Professors         │
│   └─────────┘         └─────────┘    (Professors exist independently)  │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   COMPOSITION (has-a, strong ownership)                                 │
│   ─────────────────────────────────────                                 │
│   ┌─────────┐         ┌─────────┐                                      │
│   │  House  │◆────────│  Room   │    House owns Rooms                  │
│   └─────────┘         └─────────┘    (Rooms don't exist without House) │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   INHERITANCE (is-a)                                                    │
│   ──────────────────                                                    │
│   ┌─────────┐                                                          │
│   │ Animal  │                        Dog IS-A Animal                   │
│   └────▲────┘                                                          │
│        │                                                                │
│        │ (extends)                                                      │
│   ┌────┴────┐                                                          │
│   │   Dog   │                                                          │
│   └─────────┘                                                          │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   IMPLEMENTATION (realizes)                                             │
│   ─────────────────────────                                             │
│   ┌─────────────┐                                                      │
│   │<<interface>>│                    Dog IMPLEMENTS Runnable           │
│   │  Runnable   │                                                      │
│   └──────▲──────┘                                                      │
│          ┆                                                              │
│          ┆ (implements)                                                 │
│   ┌──────┴──────┐                                                      │
│   │     Dog     │                                                      │
│   └─────────────┘                                                      │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   DEPENDENCY (uses)                                                     │
│   ─────────────────                                                     │
│   ┌─────────┐         ┌─────────┐                                      │
│   │ Client  │- - - - >│ Service │    Client uses Service temporarily   │
│   └─────────┘         └─────────┘    (method parameter, local var)     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Multiplicity Notation

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Multiplicity in UML                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Symbol    Meaning                                                     │
│   ──────    ───────                                                     │
│   1         Exactly one                                                 │
│   0..1      Zero or one (optional)                                     │
│   *         Zero or more                                               │
│   1..*      One or more                                                │
│   n         Exactly n                                                  │
│   n..m      Between n and m                                            │
│                                                                         │
│   Examples:                                                             │
│   ─────────                                                             │
│                                                                         │
│   ┌────────┐    1      * ┌────────┐                                   │
│   │Customer│─────────────│ Order  │   One customer, many orders        │
│   └────────┘             └────────┘                                    │
│                                                                         │
│   ┌────────┐   1..*   1 ┌────────┐                                    │
│   │Student │─────────────│ Class  │   Many students in one class       │
│   └────────┘             └────────┘                                    │
│                                                                         │
│   ┌────────┐    *     * ┌────────┐                                    │
│   │ Actor  │─────────────│ Movie  │   Many-to-many relationship        │
│   └────────┘             └────────┘                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Complete Example: E-Commerce System

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    E-Commerce Class Diagram                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌───────────────────┐                                                │
│   │    <<abstract>>   │                                                │
│   │       User        │                                                │
│   ├───────────────────┤                                                │
│   │ - id: UUID        │                                                │
│   │ - email: String   │                                                │
│   │ - password: Hash  │                                                │
│   ├───────────────────┤                                                │
│   │ + login()         │                                                │
│   │ + logout()        │                                                │
│   └─────────▲─────────┘                                                │
│             │                                                           │
│      ┌──────┴──────┐                                                   │
│      │             │                                                   │
│ ┌────┴─────┐  ┌────┴─────┐                                            │
│ │ Customer │  │  Admin   │                                            │
│ ├──────────┤  ├──────────┤                                            │
│ │- address │  │- level   │                                            │
│ ├──────────┤  ├──────────┤                                            │
│ │+placeOrd │  │+addProd  │                                            │
│ │+viewHist │  │+viewStat │                                            │
│ └────┬─────┘  └──────────┘                                            │
│      │                                                                  │
│      │ 1                                                                │
│      │                                                                  │
│      │ places                                                           │
│      │                                                                  │
│      │ *                                                                │
│ ┌────┴─────────────────┐         ┌─────────────────────┐              │
│ │        Order         │    *    │       Product       │              │
│ ├──────────────────────┤◆────────├─────────────────────┤              │
│ │ - orderId: UUID      │         │ - productId: UUID   │              │
│ │ - status: OrderStatus│ contains│ - name: String      │              │
│ │ - createdAt: DateTime│         │ - price: Decimal    │              │
│ ├──────────────────────┤         │ - stock: int        │              │
│ │ + calculateTotal()   │         ├─────────────────────┤              │
│ │ + cancel()           │         │ + updateStock()     │              │
│ │ + ship()             │         │ + getDetails()      │              │
│ └──────────┬───────────┘         └──────────┬──────────┘              │
│            │                                 │                         │
│            │ 1                               │                         │
│            │                                 │ *                       │
│            │ has                             │ belongs to              │
│            │                                 │                         │
│            │ 1                               │ 1                       │
│ ┌──────────┴───────────┐         ┌──────────┴──────────┐              │
│ │       Payment        │         │      Category       │              │
│ ├──────────────────────┤         ├─────────────────────┤              │
│ │ - amount: Decimal    │         │ - name: String      │              │
│ │ - method: PayMethod  │         │ - parent: Category  │              │
│ │ - status: PayStatus  │         ├─────────────────────┤              │
│ ├──────────────────────┤         │ + getProducts()     │              │
│ │ + process()          │         └─────────────────────┘              │
│ │ + refund()           │                                               │
│ └──────────────────────┘                                               │
│                                                                         │
│   ┌───────────────────┐                                                │
│   │  <<enumeration>>  │                                                │
│   │   OrderStatus     │                                                │
│   ├───────────────────┤                                                │
│   │ PENDING           │                                                │
│   │ CONFIRMED         │                                                │
│   │ SHIPPED           │                                                │
│   │ DELIVERED         │                                                │
│   │ CANCELLED         │                                                │
│   └───────────────────┘                                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Sequence Diagrams

Sequence diagrams show **how objects interact over time**. They're essential for showing API flows and use case implementations.

### Basic Notation

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Sequence Diagram Elements                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────┐          ┌─────────┐         ┌─────────┐                │
│   │ Object1 │          │ Object2 │         │ Object3 │ ◄── Participants│
│   └────┬────┘          └────┬────┘         └────┬────┘                │
│        │                    │                   │                       │
│        │  1. methodCall()   │                   │    ◄── Sync message  │
│        │ ─────────────────► │                   │                       │
│        │                    │                   │                       │
│        │                    │  2. delegate()    │                       │
│        │                    │ ─────────────────►│                       │
│        │                    │                   │                       │
│        │                    │  3. response      │    ◄── Return        │
│        │                    │ ◄─────────────────│                       │
│        │                    │                   │                       │
│        │  4. result         │                   │                       │
│        │ ◄─────────────────│                   │                       │
│        │                    │                   │                       │
│        │  5. asyncCall()    │                   │    ◄── Async message │
│        │ - - - - - - - - - >│                   │        (dashed line) │
│        │                    │                   │                       │
│        │                    │                   │                       │
│        ▼                    ▼                   ▼       ◄── Lifeline   │
│                                                                         │
│   Activation box = when object is active/processing                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Combined Fragments

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Combined Fragment Types                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   alt - Alternative (if/else)                                          │
│   ┌─────────────────────────────────────────────┐                      │
│   │ alt                                         │                      │
│   │  ┌─────────────────────────────────────────┤                      │
│   │  │ [condition1]                             │                      │
│   │  │     do something                         │                      │
│   │  ├─────────────────────────────────────────┤                      │
│   │  │ [else]                                   │                      │
│   │  │     do something else                    │                      │
│   │  └─────────────────────────────────────────┤                      │
│   └─────────────────────────────────────────────┘                      │
│                                                                         │
│   opt - Optional (if without else)                                     │
│   ┌─────────────────────────────────────────────┐                      │
│   │ opt [condition]                             │                      │
│   │     only execute if condition is true       │                      │
│   └─────────────────────────────────────────────┘                      │
│                                                                         │
│   loop - Iteration                                                     │
│   ┌─────────────────────────────────────────────┐                      │
│   │ loop [1, n] or loop [for each item]         │                      │
│   │     repeated action                         │                      │
│   └─────────────────────────────────────────────┘                      │
│                                                                         │
│   par - Parallel execution                                             │
│   ┌─────────────────────────────────────────────┐                      │
│   │ par                                         │                      │
│   │  ┌─────────────────────────────────────────┤                      │
│   │  │ action1 (parallel)                       │                      │
│   │  ├─────────────────────────────────────────┤                      │
│   │  │ action2 (parallel)                       │                      │
│   │  └─────────────────────────────────────────┤                      │
│   └─────────────────────────────────────────────┘                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Example: User Login Sequence

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Login Sequence Diagram                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────┐     ┌───────────┐    ┌────────────┐    ┌──────────┐        │
│   │Client│     │API Gateway│    │Auth Service│    │ Database │        │
│   └──┬───┘     └─────┬─────┘    └──────┬─────┘    └────┬─────┘        │
│      │               │                  │               │              │
│      │ POST /login   │                  │               │              │
│      │ ─────────────>│                  │               │              │
│      │               │                  │               │              │
│      │               │ validateRequest()│               │              │
│      │               │ ────────────────>│               │              │
│      │               │                  │               │              │
│      │               │                  │ findUser(email)              │
│      │               │                  │ ─────────────────────────>   │
│      │               │                  │               │              │
│      │               │                  │     user data │              │
│      │               │                  │ <─────────────────────────   │
│      │               │                  │               │              │
│      │               │  ┌───────────────┴───────────────┐              │
│      │               │  │ alt                           │              │
│      │               │  │  [user exists & password valid]              │
│      │               │  │     generateToken()           │              │
│      │               │  │  ┌──────────────────────────┐ │              │
│      │               │  │  │                          │ │              │
│      │               │  │  │  store session           │ │              │
│      │               │  │  │  ──────────────────────> │ │              │
│      │               │  │  │                          │ │              │
│      │               │  │  │  OK                      │ │              │
│      │               │  │  │  <────────────────────── │ │              │
│      │               │  │  │                          │ │              │
│      │               │  │  └──────────────────────────┘ │              │
│      │               │  │     return {token, user}     │              │
│      │               │  ├───────────────────────────────│              │
│      │               │  │  [else]                       │              │
│      │               │  │     return 401 Unauthorized   │              │
│      │               │  └───────────────────────────────┘              │
│      │               │                  │               │              │
│      │               │  authResult      │               │              │
│      │               │ <────────────────│               │              │
│      │               │                  │               │              │
│      │  response     │                  │               │              │
│      │ <─────────────│                  │               │              │
│      │               │                  │               │              │
│      ▼               ▼                  ▼               ▼              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Use Case Diagrams

Use Case diagrams show **what a system does** from the user's perspective.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Use Case Diagram Example                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                    ┌────────────────────────────────┐                  │
│                    │      E-Commerce System         │                  │
│                    │                                │                  │
│    ┌─────┐         │   ┌─────────────────┐         │                  │
│    │     │         │   │  Browse Products │         │                  │
│    │  😊 │─────────┼──>│                 │         │                  │
│    │     │         │   └─────────────────┘         │                  │
│    │Guest│         │            │                   │                  │
│    └─────┘         │            │ <<include>>       │                  │
│                    │            ▼                   │                  │
│                    │   ┌─────────────────┐         │                  │
│    ┌─────┐         │   │   View Product  │         │                  │
│    │     │         │   └─────────────────┘         │                  │
│    │  😊 │─────────┼──>┌─────────────────┐         │                  │
│    │     │         │   │   Place Order   │         │                  │
│    │Custo│         │   └───────┬─────────┘         │                  │
│    │ mer │         │           │                   │                  │
│    └─────┘         │           │ <<include>>       │                  │
│       │            │           ▼                   │                  │
│       │            │   ┌─────────────────┐         │                  │
│       └────────────┼──>│   Make Payment  │         │                  │
│                    │   └───────┬─────────┘         │                  │
│                    │           │                   │                  │
│                    │           │ <<extend>>        │                  │
│                    │           ▼                   │                  │
│    ┌─────┐         │   ┌─────────────────┐         │                  │
│    │     │         │   │  Apply Coupon   │         │                  │
│    │  😊 │─────────┼──>└─────────────────┘         │                  │
│    │     │         │                                │                  │
│    │Admin│         │   ┌─────────────────┐         │                  │
│    └─────┘─────────┼──>│ Manage Products │         │                  │
│                    │   └─────────────────┘         │                  │
│                    │                                │                  │
│                    └────────────────────────────────┘                  │
│                                                                         │
│   Relationships:                                                        │
│   <<include>>  - Always executed (required)                            │
│   <<extend>>   - Optionally executed (conditional)                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. State Diagrams

State diagrams show **object lifecycle** and state transitions.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Order State Diagram                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                        ●  (Initial state)                              │
│                        │                                                │
│                        │ create                                         │
│                        ▼                                                │
│                  ┌───────────┐                                         │
│                  │   DRAFT   │                                         │
│                  └─────┬─────┘                                         │
│                        │                                                │
│             ┌──────────┼──────────┐                                    │
│             │ submit   │          │ cancel                              │
│             ▼          │          ▼                                     │
│       ┌───────────┐    │    ┌───────────┐                              │
│       │  PENDING  │    │    │ CANCELLED │                              │
│       └─────┬─────┘    │    └─────┬─────┘                              │
│             │          │          │                                     │
│    ┌────────┼────────┐ │          │                                     │
│    │pay     │        │cancel      │                                     │
│    ▼        │        ▼ │          │                                     │
│ ┌────────┐  │  ┌────────┐         │                                    │
│ │CONFIRMED│  │  │(merged)│         │                                    │
│ └────┬───┘  │  └────────┘         │                                    │
│      │      │                      │                                    │
│      │ ship │                      │                                    │
│      ▼      │                      │                                    │
│ ┌────────┐  │                      │                                    │
│ │SHIPPED │  │                      │                                    │
│ └────┬───┘  │                      │                                    │
│      │      │                      │                                    │
│      │deliver                      │                                    │
│      ▼      │                      │                                    │
│ ┌────────┐  │                      ▼                                    │
│ │DELIVERED│ │                 ◉  (Final state)                         │
│ └────┬───┘  │                                                          │
│      │      │                                                          │
│      ▼      │                                                          │
│      ◉ ◄────┘                                                          │
│                                                                         │
│   Legend:                                                               │
│   ●  Initial state (filled circle)                                     │
│   ◉  Final state (circle with dot)                                     │
│   ┌──┐ State (rounded rectangle)                                       │
│   ─► Transition with trigger event                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Interview Tips for UML

### What to Draw

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Interview UML Tips                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   DO:                                                                   │
│   ───                                                                   │
│   ✓ Start with main classes/entities                                   │
│   ✓ Show key attributes (not all)                                      │
│   ✓ Show important methods                                             │
│   ✓ Indicate relationships and multiplicity                            │
│   ✓ Use proper notation for inheritance vs composition                 │
│   ✓ Draw sequence diagram for complex flows                            │
│                                                                         │
│   DON'T:                                                                │
│   ─────                                                                 │
│   ✗ Include every field and method                                     │
│   ✗ Draw getters/setters                                               │
│   ✗ Obsess over perfect UML syntax                                     │
│   ✗ Spend too much time on diagrams                                    │
│   ✗ Forget to explain as you draw                                      │
│                                                                         │
│   Time Budget (45 min interview):                                      │
│   ────────────────────────────────                                      │
│   • Requirements: 5 min                                                │
│   • Class Diagram: 10-15 min                                           │
│   • Key APIs/Methods: 10 min                                           │
│   • Sequence Diagram (if needed): 5-10 min                             │
│   • Discussion: remaining time                                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Whiteboard Shortcuts

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Whiteboard UML Shortcuts                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Instead of perfect UML, these are acceptable:                        │
│                                                                         │
│   Inheritance:     Animal                                              │
│                       △                                                 │
│                       │                                                 │
│                      Dog                                                │
│                                                                         │
│   Composition:     Order ◆──── LineItem                                │
│                                                                         │
│   Association:     User ────── Order                                   │
│                          1     *                                        │
│                                                                         │
│   Interface:       «I» Runnable                                        │
│                        ┆                                                │
│                       Dog                                               │
│                                                                         │
│   Quick class:     ┌─────────────┐                                     │
│                    │   Order     │                                     │
│                    │─────────────│                                     │
│                    │ id, status  │  ← Combine attributes               │
│                    │─────────────│                                     │
│                    │ place()     │                                     │
│                    │ cancel()    │                                     │
│                    └─────────────┘                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    UML Quick Reference                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   VISIBILITY          RELATIONSHIPS            MULTIPLICITY             │
│   + public            ────── association       1     exactly one        │
│   - private           ◇───── aggregation      0..1  zero or one        │
│   # protected         ◆───── composition      *     zero or more       │
│   ~ package           △───── inheritance      1..*  one or more        │
│                       ┆┆┆┆┆┆ implementation                             │
│                       - - -> dependency                                 │
│                                                                         │
│   CLASS STEREOTYPES                                                     │
│   <<interface>>       No implementation                                │
│   <<abstract>>        Partial implementation                           │
│   <<enumeration>>     Fixed set of values                              │
│   <<entity>>          Domain object                                    │
│   <<service>>         Business logic                                   │
│   <<repository>>      Data access                                      │
│                                                                         │
│   SEQUENCE FRAGMENTS                                                    │
│   alt   if/else                                                        │
│   opt   if (no else)                                                   │
│   loop  iteration                                                      │
│   par   parallel                                                       │
│   break exception                                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

**Next:** Continue to [07_dependency_injection.md](./07_dependency_injection.md) to learn about loose coupling through DI.
