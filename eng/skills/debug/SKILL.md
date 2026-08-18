---
name: debug
description: >-
  Systematically root-cause a bug instead of guessing at fixes. Reproduces the
  failure first, narrows the surface with evidence, forms explicit competing
  hypotheses and kills them one at a time, confirms the true cause by predicting
  and observing, then fixes the cause (not the symptom) and locks it with a
  regression test. Standalone: does NOT touch `.plan` docs. Use for a failing
  test, a crash, wrong output, a flaky test, or "it works locally but not in
  prod". Triggers: "debug this", "why is this failing", "find the root cause",
  "this test is flaky", "fix this bug", "it's broken".
---

# debug — find the actual cause, then fix that

The failure mode this skill exists to prevent: reading an error, pattern-matching
a plausible cause, changing something, and declaring victory when the symptom
moves. That's not debugging — it's guessing with extra steps, and it leaves the
real bug in place wearing a different mask.

Debugging is **evidence in, hypothesis out, repeat.** You do not change code to
see what happens; you change code to *test a stated prediction*. If you can't say
what you expect to observe before you run something, you're not ready to run it.

## 1. Reproduce it — first, always

Everything downstream is worthless without this. You cannot confirm a fix you
cannot trigger.

- Get the **exact** invocation: the command, the test name, the request, the
  input. Read the real error message and the **full stack trace**, not a summary.
- Run it yourself and watch it fail. If you can't reproduce it, that's the
  problem to solve first — ask for the missing piece (env, data, version, the
  exact steps) rather than debugging from imagination.
- Establish **when it's not broken**: does it pass on `main`? with different
  input? in isolation vs the full suite? The boundary between working and broken
  is your highest-value clue.
- **Flaky?** Then reproduction means loop it (`--repeat`, run the file 20 times)
  until you have a rate. A bug you see 1-in-10 needs a 1-in-10 harness before you
  can ever claim it's fixed.

Write down the **exact reproduction command**. You'll run it after every step.

## 2. Read the evidence properly

Before forming any theory, harvest what's already in front of you:

- The stack trace **top to bottom** — the deepest frame in *your* code is usually
  more informative than the library frame that threw.
- The actual values. Print or inspect the real input at the failure point. Half
  of all bugs are "the data wasn't the shape you assumed".
- Logs around the failure, not just at it — the state one step earlier.
- `git log` / `git blame` on the failing path. **Did this ever work?** If yes,
  `git bisect` (or a manual bisect over a handful of commits) converts a hard
  reasoning problem into a mechanical search. Reach for it early on regressions;
  it is the single highest-leverage debugging tool and the most under-used.

## 3. Narrow the surface

Cut the search space in half repeatedly instead of staring at all of it:

- Where does correct data become incorrect? Instrument the path at a midpoint
  and check: is it already wrong here, or still fine? Then bisect the path.
- Trim the reproduction to the smallest input and shortest code path that still
  fails. Every element you remove without the bug disappearing is a suspect
  eliminated.
- Isolate the layer: pure logic, or the boundary (DB, network, filesystem,
  clock, concurrency, framework)? Bugs cluster at boundaries.

## 4. Form competing hypotheses — plural, explicit

State **two or three** candidate causes, not one. A single hypothesis is a
commitment, and you'll unconsciously defend it; competing hypotheses make you
gather discriminating evidence instead.

For each: *if this is the cause, what would I expect to see that I haven't
checked yet?* Then go check the thing that **distinguishes** them.

Rank by prior probability, and be honest about it — it is far more often your
own recent change, an assumption about input shape, or a misread of an API than
it is a bug in the framework. "The library is broken" is a last resort, not a
first instinct.

Usual suspects worth walking when you're stuck: off-by-one and boundary
conditions; null/undefined/empty distinct from zero/false; type coercion; async
ordering, missing `await`, unhandled rejection; shared mutable state between
tests or requests; caching and staleness; time zones, DST, clock assumptions;
encoding; environment/config difference between where it works and where it
doesn't.

## 5. Kill hypotheses one at a time

Change **one variable per experiment** and predict the result before you run it.

- Prediction confirmed → the hypothesis survives, keep narrowing.
- Prediction wrong → *good*. That's information. Discard the hypothesis and say
  what it ruled out.

Never make two changes at once — you lose the ability to attribute the outcome.
Undo failed experiments before the next one; a pile of speculative edits becomes
its own bug.

## 6. Confirm the root cause before fixing

You've found it when you can do all three:

1. **Explain the full causal chain** — from trigger to symptom, every hop.
2. **Predict** a new case that should also fail, and watch it fail.
3. **Predict** a case that should pass, and watch it pass.

If you can't do these, you have a correlation, not a cause. Say so plainly rather
than shipping a fix you can't justify.

**Ask "why" until you hit something worth fixing.** The null dereference is the
symptom; the missing validation at the boundary is often the cause; the API that
makes an invalid state representable is sometimes the real one. Stop at the level
where the fix actually belongs — don't stop at the crash site out of convenience,
and don't spiral into rewriting the architecture.

## 7. Fix the cause, and lock it

- **Write a failing test first** that reproduces the bug at the tightest level
  you can — it's the proof, and it's what stops the bug coming back. Watch it
  fail for the right reason. Follow the repo's test style
  (`.plan/_conventions.md`, or the neighbouring test files).
- Make the **minimal** fix that addresses the cause. Resist the urge to
  refactor the surrounding code in the same change — note it and offer it
  separately (`/refactor`).
- Run the new test (green), then the **full suite** (no collateral damage), then
  the **original reproduction from §1**.
- For a flaky bug: re-run the loop harness from §1 at the same volume. One green
  run proves nothing.

## 8. Report

- **Root cause** — the causal chain in a few sentences, with `file:line`.
- **The fix** — what changed and why that's the right level to fix it.
- **Proof** — the regression test, and the reproduction now passing.
- **Related risk** — the same mistake elsewhere in the codebase (go look; bugs
  of a kind travel in packs), and any bug you found along the way but didn't fix.

## Guardrails

- **No fix without a confirmed cause.** If you're guessing, say you're guessing.
  "This might help" is an honest sentence; a confident wrong explanation is worse
  than none.
- **One variable at a time.** Always.
- **Symptom-suppression is not a fix.** A `try/catch` around the error, a
  null-check at the crash site, a retry over a race, a `sleep` in a flaky test —
  these hide the bug. If a band-aid is genuinely the right call for now, label it
  as one and file what the real fix is.
- **Don't delete or `.skip` a failing test to make things green.** The test is
  the messenger.
- **Never widen scope silently.** Found three more bugs? Report them; fix the
  one you were asked to fix.
