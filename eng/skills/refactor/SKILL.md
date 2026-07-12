---
name: refactor
description: >-
  Plan and safely execute a behavior-preserving refactor. Establishes a test
  safety net first (runs existing tests green, adds characterization tests where
  coverage is thin), learns the house style, plans the change as small atomic
  steps, then executes step by step keeping tests green the whole way — verifying
  behavior never changed. Standalone: does NOT touch `.plan` docs. Use when
  reshaping existing code without changing what it does — reducing duplication,
  untangling coupling, renaming, extracting, restructuring. Triggers: "refactor
  this", "clean up this code", "untangle this", "extract this", "restructure
  this". NOT for behavior changes — that's a feature, use `/scope`.
---

# refactor — reshape code without changing what it does

The one iron rule of refactoring: **behavior does not change.** Same inputs,
same outputs, same side effects — only the shape of the code improves. If the
behavior *should* change, that's a feature or a bug fix, not a refactor: stop and
use `/scope` instead. Your job here is to make the code better while proving,
step by step, that you broke nothing.

## 1. Define the target

Nail down exactly what and why before touching anything:

- **What** is being refactored — the file/module/function and its boundaries.
- **Why** — duplication, tangled coupling, a leaky abstraction, an unclear name,
  a function doing five things. A refactor without a reason is just churn.
- **The line you won't cross** — refactor is not rewrite and not redesign. Keep
  the scope tight. If mid-way you find the *right* fix is a behavior change, note
  it separately and raise it; don't smuggle it into the refactor.

## 2. Establish a safety net FIRST

You cannot refactor safely what you cannot verify. Before changing a line:

- **Run the existing tests** and get a green baseline. If they're already red,
  stop — fix or flag that first; you can't tell a refactor regression from a
  pre-existing failure.
- **Add characterization tests where coverage is thin.** Pin the *current*
  observable behavior (including quirks) so any accidental change trips a test.
  Follow the repo's test style (§3).
- If a chunk is genuinely untestable, say so and treat that area as high-risk —
  smaller steps, closer manual verification.

## 3. Learn the house style

The refactored code must look like the codebase, not like a stranger dropped in.
Before restructuring, find how this repo already does the thing you're moving
toward and cite it: naming, file layout, error handling, the existing patterns
for the abstraction you're introducing. Match them.

## 4. Plan atomic steps

Break the refactor into the smallest independently-verifiable transformations,
each of which leaves the tests green. For example: extract function -> rename ->
move -> inline the old call sites -> delete dead code. List the sequence and the
order, so the change is a series of safe hops, never one big-bang rewrite.

## 5. Execute step by step

Work the plan one step at a time:

- Make one transformation.
- **Run the tests.** Green -> continue. Red -> you changed behavior; revert or
  fix before moving on. Never stack a second change on an unverified one.
- Commit atomically per step **only if the user wants commits** — otherwise leave
  the steps in the working tree for them to review.

## 6. Verify behavior is unchanged

Before calling it done:

- Full test suite green.
- Read your own diff as a reviewer: is every change behavior-preserving, or did
  something subtle shift (an error now swallowed, an order changed, a default
  altered)?
- If the app can be run, sanity-check the affected path in the real app.
- Summarize: what changed structurally, what stayed identical behaviorally, and
  any characterization tests you added.

## Guardrails

- **Behavior-preserving or it's not a refactor.** If you must change behavior,
  stop and flag it; don't fold it in silently.
- **Found a bug while refactoring?** Report it separately. "Fixing" it changes
  behavior mid-refactor and muddies the diff — let the user decide.
- **Don't mix concerns.** No feature work, no dependency bumps, no reformatting
  the whole file riding along on the refactor. One kind of change at a time.
- **Small steps beat clever ones.** A reviewer should be able to see, at each
  step, that nothing broke.
