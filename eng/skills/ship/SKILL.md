---
name: ship
description: >-
  Land finished work: review the diff, split it into atomic commits in the
  repo's style, push, and open a PR whose body comes from the `.plan` doc.
disable-model-invocation: true
---

# ship: turn finished work into clean commits and a PR someone will enjoy reviewing

The pipeline's last mile. `execute` proved the code works; your job is to make it
**land well**. A reviewer's experience is decided almost entirely here: whether
the commits tell a story, and whether the PR description answers "what is this
and why" before they read a single line of the diff.

You already have the raw material for a great PR description: the `.plan` doc
contains the problem, the scope, the acceptance criteria, and the deviations. Use
it. Never write a PR body that just restates the diff.

**If a `.plan` doc exists**, read `${CLAUDE_PLUGIN_ROOT}/SPEC.md` and the ticket
doc first. **If it doesn't**, that's fine: work from the diff and the branch,
and skip the doc-updating steps.

## 1. Establish what's landing

- `git status`: anything uncommitted or untracked that belongs in this change?
- `git log <main>..HEAD --stat` and `git diff <main>...HEAD`: the full picture
  of what this branch does.
- Confirm the branch isn't the main branch. If the user is sitting on `main`
  with uncommitted work, create a branch first: never commit straight to main
  unless they explicitly ask.

**Read the diff as a reviewer before you package it.** If something in it is
obviously wrong, half-finished, or a leftover debug line, say so now: shipping
it and then reviewing it is backwards. Point at `/review` if it warrants a real
pass.

## 2. Check the gates

Don't ship work that isn't finished. Quickly verify, and report honestly rather
than blocking on perfection:

- **Tests pass.** Run the repo's test command. A red suite is a stop.
- **Acceptance criteria** (if there's a doc), are they all checked off? An
  unchecked criterion means `execute` isn't done; surface it and ask.
- **Lint / typecheck / format**: run whatever the repo enforces in CI. Failing
  CI on the first push wastes a review cycle.
- **Nothing secret.** Scan the diff for keys, tokens, `.env` files, credentials,
  or a real customer's data in a fixture. This is the one gate you never wave
  through.

## 3. Match the repo's commit conventions

Read `.plan/_conventions.md` if it exists (see `SPEC.md` §6) for the commit and
branch conventions; otherwise derive them from `git log --oneline -30`:

- Conventional Commits (`feat:` / `fix:` / `chore:`)? A ticket prefix
  (`PROJ-123: …`)? Sentence case or lowercase? Scope in parens?
- Typical commit size: does this team squash everything into one, or land
  reviewable series?

Match what you see. A commit that doesn't look like the last thirty is a smell.

## 4. Build the commit(s)

Prefer **a small series of atomic commits** over one giant blob, when the change
genuinely has parts (e.g. `refactor: extract the parser` → `feat: add CSV
import` → `test: cover duplicate asset IDs`). Each commit should build and pass
tests on its own.

Collapse to a single commit when the change really is one idea, or when the
repo's history shows that's the house norm.

For each commit message:
- **Subject**: imperative, in the repo's convention, under ~72 chars.
- **Body** (when it's not self-evident), *why*, not what. The diff says what.
  Pull the "why" from the doc's `## Problem / Context`.
- Never invent a ticket ID. Use the one in the doc's frontmatter, or none.

Show the user the planned commit breakdown and messages **before committing**.

## 5. Push and open the PR

Push the branch (set upstream if needed). Then open the PR with `gh pr create`.

If the repo has a PR template (`.github/pull_request_template.md`), **fill that
template** rather than imposing your own structure. Otherwise:

```markdown
## What
<2-3 sentences. What this change does, in the reader's terms.>

## Why
<From the doc's Problem / Context. The reason this exists.>

## How
<The approach, and any non-obvious decision: pulled from Decisions / the Eng
Review Verdict. Call out anything a reviewer would otherwise have to reverse-
engineer from the diff.>

## Acceptance criteria
<The doc's criteria, as a checked list. This is what "done" meant.>
- [x] …

## Testing
<What tests were added, what was manually verified from the QA checklist.>

## Notes for the reviewer
<Deviations from plan (plan said X, reality was Y) from the Work Log. Known
gaps, follow-ups filed, anything explicitly out of scope. The honest section.>
```

Link the issue if there is one (`Closes #N`). Add labels and reviewers only if
the repo's recent PRs show that's the norm, don't assign people uninvited.

**Confirm with the user before pushing and before creating the PR.** Both are
outward-facing and hard to take back. Draft PR is a good default if they're
unsure.

## 6. Close the loop in the doc

If a `.plan` doc exists:
- Set frontmatter `phase: shipped` and `pr: <url>`.
- Append to `## Work Log`: the PR link, the commits landed, and anything the
  shipping pass surfaced.
- Update the feature `README.md` table (phase + branch).

Then summarize: PR URL, what's in it, what still needs a human (review, QA steps
you couldn't run, follow-ups).

## Guardrails

- **Confirm before push and before PR creation.** These are outward-facing. An
  approval to commit is not an approval to push.
- **Never force-push** a shared branch, rewrite published history, or merge the
  PR. Landing it is the user's call and usually their team's process.
- **Never ship a red suite or an unchecked acceptance criterion silently.** Say
  what's failing and let the user decide.
- **Secrets are a hard stop**, not a warning.
- Don't pad the PR body. A reviewer skims; three honest sentences beat a page of
  generated ceremony.
