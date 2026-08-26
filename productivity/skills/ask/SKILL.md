---
name: ask
description: Ask which skill or flow fits your situation. A router over every skill in this repo, and the one skill to remember when you cannot remember the others.
disable-model-invocation: true
argument-hint: "What are you trying to do?"
---

Read the user's situation, name the one skill that fits, and say why in a
sentence. Where two are confusable, say which one and what the other is for.

If they gave no situation, print the map below and ask what they are working on.

Recommend one skill. A list of four is the cognitive load this skill exists to
remove.

## The eng pipeline

Six passes over one shared markdown doc in the project's `.plan/` folder. Each
runs solo or chained. The doc holds all state.

`/scope` -> `/grill` -> `/eng-review` -> `/tdd` -> `/execute` -> `/ship`

| Reach for | When |
|---|---|
| `/scope` | You have a task and no plan. Always the front door. |
| `/grill` | A scope doc exists and its open questions are still open. |
| `/eng-review` | The requirements are settled and you want the architecture challenged. |
| `/tdd` | The plan is locked and you need the test contract before any code. |
| `/execute` | The doc is fully planned and you want it built. |
| `/ship` | The work is done and needs commits, a push, and a PR. |
| `/eng-flow` | You want the whole pipeline run for you, gated between passes. Also resumes a flow. |

`/scope` proposes a **track**: `full` runs all six, `express` runs scope, tdd,
execute, ship for small well-understood work with no open questions.

## Engineering, standalone

| Reach for | When |
|---|---|
| `/conventions` | First run in a new repo. Caches house style to `.plan/_conventions.md`, which ten other skills read. |
| `/understand` | "How does X work?" or "map this repo for me." Answers with file:line evidence. |
| `/debug` | Something is broken and you want the root cause, not a guess. |
| `/spike` | "Which of these approaches should we take?" Ends in a recommendation. |
| `/adr` | A costly-to-reverse decision was made and should survive in the record. |
| `/refactor` | Reshape code without changing what it does. |
| `/backfill-tests` | Existing code has no tests and you need a safety net. |
| `/review` | Quick gut-check on the uncommitted working diff, right before you commit. |
| `/pr-review` | Full staff-level review of the branch against main, with GitHub context, before merge. |

`/understand` answers "how does this work". `/spike` answers "which should we
use". `/review` is pre-commit and local; `/pr-review` is pre-merge and pulls
`gh` context.

## Product

| Reach for | When |
|---|---|
| `/prd` | The problem needs stating properly before anyone builds. |
| `/user-stories` | A PRD or epic needs slicing into shippable, testable stories. |
| `/product-flow` | An idea needs the whole run: PRD, stories, then handoff to `/scope`. |

## The day loop

One file per day. `/daily` opens it, `/shutdown` closes it, tomorrow's `/daily`
carries forward whatever did not land.

| Reach for | When |
|---|---|
| `/daily` | Morning. Builds the brief and today's task list. |
| `/standup` | Before the meeting. Prints a speakable update, writes nothing. |
| `/shutdown` | End of day. Ticks off the plan from real evidence. |
| `/weekly` | Friday. What shipped, what slipped, and your accomplishments log. |

## Everything else

| Reach for | When |
|---|---|
| `/catchup` | You have been away and need to know what changed on a branch, PR, or range. |
| `/handoff` | This session is ending and another agent picks the work up. |
| `/stress-test` | Any plan or design needs holes poked in it. Not tied to `.plan` docs; use `/grill` for those. |
| `/caveman` | You want compressed replies for a while. |
| `/unslop` | Some text reads like AI wrote it. Rewrites or audits it. |
| `/note` | You just learned something and it belongs in the Obsidian vault. |

## Reaching for nothing

Plenty of work needs no skill. If the answer is "just do it", say that rather
than routing them into a pipeline a two-line change does not need.
