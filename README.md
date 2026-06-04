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

The doc schema every skill obeys is the keystone: see [`eng/SPEC.md`](eng/SPEC.md).

#### Doc layout (in the target project)

```
<project>/.plan/<feature-slug>/
  README.md                     # feature index + per-ticket status
  <NN>-<ticket-slug>/doc.md     # one self-contained doc per ticket
```

`.plan/` is committed so the plan lives in history (plan-said-X vs reality-was-Y).

## Install

Add this repo as a marketplace, then install the `eng` plugin:

```
/plugin marketplace add nitintf/ai-skills
/plugin install eng@nitin-ai-skills
```

(Or `/plugin marketplace add <path-to-local-clone>` while developing.)

## Develop

Skills are plain markdown at `eng/skills/<name>/SKILL.md`. Edit and reload. When
adding a field or section, update `eng/SPEC.md` **first** — it's the contract all
the skills depend on.
