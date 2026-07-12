---
name: understand
description: >-
  Map an unfamiliar codebase or subsystem before you touch it. Reads the repo's
  structure, entry points, and key paths, traces how data and control actually
  flow, and extracts the house conventions — then delivers an architecture map:
  what the major pieces are, how they fit, where to make a given change, and what
  looks risky. Standalone: does NOT touch `.plan` docs, but its output is the
  ideal warm-up before `/scope`. Use when onboarding to a new repo/job, picking up
  an unfamiliar area, or answering "how does this work?". Triggers: "understand
  this codebase", "map this repo", "how does this work", "explain this subsystem",
  "help me onboard".
---

# understand — map a codebase before you change it

You are building a mental model someone can act on. A shallow pass lists folders.
A useful map says *how the thing actually works*: where execution starts, how a
request/command flows through the layers, where the important logic lives, and
how this team builds things. Cite real `file:line` throughout — a map without
coordinates is just vibes.

## 1. Establish the scope

Don't boil the ocean. Figure out what the user actually needs to understand:

- **The whole repo** (onboarding) — the high-level architecture and how to find
  your way around.
- **A subsystem / feature / flow** ("how does auth work", "the billing path") —
  go deep on that path, shallow on the rest.

If it's ambiguous, ask once. Then scope the exploration to match — depth where it
matters, not uniform coverage everywhere.

## 2. Get the lay of the land

Orient before you dive:

- **Entry points** — `main`, server bootstrap, CLI command, route registration,
  the app's `index`. Where does execution actually begin?
- **Build & run** — the manifest (`package.json`, `go.mod`, `Cargo.toml`,
  `pyproject.toml`…), scripts, how it's started and tested. This tells you the
  language, framework, and toolchain fast.
- **Shape** — the top-level directory layout and what each major folder is for.
- **The docs that exist** — README, ARCHITECTURE, CONTRIBUTING, `CLAUDE.md`,
  ADRs. Read them, but trust the code over stale docs.

For a large codebase, dispatch parallel `Explore` agents to map different areas
in parallel, then synthesize — don't read every file yourself.

## 3. Trace the important paths

This is the core. For the area in scope, follow the flow end to end rather than
reading files at random:

- Start at the entry point and follow one real request/command through the
  layers: routing -> handler -> service/domain -> data access -> external calls
  and back. Note each hop with `file:line`.
- Identify the **key modules** and what each is responsible for.
- Find the **data model** — the core types/entities and where they're defined.
- Note **external integrations** — DBs, queues, third-party APIs, other services.
- Follow the **seams**: where modules call into each other is where the bugs and
  the important design decisions live.

## 4. Extract the house conventions

The same conventions `/scope` and `/pr-review` care about — capturing them here
is what makes this a warm-up for the pipeline, not a throwaway. With `file:line`:

- How are APIs / handlers / services defined?
- How are components structured (props, state, styling, layout)?
- Error handling, logging, config access, validation, async patterns.
- Naming, folder conventions, and the existing **test style**.

## 5. Deliver the map

Output to chat (write a file only if asked). Make it act-on-able:

- **Overview** — 3-5 sentences: what this system is, its architecture in one
  breath, the core flow.
- **Key modules** — a short table: module -> responsibility -> `file:line`.
- **How it flows** — the main path traced in §3, as a numbered walk or a small
  Mermaid diagram if it genuinely clarifies.
- **Data model & integrations** — the core entities and external dependencies.
- **Conventions** — the house patterns from §4, so the next change fits in.
- **Where you'd make change X** — if the user had a goal, point at the exact
  files/functions they'd touch. This is often the most valuable section.
- **Risky / unclear areas** — sharp edges, god objects, undertested code, and
  anything you genuinely couldn't resolve. Flag it; don't paper over it.

## Stay honest

- **Don't invent architecture.** If you didn't trace it, say "I didn't verify
  this path" rather than describing a flow you assumed.
- **Coordinates over adjectives.** "The parser is complex" is useless;
  ``parser.ts:120` mixes tokenizing and evaluation`` is a finding.
- You map and explain; you don't change anything. If the user wants to act on the
  map, `/scope` is the next step.
