# Communication Tips

> "The best system designers aren't just technical—they're excellent communicators."

Your communication skills can make or break a system design interview. Here's how to excel.

---

## Thinking Out Loud

### Why It Matters

```
┌────────────────────────────────────────────────────────────────┐
│                WHY THINK OUT LOUD?                              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SILENT THINKING:                                              │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ Candidate: *stares at whiteboard for 2 minutes*         │  │
│  │ Interviewer: "I have no idea what they're thinking"     │  │
│  │                                                          │  │
│  │ Result: Interviewer can't give credit for good thinking │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  THINKING OUT LOUD:                                            │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ Candidate: "I'm considering two approaches here.        │  │
│  │            Option A would be faster but uses more       │  │
│  │            memory. Option B is the opposite..."         │  │
│  │ Interviewer: "Great analytical thinking!"               │  │
│  │                                                          │  │
│  │ Result: Credit for problem-solving process              │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### How to Think Out Loud

**Use these phrases:**

```
EXPLORING OPTIONS:
- "Let me think about a few approaches here..."
- "I see two ways to solve this..."
- "My initial thought is X, but let me consider Y..."

MAKING DECISIONS:
- "I'm going to go with X because..."
- "The trade-off here is..."
- "Given our requirements, I think X makes more sense..."

ACKNOWLEDGING UNCERTAINTY:
- "I'm not 100% sure, but I believe..."
- "If I remember correctly..."
- "My intuition says X, but I'd want to verify..."

TRANSITIONING:
- "Now that we have the high-level design, let's dive into..."
- "Before I move on, does this make sense?"
- "I want to make sure I'm on the right track..."
```

### Practice Exercise

```
BAD (silent):
*draws database* *draws cache* *draws arrows*

GOOD (verbal):
"Let me draw out the architecture. Users will first hit
our load balancer here. The load balancer distributes
requests to our API servers. For read requests, we'll
first check our Redis cache—I'm putting that here—
because most reads will be for recently accessed data.
On a cache miss, we query our primary database here..."
```

---

## Structuring Your Explanations

### The "What, Why, How" Framework

```
┌────────────────────────────────────────────────────────────────┐
│                WHAT → WHY → HOW                                 │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  WHAT: State what you're going to do                           │
│  "I'm going to add a cache layer here."                        │
│                                                                 │
│  WHY: Explain the reasoning                                    │
│  "This is because we have a 100:1 read/write ratio,           │
│   and caching will reduce database load significantly."        │
│                                                                 │
│  HOW: Describe the implementation                              │
│  "I'll use Redis with an LRU eviction policy.                 │
│   We'll cache the most recent 1000 items per user,            │
│   with a 1-hour TTL."                                          │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### Example Application

```
POOR EXPLANATION:
"We need a message queue."
[draws box labeled "Kafka"]

STRONG EXPLANATION:
"WHAT: I'm adding a message queue between the API and
the notification service.

WHY: Two reasons. First, the notification service is slow
(sending emails can take seconds), and we don't want to
block the API response. Second, if the notification
service goes down, we don't want to lose messages.

HOW: I'll use Kafka because we need durability and can
handle the operational complexity. Messages will be
partitioned by user_id for ordering guarantees."
```

---

## Using the Whiteboard Effectively

### Layout Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    WHITEBOARD LAYOUT                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  REQUIREMENTS          │    MAIN DIAGRAM                  │  │
│  │  ──────────────────    │                                  │  │
│  │  Functional:           │    [Architecture Drawing]        │  │
│  │  • Feature A           │                                  │  │
│  │  • Feature B           │                                  │  │
│  │                        │                                  │  │
│  │  Non-Functional:       │                                  │  │
│  │  • 1M users            │                                  │  │
│  │  • 99.9% uptime        │                                  │  │
│  │                        │                                  │  │
│  ├────────────────────────┤                                  │  │
│  │  CAPACITY              │                                  │  │
│  │  ──────────────────    │                                  │  │
│  │  • 1000 QPS            │                                  │  │
│  │  • 10 TB storage       │                                  │  │
│  │                        │                                  │  │
│  ├────────────────────────┼──────────────────────────────────┤  │
│  │  PARKING LOT           │  APIS / DATA MODEL               │  │
│  │  ──────────────────    │  ──────────────────              │  │
│  │  • Security            │  POST /tweets                    │  │
│  │  • Monitoring          │  GET /timeline                   │  │
│  │  • Analytics           │  Users: id, name...              │  │
│  └────────────────────────┴──────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Drawing Tips

```
DO:
✓ Draw large enough to see from across the room
✓ Use boxes for components, arrows for data flow
✓ Label everything
✓ Use different colors if available
✓ Keep it organized (don't let it become messy)

DON'T:
✗ Draw tiny diagrams in one corner
✗ Leave boxes unlabeled
✗ Create spaghetti arrows
✗ Erase and redraw constantly
✗ Turn your back to interviewer for too long
```

### Component Symbols

```
STANDARD SYMBOLS:

┌─────────────┐
│   Service   │     Rectangle = Service/Server
└─────────────┘

   ┌─────┐
   │     │
  ─┴─────┴─           Cylinder = Database
  └───────┘

  ╱─────────╲
 ╱           ╲        Cloud = External Service/CDN
 ╲           ╱
  ╲─────────╱

      │
   ───┴───            Arrow = Data Flow (label with what flows)
      │
      ▼

  ┌─┬─┬─┬─┐
  │ │ │ │ │           Queue = Message Queue
  └─┴─┴─┴─┘
```

---

## Handling Questions and Feedback

### When Interviewer Asks a Question

```
SITUATION: Interviewer interrupts with a question

WRONG RESPONSE:
"Oh... um... I didn't think about that."
[Looks flustered]

RIGHT RESPONSE:
"Great question. Let me think about that."
[Pause briefly]
"I think the answer is X because Y.
Does that address your concern?"
```

### When Interviewer Gives a Hint

```
INTERVIEWER: "What about consistency in this design?"

WRONG RESPONSE:
"Oh yeah, consistency. So we'll make it consistent."

RIGHT RESPONSE:
"Good point—I should address the consistency model.
Given our requirements for high availability, I'd
opt for eventual consistency here. Users can tolerate
seeing slightly stale data for a few seconds.

For critical operations like payments, I'd use
synchronous replication to ensure strong consistency.

Does that align with what you were thinking?"
```

### When You Don't Know Something

```
HONEST APPROACHES:

1. "I'm not deeply familiar with that technology, but
   my understanding is [X]. Is that correct?"

2. "I haven't worked with that specific tool, but I
   know it's similar to [Y] which I have used."

3. "I don't know the exact answer, but here's how I
   would approach figuring it out: [reasoning]"

NEVER:
✗ Make up facts
✗ Pretend to know something you don't
✗ Get defensive
```

---

## Common Communication Mistakes

### Mistake 1: Monologuing

```
PROBLEM: Talking for 10 minutes without pause

FIX: Check in regularly

"I've covered the core architecture. Before I go into
the data model, does this approach make sense? Any
concerns so far?"
```

### Mistake 2: Being Too Quiet

```
PROBLEM: Only speaking when asked

FIX: Narrate your process

Instead of: *silently draws*
Do: "I'm adding a cache here because our read/write
    ratio suggests we'll benefit from caching..."
```

### Mistake 3: Defensive Responses

```
PROBLEM: Arguing when challenged

INTERVIEWER: "I'm not sure that will scale."

WRONG: "Yes it will. This is how everyone does it."

RIGHT: "That's a fair concern. Let me think about the
       scaling characteristics... You're right, at
       10x load we might hit [problem]. We could
       address this by [solution]."
```

### Mistake 4: Not Acknowledging Trade-offs

```
PROBLEM: Presenting solution as perfect

WRONG: "This design is optimal."

RIGHT: "This design optimizes for read latency. The
       trade-off is higher write complexity and
       eventual consistency. Given our requirements,
       I think that's the right trade-off."
```

---

## Confidence Without Arrogance

### The Right Balance

```
┌────────────────────────────────────────────────────────────────┐
│                 CONFIDENCE SPECTRUM                             │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  UNDER-CONFIDENT          CONFIDENT           ARROGANT         │
│  ───────────────────────────────────────────────────────────── │
│                                                                 │
│  "I guess maybe we       "I'd recommend       "Obviously the   │
│   could use a cache?      caching here        only solution    │
│   I'm not sure if         because of our      is to use        │
│   that's right..."        read patterns.      caching."        │
│                           The trade-off                        │
│                           is..."                               │
│                                                                 │
│           ✗                    ✓                   ✗           │
│                                                                 │
│  Shows uncertainty       Shows knowledge      Dismisses        │
│  in everything           AND humility         alternatives     │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### Confident Phrases

```
USE:
- "Based on the requirements, I recommend..."
- "In my experience, X works well for this because..."
- "The industry standard approach is X. We could also consider Y..."
- "I'm confident about X. For Y, I'd want to validate..."

AVOID:
- "I guess..." "Maybe..." "I'm not sure but..."
- "This is obviously..." "Everyone knows..."
- "That's wrong..." "That won't work..."
```

---

## Key Takeaways

```
┌────────────────────────────────────────────────────────────────┐
│               COMMUNICATION CHECKLIST                           │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  □ Think out loud throughout the interview                     │
│  □ Use "What, Why, How" for explanations                       │
│  □ Keep whiteboard organized and legible                       │
│  □ Check in with interviewer every 10-15 minutes              │
│  □ Welcome questions and feedback                              │
│  □ Acknowledge trade-offs proactively                          │
│  □ Be honest when you don't know something                     │
│  □ Stay confident but humble                                   │
│                                                                 │
│  REMEMBER: They're evaluating your communication               │
│            as much as your technical skills!                   │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

*Next: [Red Flags](04_red_flags.md) →*
