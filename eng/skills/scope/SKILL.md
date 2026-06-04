---
name: scope
description: >-
  Front door of the eng pipeline. Takes a task description, explores the codebase
  deeply, decides (with the user) whether it needs a Jira ticket and whether to
  split into one or many tickets, then writes a planning doc per ticket into the
  project's .plan folder — including real file:line touchpoints, house
  conventions, and open questions for the next step. Use when the user describes
  a feature/task and wants it scoped, broken down, or turned into Jira tickets.
  Triggers: "scope this", "break this down", "turn this into tickets", "plan this
  feature".
---

# scope — explore, decide ticket breakdown, draft the planning docs

You are the first pass of a five-skill pipeline. Everything downstream
(`grill`, `eng-review`, `tdd`, `execute`) reads the docs you produce, so the
quality of your exploration and the sharpness of your open questions determine
whether the rest of the pipeline succeeds.

**First, read the doc schema** at `${CLAUDE_PLUGIN_ROOT}/SPEC.md` and obey it
exactly — file layout, section headings, frontmatter keys.

## Steps

### 1. Understand the task
Take the user's task description verbatim. If it's a one-liner, that's fine —
your job is to expand it through exploration, not to demand a spec upfront.

### 2. Explore the codebase — do this thoroughly
This is the highest-value part of the skill. Do not skim.
- Find the files, modules, and existing patterns this task touches.
- Record **real `file:line` references**, not vibes ("modify the parser" is
  useless; ``match.ts:42`` is gold).
- While exploring, note **house conventions** relevant to the task: how are
  APIs defined here? how are React components structured? how are tests
  written? where does config live? Capture these with file refs — they go in
  the `## Conventions & Patterns` section so downstream code matches house style.
- For broad codebases, consider dispatching parallel Explore agents to map
  different areas, then synthesize.

### 3. Decide the ticket breakdown — ASK, never guess
Once you understand the scope, present a proposal to the user with the
interactive question tool. Cover:
- **Does this even need a Jira ticket?** (some work is trivial / a chore)
- **One ticket or many?** If many, propose the specific boundaries and *why*
  these and not others, with a one-line rationale each.
- Let the user confirm, merge, split, or override.

This is the single highest-leverage moment in the pipeline. Getting the
breakdown wrong wastes everything downstream. Show your reasoning; let them decide.

### 4. Write the docs
Create `<project-root>/.plan/<feature-slug>/`:
- `README.md` — feature index per the schema: original task, breakdown decision
  + rationale, and the ticket table (phase `scoped`).
- One `<NN>-<ticket-slug>/doc.md` per ticket per the schema. Fill: Problem,
  Scope (in/out), Codebase Touchpoints, Conventions & Patterns, and most
  importantly **Open Questions**.
- Set frontmatter `phase: scoped`, `needs-jira`, `depends-on`.

### 5. Open Questions are the handoff — invest in them
Every ambiguity you couldn't resolve from the code becomes an Open Question.
Be specific and code-aware ("the CSV import at `import.ts:88` has no dedupe —
what should happen on a duplicate asset ID?"). These are `grill`'s starting
ammunition. A vague question here = a weak grill later.

### 6. Hand off
Tell the user what you created (paths), summarize the breakdown, and end with:
"Run `/grill` next to resolve the open questions and sharpen scope."
