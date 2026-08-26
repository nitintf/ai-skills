---
name: conventions
description: >-
  Scan a repo once and cache its house style to `.plan/_conventions.md`, how
  APIs are defined, how components are structured, error handling, logging,
  config, naming, the existing test style, and which shared primitives already
  exist, each with real file:line evidence. Every other eng skill reads this
  cache instead of re-deriving house style on each run, so plans and reviews stay
  consistent and cheap. Use once per repo (or when it has drifted). Triggers:
  "extract the conventions", "learn this codebase's style", "refresh conventions",
  "build the house style cache", "how does this repo do things".
---

# conventions: derive the house style once, so ten skills don't derive it ten times

Almost every skill in this plugin needs the same answer: *how does this repo
already do the thing I'm about to plan, review, or write?* Left to themselves
they each re-explore, burn tokens, and reach subtly different conclusions, so
`scope`'s plan and `pr-review`'s judgment end up disagreeing about the same repo.

You produce the shared answer. One file, real evidence, honest about gaps.

**Read `${CLAUDE_PLUGIN_ROOT}/CONVENTIONS.md` first**: it defines the checklist
of what counts as a convention and the exact output format. Follow it exactly;
consumers parse this file.

## 1. Decide the scan boundary

Ask yourself (and the user, if it's genuinely ambiguous) what "this repo" means:

- **Single app**: scan it all.
- **Monorepo**: conventions often differ per package. Either scan the whole
  thing and note the per-package differences, or scope to the packages the user
  actually works in. Say which you did in the `scanned:` frontmatter.
- **A refresh**: if `.plan/_conventions.md` already exists, read it first and
  update rather than starting cold. Report what changed since its `commit:`.

## 2. Orient before you dive

Fast passes that buy the most context per token:

- The manifest (`package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`),
  language, framework, and the real build/test/lint commands.
- Top-level layout, and any `README` / `ARCHITECTURE` / `CONTRIBUTING` /
  `CLAUDE.md` / ADRs. Read them, but **trust the code over the docs**: stale
  documented conventions are exactly the trap this file exists to avoid.
- `git log --since="3 months ago" --stat`, what's actually being changed lately.
  Recent code is the best evidence of the current convention.

## 3. Find the canonical example for each area

Walk the checklist in `CONVENTIONS.md` §1. For each area the repo actually has,
you're hunting one thing: **the file a teammate would tell you to copy.**

- Find three or more instances of the pattern, not one: one instance is an
  anecdote, three is a convention.
- Pick the clearest recent one as the canonical example and cite it `file:line`.
- Write down **how to add a new one** as concrete steps, because that's what
  downstream skills actually need to follow.
- Note the trap: the deprecated helper, the legacy variant, the thing that looks
  right but isn't.

For a large repo, dispatch parallel `Explore` agents across areas (API, UI,
tests, config) and synthesize, don't read the whole tree yourself.

## 4. Catalogue the existing primitives

The single most common house-style violation is reinventing something that
already exists. Build the "check here before writing a new one" table: the HTTP
client, the logger, the date helper, the button, the modal, the test factory,
the error type. This table saves more downstream damage than any other section.

## 5. Be honest about disagreement

Real repos are inconsistent. Record it as a first-class finding:

- Where does the codebase disagree with itself, and **which way is winning**?
  Use recency to judge: "handlers written since March use the service layer".
- What did you look for and genuinely fail to establish? Put it under
  **Not determined**. A named gap is worth more than an invented convention.

## 6. Write the cache

Write `.plan/_conventions.md` in the exact format from `CONVENTIONS.md` §2,
including the `generated` / `commit` / `scanned` frontmatter, consumers use
`commit` to detect staleness.

Create `.plan/` if it doesn't exist. This file is committed with the repo: it's
shared team knowledge, and its diff over time is a genuinely useful record of how
the codebase's style evolved.

## 7. Hand off

Tell the user the path, summarize the 3-5 most important conventions you found,
and call out anything surprising (an inconsistency, a primitive they may not have
known existed). Then: "every eng skill will read this now, re-run `/conventions`
if the codebase drifts."

## Guardrails

- **Reality, not best practice.** If business logic lives in route handlers,
  that's the convention. Flag it as a smell if you want, but record what's true:
  a file full of aspiration makes every downstream plan generate code that
  doesn't fit.
- **Coordinates, not adjectives.** Every entry cites `file:line`. "Errors are
  handled consistently" is not a finding.
- **Three instances or it's not a convention.** Don't promote one file's quirk
  into a rule the whole pipeline then follows.
- **Never fill a row by inventing it.** Empty and "Not determined" are correct
  answers.
- You read and write one file. You don't change any code.
