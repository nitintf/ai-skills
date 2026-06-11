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

The five pipeline skills obey the doc schema in [`eng/SPEC.md`](eng/SPEC.md);
`/pr-review` is independent of it.

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

## Install

Add this repo as a marketplace, then install the plugins you want:

```
/plugin marketplace add nitintf/ai-skills
/plugin install eng@nitin-ai-skills
/plugin install product@nitin-ai-skills
/plugin install productivity@nitin-ai-skills
```

(Or `/plugin marketplace add <path-to-local-clone>` while developing.)

## Develop

Skills are plain markdown at `eng/skills/<name>/SKILL.md`. Edit and reload. When
adding a field or section, update `eng/SPEC.md` **first** — it's the contract all
the skills depend on.
