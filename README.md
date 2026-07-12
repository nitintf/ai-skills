# nitin-ai-skills

Personal Claude Code plugins — reusable skill packs for engineering workflows,
packaged as a [Claude Code plugin marketplace](https://docs.claude.com/en/docs/claude-code/plugins)
so they work in any project.

## Plugins

### `eng` — plan-to-ship engineering pipeline

Five composable skills plus an orchestrator. Each skill is a **single pass over a
shared markdown doc** that lives in the target project's `.plan/` folder, so they
work solo or chained. The doc holds all state; the skills communicate through it.

| Skill         | What it does                                                        |
|---------------|---------------------------------------------------------------------|
| `/scope`      | Explore the codebase, decide ticket breakdown (asks you), draft a planning doc per ticket with real `file:line` touchpoints, house conventions, and open questions. Drafts Jira ticket text (output only). |
| `/grill`      | Read the doc's open questions, grill you (eng + business), explore for context, write answers into Decisions and sharpen acceptance criteria. |
| `/eng-review` | EM-style review: architecture, edge cases, tests, performance, and **consistency with how this codebase already builds things**. Folds fixes back in. |
| `/tdd`        | Turn acceptance criteria into a test contract: unit-test spec + manual/UI QA checklist. Specifies tests; doesn't write them. |
| `/execute`    | Write the specified tests (failing first), implement against the plan & house conventions, make tests pass, verify acceptance criteria, run QA, update the doc. |
| `/eng-flow`   | Orchestrator — runs scope → grill → eng-review → tdd → execute off the doc's `phase`, pausing at a gate between each. Resumes wherever you left off. |
| `/pr-review`  | **Standalone** (not in the pipeline). Staff/principal-engineer review of the current branch vs main: reads commits + diff, pulls PR context via `gh`, and reviews correctness → architecture → **consistency with house style**, separating blocking issues from nits. Doesn't touch `.plan` docs. |

**Standalone skills** (not in the pipeline, don't touch `.plan` docs):

| Skill             | What it does                                                    |
|-------------------|----------------------------------------------------------------|
| `/pr-review`      | Staff/principal review of the current branch vs main, with `gh` context: correctness → architecture → **house-style consistency**, blocking vs nits. Your **pre-merge** review. |
| `/review`         | Fast **pre-commit** gut-check of your uncommitted working diff (staged + unstaged + new files): correctness, consistency, obvious security, leftover debug/dead code, missing tests. Lighter than `/pr-review`; no branch/`gh`. |
| `/understand`     | Map an unfamiliar codebase or subsystem: entry points, key modules, traced data/control flow, house conventions, and where you'd make a given change. The ideal warm-up before `/scope`. |
| `/refactor`       | Plan + safely execute a **behavior-preserving** refactor: test safety net first (runs green, adds characterization tests), house-style match, atomic steps kept green, verify nothing changed. |
| `/backfill-tests` | Add tests to existing untested code: characterization tests that lock in current behavior and **surface suspected bugs** instead of encoding them. Complements `/tdd` (which specs tests for new features). |

The five pipeline skills obey the doc schema in [`eng/SPEC.md`](eng/SPEC.md); the
standalone skills (`/pr-review`, `/review`, `/understand`, `/refactor`,
`/backfill-tests`) are independent of it.

#### Doc layout (in the target project)

```
<project>/.plan/<feature-slug>/
  README.md                     # feature index + per-ticket status
  <NN>-<ticket-slug>/doc.md     # one self-contained doc per ticket
```

`.plan/` is committed so the plan lives in history (plan-said-X vs reality-was-Y).

### `product` — product-thinking skills

Standalone from `eng`, but their output (written to `.plan/<feature>/`) can feed
`/scope`.

| Skill           | What it does                                                      |
|-----------------|------------------------------------------------------------------|
| `/prd`          | Write a staff-level PRD (Google/Meta/Amazon bar): problem, measurable goals & non-goals, success metrics, prioritized requirements, risks, rollout. Supports the Amazon PR/FAQ format. NOT in the eng doc schema. |
| `/user-stories` | Slice a PRD/epic into INVEST user stories with Gherkin acceptance criteria, ordered with dependencies. Feeds `/scope`. |

### `productivity` — workflow helpers

| Skill        | What it does                                                         |
|--------------|---------------------------------------------------------------------|
| `/catchup`   | Summarize what changed (branch / PR / commit range / file) so you can resume or review fast. |
| `/caveman`   | Ultra-terse communication mode — ~75% fewer tokens, full technical accuracy. Persists until "normal mode". |
| `/handoff`   | Compact the conversation into a handoff doc (saved to the OS temp dir) for a fresh agent to continue. |
| `/grill-me`  | Standalone relentless interview on any plan/design (not tied to `.plan` docs — use eng's `/grill` for those). |

### `brain` — Obsidian second-brain capture

Turns a spoken or typed brain-dump into a well-placed, well-written note in your
own voice. Reads the vault's real folder tree to decide placement, keeps notes
sounding like you (not AI), and keeps the graph connected.

| Skill    | What it does                                                             |
|----------|-------------------------------------------------------------------------|
| `/note`  | Capture something you just learned into your Obsidian vault. Auto-detects mode — **verbatim** (you dumped the full content), **light expand** (topic + a few points), or **topic-only** (just a title, written from scratch). Places it in the right `Learn/` folder, writes it in your note-taking voice, adds a Mermaid diagram only when a concept is truly structural (~1 note in 4), updates the parent `index.md` hub, and does **bidirectional linking**: links out to related notes *and* back-references the new note from existing ones (inserting contextual links and promoting plain-text mentions to `[[wikilinks]]`). Merges and edits to other notes are shown as a plan + diff first. |

Voice rules live in [`brain/VOICE.md`](brain/VOICE.md), which `/note` loads before
writing every note. The vault path is set at the top of
[`brain/skills/note/SKILL.md`](brain/skills/note/SKILL.md).

## Install

Add this repo as a marketplace, then install the plugins you want:

```
/plugin marketplace add nitintf/ai-skills
/plugin install eng@nitin-ai-skills
/plugin install product@nitin-ai-skills
/plugin install productivity@nitin-ai-skills
/plugin install brain@nitin-ai-skills
```

(Or `/plugin marketplace add <path-to-local-clone>` while developing.)

## Update an installed plugin

The marketplace is sourced from GitHub, so editing files in this repo does
**nothing** until the change is pushed and the installed copy is refreshed.
Whenever you change a skill:

1. **Push the code** to `nitintf/ai-skills` (commit + push to `main`).
2. **Refresh the marketplace** — re-pulls the latest from GitHub:
   ```
   /plugin marketplace update nitin-ai-skills
   ```
3. **Update the plugin** — `/plugin` menu → the plugin (e.g. `brain`) → **Update**
   (or reinstall). Bump `version` in the plugin's
   `.claude-plugin/plugin.json` when you want the update to register cleanly.

Installing a brand-new plugin (like `brain` the first time) is the same flow:
push → `/plugin marketplace update nitin-ai-skills` → `/plugin install brain@nitin-ai-skills`.

## Develop

Skills are plain markdown at `eng/skills/<name>/SKILL.md`. Edit and reload. When
adding a field or section, update `eng/SPEC.md` **first** — it's the contract all
the skills depend on.
