# Bloom Filters

## What is a Bloom Filter?

A **Bloom Filter** is a space-efficient probabilistic data structure that tests whether an element is a member of a set. It can tell you:
- **Definitely NOT in set** (100% accurate)
- **Possibly in set** (may have false positives)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Bloom Filter Concept                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Problem: Check if username exists (among 100M users)                 │
│                                                                         │
│   Naive approach:                                                      │
│   SELECT * FROM users WHERE username = 'john'                          │
│   → Database query every time (slow!)                                  │
│                                                                         │
│   HashSet approach:                                                    │
│   Store all 100M usernames in memory                                   │
│   → ~5GB memory (expensive!)                                           │
│                                                                         │
│   Bloom Filter approach:                                               │
│   Store probabilistic representation                                   │
│   → ~100MB memory                                                      │
│   → "Definitely not exists" = skip DB                                  │
│   → "Might exist" = check DB                                           │
│                                                                         │
│   Trade-off: Small chance of false positives                          │
│   (says "might exist" when it doesn't)                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## How It Works

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Bloom Filter Structure                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Bit Array (m bits, initially all 0):                                 │
│   ─────────────────────────────────────                                 │
│   Index:  0   1   2   3   4   5   6   7   8   9                       │
│   Bits:  [0] [0] [0] [0] [0] [0] [0] [0] [0] [0]                      │
│                                                                         │
│   k hash functions: h1, h2, h3                                        │
│                                                                         │
│   INSERT "apple":                                                      │
│   ─────────────────                                                     │
│   h1("apple") % 10 = 2                                                │
│   h2("apple") % 10 = 5                                                │
│   h3("apple") % 10 = 8                                                │
│                                                                         │
│   Set bits 2, 5, 8 to 1:                                              │
│   Index:  0   1   2   3   4   5   6   7   8   9                       │
│   Bits:  [0] [0] [1] [0] [0] [1] [0] [0] [1] [0]                      │
│                                                                         │
│   INSERT "banana":                                                     │
│   ────────────────                                                      │
│   h1("banana") % 10 = 1                                               │
│   h2("banana") % 10 = 5  (already 1)                                  │
│   h3("banana") % 10 = 7                                               │
│                                                                         │
│   Set bits 1, 5, 7 to 1:                                              │
│   Index:  0   1   2   3   4   5   6   7   8   9                       │
│   Bits:  [0] [1] [1] [0] [0] [1] [0] [1] [1] [0]                      │
│                                                                         │
│   QUERY "apple":                                                       │
│   ───────────────                                                       │
│   Check bits 2, 5, 8 → all are 1 → "MIGHT EXIST" ✓                   │
│                                                                         │
│   QUERY "cherry":                                                      │
│   ────────────────                                                      │
│   h1("cherry") % 10 = 3                                               │
│   h2("cherry") % 10 = 6                                               │
│   h3("cherry") % 10 = 9                                               │
│   Check bits 3, 6, 9 → bit 3 is 0 → "DEFINITELY NOT EXISTS" ✗        │
│                                                                         │
│   QUERY "grape" (false positive example):                             │
│   ───────────────────────────────────────                               │
│   h1("grape") % 10 = 1  (set by banana)                               │
│   h2("grape") % 10 = 5  (set by apple/banana)                         │
│   h3("grape") % 10 = 8  (set by apple)                                │
│   All bits are 1 → "MIGHT EXIST" (but it doesn't!)                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Properties

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Bloom Filter Properties                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ✓ NO FALSE NEGATIVES                                                 │
│     If filter says "not in set" → definitely not in set               │
│                                                                         │
│   ✗ FALSE POSITIVES POSSIBLE                                           │
│     If filter says "might be in set" → check actual data              │
│                                                                         │
│   ✓ SPACE EFFICIENT                                                    │
│     ~10 bits per element for 1% false positive rate                   │
│     1 billion elements ≈ 1.2 GB                                        │
│                                                                         │
│   ✓ O(k) INSERT AND QUERY                                              │
│     k = number of hash functions (typically 3-10)                     │
│     Constant time regardless of set size                              │
│                                                                         │
│   ✗ CANNOT DELETE                                                      │
│     Clearing a bit might affect other elements                        │
│     (Use Counting Bloom Filter for deletion)                          │
│                                                                         │
│   ✗ CANNOT LIST ELEMENTS                                               │
│     Only membership test, not enumeration                             │
│                                                                         │
│   False Positive Rate:                                                 │
│   ────────────────────                                                  │
│   p ≈ (1 - e^(-kn/m))^k                                               │
│                                                                         │
│   Where:                                                               │
│   m = number of bits                                                   │
│   n = number of elements                                               │
│   k = number of hash functions                                         │
│                                                                         │
│   Optimal k = (m/n) * ln(2) ≈ 0.7 * (m/n)                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Implementation

### Python

```python
import math
import mmh3  # MurmurHash3

class BloomFilter:
    def __init__(self, expected_elements: int, false_positive_rate: float = 0.01):
        """
        Initialize Bloom Filter.

        Args:
            expected_elements: Expected number of elements to insert
            false_positive_rate: Desired false positive probability (default 1%)
        """
        # Calculate optimal size and hash functions
        self.size = self._optimal_size(expected_elements, false_positive_rate)
        self.hash_count = self._optimal_hash_count(self.size, expected_elements)
        self.bit_array = [0] * self.size
        self.count = 0

        print(f"Bloom Filter initialized:")
        print(f"  Size: {self.size} bits ({self.size / 8 / 1024:.2f} KB)")
        print(f"  Hash functions: {self.hash_count}")

    def _optimal_size(self, n: int, p: float) -> int:
        """Calculate optimal bit array size"""
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    def _optimal_hash_count(self, m: int, n: int) -> int:
        """Calculate optimal number of hash functions"""
        k = (m / n) * math.log(2)
        return int(k)

    def _get_hash_values(self, item: str) -> list:
        """Generate k hash values for an item"""
        # Use two hash functions to simulate k hash functions
        # h(i) = h1 + i * h2
        h1 = mmh3.hash(item, 0) % self.size
        h2 = mmh3.hash(item, 1) % self.size

        return [(h1 + i * h2) % self.size for i in range(self.hash_count)]

    def add(self, item: str) -> None:
        """Add an item to the filter"""
        for index in self._get_hash_values(item):
            self.bit_array[index] = 1
        self.count += 1

    def might_contain(self, item: str) -> bool:
        """
        Check if item might be in the set.

        Returns:
            False = Definitely not in set
            True = Might be in set (could be false positive)
        """
        return all(self.bit_array[i] == 1 for i in self._get_hash_values(item))

    def __contains__(self, item: str) -> bool:
        """Support 'in' operator"""
        return self.might_contain(item)

    @property
    def fill_ratio(self) -> float:
        """Ratio of bits set to 1"""
        return sum(self.bit_array) / self.size

# Demo
if __name__ == "__main__":
    # Create filter for 1 million elements with 1% false positive rate
    bf = BloomFilter(expected_elements=1_000_000, false_positive_rate=0.01)

    # Add some usernames
    existing_users = ["alice", "bob", "charlie", "david", "eve"]
    for user in existing_users:
        bf.add(user)

    # Test membership
    print("\n=== Membership Tests ===")
    test_users = ["alice", "bob", "frank", "grace", "charlie"]

    for user in test_users:
        result = "might exist" if user in bf else "definitely not exists"
        actual = "actually exists" if user in existing_users else "actually doesn't exist"
        print(f"{user}: {result} ({actual})")

    # Demonstrate false positive rate
    print("\n=== False Positive Test ===")
    import random
    import string

    # Add 100,000 random strings
    for _ in range(100_000):
        random_str = ''.join(random.choices(string.ascii_lowercase, k=10))
        bf.add(random_str)

    # Test 10,000 strings that were NOT added
    false_positives = 0
    tests = 10_000
    for _ in range(tests):
        test_str = ''.join(random.choices(string.ascii_uppercase, k=10))
        if test_str in bf:  # All uppercase, so definitely not added
            false_positives += 1

    print(f"False positive rate: {false_positives/tests*100:.2f}%")
    print(f"Fill ratio: {bf.fill_ratio*100:.1f}%")
```

### Java

```java
import java.util.BitSet;

public class BloomFilter {
    private BitSet bitSet;
    private int size;
    private int hashCount;

    public BloomFilter(int expectedElements, double falsePositiveRate) {
        this.size = optimalSize(expectedElements, falsePositiveRate);
        this.hashCount = optimalHashCount(size, expectedElements);
        this.bitSet = new BitSet(size);

        System.out.printf("Bloom Filter: %d bits, %d hash functions%n",
                         size, hashCount);
    }

    private int optimalSize(int n, double p) {
        return (int) (-(n * Math.log(p)) / (Math.log(2) * Math.log(2)));
    }

    private int optimalHashCount(int m, int n) {
        return (int) ((m / (double) n) * Math.log(2));
    }

    private int[] getHashValues(String item) {
        int[] hashes = new int[hashCount];
        int h1 = item.hashCode();
        int h2 = h1 >>> 16;  // Simple second hash

        for (int i = 0; i < hashCount; i++) {
            hashes[i] = Math.abs((h1 + i * h2) % size);
        }
        return hashes;
    }

    public void add(String item) {
        for (int index : getHashValues(item)) {
            bitSet.set(index);
        }
    }

    public boolean mightContain(String item) {
        for (int index : getHashValues(item)) {
            if (!bitSet.get(index)) {
                return false;  // Definitely not in set
            }
        }
        return true;  // Might be in set
    }
}
```

---

## Use Cases

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Bloom Filter Use Cases                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. CACHE LOOKUPS                                                     │
│      ─────────────────                                                  │
│      Check if key might be in cache before expensive lookup            │
│      "Not in filter" → Skip cache check entirely                       │
│                                                                         │
│   2. DATABASE QUERIES                                                  │
│      ─────────────────                                                  │
│      Avoid disk reads for non-existent rows                           │
│      Used by: HBase, Cassandra, LevelDB                               │
│                                                                         │
│   3. USERNAME AVAILABILITY                                             │
│      ─────────────────────────                                          │
│      Quick check before database query                                 │
│      "Definitely available" → No DB query needed                       │
│                                                                         │
│   4. MALWARE/SPAM DETECTION                                           │
│      ──────────────────────────                                         │
│      Check URL against known malicious URLs                           │
│      Used by: Google Safe Browsing                                    │
│                                                                         │
│   5. DEDUPLICATION                                                     │
│      ──────────────                                                     │
│      Check if message/event already processed                         │
│      "Definitely not seen" → Process it                               │
│                                                                         │
│   6. RECOMMENDATION SYSTEMS                                           │
│      ────────────────────────                                           │
│      Track items user has already seen                                │
│      Don't recommend if "might have seen"                             │
│                                                                         │
│   7. NETWORK ROUTERS                                                  │
│      ────────────────────                                               │
│      Check packet against routing table                               │
│      Memory-constrained environment                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Variants

### Counting Bloom Filter

Supports deletion by using counters instead of bits.

```
Standard:  [0] [1] [1] [0] [1] [0]  (bits)
Counting:  [0] [2] [1] [0] [3] [0]  (counters)

Insert: increment counters
Delete: decrement counters

Trade-off: More space (4 bits per counter typical)
```

### Scalable Bloom Filter

Grows as elements are added to maintain false positive rate.

```
Start with small filter
When fill ratio exceeds threshold:
  Create new filter (larger)
  New inserts go to new filter
  Queries check all filters
```

### Cuckoo Filter

Alternative supporting deletion with better space efficiency.

```
Advantages over Bloom Filter:
• Supports deletion
• Better lookup performance
• Better space efficiency for low FP rates
```

---

## When to Use / When NOT to Use

### When to Use

✅ Need to check "definitely not in set"
✅ Can tolerate false positives
✅ Memory is constrained
✅ Set is very large
✅ Avoiding expensive operations (disk, network)

### When NOT to Use

❌ Need exact membership (no false positives)
❌ Need to delete elements (use Counting BF)
❌ Need to enumerate elements
❌ Set is small (just use HashSet)
❌ False positives are unacceptable

---

## Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "Can it have false negatives?" | Core understanding | No, only false positives |
| "How to delete from Bloom Filter?" | Variant knowledge | Standard can't; use Counting Bloom Filter |
| "How to size the filter?" | Math awareness | m = -n*ln(p)/(ln2)², or use libraries |
| "When would you NOT use it?" | Practical judgment | Small sets, need exact answers, need deletion |

---

**Next:** Continue to [09_rate_limiters.md](./09_rate_limiters.md) to learn about protecting your systems.
