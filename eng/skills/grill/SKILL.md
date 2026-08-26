---
name: grill
description: Interview you about a scope doc's open questions, then add its own, and write the answers into the doc's Decisions.
disable-model-invocation: true
---

# grill: interrogate the requirements until they're sharp

You are the second pass of the pipeline. A `scope` doc already exists with
`## Open Questions`. Your job is to turn ambiguity into recorded decisions so
that `eng-review`, `tdd`, and `execute` have an unambiguous target.

**First, read the doc schema** at `${CLAUDE_PLUGIN_ROOT}/SPEC.md` and the
target ticket doc(s) under `.plan/`. If multiple tickets exist, ask the user
which to grill, or go ticket by ticket.

## Steps

### 1. Start from the doc's Open Questions
Read `## Open Questions` first and ask those: these are the gaps `scope` already
identified. Don't reinvent them; lead with them.

### 2. Add your own questions: eng + business
Once the recorded questions are answered, probe further from two angles:
- **Engineering:** edge cases, error/empty/duplicate inputs, failure modes,
  concurrency, migration/backfill, performance limits, security/permissions,
  observability, rollback.
- **Business / product:** who is this for, what's the success condition, what's
  explicitly out of scope, what happens to existing data/users, priority.

Ask in **small batches** (use the interactive question tool), not a wall of 20.
React to each answer, good grilling is adaptive.

### 3. Explore if you need context
If a question can be answered by reading the code rather than asking the user,
go read it (or dispatch an Explore agent). Don't make the user answer things the
codebase already decides. Bring evidence to your questions.

Check `.plan/_conventions.md` first (protocol in `${CLAUDE_PLUGIN_ROOT}/SPEC.md`
§6): a surprising number of "how should we do this?" questions are already
answered by how the repo does everything else, and asking the user something the
codebase has already decided wastes the grilling.

### 4. Write results back into the doc
- Move each resolved question from `## Open Questions` into `## Decisions` with
  the answer and a one-line rationale. **Don't leave it in both places.**
- Sharpen `## Scope` (especially the **Out** list) based on what you learned.
- Tighten or add `## Acceptance Criteria`, grilling usually surfaces the real
  contract. Make these checkable given/when/then statements.
- If genuinely new ambiguities appear that the user defers, leave them in
  `## Open Questions` (honestly, don't pretend everything is resolved).

### 5. Advance phase and hand off
Set frontmatter `phase: grilled` (and update the README table). End with:
"Run `/eng-review` next to pressure-test the plan against the codebase."

If the doc was `track: express` and you were run on it anyway, that's a
deliberate escalation, set `track: full` and say so, so the rest of the pipeline
follows the full path.
