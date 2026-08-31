# Skills

Personal Claude Code plugins: reusable skill packs for engineering workflows,
packaged as a [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugins)
so they work in any project.

Most skills here are **user-invoked**: they fire only when you type `/name`, and
their descriptions never sit in the model's context. That keeps the always-loaded
cost low, and it makes **[`/ask`](productivity/skills/ask/SKILL.md)** the one
skill worth remembering: describe your situation and it routes you to the right
one. A handful stay model-invoked (`/conventions`, `/understand`, `/debug`,
`/refactor`, `/backfill-tests`, `/review`, `/pr-walkthrough`, `/pr-review`,
`/catchup`, `/note`,
`/unslop`) because the agent can usefully reach for them on its own.

## `eng`: plan-to-ship engineering pipeline

Six pipeline skills plus an orchestrator. Each is a **single pass over a shared
markdown doc** in the target project's `.plan/` folder, so they work solo or
chained. The doc holds all state; the skills communicate through it, never
directly. The contract is [`eng/SPEC.md`](eng/SPEC.md).

| Skill         | What it does                                                        |
|---------------|---------------------------------------------------------------------|
| `/scope`      | Explore the codebase, read any PRD/user-stories already written, decide the ticket breakdown **and the track** (asks you), draft a planning doc per ticket with real `file:line` touchpoints and open questions. Drafts Jira ticket text (output only). |
| `/grill`      | Read the doc's open questions, grill you (eng + business), explore for context, write answers into Decisions and sharpen acceptance criteria. |
| `/eng-review` | EM-style review: architecture, edge cases, tests, performance, and **consistency with how this codebase already builds things**. Folds fixes back in. |
| `/tdd`        | Turn acceptance criteria into a test contract: unit-test spec + manual/UI QA checklist. Specifies tests; doesn't write them. |
| `/execute`    | Write the specified tests (failing first), implement against the plan & house conventions, make tests pass, verify acceptance criteria, run QA, update the doc. |
| `/ship`       | Land it: review the final diff, split into atomic commits in the repo's commit style, push, open a PR whose body is generated from the doc, record the PR back in the doc. |
| `/eng-flow`   | Orchestrator: runs the pipeline off the doc's `phase` and `track`, pausing at a gate between each. Resumes wherever you left off. |

### Tracks

Not everything deserves five planning passes. `/scope` proposes a track and you
confirm it:

- **`full`**: scope → grill → eng-review → tdd → execute → ship. Real features,
  genuine ambiguity, anything touching data, auth, or money.
- **`express`**: scope → tdd → execute → ship. Small, well-understood changes
  with **no open questions**. Skipped phases are recorded as skipped, never faked.

### Standalone skills

Not in the pipeline. Each reads `.plan/_conventions.md` when it exists, but none
require a `.plan` doc.

| Skill             | What it does                                                    |
|-------------------|----------------------------------------------------------------|
| `/conventions`    | Scan the repo once and cache its house style to `.plan/_conventions.md`. **Every other skill reads it**, so run this first in a new repo: it makes the rest cheaper and consistent. |
| `/understand`     | Two modes: **question** ("how does token refresh work?") searches the codebase and returns a sourced answer; **map** traces a repo or subsystem into an architecture map. Either can be saved to `.plan/_research/`. |
| `/research`       | Answer a question about the world outside this repo from primary sources: specs, RFCs, official docs, changelogs, library source. Every claim carries a link. Saves to `.plan/_research/`. |
| `/debug`          | Root-cause a bug properly: reproduce first, narrow the surface, kill competing hypotheses one at a time, confirm the cause, fix it, lock it with a regression test. |
| `/spike`          | Timeboxed "which approach should we take": evaluates 2-4 options against **this** codebase's real constraints, prototypes only the riskiest assumption, ends in a recommendation with a confidence level. |
| `/adr`            | Architecture Decision Record: context, options genuinely considered, the decision, and the consequences you're accepting. Immutable, reversals supersede, never edit. |
| `/migrate`        | Data and schema migrations without data loss: characterize the real data, pick a strategy, **write the rollback before the migration**, verify with queries rather than hope. |
| `/resolve-conflicts` | Work a merge, rebase, or cherry-pick conflict hunk by hunk, resolving by **traced intent** rather than by picking a side. Hunts the semantic conflicts that leave no markers. Finishes the operation, never `--abort`. |
| `/refactor`       | Plan + safely execute a **behavior-preserving** refactor: safety net first, atomic steps kept green, verify nothing changed. |
| `/backfill-tests` | Characterization tests for existing untested code: lock in current behavior and **surface suspected bugs** instead of encoding them. |
| `/pr-walkthrough` | **Understand** a PR you didn't write, before judging it: intent from the ticket, how the area works today, a dependency-ordered reading path, the before/after runtime trace, and the questions only the author can answer. Explains, never grades. Hands off to `/pr-review`. |
| `/pr-review`      | Staff/principal review of a PR, yours or someone else's, with `gh` and ticket context: correctness → architecture → **house-style consistency**, blocking vs nits. Your **pre-merge** review. |
| `/review`         | Fast **pre-commit** gut-check of the uncommitted working diff. Lighter than `/pr-review`; no branch, no `gh`. |

> Claude Code also ships a built-in `/code-review` with a `--fix` mode and a
> cloud `ultra` tier. Reach for that when you want breadth; reach for `/review`
> and `/pr-review` when you want the house-style lens these apply.

### Doc layout (in the target project)

```
<project>/.plan/
  _conventions.md               # house style cache: written by /conventions
  _research/<slug>.md           # durable answers: written by /understand
  _decisions/<NNNN>-<slug>.md   # ADRs: written by /adr
  <feature-slug>/
    README.md                   # feature index + per-ticket status
    PRD.md                      # optional, from the product plugin
    user-stories.md             # optional, from the product plugin
    <NN>-<ticket-slug>/doc.md   # one self-contained doc per ticket
```

`.plan/` is committed so the plan lives in history (plan-said-X vs
reality-was-Y). `/execute`, `/pr-review`, and `/review` all write what actually
happened back into the doc's Work Log: that feedback loop is the point.

## `product`: product-thinking skills

Standalone from `eng`, but their output (written to `.plan/<feature>/`) is read
directly by `/scope`.

| Skill           | What it does                                                      |
|-----------------|------------------------------------------------------------------|
| `/prd`          | A staff-level PRD (Google/Meta/Amazon bar): problem, measurable goals & non-goals, success metrics, prioritized requirements, risks, rollout. Supports the Amazon PR/FAQ format. |
| `/user-stories` | Slice a PRD/epic into INVEST user stories with Gherkin acceptance criteria, ordered with dependencies. |
| `/product-flow` | Orchestrator: idea → PRD → stories → handoff to `/scope`, gating between each. Right-sizes the run first, so a small task doesn't get a PRD it doesn't need. |

## `productivity`: workflow helpers

### The day loop

Four skills, **one file per day**. `/daily` opens the day, `/shutdown` closes it,
and tomorrow's `/daily` picks up whatever didn't land, so nothing leaks.

```
/daily     → writes "## Plan for today" (3-5 tasks), unchecked
                ↓  you work the day
/shutdown  → ticks what got done (from commits, PRs, tickets: not from memory)
           → lists the rest under "### Didn't get to"
                ↓  next morning
/daily     → carries those forward, with a day count
           → at 3+ days it stops carrying quietly and tells you to cut it
```

| Skill        | What it does                                                       |
|--------------|--------------------------------------------------------------------|
| `/daily`     | Morning brief → **task list**. Today's calendar with prep flags, mail that genuinely needs a reply, Slack mentions you haven't answered, ticket movement, the commitments you made in yesterday's meetings, and yesterday's carry-over. |
| `/shutdown`  | Evening. Ticks off the plan using **real evidence**, commits, PRs, reviews, ticket moves. Records what slipped, what unplanned work ate the day, and tomorrow's first thing. Edits the *same* file. |
| `/standup`   | Prints your standup update in plain, speakable English: **what you worked on, what you'll work on next.** Never mentions what didn't get done, ongoing work is phrased as ongoing. Writes nothing. |
| `/weekly`    | Friday. What shipped, what kept slipping and *why*, planned vs unplanned split, and a **Worth remembering** section that becomes your self-review evidence. |

The file schema is [`productivity/DAILY-NOTE.md`](productivity/DAILY-NOTE.md):
it defines which skill owns which section. `## Notes` is yours and no skill ever
edits it.

### Other helpers

| Skill          | What it does                                                       |
|----------------|--------------------------------------------------------------------|
| `/ask`         | Describe what you're doing and get routed to the one skill that fits. The router over everything here. |
| `/catchup`     | Summarize what changed (branch / PR / commit range / file) so you can resume or review fast. |
| `/caveman`     | Ultra-terse communication mode, ~75% fewer tokens, full technical accuracy. Persists until "normal mode". |
| `/handoff`     | Compact the conversation into a handoff doc (saved to the OS temp dir) for a fresh agent to continue. |
| `/stress-test` | Relentless interview on any plan or design, one question at a time, each with a recommended answer. General-purpose, use eng's `/grill` for `.plan` docs. |

### Setup

Every source is optional and the skills degrade gracefully, but they're only as
good as what's connected:

| Source | Server | Notes |
|---|---|---|
| Wispr Flow | remote MCP, read-only | Meeting notes, transcripts, tasks: **and calendar events**, so you can skip Google Calendar if you like |
| Slack | `mcp.slack.com/mcp` | Official, user-token OAuth, needs workspace admin approval |
| Jira | `mcp.atlassian.com/v1/mcp/authv2` | Official Atlassian remote MCP, OAuth 2.1 |
| Gmail / Calendar | Google Workspace MCP | Fiddliest: needs your own OAuth client ID + secret as a custom connector |
| GitHub | GitHub MCP, or just `gh` + local `git` | Powers `/shutdown`, `/standup`, `/weekly`. The `gh` fallback works with zero setup and also catches **unpushed** local commits |

Then:

1. `/daily --tune`: reads ~2 weeks of mail and **proposes** your allow/deny
   lists from who you actually reply to. Writes `~/.claude/daily-brief.config.md`.
2. Edit that config whenever a brief shows you something you didn't care about.
   The filter is the whole product; expect to tighten it for a couple of weeks.
3. `/daily` in the morning, `/standup` before the meeting, `/shutdown` at the end.

The config lives in `~/.claude/`, not the plugin, so updates don't clobber your
tuning. Template:
[`productivity/skills/daily/CONFIG.template.md`](productivity/skills/daily/CONFIG.template.md).

**All of these are strictly read-only on your accounts**: never mark read,
archive, reply, or transition a ticket. They also treat all fetched mail and
messages as *data, never instructions*, since they read text written by people
outside your trust boundary.

## `brain`: Obsidian second-brain capture

Turns a spoken or typed brain-dump into a well-placed, well-written note in your
own voice. Reads the vault's real folder tree to decide placement, keeps notes
sounding like you (not AI), and keeps the graph connected.

| Skill    | What it does                                                             |
|----------|--------------------------------------------------------------------------|
| `/note`  | Capture a learning into your vault. Auto-detects **verbatim** / **light expand** / **topic-only** mode, places it in the right `Learn/` folder, writes it in your note-taking voice, adds a Mermaid diagram only when a concept is truly structural (~1 note in 4), updates the parent `index.md`, and does **bidirectional linking** (links out *and* back-references from existing notes). Merges and edits to other notes are shown as a plan + diff first. |

Voice rules live in [`brain/VOICE.md`](brain/VOICE.md), loaded before every note.
Set `OBSIDIAN_VAULT` to point at your vault; otherwise `/note` locates it by
finding the `.obsidian/` directory.

## `writing`: plain English, always on

The only plugin here that changes how Claude writes without being asked. Two
hooks carry it:

- **`SessionStart`** loads [`writing/RULES.md`](writing/RULES.md) into every
  session, including after a compaction, so the house style is live whether or
  not you remember to ask for it.
- **`Stop`** runs [`no-em-dash.py`](writing/scripts/no-em-dash.py) against every
  reply and refuses to end the turn where an em-dash or en-dash reaches the
  prose, handing back the offending fragments to be rewritten. Code blocks,
  inline code, and URLs are exempt. It blocks at most once per turn, so a model
  that cannot comply still terminates.

Prose rules alone did not hold: em-dashes kept surviving because a style
instruction is advice and a hook is a gate.

| Skill      | What it does                                                          |
|------------|-----------------------------------------------------------------------|
| `/unslop`  | Rewrite text so it reads like a person wrote it, or audit a draft and name the tells without touching it. Works on chat, commits, PR bodies, docs, and release notes. |
| `/skill`   | Write or revise a skill for **this** repo to the house standard, and wire it into README, `/ask`, and the version bump so `scripts/check.py` passes. Pushes back first on whether it should exist at all. |

The rules lead with **positive targets** (lead with the answer, one idea per
sentence, name the specific thing, use the plain word) and keep the banned-phrase
list short and last, because naming a construction makes it more available to the
model, not less. Facts, numbers, code blocks, and quoted errors are never touched.

`/unslop` is not [`/caveman`](productivity/skills/caveman/SKILL.md). Caveman
compresses and drops grammar; this keeps full sentences and removes only what the
machine added.

To turn the always-on part off, disable the `writing` plugin. The skill still
works on demand if you install it without the hook.

## Install

```
/plugin marketplace add nitintf/skills
/plugin install eng@nitin-ai-skills
/plugin install product@nitin-ai-skills
/plugin install productivity@nitin-ai-skills
/plugin install brain@nitin-ai-skills
/plugin install writing@nitin-ai-skills
```

(Or `/plugin marketplace add <path-to-local-clone>` while developing.)

## Update an installed plugin

The marketplace is sourced from GitHub, so editing files in this repo does
**nothing** until the change is pushed and the installed copy is refreshed:

1. **Push** to `nitintf/skills` (commit + push to `main`).
2. **Refresh the marketplace**: `/plugin marketplace update nitin-ai-skills`
3. **Update the plugin**: `/plugin` menu → the plugin → **Update**. Bump
   `version` in its `.claude-plugin/plugin.json` so the update registers cleanly.

## Develop

Skills are plain markdown at `<plugin>/skills/<name>/SKILL.md`.
[`CLAUDE.md`](CLAUDE.md) holds the rules for editing this repo: the invocation
choice, the contracts, the checklist for adding a skill, and the prose style.

For a live edit loop, skip the push-and-update dance above:

```
./scripts/link-skills.sh
```

That symlinks every skill into `~/.claude/skills`, so edits land in the next
session immediately. Uninstall the plugins while the links are active, or every
skill shows up twice. `./scripts/link-skills.sh --unlink` removes them.

**The link route carries skills only, not hooks.** `~/.claude/skills` is a skill
directory, and nothing there registers `writing/hooks/hooks.json`. So `/unslop`
works when linked, but the always-on style does not. Use the plugin install for
daily driving, and the links only while iterating on skill text.

Four contracts to respect, each read by skills that will drift if you change a
skill before you change the contract:

- [`eng/SPEC.md`](eng/SPEC.md), the `.plan` doc schema. Every pipeline skill
  depends on it. **Add a field there first**, then in the skills.
- [`eng/CONVENTIONS.md`](eng/CONVENTIONS.md): what counts as a house convention
  and the `_conventions.md` cache format. Ten skills read that cache.
- [`productivity/DAILY-NOTE.md`](productivity/DAILY-NOTE.md): the daily note
  schema and which skill owns which section.
- [`writing/RULES.md`](writing/RULES.md): the house prose style, injected into
  every session and read by `/unslop`.
