---
name: adr
description: >-
  Write an Architecture Decision Record: the forces, the options genuinely
  considered, the choice, and the consequences you are accepting. Also
  supersedes an earlier ADR.
disable-model-invocation: true
---

# adr: record why, so the next person doesn't have to guess

Codebases preserve *what* was decided perfectly and *why* not at all. Two years
later someone finds the odd-looking choice, assumes it was a mistake, "fixes" it,
and rediscovers the constraint the hard way. An ADR is the cheapest possible
insurance against that.

An ADR is **immutable history, not documentation**. It records what was decided,
by whom, under which constraints, *at a point in time*. When the decision
changes, you don't edit the old record: you write a new one that supersedes it.
That's the whole discipline, and it's what makes the trail trustworthy.

## 1. Check it deserves an ADR

Not every decision needs one. The test: **would reversing this be expensive, and
would a competent newcomer be puzzled by it?**

Worth recording: choosing a datastore, a framework, or a third-party service;
an architectural boundary (monolith vs services, where a layer sits); an API or
schema contract others depend on; auth and permissions models; a deliberate
deviation from your own conventions; adopting or dropping a major dependency;
anything where you rejected the obvious option for a non-obvious reason.

Not worth it: naming, formatting, library-internal choices, anything you'd change
in an afternoon. If it belongs in the ticket's `## Decisions` section, leave it
there, say so and stop. Filing ADRs for trivia is how teams learn to ignore the
folder.

If it's a close call, say what you think and let the user decide.

## 2. Gather the real context

An ADR built from the user's one-line summary will be thin. Dig:

- **Read the code.** What actually got built? Cite `file:line`. If the decision
  is already implemented, the code is the most reliable witness to what was
  really chosen: and sometimes reveals that the stated decision and the built
  one differ, which is itself worth recording.
- **Read the doc trail.** A `.plan` ticket's `## Decisions` and `## Eng Review
  Verdict`, PR discussion, existing ADRs in `.plan/_decisions/`. Much of the
  reasoning already exists in prose; your job is often to consolidate it.
- **Find the earlier ADRs this touches**: the one it supersedes, or the ones it
  constrains.

## 3. Grill for what's missing

Ask in small batches, with your recommended answer for each. The questions that
make an ADR worth reading:

- **What forced this?** What changed, or what broke, that made the status quo
  untenable? A decision with no pressure behind it reads as arbitrary.
- **What else did you genuinely consider?** This is the section future readers
  care about most, and the one people skip. An ADR with one option isn't a
  decision record, it's an announcement.
- **What are the constraints?** Deadline, team size and skills, existing
  infrastructure, cost, compliance, an existing contract you can't break. These
  are what make a "wrong-looking" choice correct in context.
- **What are you giving up?** Every real decision has a cost. If the user can't
  name a downside, push: an option with no downside means the alternatives
  weren't seriously explored.
- **What would make you reverse this?** The condition that invalidates it.

Don't invent answers to material questions. Unresolved goes in the doc as such.

## 4. Write it

Number sequentially from the existing files in `.plan/_decisions/` (`0001-`,
`0002-`, …; create the folder if needed). Numbers are permanent, never renumber.

Filename: `.plan/_decisions/<NNNN>-<kebab-case-title>.md`

```markdown
---
number: <NNNN>
title: <short imperative phrase, e.g. "Use Postgres row-level security for tenancy">
status: accepted        # proposed | accepted | superseded | deprecated
date: <YYYY-MM-DD>
deciders: <who actually made the call>
supersedes: <NNNN or none>
superseded-by: none
tags: [<area, e.g. data, auth, infra>]
---

# <NNNN>. <Title>

## Status
**Accepted**, <date>. <If superseded, link the successor here.>

## Context
<The forces at play, in the present tense of the decision. What exists today,
what changed, what pressure made this necessary, and the constraints that
bounded the choice, deadline, cost, team, compliance, existing systems.

Write this so a reader who wasn't there understands the situation before they
see the answer. This is the section that makes the decision defensible later.>

## Options considered

### Option A: <name>  ✅ chosen
<What it is, in a sentence or two.>
- **Pros:** …
- **Cons:** …

### Option B: <name>
<Same treatment. Give it a fair hearing: a straw man here fools nobody and
destroys the document's credibility.>
- **Pros:** …
- **Cons:** …
- **Why not:** <the specific reason it lost, tied to a constraint in Context>

## Decision
<The chosen option, stated plainly and specifically enough to be actionable.
Then the reasoning: which constraint decided it, and what the deciding tradeoff
was. One paragraph, not a summary of the whole document.>

## Consequences

**What this makes easier**
- …

**What this makes harder: the price we're paying**
- <Be honest and concrete. An ADR with no costs is marketing.>

**What we now have to do**
- <Follow-on work this obligates: migrations, docs, guardrails, monitoring.>

## Revisit if
<The concrete condition that would invalidate this, a scale threshold, a
dependency changing, a constraint lifting. Gives the next reader permission to
reopen it, and a test for whether they should.>

## References
<`file:line` for the implementation, the .plan ticket, PRs, related ADRs, and
any external material that informed it.>
```

## 5. Superseding an earlier decision

When a decision is reversed or replaced, **do not edit the old ADR**:

1. Write a **new** ADR with the next number. Set `supersedes: <old NNNN>`. Its
   Context must explain *what changed since*: that delta is the entire value of
   the pair.
2. In the old ADR, change only `status:` to `superseded` and set
   `superseded-by:`, plus a one-line pointer in its Status section. Leave the
   rest of it untouched, including anything that turned out to be wrong.

The old reasoning being visibly wrong in hindsight is the point. That's how a
team learns what it mispredicts.

## 6. Wire it up

- Link the ADR from the originating `.plan` ticket's `## Decisions` section.
- Update `.plan/_decisions/README.md` (create it if absent) with a one-line index
  entry: number, title, status, date.
- If the repo already keeps ADRs somewhere else (`docs/adr/`, `docs/decisions/`),
  **use that location and match its existing format** instead of imposing this
  one. Check before writing.

## Guardrails

- **Never edit an accepted ADR's substance.** Fix a typo, sure. Changing the
  reasoning after the fact destroys the record's only value. Supersede instead.
- **Options is not optional.** A single-option ADR is an announcement. If there
  genuinely was no alternative, say why explicitly: that's a finding.
- **Name the costs.** Every accepted decision has them; an ADR that lists only
  benefits wasn't honest at the time and won't be trusted later.
- **Don't invent context.** If nobody remembers why, write "the original
  rationale is not recorded": a truthful gap beats a plausible fiction that
  future readers will treat as fact.
- **Match the repo's existing ADR convention** if it has one.
