---
name: execute
description: >-
  Final pass of the eng pipeline. Implements a fully-planned .plan ticket: writes
  the unit tests the doc specified (TDD — failing first), implements against the
  acceptance criteria following the repo's conventions, runs the tests until they
  pass, then verifies the acceptance criteria and walks the manual QA checklist.
  Updates the doc's Work Log and the README status. Use when a tested .plan doc is
  ready to build. Triggers: "execute", "implement this", "build this ticket",
  "do the work".
---

# execute — implement, test, and verify against the plan

You are the final pass. The doc is scoped, grilled, reviewed, and has a test
contract. Your job is to build it the way the plan says and prove it works.

**First, read the doc schema** at `${CLAUDE_PLUGIN_ROOT}/SPEC.md` and the target
ticket doc end to end — Acceptance Criteria, Test Plan, Codebase Touchpoints,
and Conventions & Patterns are your instructions.

**Then read `.plan/_conventions.md`** if it exists (protocol in `SPEC.md` §6).
The ticket doc carries only the conventions relevant to this ticket; the cache
has the rest — the test command, the error and logging patterns, the import
style, and the **existing primitives table**. Check that table before you write
any helper: reinventing something the repo already has is the most common way
generated code fails to look like the team wrote it.

## Steps

### 0. Pick the ticket & respect dependencies
If multiple tickets, choose the lowest-numbered unimplemented one whose
`depends-on` are all `implemented`. Don't start a ticket whose dependencies
aren't done. Confirm with the user before writing code (this is the gate — never
auto-run implementation silently). Create/checkout a branch and record it in the
doc frontmatter `branch:` and the README table.

### 1. Write the tests first (TDD)
Implement the `### Unit Tests` spec — following the existing test files/patterns
it cites. Run them; they should fail for the right reason. This locks the
contract before you write the implementation.

### 2. Implement against the plan
Build the change using the `## Codebase Touchpoints` as your map and the
`## Conventions & Patterns` as your style guide — match how this repo already
builds APIs/components/etc. so the code looks like the team wrote it. Stay inside
`## Scope` (respect the **Out** list — no creep).

### 3. Make the tests pass
Run the unit tests until green. Fix the implementation, not the tests (unless a
test was wrong — note that in the Work Log).

### 4. Verify the acceptance criteria
Go through `## Acceptance Criteria` one by one and check each off only when
actually satisfied. If one can't be met, stop and surface it — don't fake it.

### 5. Walk the manual / UI QA checklist
Run the `### Manual / UI QA` steps yourself where you can (use a browser/QA
skill if available); for steps that need a human, present the checklist and ask
the user to confirm. Record outcomes.

### 6. Close the loop
- Append to `## Work Log`: what you implemented, **plan-vs-reality** deviations,
  test results, QA outcomes. Be specific about where the plan was wrong — that
  record is the reason `.plan/` is committed.
- If you discovered a convention the cache doesn't have, append it to
  `.plan/_conventions.md`.
- If a decision you made along the way is architecturally significant, suggest
  `/adr` so it outlives the ticket.
- Set frontmatter `phase: implemented`; update the README table (phase + branch).
- Summarize for the user: what shipped, what's verified, anything outstanding.
  End with: "Run `/ship` to commit, push, and open the PR."
