# Doc Schema: the contract every `eng` skill obeys

This is the keystone of the `eng` plugin. The pipeline skills do not talk to each
other directly, they communicate **through documents on disk**. One skill
writes a section, the next reads it. That only works if every skill agrees on
the exact file layout, section headings, and frontmatter fields defined here.

**Rule for skill authors:** read the section headings and frontmatter keys below
verbatim. Do not invent, rename, or reorder them. If a skill needs a new field,
it gets added *here first*, then in the skills.

---

## 1. Where docs live

Always in the **current working project** (the repo the user is running in),
never in the plugin repo. The path is:

```
<project-root>/.plan/
  _conventions.md                 # project-wide house style cache (see §5)
  _research/
    <question-slug>.md            # durable answers written by `understand`
  _decisions/
    <NNNN>-<decision-slug>.md     # ADRs written by `adr`
  <feature-slug>/
    README.md                     # feature-level index + state (the entry point)
    PRD.md                        # optional, written by product's `prd`
    user-stories.md               # optional, written by product's `user-stories`
    <NN>-<ticket-slug>/
      doc.md                      # one self-contained doc per ticket
```

- `<feature-slug>`, kebab-case, derived from the task (e.g. `jira-assets-csv`).
- `<NN>`, zero-padded order prefix (`01`, `02`, …). Encodes dependency order.
- **Always a folder per ticket, even when there is only one ticket.** Uniform
  layout means no skill ever has to branch on "is this a file or a folder?".
- One `doc.md` per ticket. Never split into `prd.md` / `tests.md` / etc.:
  the pipeline skills run sequentially, so extra files only add handoff seams
  that break.
- The `_`-prefixed entries are **project-scoped, not feature-scoped**. The
  underscore sorts them away from feature folders and marks them as shared.
- `PRD.md` and `user-stories.md` are written by the separate `product` plugin.
  They are **inputs** to `scope`, not part of the pipeline's own schema: `scope`
  reads them if present and never rewrites them.

`.plan/` is committed to git (the whole point of "plan said X, reality was Y"
is lost if the plan isn't in history).

---

## 2. `README.md` (feature level): written by `scope`, status owned by `execute`/`ship`

```markdown
---
feature: <feature-slug>
created: <YYYY-MM-DD>
track: full              # full | express: see §5
phase: scoped            # see lifecycle below. this is the FEATURE's furthest phase
sources: []              # e.g. ["PRD.md", "user-stories.md"] if scope read them
---

# <Feature title>

## Original Task
<verbatim paste of what the user asked for>

## Breakdown Decision
<1 ticket or N? Why. If N, why these boundaries and not others.
If a track was chosen, say why (see §5).>

## Tickets
| #  | Ticket            | Phase     | Needs Jira | Depends on | Branch |
|----|-------------------|-----------|------------|------------|--------|
| 01 | csv-parser        | scoped    | yes        |,          |,      |
| 02 | entity-matcher    | scoped    | yes        | 01         |,      |
```

`execute` updates the `Phase` and `Branch` columns as work progresses; `ship`
sets the final `shipped` phase.

---

## 3. `doc.md` (per ticket): the canonical template

Every ticket doc has exactly these sections, in this order. A skill that owns a
section fills it; sections it doesn't own yet stay as the placeholder line.

```markdown
---
ticket: <NN>-<ticket-slug>
title: <human title>
track: full              # full | express: inherited from the feature, overridable
phase: scoped            # scoped → grilled → reviewed → tested → implemented → shipped
needs-jira: true         # false if this work doesn't warrant a ticket
depends-on: []           # list of <NN> prefixes, e.g. ["01"]
branch: null             # set by execute when work starts
pr: null                 # set by ship, PR URL or number
---

# <Ticket title>

## Problem / Context
<why this exists, the user-facing or system need>

## Scope
**In:** <what this ticket covers>
**Out:** <explicitly not covered, prevents creep>

## Codebase Touchpoints
<real file:line references the work will read or change. A map, not a vibe.>
- `path/to/file.ts:42`, <what's there / what changes>

## Conventions & Patterns
<how THIS repo already does the things this ticket needs, with file refs, so the
implementation matches house style instead of generic boilerplate.

Source this from `.plan/_conventions.md` when it exists (see §5): copy in only
the entries relevant to THIS ticket plus anything ticket-specific you found.
Don't restate the whole cache; link to it: "see `.plan/_conventions.md`".>

## Open Questions
<written by `scope`. Each is a real ambiguity the downstream skills must resolve.
`grill` reads these first. Use a checkbox list; resolved ones move to Decisions.>
- [ ] <question>

## Decisions
<written by `grill` (and anyone who resolves a question). The answer, plus who
decided / why. This is the resolved counterpart to Open Questions.

If a decision is architecturally significant and outlives this ticket, also write
an ADR (`/adr`) under `.plan/_decisions/` and link it from here.>
- <decision + rationale>

## Acceptance Criteria
<the CONTRACT. Checkable given/when/then statements. `execute` verifies against
these and checks them off. This is the most important section in the doc.>
- [ ] <criterion>

## Test Plan
### Unit Tests
<specified by `tdd`, what to test, edge cases. `execute` writes & runs them.>
### Manual / UI QA
<a checklist a human runs after implementation: clicks, flows, edge inputs.>
- [ ] <step + expected result>

## Eng Review Verdict
<written by `eng-review`. Dimension scores, what would make each a 10, and the
changes folded back into the sections above.>

## Jira Ticket
<OUTPUT ONLY, text to copy-paste into Jira. The plugin never calls the Jira API.>
### Title
<one line>
### Description
<formatted description: context, scope, acceptance criteria, out-of-scope>

## Work Log
<append-only. `execute` writes what was implemented, deviations from plan (plan
said X, reality was Y), test results, QA outcomes. `pr-review` and `review`
append a dated entry for any finding that contradicts the plan: that feedback
is the whole reason `.plan/` is committed. `ship` appends the PR link.>
```

---

## 4. Phase lifecycle

Both `README.md` and each `doc.md` carry a `phase`. Skills advance it; the
orchestrator reads it to decide what runs next. The doc holds the state, the
orchestrator stays stateless.

| phase         | set by      | meaning                                              |
|---------------|-------------|------------------------------------------------------|
| `scoped`      | scope       | doc exists, touchpoints + open questions written     |
| `grilled`     | grill       | questions resolved into Decisions, scope sharpened   |
| `reviewed`    | eng-review  | plan pressure-tested, verdict written, fixes folded  |
| `tested`      | tdd         | unit test spec + manual QA checklist written         |
| `implemented` | execute     | code written, tests pass, QA done, acceptance met    |
| `shipped`     | ship        | committed, pushed, PR opened and linked in the doc   |

A feature's `README.md` phase reflects its **least-advanced** ticket (i.e. the
feature isn't `reviewed` until every ticket is at least `reviewed`).

---

## 5. Tracks: full vs express

Not every ticket deserves five planning passes. The `track` field says which
path this work takes, and `eng-flow` reads it to decide what to run.

| track     | phases run                                        | when                                             |
|-----------|---------------------------------------------------|--------------------------------------------------|
| `full`    | scope → grill → eng-review → tdd → execute → ship | real features, anything with genuine ambiguity, anything touching data/auth/money |
| `express` | scope → tdd → execute → ship                      | small, well-understood changes: a bug fix, a copy change, a contained addition with no open questions |

Rules:

- **`scope` proposes the track and the user confirms it**: same interactive
  moment as the ticket breakdown. Never pick `express` silently.
- On `express`, the `grilled` and `reviewed` phases are **skipped, not faked**.
  The doc keeps `track: express` so it's honest about what wasn't done, and the
  phase jumps `scoped` → `tested`.
- **Express is not available** when `## Open Questions` is non-empty. Unresolved
  ambiguity is exactly what `grill` exists for: if there are open questions, the
  ticket is `full` by definition.
- Any skill can be run manually on an express ticket. `/grill` on an express doc
  upgrades it to `full`; that's a legitimate mid-flight escalation, not an error.

---

## 6. `_conventions.md`: the shared house-style cache

Eight skills need to know "how does this repo already do things". Re-deriving
that on every invocation is wasted exploration *and* produces inconsistent
answers between skills. So it's derived once and cached.

```
<project-root>/.plan/_conventions.md
```

- **Written by `/conventions`.** Its format and the checklist of what belongs in
  it live in `CONVENTIONS.md`, next to this file.
- **Read by** `scope`, `grill`, `eng-review`, `tdd`, `execute`, `ship`,
  `pr-walkthrough`, `pr-review`, `review`, `refactor`, `backfill-tests`,
  `debug`, `understand`.
- **Every consuming skill follows the same protocol:**
  1. Read `.plan/_conventions.md` if it exists.
  2. Check its `generated` date and `commit` frontmatter against `git log -1`.
     If the repo has moved substantially since, say so and offer to refresh,
     don't silently trust a stale cache.
  3. Explore the codebase **only for the gaps**: patterns the cache doesn't
     cover, or the specific files this task touches.
  4. If you discover a convention the cache is missing, append it there so the
     next skill gets it for free.
- **If the cache doesn't exist**, fall back to exploring as before, and suggest
  `/conventions` once so the next run is cheaper. Never block on it.

---

## 7. Conventions for skill authors

- **Read before write.** Always read the existing `doc.md` / `README.md` before
  editing so you preserve sections you don't own.
- **Never silently decide the breakdown or the track.** `scope` must ask the
  user (need a ticket at all? / 1 or N? / full or express?) interactively.
- **Resolve, don't duplicate.** When `grill` answers an Open Question, move it to
  Decisions and remove it from Open Questions, don't leave both.
- **Acceptance Criteria is the contract.** Spend effort making it sharp; every
  later skill keys off it.
- **Close the loop.** If you learn something during review or implementation that
  contradicts the plan, write it into `## Work Log`. A plan doc that only records
  intentions and never outcomes is half a doc.
- **End by suggesting the next skill** (e.g. scope → "run `/grill` next"). This
  gives the pipeline feel without hard-coupling the skills.
- The current phase **and track** determine the next skill (see §5).
