---
name: backfill-tests
description: >-
  Add tests to existing untested code. Picks a target by risk, reads the code to
  understand what it actually does, matches the repo's test style, then writes
  characterization tests that lock in current behavior — covering happy path,
  edge cases, and error paths. Surfaces suspected bugs instead of silently
  encoding them. Standalone: does NOT touch `.plan` docs. Complements `/tdd`,
  which specs tests for NEW features; this covers code that already shipped
  without them. Use when a module has no tests, before refactoring risky code, or
  when hardening a legacy area. Triggers: "add tests for this", "backfill tests",
  "this has no tests", "cover this code", "characterization tests".
---

# backfill-tests — add tests to code that already shipped without them

You're putting a safety net under existing code. The critical mindset shift from
`/tdd`: those tests describe what code *should* do from a spec. These tests
describe what the code *currently does*, quirks and all. Their job is to lock in
today's behavior so a future change (a refactor, a fix) can't silently break it.

## 1. Pick the target and justify it

You can't test everything at once, so prioritize by risk:

- **Complexity** — branchy, stateful, or subtle logic breaks quietly.
- **Criticality** — money, auth, data integrity, anything a failure hurts.
- **Churn** — code that changes often needs a net most.
- **History** — areas with a track record of bugs.

If the ask is broad ("test this module"), propose a priority order and start with
the highest-risk piece rather than the easiest.

## 2. Understand what the code actually does

Read the target closely before writing a single assertion. You are documenting
**real** behavior, not ideal behavior:

- Trace each branch and what it returns / does.
- Note the quirks: odd defaults, silent error handling, off-by-one-looking
  edges, implicit assumptions. These are exactly what a test should pin.
- Identify inputs, outputs, and side effects (I/O, state mutation, calls out).

## 3. Match the house test style

The new tests must look like the repo wrote them.

**Read the Tests section of `.plan/_conventions.md`** if it exists (protocol in
`${CLAUDE_PLUGIN_ROOT}/SPEC.md` §6): framework, the exact command to run one
file, where tests live, naming, structure, the **fixtures and factories that
already exist**, and how boundaries get faked. Use the existing builders rather
than hand-rolling setup — that's the difference between tests that read like the
team's and tests that read like a generator's.

Where the cache is silent, find existing test files and cite `file:line` for the
same list. New tests that diverge from house style are a finding against
yourself — match it.

Note also what the repo **doesn't** test. If this team never unit-tests
controllers, adding a suite of them is a bigger conversation than a backfill;
raise it rather than unilaterally changing the team's testing philosophy.

## 4. Write the tests

Prefer testing **observable behavior** over implementation details (tests coupled
to internals break on every refactor, defeating the point). Cover:

- **Happy path** — the normal case, asserting the actual current output.
- **Edge cases** — empty, null/undefined, boundary, duplicate, malformed input.
- **Error paths** — what it does when things go wrong (throws? returns a
  sentinel? swallows silently?). Pin whatever it *actually* does.
- The behaviors most likely to break under future change.

## 5. Run and confirm green

The tests must pass against the current code — that's what "characterization"
means. Run them.

**If a test reveals what looks like a bug** (the current behavior is clearly
wrong), do NOT assert the buggy value as if it's correct — that cements the bug.
Instead mark it clearly: a skipped/xfail test with a comment, or a note in your
report, so the user can decide whether to fix the code or accept the behavior.
Surfacing the bug is more valuable than the coverage.

## 6. Report

- What you covered and why (the risk rationale).
- Coverage gained — roughly what's now protected vs still bare.
- **Suspected bugs found** — the standout deliverable; list each with `file:line`
  and what looks wrong.

## Guardrails

- **Lock current behavior, not wished-for behavior.** If it's weird today, the
  test asserts the weird thing (or flags it) — it doesn't quietly "fix" it.
- **Surface bugs, don't encode them.** A green test over buggy output is a trap.
- **Don't chase 100%.** Cover what's risky and load-bearing; a coverage number
  isn't the goal, protection against regressions is.
- You write and run tests; you don't change the code under test. If a fix is
  wanted, that's a separate step (`/refactor` or a bug fix).
