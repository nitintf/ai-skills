# Doc Schema — the contract every `eng` skill obeys

This is the keystone of the `eng` plugin. The five skills do not talk to each
other directly — they communicate **through documents on disk**. One skill
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
<project-root>/.plan/<feature-slug>/
  README.md                       # feature-level index + state (the entry point)
  <NN>-<ticket-slug>/
    doc.md                        # one self-contained doc per ticket
```

- `<feature-slug>` — kebab-case, derived from the task (e.g. `jira-assets-csv`).
- `<NN>` — zero-padded order prefix (`01`, `02`, …). Encodes dependency order.
- **Always a folder per ticket, even when there is only one ticket.** Uniform
  layout means no skill ever has to branch on "is this a file or a folder?".
- One `doc.md` per ticket. Never split into `prd.md` / `tests.md` / etc. —
  the skills run sequentially, so extra files only add handoff seams that break.

`.plan/` is committed to git (the whole point of "plan said X, reality was Y"
is lost if the plan isn't in history).

---

## 2. `README.md` (feature level) — written by `scope`, status owned by `execute`

```markdown
---
feature: <feature-slug>
created: <YYYY-MM-DD>
phase: scoped            # see lifecycle below — this is the FEATURE's furthest phase
---

# <Feature title>

## Original Task
<verbatim paste of what the user asked for>

## Breakdown Decision
<1 ticket or N? Why. If N, why these boundaries and not others.>

## Tickets
| #  | Ticket            | Phase     | Needs Jira | Depends on | Branch |
|----|-------------------|-----------|------------|------------|--------|
| 01 | csv-parser        | scoped    | yes        | —          | —      |
| 02 | entity-matcher    | scoped    | yes        | 01         | —      |
```

`execute` updates the `Phase` and `Branch` columns as work progresses.

---

## 3. `doc.md` (per ticket) — the canonical template

Every ticket doc has exactly these sections, in this order. A skill that owns a
section fills it; sections it doesn't own yet stay as the placeholder line.

```markdown
---
ticket: <NN>-<ticket-slug>
title: <human title>
phase: scoped            # scoped → grilled → reviewed → tested → implemented
needs-jira: true         # false if this work doesn't warrant a ticket
depends-on: []           # list of <NN> prefixes, e.g. ["01"]
branch: null             # set by execute when work starts
---

# <Ticket title>

## Problem / Context
<why this exists, the user-facing or system need>

## Scope
**In:** <what this ticket covers>
**Out:** <explicitly not covered — prevents creep>

## Codebase Touchpoints
<real file:line references the work will read or change. A map, not a vibe.>
- `path/to/file.ts:42` — <what's there / what changes>

## Conventions & Patterns
<how THIS repo already does the things this ticket needs, with file refs, so the
implementation matches house style instead of generic boilerplate. e.g. "APIs are
defined as … see `src/api/foo.ts:10`; React components follow … see `…`">

## Open Questions
<written by `scope`. Each is a real ambiguity the downstream skills must resolve.
`grill` reads these first. Use a checkbox list; resolved ones move to Decisions.>
- [ ] <question>

## Decisions
<written by `grill` (and anyone who resolves a question). The answer, plus who
decided / why. This is the resolved counterpart to Open Questions.>
- <decision + rationale>

## Acceptance Criteria
<the CONTRACT. Checkable given/when/then statements. `execute` verifies against
these and checks them off. This is the most important section in the doc.>
- [ ] <criterion>

## Test Plan
### Unit Tests
<specified by `tdd` — what to test, edge cases. `execute` writes & runs them.>
### Manual / UI QA
<a checklist a human runs after implementation — clicks, flows, edge inputs.>
- [ ] <step + expected result>

## Eng Review Verdict
<written by `eng-review`. Dimension scores, what would make each a 10, and the
changes folded back into the sections above.>

## Jira Ticket
<OUTPUT ONLY — text to copy-paste into Jira. The plugin never calls the Jira API.>
### Title
<one line>
### Description
<formatted description: context, scope, acceptance criteria, out-of-scope>

## Work Log
<append-only notes written by `execute`: what was implemented, deviations from
plan (plan said X, reality was Y), test results, QA outcomes.>
```

---

## 4. Phase lifecycle

Both `README.md` and each `doc.md` carry a `phase`. Skills advance it; the
orchestrator reads it to decide what runs next. The doc holds the state — the
orchestrator stays stateless.

| phase         | set by      | meaning                                              |
|---------------|-------------|------------------------------------------------------|
| `scoped`      | scope       | doc exists, touchpoints + open questions written     |
| `grilled`     | grill       | questions resolved into Decisions, scope sharpened   |
| `reviewed`    | eng-review  | plan pressure-tested, verdict written, fixes folded  |
| `tested`      | tdd         | unit test spec + manual QA checklist written         |
| `implemented` | execute     | code written, tests pass, QA done, acceptance met    |

A feature's `README.md` phase reflects its **least-advanced** ticket (i.e. the
feature isn't `reviewed` until every ticket is at least `reviewed`).

---

## 5. Conventions for skill authors

- **Read before write.** Always read the existing `doc.md` / `README.md` before
  editing so you preserve sections you don't own.
- **Never silently decide the breakdown.** `scope` must ask the user
  (need a ticket at all? / 1 / N / how many) via an interactive question.
- **Resolve, don't duplicate.** When `grill` answers an Open Question, move it to
  Decisions and check/remove it from Open Questions — don't leave both.
- **Acceptance Criteria is the contract.** Spend effort making it sharp; every
  later skill keys off it.
- **End by suggesting the next skill** (e.g. scope → "run `/grill` next"). This
  gives the pipeline feel without hard-coupling the skills.
- The current phase determines the next skill: scope → grill → eng-review → tdd
  → execute.
