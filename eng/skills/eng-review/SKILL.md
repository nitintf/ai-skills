---
name: eng-review
description: >-
  Third pass of the eng pipeline. An engineering-manager review of a .plan doc:
  rates the plan across architecture, edge cases, test coverage, performance, and
  — critically — consistency with how THIS codebase already builds things (APIs,
  components, patterns), so the eventual code matches house style. Scores each
  dimension 0-10, explains what would make each a 10, and folds the fixes back
  into the doc. Use when a grilled .plan doc is ready for architectural review
  before defining tests. Triggers: "eng review", "review the plan", "review the
  architecture", "lock in the plan".
---

# eng-review — pressure-test the plan and align it to house conventions

You are the third pass of the pipeline. The doc has been scoped and grilled.
Your job is to catch architecture and consistency problems *before* tests and
code, and to leave the plan provably better.

**First, read the doc schema** at `${CLAUDE_PLUGIN_ROOT}/SPEC.md`, the target
ticket doc, and the `## Codebase Touchpoints` / `## Conventions & Patterns` it
references. If multiple tickets, review each (or ask which).

**Also read `.plan/_conventions.md`** if it exists (protocol in `SPEC.md` §6).
It is the shared answer to "how does this repo do things", and dimension 2 below
is where it earns its keep — you're checking the plan against a recorded
standard rather than one you invent on the spot. Verify against real code where
the plan's claims are load-bearing, and append anything the cache is missing.

## Review dimensions — rate each 0-10

For every dimension: give a score, state the one or two things that would make
it a 10, then **apply those fixes to the doc** (don't just critique).

1. **Architecture & approach** — is the design sound, simple, and the right
   shape for the problem? Any over- or under-engineering?
2. **Consistency with the codebase** — THE dimension you must not skip. Does the
   plan match how this repo already does these things? Start from
   `.plan/_conventions.md` (the checklist behind it is in
   `${CLAUDE_PLUGIN_ROOT}/CONVENTIONS.md`), and re-read the real code where it
   matters:
   - How are APIs/endpoints/services defined here? Does the plan follow it?
   - How are React components structured (props, state, styling, file layout)?
   - Naming, error handling, logging, config, folder conventions, test style.
   - **Is the plan reinventing a primitive that already exists?** Check the
     cache's "existing primitives" table. This is the most common failure.
   Cite `file:line` for the pattern the plan should follow. The goal: code that
   looks like the team wrote it, not generic boilerplate.
3. **Edge cases & failure modes** — empty/duplicate/malformed inputs, partial
   failure, retries, idempotency, race conditions.
4. **Test coverage** — will the planned tests actually prove the acceptance
   criteria? Gaps?
5. **Performance & scale** — N+1s, unbounded loops/queries, large payloads,
   anything that won't hold at real data sizes.
6. **Data & migration safety** — schema changes, backfills, rollback,
   backward compatibility.

## Steps

1. Walk the dimensions interactively with the user — surface the real issues,
   give an opinionated recommendation for each, let them weigh in on judgment
   calls. Don't just dump a report.
2. Fold accepted changes back into the relevant sections (Scope, Touchpoints,
   Conventions & Patterns, Acceptance Criteria, Test Plan).
3. Write the `## Eng Review Verdict` section: dimension scores, what a 10 needs,
   and what you changed.
4. Set frontmatter `phase: reviewed` (update the README table). End with:
   "Run `/tdd` next to define the test contract."
