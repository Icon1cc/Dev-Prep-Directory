# Time Management Strategies

Different companies use different interview lengths. Here's how to adapt your approach.

## Interview Length Comparison

```
┌─────────────────────────────────────────────────────────────────────┐
│                    INTERVIEW LENGTHS BY COMPANY                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  30 minutes: Screening rounds, some startups                       │
│  45 minutes: Most common (Google, Meta, Amazon)                    │
│  60 minutes: Senior roles, some companies (Netflix, Uber)          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 30-Minute Interview Strategy

### Time Allocation

```
┌──────────────────────────────────────────────────────────────┐
│                 30-MINUTE BREAKDOWN                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  0:00-3:00   │ Requirements (3 min)                         │
│              │ - 2-3 clarifying questions MAX               │
│              │ - Quick scope definition                     │
│              │                                              │
│  3:00-5:00   │ Capacity Estimation (2 min)                  │
│              │ - Only key numbers                           │
│              │ - Skip if interviewer suggests               │
│              │                                              │
│  5:00-20:00  │ High-Level Design (15 min)                   │
│              │ - Quick API mention                          │
│              │ - Focus on architecture diagram              │
│              │ - Cover main data flow                       │
│              │                                              │
│  20:00-28:00 │ One Deep Dive (8 min)                        │
│              │ - Pick most critical component               │
│              │ - OR follow interviewer's lead               │
│              │                                              │
│  28:00-30:00 │ Quick Wrap-up (2 min)                        │
│              │ - 30-second summary                          │
│              │ - One bottleneck mention                     │
│              │                                              │
└──────────────────────────────────────────────────────────────┘
```

### 30-Minute Tips

```
DO:
✓ Be concise - every minute counts
✓ Skip detailed capacity math if short on time
✓ Focus on breadth over depth
✓ Draw diagram while talking (saves time)

DON'T:
✗ Spend more than 3 min on requirements
✗ Deep dive into multiple components
✗ Get stuck on one aspect
✗ Forget to show the complete picture
```

### Example 30-Min Pacing (URL Shortener)

```
0:00  "Design a URL shortener like bit.ly"
0:30  "Quick questions: Scale? Custom URLs? Analytics?"
2:00  "So we need: shorten, redirect, maybe analytics"
3:00  "Quick math: 100M URLs/month, 100:1 read:write..."
5:00  [Start drawing] "Here's the architecture..."
15:00 "For the short code generation, I'd use..."
25:00 "Main bottleneck is the redirect latency..."
28:00 "To summarize: API → Cache → DB, base62 encoding"
```

---

## 45-Minute Interview Strategy

### Time Allocation

```
┌──────────────────────────────────────────────────────────────┐
│                 45-MINUTE BREAKDOWN                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  0:00-5:00   │ Requirements (5 min)                         │
│              │ - 4-5 clarifying questions                   │
│              │ - Functional requirements                    │
│              │ - Non-functional requirements                │
│              │                                              │
│  5:00-10:00  │ Capacity Estimation (5 min)                  │
│              │ - Traffic (QPS)                              │
│              │ - Storage                                    │
│              │ - Bandwidth                                  │
│              │                                              │
│  10:00-25:00 │ High-Level Design (15 min)                   │
│              │ - API design                                 │
│              │ - Data model                                 │
│              │ - Architecture diagram                       │
│              │ - Explain data flow                          │
│              │                                              │
│  25:00-40:00 │ Deep Dive (15 min)                           │
│              │ - 1-2 components in detail                   │
│              │ - Trade-off discussions                      │
│              │ - Edge cases                                 │
│              │                                              │
│  40:00-45:00 │ Wrap-up (5 min)                              │
│              │ - Summarize design                           │
│              │ - Bottlenecks                                │
│              │ - Future improvements                        │
│              │                                              │
└──────────────────────────────────────────────────────────────┘
```

### 45-Minute Tips

```
DO:
✓ Balance breadth and depth
✓ Complete capacity estimation
✓ Cover all major components
✓ Have time for meaningful deep dive
✓ Discuss trade-offs throughout

DON'T:
✗ Rush through requirements
✗ Skip capacity estimation
✗ Spend too long on one area
✗ Forget wrap-up
```

---

## 60-Minute Interview Strategy

### Time Allocation

```
┌──────────────────────────────────────────────────────────────┐
│                 60-MINUTE BREAKDOWN                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  0:00-7:00   │ Requirements (7 min)                         │
│              │ - Thorough clarifying questions              │
│              │ - Detailed functional requirements           │
│              │ - Clear non-functional requirements          │
│              │ - Prioritize features                        │
│              │                                              │
│  7:00-15:00  │ Capacity Estimation (8 min)                  │
│              │ - Detailed calculations                      │
│              │ - Traffic patterns                           │
│              │ - Storage growth projections                 │
│              │ - Peak vs average load                       │
│              │                                              │
│  15:00-35:00 │ High-Level Design (20 min)                   │
│              │ - Complete API design                        │
│              │ - Detailed data model                        │
│              │ - Full architecture diagram                  │
│              │ - All major data flows                       │
│              │ - Technology choices justified               │
│              │                                              │
│  35:00-55:00 │ Deep Dive (20 min)                           │
│              │ - 2-3 components in detail                   │
│              │ - Thorough trade-off analysis                │
│              │ - Edge cases and failure modes               │
│              │ - Scaling strategies                         │
│              │                                              │
│  55:00-60:00 │ Wrap-up (5 min)                              │
│              │ - Complete summary                           │
│              │ - Multiple bottlenecks                       │
│              │ - Detailed improvements roadmap              │
│              │                                              │
└──────────────────────────────────────────────────────────────┘
```

### 60-Minute Tips

```
DO:
✓ Take time for thorough requirements
✓ Show detailed calculations
✓ Cover multiple deep dive areas
✓ Discuss failure scenarios
✓ Show senior-level thinking

DON'T:
✗ Still rush (60 min goes fast!)
✗ Go too deep too early
✗ Ignore interviewer cues
✗ Forget the big picture
```

---

## Time Management Techniques

### The "Check-In" Technique

```
Every 10-15 minutes, briefly check:

"I've covered [X, Y, Z]. Should I continue with [next topic]
or would you like me to dive deeper into something?"

Benefits:
- Shows awareness of time
- Gets interviewer feedback
- Prevents going off track
```

### The "Parking Lot" Technique

```
When you think of something but it's not the right time:

"That's a great point about [X]. Let me note that and
come back to it after I finish the high-level design."

[Write it in corner of whiteboard]

Benefits:
- Shows you're thinking ahead
- Keeps you on track
- Don't lose good ideas
```

### The "Time Box" Technique

```
Mentally allocate time and stick to it:

"I'm going to spend 5 minutes on capacity estimation,
then move to the architecture."

[After 5 minutes]

"I have the key numbers. Let me move on to keep us on track."

Benefits:
- Prevents rabbit holes
- Ensures complete coverage
- Shows time awareness
```

---

## Recovery Strategies

### If You're Running Behind

```
SITUATION: 20 minutes in, still on requirements

RECOVERY:
1. "Let me move forward with what we have"
2. Skip detailed capacity math
3. Focus on architecture breadth
4. Accept less deep dive time

SAY:
"I want to make sure we cover the full design.
Let me sketch the architecture and we can dive
deeper into specific areas."
```

### If You're Running Ahead

```
SITUATION: 25 minutes in, design feels complete

RECOVERY:
1. Don't artificially slow down
2. Go deeper on critical components
3. Discuss more trade-offs
4. Cover failure scenarios
5. Mention monitoring/observability

SAY:
"I've covered the main design. Should I dive deeper
into [specific component] or discuss failure scenarios?"
```

### If You Get Stuck

```
SITUATION: Don't know how to proceed

RECOVERY:
1. Acknowledge it briefly
2. State what you do know
3. Propose an approach
4. Ask for guidance

SAY:
"I'm not entirely sure about [X]. My instinct is [Y]
because [reason]. Does that seem reasonable, or should
I consider a different approach?"
```

---

## Quick Reference Card

```
┌────────────────────────────────────────────────────────────────┐
│                TIME ALLOCATION CHEAT SHEET                      │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase            │ 30 min │ 45 min │ 60 min                  │
│  ─────────────────┼────────┼────────┼────────                  │
│  Requirements     │ 3 min  │ 5 min  │ 7 min                   │
│  Estimation       │ 2 min  │ 5 min  │ 8 min                   │
│  High-Level       │ 15 min │ 15 min │ 20 min                  │
│  Deep Dive        │ 8 min  │ 15 min │ 20 min                  │
│  Wrap-up          │ 2 min  │ 5 min  │ 5 min                   │
│                                                                 │
│  KEY RULE: Breadth first, then depth                           │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

*Next: [Communication Tips](03_communication_tips.md) →*
