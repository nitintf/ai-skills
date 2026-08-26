---
name: understand
description: >-
  Answer a question about a codebase, or map an unfamiliar one, with real
  file:line evidence. Two modes, auto-detected: QUESTION mode ("how does auth
  refresh work?", "where is rate limiting enforced?") searches the whole codebase
  and delivers a sourced answer; MAP mode ("understand this repo", "explain the
  billing subsystem") traces entry points, data flow, key modules, and house
  conventions into an architecture map. Either can be saved as a durable doc under
  `.plan/_research/`. Standalone: does NOT touch `.plan` ticket docs, but it's the
  ideal warm-up before `/scope`. Triggers: "how does X work", "where is X
  handled", "why does this do X", "understand this codebase", "map this repo",
  "explain this subsystem", "help me onboard", "research this".
---

# understand: answer it, or map it, with coordinates

Two jobs, one skill, because they're the same machinery pointed differently:

- **Question mode**: the user has a specific question. `"how does token refresh
  work?"`, `"where do we enforce rate limits?"`, `"why is this cached twice?"`,
  `"what would break if I changed this signature?"` You hunt across the whole
  codebase and come back with a **sourced answer**.
- **Map mode**: the user needs a mental model of an area or a whole repo. You
  trace how it actually works and deliver an **architecture map**.

The bar for both: **coordinates, not adjectives.** "The parser is complex" is
useless; ``parser.ts:120` mixes tokenizing and evaluation`` is a finding. An
answer without `file:line` is a guess wearing a suit.

## 1. Pick the mode and the scope

Auto-detect; ask only if genuinely ambiguous.

- Interrogative input, or a specific behavior/symbol/flow named → **question**.
- A repo, subsystem, or area named with no question → **map**.
- Both ("explain billing and tell me where I'd add proration") → map with the
  question as the section that matters most.

Then bound it. Don't boil the ocean: a question needs depth along one path, an
onboarding map needs breadth with depth only on the main flow. If the ask is
huge ("understand this monorepo"), say what you're covering and what you're not.

**Read `.plan/_conventions.md` if it exists** (see `${CLAUDE_PLUGIN_ROOT}/SPEC.md`
§6): it front-loads the toolchain, layout, and house patterns, so you can spend
your exploration on the actual question instead of re-deriving the basics.

---

## Question mode

### Q1. Find the ground truth

Search wide before reading deep. Attack from several angles, because any single
search misses things:

- **By symbol**: the function, class, type, or constant named in the question,
  and its call sites.
- **By string**: user-visible text, error messages, log lines, env var names,
  route paths, config keys. These are often the fastest way into a subsystem.
- **By concept**: the plausible vocabulary this codebase would use ("refresh",
  "renew", "rotate", "reauth"). Teams name things idiosyncratically; try several.
- **By structure**: the directory where this *should* live, whether or not it does.

For a broad codebase, dispatch parallel `Explore` agents on different angles and
synthesize: one agent per search strategy beats one agent reading everything.

### Q2. Trace it, don't infer it

Follow the real path from the outside in and read the code at each hop. The
answer to "how does X work" is a chain of `file:line`, not a summary of what the
names suggest.

Pay attention to the things that quietly change the answer:
- Conditionals, feature flags, and env-dependent branches: "it depends" is
  frequently the true answer, and *what* it depends on is the useful part.
- Middleware, decorators, interceptors, and framework magic that runs without
  appearing at the call site.
- Overrides, subclasses, and config that shadow the obvious implementation.
- **Dead code.** Confirm the path you're describing actually executes, check
  it has live callers. Describing a well-written function that nothing calls is a
  classic and confident way to be wrong.

### Q3. Answer

Lead with the answer, then the evidence:

- **Answer**: 2-5 sentences, directly addressing what was asked. No preamble.
- **How it works**: the traced chain, each step with `file:line`. A numbered
  walk, or a small Mermaid diagram if the shape genuinely needs one.
- **The details that matter**: the conditionals, the edge cases, the config
  that changes behavior, the surprising part.
- **Related code you should know about**: adjacent things the user will need.
- **What I could not determine**: the parts you couldn't verify, said plainly.

---

## Map mode

### M1. Get the lay of the land

- **Entry points**: `main`, server bootstrap, CLI command, route registration,
  the app's `index`. Where does execution actually begin?
- **Build & run**: the manifest, the scripts, how it's started and tested.
- **Shape**: the top-level layout and what each major folder is for.
- **The docs that exist**: README, ARCHITECTURE, CONTRIBUTING, `CLAUDE.md`,
  ADRs. Read them, but **trust the code over stale docs**.

For a large codebase, dispatch parallel `Explore` agents across areas, then
synthesize, don't read every file yourself.

### M2. Trace the important paths

This is the core. Follow flows end to end rather than reading files at random:

- Start at an entry point and follow one real request/command through the layers:
  routing → handler → service/domain → data access → external calls and back.
  Note each hop with `file:line`.
- Identify the **key modules** and what each is responsible for.
- Find the **data model**, the core types/entities and where they're defined.
- Note **external integrations**, DBs, queues, third-party APIs, other services.
- Follow the **seams**: where modules call into each other is where the bugs and
  the important design decisions live.

### M3. Extract the house conventions

The same ones `/scope` and `/pr-review` need: capturing them is what makes this
a warm-up for the pipeline rather than a throwaway. With `file:line`: how APIs
and components are defined, error handling, logging, config, naming, folder
conventions, and the existing test style.

If `.plan/_conventions.md` already exists, don't redo this: cite it, and append
anything new you found. If it doesn't and the user is onboarding, suggest
`/conventions` once: it makes every later skill cheaper.

### M4. Deliver the map

- **Overview**: 3-5 sentences, saying what this system is, its architecture in one
  breath, the core flow.
- **Key modules**: a short table, module → responsibility → `file:line`.
- **How it flows**: the traced path from M2, as a numbered walk or a small
  Mermaid diagram if it genuinely clarifies.
- **Data model & integrations**: core entities and external dependencies.
- **Conventions**: the house patterns, so the next change fits in.
- **Where you'd make change X**: if the user had a goal, point at the exact
  files and functions. Often the most valuable section.
- **Risky / unclear areas**: sharp edges, god objects, undertested code, and
  anything you genuinely couldn't resolve.

---

## Persist it

Default to answering **in chat**. Then offer to save:

> "Want me to save this to `.plan/_research/<slug>.md`?"

Save without asking if the user's request implied a document ("write up", "give
me a doc", "prepare an answer I can share", `/understand --save`). Use a
descriptive slug (`auth-token-refresh.md`, not `research-1.md`), and include
frontmatter so a future reader can judge its age:

```markdown
---
question: <the question, or the area mapped>
mode: question | map
date: <YYYY-MM-DD>
commit: <short SHA it was written against>
---
```

A saved research doc is a **snapshot, not documentation**, the code moves and
this won't. The `commit` field is what tells the next reader whether to trust it.
If you're answering a question that already has a doc in `.plan/_research/`, read
it first, then verify it against current code and update it rather than filing a
near-duplicate.

## Stay honest

- **Don't invent architecture.** If you didn't trace it, say "I didn't verify
  this path" rather than describing a flow you assumed. Confident-wrong is the
  worst possible output here, the user will act on it.
- **Distinguish what the code does from what it looks like it does.** Names lie,
  comments rot, docs go stale.
- **Say what you couldn't find.** A named gap is useful; a smoothed-over one is a
  trap. "I found no rate limiting on this path" is a real and valuable finding:
  but only say it after you've actually searched several ways.
- You map and explain; you don't change anything. To act on it: `/scope` for a
  feature, `/debug` for a bug, `/spike` to choose between approaches.
