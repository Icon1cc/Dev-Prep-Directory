# Search Systems

## What is a Search System?

A **Search System** enables efficient retrieval of documents matching a query. Unlike database queries that match exact values, search systems handle fuzzy matching, ranking, and full-text search across large document collections.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Database Query vs Search                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Database Query:                  Search Query:                       │
│   ───────────────                  ─────────────                        │
│                                                                         │
│   SELECT * FROM products           "best laptop under $1000"           │
│   WHERE name = 'laptop'                                                │
│                                    Handles:                            │
│   Exact match only                 • Fuzzy matching ("labtop")        │
│                                    • Synonyms ("notebook")             │
│                                    • Ranking by relevance             │
│                                    • Typo tolerance                    │
│                                    • Natural language                  │
│                                                                         │
│   Use Database When:               Use Search When:                    │
│   • Exact lookups                  • Full-text search                 │
│   • Structured queries             • Relevance ranking               │
│   • ACID needed                    • Fuzzy matching                  │
│   • Joins required                 • Autocomplete                    │
│                                    • Faceted search                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Core Concepts

### Inverted Index

The fundamental data structure powering search engines.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Inverted Index                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Documents:                                                           │
│   ──────────                                                            │
│   Doc1: "The quick brown fox"                                          │
│   Doc2: "The quick rabbit"                                             │
│   Doc3: "Brown fox jumps"                                              │
│                                                                         │
│   Forward Index (how we store):                                        │
│   ─────────────────────────────                                         │
│   Doc1 → [the, quick, brown, fox]                                     │
│   Doc2 → [the, quick, rabbit]                                         │
│   Doc3 → [brown, fox, jumps]                                          │
│                                                                         │
│   Inverted Index (how we search):                                      │
│   ────────────────────────────────                                      │
│   "brown"  → [Doc1, Doc3]                                             │
│   "fox"    → [Doc1, Doc3]                                             │
│   "jumps"  → [Doc3]                                                   │
│   "quick"  → [Doc1, Doc2]                                             │
│   "rabbit" → [Doc2]                                                   │
│   "the"    → [Doc1, Doc2]                                             │
│                                                                         │
│   Search "brown fox":                                                  │
│   ───────────────────                                                   │
│   "brown" → [Doc1, Doc3]                                              │
│   "fox"   → [Doc1, Doc3]                                              │
│   Intersection → [Doc1, Doc3] ✓                                       │
│                                                                         │
│   With positions (for phrase search):                                  │
│   ─────────────────────────────────                                     │
│   "brown" → [Doc1:pos2, Doc3:pos0]                                    │
│   "fox"   → [Doc1:pos3, Doc3:pos1]                                    │
│   "brown fox" phrase → Doc1 (pos2,3), Doc3 (pos0,1) ✓                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Text Analysis Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Text Analysis Pipeline                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Input: "The Quick Brown Foxes are JUMPING!"                          │
│                       │                                                 │
│                       ▼                                                 │
│   ┌─────────────────────────────────────┐                              │
│   │ 1. CHARACTER FILTERS                │                              │
│   │    Remove HTML, convert encoding    │                              │
│   └─────────────────────────────────────┘                              │
│                       │                                                 │
│                       ▼                                                 │
│   "The Quick Brown Foxes are JUMPING"                                  │
│                       │                                                 │
│                       ▼                                                 │
│   ┌─────────────────────────────────────┐                              │
│   │ 2. TOKENIZER                        │                              │
│   │    Split into tokens                │                              │
│   └─────────────────────────────────────┘                              │
│                       │                                                 │
│                       ▼                                                 │
│   ["The", "Quick", "Brown", "Foxes", "are", "JUMPING"]                │
│                       │                                                 │
│                       ▼                                                 │
│   ┌─────────────────────────────────────┐                              │
│   │ 3. TOKEN FILTERS                    │                              │
│   │    Lowercase, stemming, stopwords   │                              │
│   └─────────────────────────────────────┘                              │
│                       │                                                 │
│                       ▼                                                 │
│   ["quick", "brown", "fox", "jump"]                                   │
│                                                                         │
│   Common Token Filters:                                                │
│   ─────────────────────                                                 │
│   • Lowercase: "QUICK" → "quick"                                      │
│   • Stemming: "jumping" → "jump", "foxes" → "fox"                    │
│   • Stop words: Remove "the", "are", "is"                             │
│   • Synonyms: "quick" → "quick", "fast", "rapid"                     │
│   • N-grams: "quick" → "qu", "ui", "ic", "ck"                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Relevance Scoring

### TF-IDF (Term Frequency - Inverse Document Frequency)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TF-IDF Scoring                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   TF (Term Frequency):                                                 │
│   ────────────────────                                                  │
│   How often term appears in document                                   │
│   TF = count(term in doc) / total_terms_in_doc                        │
│                                                                         │
│   IDF (Inverse Document Frequency):                                    │
│   ──────────────────────────────────                                    │
│   How rare is the term across all documents                           │
│   IDF = log(total_docs / docs_containing_term)                        │
│                                                                         │
│   TF-IDF = TF × IDF                                                   │
│                                                                         │
│   Example:                                                             │
│   ────────                                                              │
│   Query: "machine learning"                                           │
│   Total docs: 1,000,000                                               │
│                                                                         │
│   "the" appears in 900,000 docs                                       │
│   IDF(the) = log(1M/900K) = 0.05 (very common = low weight)          │
│                                                                         │
│   "learning" appears in 10,000 docs                                   │
│   IDF(learning) = log(1M/10K) = 2.0 (rarer = higher weight)          │
│                                                                         │
│   "machine" appears 5 times in doc (total 100 words)                  │
│   TF(machine) = 5/100 = 0.05                                          │
│                                                                         │
│   Score: TF × IDF for each term, sum them up                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### BM25 (Modern Standard)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BM25 Scoring                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   BM25 = TF-IDF improved with:                                        │
│   • Document length normalization                                      │
│   • Term frequency saturation                                          │
│                                                                         │
│   TF saturation:                                                       │
│   ───────────────                                                       │
│   "machine" appears 5 times → score = X                               │
│   "machine" appears 50 times → score ≈ X (diminishing returns)        │
│                                                                         │
│   Document length:                                                     │
│   ────────────────                                                      │
│   Short doc with 3 matches > Long doc with 3 matches                  │
│   (term density matters)                                               │
│                                                                         │
│   Used by: Elasticsearch, Solr, Lucene                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Search Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Elasticsearch Architecture                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                          ┌─────────────┐                               │
│                          │   Client    │                               │
│                          └──────┬──────┘                               │
│                                 │                                       │
│                                 ▼                                       │
│                    ┌─────────────────────────┐                         │
│                    │    Coordinator Node     │                         │
│                    │  (routes & aggregates)  │                         │
│                    └───────────┬─────────────┘                         │
│                                │                                       │
│              ┌─────────────────┼─────────────────┐                    │
│              ▼                 ▼                 ▼                    │
│        ┌──────────┐      ┌──────────┐      ┌──────────┐              │
│        │  Data    │      │  Data    │      │  Data    │              │
│        │  Node 1  │      │  Node 2  │      │  Node 3  │              │
│        └──────────┘      └──────────┘      └──────────┘              │
│                                                                         │
│   Index: "products"                                                    │
│   ┌─────────────────────────────────────────────────────┐             │
│   │ Shard 0 (Primary) │ Shard 1 (Primary) │ Shard 2    │             │
│   │    Node 1         │    Node 2         │  Node 3    │             │
│   ├───────────────────┼───────────────────┼────────────┤             │
│   │ Shard 0 (Replica) │ Shard 1 (Replica) │ Shard 2 R  │             │
│   │    Node 2         │    Node 3         │  Node 1    │             │
│   └─────────────────────────────────────────────────────┘             │
│                                                                         │
│   Index = Collection of documents                                      │
│   Shard = Partition of index (holds subset of data)                   │
│   Replica = Copy of shard for availability                            │
│                                                                         │
│   Search Flow:                                                         │
│   ────────────                                                          │
│   1. Coordinator receives query                                        │
│   2. Forwards to all shards (scatter)                                 │
│   3. Each shard returns top N results                                 │
│   4. Coordinator merges and re-ranks (gather)                         │
│   5. Returns final top N to client                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Common Search Features

### 1. Autocomplete / Typeahead

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Autocomplete Implementation                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   User types: "mac"                                                    │
│   Suggestions: ["macbook", "machine learning", "mac and cheese"]       │
│                                                                         │
│   Techniques:                                                          │
│   ───────────                                                           │
│                                                                         │
│   1. PREFIX MATCHING                                                   │
│      Index: "macbook" → ["m", "ma", "mac", "macb", "macbo", ...]     │
│      Query: Find all starting with "mac"                              │
│                                                                         │
│   2. N-GRAM TOKENIZATION                                               │
│      "macbook" → ["mac", "acb", "cbo", "boo", "ook"]                 │
│      Enables partial matching anywhere in word                        │
│                                                                         │
│   3. EDGE N-GRAMS (prefix only)                                       │
│      "macbook" → ["m", "ma", "mac", "macb", "macbo", "macboo"]       │
│      More efficient for autocomplete                                  │
│                                                                         │
│   Ranking suggestions:                                                 │
│   ────────────────────                                                  │
│   • Popularity (search frequency)                                      │
│   • Recency                                                            │
│   • User history                                                       │
│   • Exact prefix match first                                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2. Faceted Search

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Faceted Search                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Search: "laptop"                                                     │
│                                                                         │
│   Results: 1,234 laptops                                              │
│                                                                         │
│   Facets:                           Filter:                            │
│   ────────                          ───────                            │
│   Brand:                            [x] Apple                          │
│   ├── Apple (450)                   [x] Dell                          │
│   ├── Dell (320)                                                      │
│   ├── HP (280)                      Price:                            │
│   └── Lenovo (184)                  $500 - $1000                      │
│                                                                         │
│   Price:                            Refined Results: 89 laptops       │
│   ├── Under $500 (123)                                                │
│   ├── $500-$1000 (456)                                                │
│   └── Over $1000 (655)                                                │
│                                                                         │
│   Implementation:                                                      │
│   ───────────────                                                       │
│   {                                                                    │
│     "query": { "match": { "title": "laptop" }},                       │
│     "aggs": {                                                          │
│       "brands": { "terms": { "field": "brand" }},                     │
│       "price_ranges": {                                                │
│         "range": {                                                     │
│           "field": "price",                                           │
│           "ranges": [                                                  │
│             { "to": 500 },                                            │
│             { "from": 500, "to": 1000 },                              │
│             { "from": 1000 }                                          │
│           ]                                                            │
│         }                                                              │
│       }                                                                │
│     }                                                                  │
│   }                                                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3. Fuzzy Search

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Fuzzy Matching                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   User types: "iphne" (typo)                                          │
│   Should match: "iphone"                                               │
│                                                                         │
│   Levenshtein Distance:                                                │
│   ─────────────────────                                                 │
│   Minimum edits (insert, delete, substitute) to transform             │
│                                                                         │
│   "iphne" → "iphone"                                                  │
│   1. Insert 'o': "iphone" (1 edit)                                    │
│   Distance = 1                                                         │
│                                                                         │
│   Fuzziness settings:                                                  │
│   ───────────────────                                                   │
│   • AUTO: 0-2 chars = exact, 3-5 = 1 edit, >5 = 2 edits              │
│   • fuzziness: 1 = allow 1 edit                                       │
│   • fuzziness: 2 = allow 2 edits                                      │
│                                                                         │
│   Query:                                                               │
│   {                                                                    │
│     "match": {                                                         │
│       "title": {                                                       │
│         "query": "iphne",                                             │
│         "fuzziness": "AUTO"                                           │
│       }                                                                │
│     }                                                                  │
│   }                                                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Popular Search Systems

| System | Type | Best For |
|--------|------|----------|
| Elasticsearch | Distributed | General purpose, analytics |
| Apache Solr | Distributed | Enterprise search |
| Algolia | SaaS | Fast setup, great UX |
| Meilisearch | Single node | Simple, typo-tolerant |
| Typesense | Distributed | Open source Algolia alternative |

---

## When to Use / When NOT to Use

### When to Use Search Engine

✅ Full-text search required
✅ Relevance ranking needed
✅ Typo tolerance important
✅ Autocomplete feature
✅ Faceted navigation
✅ Complex text queries

### When NOT to Use

❌ Exact lookups only (use database)
❌ ACID transactions required
❌ Primary data store (use as secondary)
❌ Simple CRUD operations
❌ Joins across documents

---

## Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "Why not just use DB LIKE?" | Understanding search | LIKE doesn't rank, scale, or handle typos |
| "Search engine as primary DB?" | Architecture judgment | No—use as secondary; sync from primary DB |
| "How to keep search in sync?" | System design | CDC, message queue, or periodic reindex |
| "Elasticsearch vs Solr?" | Technology awareness | Both Lucene-based; ES easier to scale, better DX |

---

**Next:** Continue to [08_bloom_filters.md](./08_bloom_filters.md) to learn about probabilistic data structures.
