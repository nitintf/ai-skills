---
name: scope
description: Explore the codebase and turn a task into planning docs in `.plan/`, one per ticket, with real file:line touchpoints, a chosen track, and open questions. Front door of the eng pipeline.
disable-model-invocation: true
---

# scope: explore, decide ticket breakdown, draft the planning docs

You are the first pass of a five-skill pipeline. Everything downstream
(`grill`, `eng-review`, `tdd`, `execute`) reads the docs you produce, so the
quality of your exploration and the sharpness of your open questions determine
whether the rest of the pipeline succeeds.

**First, read the doc schema** at `${CLAUDE_PLUGIN_ROOT}/SPEC.md` and obey it
exactly, file layout, section headings, frontmatter keys.

## Steps

### 1. Understand the task: and check what's already written
Take the user's task description verbatim. If it's a one-liner, that's fine:
your job is to expand it through exploration, not to demand a spec upfront.

**Before exploring, look for existing product input** in
`.plan/<feature-slug>/`:
- `PRD.md`, written by `/prd`. Its Goals, Non-Goals, and prioritized
  Requirements are the authority on *what* and *why*. Its Non-Goals map almost
  directly onto your `## Scope → Out`.
- `user-stories.md`, written by `/user-stories`. Stories often map 1:1 onto
  tickets, and their Gherkin acceptance criteria are a head start on yours.

If either exists, read it and record it in the README's `sources:` frontmatter.
**Never rewrite these files**: they belong to the `product` plugin; you consume
them. If one exists and contradicts what the user just told you, ask which wins.

If the task is big and vague with no PRD, it's fair to suggest `/prd` first
rather than scoping from fog, but don't insist.

### 2. Load the house conventions, then explore the gaps
**Read `.plan/_conventions.md` first** if it exists (protocol in `SPEC.md` §6):
it already answers how APIs are defined, how components are structured, where
config lives, and what the test style is. Check its `commit:` against
`git log -1` and flag drift rather than trusting a stale cache. If it doesn't
exist, explore for conventions as normal and suggest `/conventions` once: it
makes every later skill in the pipeline cheaper and more consistent.

Then explore the codebase for what the cache can't tell you. **This is the
highest-value part of the skill. Do not skim.**
- Find the files, modules, and existing patterns this task touches.
- Record **real `file:line` references**, not vibes ("modify the parser" is
  useless; ``match.ts:42`` is gold).
- Note the **task-specific** conventions: not the whole house style, but how
  this repo does the particular things this ticket needs. Put those in
  `## Conventions & Patterns` and reference the cache for the rest rather than
  copying it wholesale.
- If you discover a convention the cache is missing, append it there.
- For broad codebases, consider dispatching parallel Explore agents to map
  different areas, then synthesize.

### 3. Decide breakdown and track: ASK, never guess
Once you understand the scope, present a proposal to the user with the
interactive question tool. Cover:
- **Does this even need a Jira ticket?** (some work is trivial / a chore)
- **One ticket or many?** If many, propose the specific boundaries and *why*
  these and not others, with a one-line rationale each.
- **Full or express track?** (see `SPEC.md` §5). Recommend **express**:
  scope → tdd → execute → ship, skipping grill and eng-review: only when the
  work is small, well understood, and you finished exploring with **no open
  questions**. Recommend **full** for anything with real ambiguity, or that
  touches data, auth, money, or a public contract. Say which you'd pick and why.
- Let the user confirm, merge, split, or override.

This is the single highest-leverage moment in the pipeline. Getting the
breakdown wrong wastes everything downstream. Show your reasoning; let them decide.

### 4. Write the docs
Create `<project-root>/.plan/<feature-slug>/`:
- `README.md`, the feature index per the schema: original task, breakdown decision
  + rationale (including the track choice), the ticket table (phase `scoped`),
  and `sources:` listing any PRD/user-stories you read.
- One `<NN>-<ticket-slug>/doc.md` per ticket per the schema. Fill: Problem,
  Scope (in/out), Codebase Touchpoints, Conventions & Patterns, and most
  importantly **Open Questions**.
- Set frontmatter `phase: scoped`, `track`, `needs-jira`, `depends-on`.

### 5. Open Questions are the handoff: invest in them
Every ambiguity you couldn't resolve from the code becomes an Open Question.
Be specific and code-aware ("the CSV import at `import.ts:88` has no dedupe:
what should happen on a duplicate asset ID?"). These are `grill`'s starting
ammunition. A vague question here = a weak grill later.

**Open Questions and the express track are mutually exclusive.** If you have
open questions, the ticket is `full`: don't propose express and then leave
ambiguity unresolved. Conversely, don't manufacture questions to justify the
full track on genuinely simple work.

### 6. Hand off
Tell the user what you created (paths), summarize the breakdown, and end with
the next step for the chosen track:
- **full** → "Run `/grill` next to resolve the open questions and sharpen scope."
- **express** → "No open questions, so this is on the express track: run `/tdd`
  next to define the test contract. Run `/grill` instead if you want the full
  treatment."
