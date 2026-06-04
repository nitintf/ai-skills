---
name: eng-flow
description: >-
  Orchestrator for the eng pipeline. Runs the five skills in order — scope →
  grill → eng-review → tdd → execute — driven entirely off the phase recorded in
  the .plan doc, pausing at a gate between each so the user stays in control. Picks
  up wherever the doc left off, so it's also "resume my planning flow". Use when
  the user wants to run the whole plan-to-ship pipeline rather than invoking skills
  one at a time. Triggers: "eng flow", "run the pipeline", "plan to ship", "take
  this from idea to code", "resume the flow".
---

# eng-flow — run the pipeline end to end, one gate at a time

You orchestrate the five `eng` skills. You are deliberately **dumb**: the doc
holds all the state. You read the current `phase` and run the next skill. This is
exactly why the skills also work solo — there's no orchestrator-only logic.

**First, read the doc schema** at `${CLAUDE_PLUGIN_ROOT}/SPEC.md` so you
understand the phase lifecycle.

## How it works

### 1. Find or start the feature
- If the user gave a task with no `.plan` doc yet → start at `scope`.
- If a `.plan/<feature-slug>/` exists → read its `README.md` and the ticket
  docs to find the current `phase`. If several features exist, ask which.

### 2. Run the next skill based on phase
Use this mapping (the doc's phase → the skill to run next):

| current phase | next skill   |
|---------------|--------------|
| (no doc)      | `scope`      |
| `scoped`      | `grill`      |
| `grilled`     | `eng-review` |
| `reviewed`    | `tdd`        |
| `tested`      | `execute`    |
| `implemented` | done         |

Invoke that skill (via the Skill tool) and let it do its full job, including
writing its results and advancing the phase.

### 3. Gate between every step
After each skill completes, **stop and check in with the user** before running
the next one. Summarize what that step produced and what's next, e.g.:
"Scope is done — 3 tickets drafted in `.plan/jira-assets-csv/`. Next is `/grill`
to resolve 7 open questions. Continue?" Only proceed on confirmation.

The gate matters most before `execute` (code gets written) — never blow through
that one.

### 4. Multi-ticket features
Run the planning phases (scope→tdd) for the whole feature, then `execute` tickets
in dependency order. Respect each doc's `depends-on`.

### 5. Stop when done
When every ticket is `implemented`, report what shipped and suggest the project's
ship/PR flow. The user can re-run `/eng-flow` anytime to resume — it just reads
the phase and continues.
