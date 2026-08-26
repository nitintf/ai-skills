---
name: user-stories
description: Slice a PRD or epic into INVEST user stories with Gherkin acceptance criteria, sized to ship independently and ordered by dependency.
disable-model-invocation: true
---

# user-stories: slice product intent into shippable, testable stories

Turn a PRD/epic/feature into a set of user stories that a team could pick up.
Good stories are **INVEST**: Independent, Negotiable, Valuable, Estimable, Small,
Testable. Each delivers user-visible value and has acceptance criteria you could
hand to QA.

## Process

### 1. Source the intent
- If a `PRD.md` exists (e.g. in `.plan/<feature-slug>/`), read it.
- Otherwise take the epic/feature from the user, and explore the codebase or ask
  enough to slice responsibly.
- Load a personas skill if one is installed (check the available skills for a
  `*-personas` skill) so stories name real personas, not "the user" generically.
  If there isn't one, ask who the actual users are rather than inventing them.

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
**Depends on:** <other story IDs, or none>

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
- The set covers the PRD's P0 goals, flag any goal with no story.
- Stories are ordered with dependencies explicit.

### 5. Hand off
Summarize the story set (count, P0s, ordering). Suggest:
"Run `/scope` to turn these into eng tickets and start the build pipeline."
