---
name: tdd
description: >-
  Turn a reviewed `.plan` doc's acceptance criteria into a test contract: a
  unit-test spec plus a manual QA checklist. Specifies tests; does not write
  code.
disable-model-invocation: true
---

# tdd: define the test contract before any code is written

You are the fourth pass of the pipeline. The plan is scoped, grilled, and
reviewed. Your job is to translate the **Acceptance Criteria** into tests, so
that `execute` writes failing tests first, then makes them pass.

**First, read the doc schema** at `${CLAUDE_PLUGIN_ROOT}/SPEC.md` and the target
ticket doc: especially `## Acceptance Criteria` and `## Conventions & Patterns`.

**Then read `.plan/_conventions.md`** if it exists (protocol in `SPEC.md` §6),
specifically its **Tests** section: the framework, the run command, where tests
live, the naming and structure, the fixtures and factories that already exist,
and how boundaries get faked. That section is the whole reason the cache exists
for you: generated tests that don't match a team's test style are the most
visible way AI-written code announces itself. If there's no cache, read two or
three neighbouring test files and derive it yourself.

You **specify** tests here; you do not write or run them. `execute` does that.

**If the doc is `track: express`**, it skipped grill and eng-review, so you are
the first real pressure on the acceptance criteria. Read them with more suspicion
than usual: if they're vague or untestable, that's a signal the ticket wasn't as
simple as it looked. Say so and suggest escalating to `/grill`.

## Steps

### 1. Derive unit tests from acceptance criteria
Every acceptance criterion should map to at least one test. For each, specify:
- what unit/function/component is under test
- the input/setup, the expected output/behavior
- edge cases: empty, duplicate, malformed, boundary, error paths
- which existing test file/pattern it should follow (cite `file:line` from the
  repo's test suite so the tests match house style, same framework, helpers,
  naming, fixtures).

Write this into `## Test Plan → ### Unit Tests`. Be concrete enough that
`execute` can write the tests without re-deriving them.

### 2. Build the manual / UI QA checklist
Unit tests don't cover everything. Write a `### Manual / UI QA` checklist a human
runs *after* the feature works: the click-through, the real flow, the inputs you
can't easily unit test. Each item is a step + expected result, as a checkbox.
Think: happy path, the nastiest realistic input, and the "did we break anything
adjacent" check.

### 3. Sanity-check coverage against the contract
Before finishing, verify every Acceptance Criterion is covered by either a unit
test or a QA step. If a criterion isn't testable, that's a smell, flag it and
consider sharpening the criterion.

### 4. Advance phase and hand off
Set frontmatter `phase: tested` (update the README table). End with:
"Run `/execute` next to implement against this test contract, or hand the doc
to Claude directly."
