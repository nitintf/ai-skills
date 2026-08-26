---
name: eng-flow
description: Run the whole eng pipeline off the `.plan` doc's phase and track, pausing at a gate between each pass. Resumes wherever you left off.
disable-model-invocation: true
---

# eng-flow: run the pipeline end to end, one gate at a time

You orchestrate the `eng` pipeline. You are deliberately **dumb**: the doc holds
all the state. You read the current `phase` and `track` and run the next skill.
This is exactly why the skills also work solo: there's no orchestrator-only
logic.

**First, read the doc schema** at `${CLAUDE_PLUGIN_ROOT}/SPEC.md` so you
understand the phase lifecycle (§4) and the track rules (§5).

## How it works

### 1. Find or start the feature
- If a `.plan/<feature-slug>/` exists → read its `README.md` and the ticket
  docs to find the current `phase` and `track`. If several features exist, ask
  which.
- If the user gave a task with no `.plan` doc yet → start at `scope`.

**Two things worth checking before you start a cold feature:**
- **No `.plan/_conventions.md`?** Suggest `/conventions` first. It's one pass
  that makes every skill after it cheaper and more consistent: the pipeline
  works without it, but not as well.
- **Unfamiliar repo?** Suggest `/understand` as a warm-up so `scope` isn't
  exploring blind.

Offer these; don't force them. If the user wants to get going, get going.

### 2. Run the next skill based on phase and track

| current phase | next, `track: full` | next, `track: express` |
|---------------|----------------------|-------------------------|
| (no doc)      | `scope`              | `scope`                 |
| `scoped`      | `grill`              | `tdd`                   |
| `grilled`     | `eng-review`         | `eng-review`            |
| `reviewed`    | `tdd`                | `tdd`                   |
| `tested`      | `execute`            | `execute`               |
| `implemented` | `ship`               | `ship`                  |
| `shipped`     | done                 | done                    |

Invoke that skill (via the Skill tool) and let it do its full job, including
writing its results and advancing the phase.

`scope` decides the track with the user, so on a cold start you won't know it
until scope is done: that's fine, read it from the doc afterwards.

### 3. Gate between every step
After each skill completes, **stop and check in with the user** before running
the next one. Summarize what that step produced and what's next, e.g.:
"Scope is done, 3 tickets drafted in `.plan/jira-assets-csv/`, full track. Next
is `/grill` to resolve 7 open questions. Continue?" Only proceed on confirmation.

Two gates matter more than the rest and must never be blown through:
- **before `execute`**: code gets written;
- **before `ship`**: commits get pushed and a PR opens, which is outward-facing
  and hard to take back.

### 4. Multi-ticket features
Run the planning phases (through `tdd`) for the whole feature, then `execute`
tickets in dependency order. Respect each doc's `depends-on`: never start a
ticket whose dependencies aren't `implemented`.

Tickets can carry **different tracks**. A feature might have one meaty ticket on
`full` and two trivial ones on `express`; read each doc's own track rather than
assuming the feature's.

For `ship`, ask whether the user wants one PR for the feature or one per ticket.
Don't assume.

### 5. Know when to leave the pipeline
The pipeline is for building a planned change. If what's actually in front of you
is something else, say so and point at the right skill instead of forcing it
through scope:

| the situation | the skill |
|---------------|-----------|
| something is broken and the cause is unknown | `/debug` |
| behavior shouldn't change, only the shape | `/refactor` |
| existing code needs a safety net | `/backfill-tests` |
| the approach itself isn't decided yet | `/spike` |
| a question needs answering, not building | `/understand` |
| a significant decision needs recording | `/adr` |

### 6. Stop when done
When every ticket is `shipped`, report what landed: PR links, what's verified,
what still needs a human. The user can re-run `/eng-flow` anytime to resume; it
just reads the phase and continues.
