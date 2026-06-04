---
name: user-stories
description: >-
  Break a PRD, epic, or feature idea into well-formed user stories — "As a
  <persona>, I want <goal>, so that <benefit>" — each with clear, testable
  acceptance criteria (Gherkin given/when/then). Uses real personas when a
  personas skill is available, sizes stories to be independently shippable, and
  orders them. Output feeds /scope. Use when the user has a PRD/epic to slice or
  asks for user stories. Triggers: "user stories", "break into stories", "write
  stories for this", "slice this epic", "story map".
---

# user-stories — slice product intent into shippable, testable stories

Turn a PRD/epic/feature into a set of user stories that a team could pick up.
Good stories are **INVEST**: Independent, Negotiable, Valuable, Estimable, Small,
Testable. Each delivers user-visible value and has acceptance criteria you could
hand to QA.

## Process

### 1. Source the intent
- If a `PRD.md` exists (e.g. in `.plan/<feature-slug>/`), read it.
- Otherwise take the epic/feature from the user, and explore the codebase or ask
  enough to slice responsibly.
- Load a personas skill (e.g. `enernet-personas`) if available so stories name
  real personas, not "the user" generically.

### 2. Build a story map
Lay out the user's journey as a backbone (the big steps), then slice stories
under each step. This keeps the set coherent and surfaces gaps. Prefer **vertical
slices** (thin end-to-end value) over horizontal layers (all the backend, then
all the frontend).

### 3. Write each story
Save to `<project>/.plan/<feature-slug>/user-stories.md` (or where the user
prefers). For each:

```markdown
## US-<n>: <short title>

**As a** <persona>
**I want** <goal/capability>
**So that** <benefit/why>

**Priority:** P0 | P1 | P2
**Depends on:** <other story IDs, or —>

### Acceptance Criteria
- [ ] **Given** <context> **when** <action> **then** <expected outcome>
- [ ] …

### Notes
<edge cases, out-of-scope, open questions for grilling later>
```

### 4. Quality bar
- Every story is independently demoable (vertical slice), not "build the schema."
- Acceptance criteria are testable and unambiguous (no "works well").
- Personas are real and specific.
- The set covers the PRD's P0 goals — flag any goal with no story.
- Stories are ordered with dependencies explicit.

### 5. Hand off
Summarize the story set (count, P0s, ordering). Suggest:
"Run `/scope` to turn these into eng tickets and start the build pipeline."
