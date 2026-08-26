---
name: skill
description: Write or revise a skill for this repo, to the house standard, and wire it up so the checks pass.
disable-model-invocation: true
argument-hint: "What should the skill do?"
---

# skill: author a skill for this repo

Write a new `SKILL.md`, or bring an existing one up to standard, and leave the
repo passing `scripts/check.py`.

Read [`CLAUDE.md`](../../../CLAUDE.md) first. It holds the invariants this skill
implements, and it wins wherever the two disagree.

## Step 1: Decide it should exist

Push back before writing. The repo has thirty skills, and each one the user has
to remember is a cost.

| Situation | Do this instead |
|---|---|
| An existing skill covers it with one more branch | Add the branch to that skill. |
| It is a one-off | Just do the task. |
| It is a fact, not a process | Put it in a reference file, and point at it. |
| Two skills would both need it | Write it as one model-invoked skill both can call. |

A skill earns its place when it encodes a **process worth repeating exactly**,
and the agent gets it wrong without the instructions. Say which of those two is
true before continuing.

## Step 2: Choose the invocation

The one decision that costs on every turn of every session.

Ask: **could the model usefully reach for this on its own?**

| Answer | Invocation | Frontmatter |
|---|---|---|
| No, the user always types it | User-invoked | `disable-model-invocation: true`, description is one human-facing line with no trigger list |
| Yes, the agent should fire it autonomously, or another skill must call it | Model-invoked | Omit the field, description carries rich trigger phrasing |

Default to user-invoked. Reuse is not the test, and "it would be nice if it fired
sometimes" is not the test. Only genuine autonomous reach earns the permanent
context cost.

Where you pick model-invoked, write the reason down. It goes in the commit.

## Step 3: Write it

Structure follows the work, not a template. A process skill is ordered steps; a
reference skill is a flat rule set; many are both. What holds either way:

- **Lead the body with the skill's job** in a sentence, and its **defining
  constraint**: the one fact that makes it behave differently from the obvious
  default. For `/migrate` that is writing the rollback before the migration.
- **Prompt the positive.** State the target behavior. Naming a banned behavior
  makes it more available to the model, not less, so prohibitions are for hard
  guardrails only, and each one is paired with the positive target.
- **Branches go in tables**, never in a paragraph. The reader is scanning for the
  one row that matches their situation.
- **Push reference behind a pointer** when only some runs need it. Inline what
  every run needs. A sibling file in the skill's own folder is the usual home.
- **Point at a single source of truth**, never restate one. `SPEC.md`,
  `CONVENTIONS.md`, `DAILY-NOTE.md`, and `RULES.md` are all contracts other
  skills read; a skill that copies one will drift from it.
- **Reach a named skill by telling the agent to call the Skill tool with it.**
  This only works for model-invoked skills. For a user-invoked precondition, tell
  the user to run it.
- **End on `## Done when`**, with bounds the agent can actually check. "Every
  claim links to its source" is checkable. "Understanding reached" is not.

Prose follows [`writing/RULES.md`](../../RULES.md), the same as everything else
here. **No em-dashes.**

Then cut. Delete any sentence the model would obey by default: it costs context
to say nothing. Test each one by asking whether behavior changes without it.

## Step 4: Wire it up

All five, or `scripts/check.py` fails:

1. `<plugin>/skills/<name>/SKILL.md`, where the directory name matches `name:`.
2. A row in `README.md`, in the right plugin's table.
3. A row in [`/ask`](../../../productivity/skills/ask/SKILL.md), in the right
   group. A router that omits a skill is a router that lies.
4. Bump `version` in that plugin's `.claude-plugin/plugin.json`.
5. Run `python3 scripts/check.py` and `claude plugin validate . --strict`.

Write the description as a `>-` folded block. A bare `": "` in an unquoted YAML
scalar parses as a mapping, and Claude Code's own validator accepts it and then
silently drops every frontmatter field at runtime.

## Revising an existing skill

Same standard, plus: renaming means updating `README.md`, `/ask`, and the
directory together. Removing means deleting its rows from both.

Where a skill has grown past roughly 150 lines, look for reference to push into a
sibling file rather than trimming words. Length is usually a hierarchy problem.

## Done when

- The reason it is a skill and not a branch of an existing one is stated.
- The invocation choice is made deliberately, and a model-invoked choice carries
  its reason.
- The body opens with the job and the defining constraint.
- Every branch is a table or a list.
- `## Done when` bounds are checkable without opening the skill.
- No em-dash, and the description is a `>-` block.
- README, `/ask`, and the plugin version are all updated.
- `python3 scripts/check.py` and `claude plugin validate . --strict` both pass.
