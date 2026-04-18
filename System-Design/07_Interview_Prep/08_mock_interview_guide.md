# Mock Interview Guide

How to practice effectively with mock interviews.

---

## Why Mock Interviews Matter

```
┌────────────────────────────────────────────────────────────────┐
│                SOLO STUDY vs MOCK INTERVIEW                     │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SOLO STUDY:                                                   │
│  - Think about the answer                                      │
│  - Read solutions                                              │
│  - Feel prepared                                               │
│                                                                 │
│  MOCK INTERVIEW:                                               │
│  - Explain answer out loud                                     │
│  - Handle real-time questions                                  │
│  - Manage time pressure                                        │
│  - Get feedback on communication                               │
│                                                                 │
│  The gap is HUGE. Mock interviews bridge it.                   │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Finding Practice Partners

### Option 1: Peer Practice
```
WHERE TO FIND:
- Colleagues preparing for interviews
- Online communities (Blind, Reddit, Discord)
- Study groups

SETUP:
- Take turns being interviewer/candidate
- 45 min interview + 15 min feedback
- Use question bank in this repo
```

### Option 2: Professional Services
```
PLATFORMS:
- Pramp (free peer matching)
- Interviewing.io (professional interviewers)
- Exponent (recorded practice)

PROS:
- Experienced interviewers
- Structured feedback
- More realistic

CONS:
- Can be expensive
- Limited availability
```

### Option 3: Solo Practice (Backup)
```
IF NO PARTNER AVAILABLE:
- Record yourself on video
- Explain out loud to camera
- Review recording critically
- Time yourself strictly

NOT AS GOOD AS REAL MOCK, but better than just reading
```

---

## For the Interviewer Role

### Pre-Interview Setup

```
1. CHOOSE A QUESTION
   - Match candidate's target level
   - Prepare your own solution (know the answer!)

2. SET THE SCENE
   - "Pretend this is a real interview"
   - "I'll be taking notes like a real interviewer"
   - "45 minutes, I'll keep time"

3. HAVE READY:
   - Timer
   - The question
   - Follow-up questions
   - Evaluation rubric
```

### During the Interview

```
FIRST 5 MINUTES:
- State the problem clearly
- Answer clarifying questions
- Don't give hints yet

MIDDLE 30 MINUTES:
- Let candidate drive
- Take notes on what they do well/poorly
- Redirect if going off track
- Ask probing questions when they pause

LAST 10 MINUTES:
- Ask about bottlenecks
- Ask "what would you improve?"
- Let them ask you questions
```

### Good Probing Questions

```
DURING REQUIREMENTS:
- "What about [edge case]?"
- "Do we need to support [feature]?"

DURING DESIGN:
- "Why did you choose [technology]?"
- "What happens if [component] fails?"
- "How does this scale to 10x users?"

DURING DEEP DIVE:
- "Walk me through what happens when..."
- "What's the trade-off here?"
- "What alternatives did you consider?"
```

### Evaluation Rubric

```
┌────────────────────────────────────────────────────────────────┐
│                  SCORING RUBRIC (1-5 scale)                     │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  REQUIREMENTS GATHERING           /5                           │
│  □ Asked clarifying questions                                  │
│  □ Identified functional requirements                          │
│  □ Identified non-functional requirements                      │
│  □ Prioritized features appropriately                          │
│                                                                 │
│  CAPACITY ESTIMATION              /5                           │
│  □ Made reasonable assumptions                                 │
│  □ Showed calculations                                         │
│  □ Used results to inform design                               │
│                                                                 │
│  HIGH-LEVEL DESIGN                /5                           │
│  □ Clear architecture diagram                                  │
│  □ Appropriate component choices                               │
│  □ Explained data flow                                         │
│  □ Addressed scalability                                       │
│                                                                 │
│  DETAILED DESIGN                  /5                           │
│  □ Deep dove into critical components                          │
│  □ Discussed trade-offs                                        │
│  □ Handled edge cases                                          │
│                                                                 │
│  COMMUNICATION                    /5                           │
│  □ Organized approach                                          │
│  □ Clear explanations                                          │
│  □ Responded well to feedback                                  │
│  □ Good use of whiteboard                                      │
│                                                                 │
│  OVERALL SCORE: ___/25                                         │
│                                                                 │
│  21-25: Strong hire                                            │
│  16-20: Hire with minor concerns                               │
│  11-15: Borderline                                             │
│  0-10:  No hire                                                │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## For the Candidate Role

### Before the Mock

```
1. Treat it like a real interview
   - Dress professionally (optional but helps mindset)
   - Clear your schedule
   - Have paper/whiteboard ready

2. Set up your environment
   - Quiet room
   - Good internet (if remote)
   - Water nearby

3. Mindset
   - This is practice, mistakes are learning
   - Focus on process, not just answer
```

### During the Mock

```
1. START STRONG
   - Greet warmly
   - Confirm you understand the problem
   - Ask clarifying questions

2. COMMUNICATE CONSTANTLY
   - Think out loud
   - Explain your reasoning
   - Check in with interviewer

3. MANAGE TIME
   - Wear a watch
   - Move on if stuck
   - Save time for wrap-up

4. HANDLE FEEDBACK
   - Don't get defensive
   - Thank for hints
   - Incorporate suggestions
```

### After the Mock

```
1. RECEIVE FEEDBACK GRACEFULLY
   - Listen fully before responding
   - Take notes
   - Ask clarifying questions

2. SELF-REFLECT
   - What went well?
   - What was difficult?
   - What would I do differently?

3. CREATE ACTION ITEMS
   - Specific things to improve
   - Topics to study more
   - Schedule next practice
```

---

## Feedback Template

### For Interviewer to Give

```
FEEDBACK STRUCTURE:

1. STRENGTHS (What went well):
   - [Specific example 1]
   - [Specific example 2]

2. AREAS TO IMPROVE:
   - [Specific example 1] - Suggestion: [how to improve]
   - [Specific example 2] - Suggestion: [how to improve]

3. OVERALL IMPRESSION:
   - Would this pass a real interview?
   - What's the #1 thing to work on?

EXAMPLE:

"STRENGTHS:
- Great clarifying questions at the start
- Clear explanation of the fan-out trade-offs

AREAS TO IMPROVE:
- Capacity estimation was rushed - take time to show your math
- Database choice wasn't justified - explain WHY you chose it

OVERALL:
This would likely be a borderline result. The #1 thing to focus
on is slowing down during estimation and showing your reasoning."
```

---

## Mock Interview Schedule

### Recommended Progression

```
WEEK 1: Foundation
- 2 mock interviews
- Focus: Requirements gathering, basic structure
- Questions: URL Shortener, Pastebin

WEEK 2: Building Skills
- 2 mock interviews
- Focus: Capacity estimation, architecture
- Questions: Twitter, Instagram

WEEK 3: Intermediate
- 2-3 mock interviews
- Focus: Deep dives, trade-offs
- Questions: Messenger, Dropbox

WEEK 4: Advanced
- 2-3 mock interviews
- Focus: Complete polish
- Questions: Uber, YouTube

WEEK 5+: Before Interview
- 1-2 final mocks
- Focus: Target company's style
- Get feedback from experienced interviewer if possible
```

---

## Common Issues and Fixes

| Issue | Fix |
|-------|-----|
| Running out of time | Practice with timer, skip details early |
| Not enough depth | Prepare 3 deep-dive topics per question |
| Poor communication | Record yourself, watch playback |
| Forgetting requirements | Write them down, refer back |
| Getting stuck | Practice "parking lot" technique |
| Defensive about feedback | Reframe as learning opportunity |

---

## Mock Interview Checklist

### Before
```
□ Question selected
□ Environment set up
□ Timer ready
□ Paper/whiteboard ready
□ Recording set up (optional)
```

### During
```
□ Introductions done
□ Problem stated clearly
□ Time being tracked
□ Notes being taken
□ Follow-up questions asked
```

### After
```
□ Detailed feedback given
□ Scores recorded
□ Action items identified
□ Next session scheduled
```

---

*Next: [Final Revision Sheet](09_final_revision.md) →*
