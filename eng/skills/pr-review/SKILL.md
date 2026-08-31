---
name: pr-review
description: >-
  Staff/principal-engineer review of a pull request, yours or someone else's.
  Takes a PR number, URL, branch, or the current branch, reads the commits and
  diff against the base, pulls extra context from GitHub via `gh` (PR description,
  CI, existing review threads) and the linked ticket from whichever tracker the
  repo uses, then reviews the change the way a senior reviewer actually does:
  correctness and edge cases first, then architecture, then, critically,
  consistency with how THIS codebase already builds things, so the code reads
  like the team wrote it. Runs standalone but reads the `.plan` doc and
  conventions cache when they exist, so it can review against the agreed
  acceptance criteria and record findings that contradict the plan. For a big or
  unfamiliar PR, run `/eng:pr-walkthrough` first and review with that in hand.
  Use when the user wants a PR or branch reviewed before it lands. Triggers:
  "review this PR", "pr review", "review PR #123", "review my branch", "review
  before I merge", "code review this". Do NOT use for: explaining a change
  without judging it (that's `/eng:pr-walkthrough`) or an uncommitted working
  diff (that's `/eng:review`).
---

# pr-review: review a PR like a staff/principal engineer would

You are reviewing a change before it lands. A junior reviewer rubber-stamps the
diff line by line. A staff/principal engineer asks: *is this the right change,
is it correct, will it age well, and does it look like our codebase?* Your job is
the latter. Be specific, cite `file:line`, and separate **blocking** issues from
**nits** so the author knows what actually gates the merge.

## 1. Establish what you're reviewing

Figure out the target, then gather the context. Don't review blind.

**Pick the target first.** The user may hand you a PR number or URL, a branch
name, or nothing at all.

- **A PR number / URL** (usually someone else's work): `gh pr view <n>` for the
  metadata, then either `gh pr checkout <n>` so you can open surrounding files
  and run tests, or `gh pr diff <n>` read-only. Check out only when `git status`
  is clean; if it isn't, say so and ask rather than stashing the user's work.
  Whichever you pick, `<base>` below is the PR's base branch, not necessarily
  `main`.
- **Nothing given**: the current branch, and its PR if one exists.

**If the PR is large or lands in code you don't know, run
`/eng:pr-walkthrough` first.** It maps how the area works today, orders the diff
by dependency, and traces the runtime path. Reviewing an unfamiliar subsystem
without that step produces nits, because nits are all that's visible without
context. If a walkthrough already ran in this session, build on it: don't redo
§1 and §2 from scratch.

- **The change itself**: the branch vs its base:
  - `git merge-base HEAD <base>` to find the fork point, then
    `git diff <merge-base>...HEAD` for the real diff (three-dot: only what THIS
    branch changed, not unrelated drift on the base branch).
  - `git log <merge-base>..HEAD --stat`, read the commits. The commit messages
    and their grouping tell you the author's intent and the story of the change.
- **GitHub context via `gh`** (if the branch has a PR: `gh pr view` to check):
  - `gh pr view --json title,body,labels,comments,reviews,files,additions,deletions`
    gives the PR description (what they say it does + why), labels, and any existing
    review threads so you don't repeat points already raised.
  - `gh pr diff` as a cross-check on the local diff.
  - `gh pr checks`, CI status. A red build is context: don't praise tests that
    aren't passing.
  - **The linked ticket**, so you can judge the change against what it was
    *supposed* to do. Use whichever tracker the repo actually uses: a key like
    `BR-1234` or `PROJ-88` in the branch, title, or commits means Jira, so fetch
    it with the Atlassian MCP tools (`getJiraIssue`) when they're available;
    `Closes #N` in the body means GitHub issues, so `gh issue view N`. If there's
    no ticket and the body is thin, say so: it limits what you can assert about
    intent.
- If there's no PR yet, review the branch diff directly and say so.

**Read enough of the diff to understand intent, not just the changed lines.**
Open the surrounding code and the files the change calls into: a diff reviewed
in isolation hides the bugs that live at the seams.

## 2. Learn the house style before you judge

This is what separates a staff review from a linter. Before you call something
wrong, know how the codebase already does it.

**Start with `.plan/_conventions.md`** if the repo has one (protocol in
`${CLAUDE_PLUGIN_ROOT}/SPEC.md` §6): it's the recorded house style, so your
review judges against the same standard `/scope` planned against instead of one
you improvise. Check its `commit:` for staleness. Then verify against real code
for the specific things this PR touches:

- How are APIs / endpoints / services / handlers defined here?
- How are components structured (props, state, styling, file layout)?
- Error handling, logging, config access, validation, async patterns.
- Naming, folder conventions, and, crucially, the existing **test style**.
- **Did the PR reinvent an existing primitive?** Check the cache's primitives
  table against anything new the diff introduces.

The bar: *would a teammate reading this PR be able to tell it was written by
someone new?* If yes, that's a finding. Point at the file:line of the pattern it
should have followed.

**If a `.plan` doc exists for this work**, read it too. Reviewing against the
stated acceptance criteria is far stronger than reviewing the diff alone: you
can check whether what was built is what was agreed, and spot scope creep against
the `## Scope → Out` list.

## 3. Review dimensions

Work top-down, correctness gates the merge; polish doesn't. For each finding,
give the `file:line`, say *why* it matters, and propose the fix.

1. **Correctness & edge cases**: does it do what the PR/issue claims? Empty,
   null, duplicate, malformed, concurrent, and boundary inputs. Off-by-ones,
   error paths that swallow failures, conditions inverted under refactor.
2. **Architecture & design**: right shape for the problem? Over- or
   under-engineered? Leaky abstractions, wrong layer, responsibilities in the
   wrong place, coupling that will hurt later. Is there a simpler change that
   does the same job?
3. **Consistency with the codebase**: the dimension you must not skip (§2).
   Reinventing a helper that exists, diverging from house patterns, one-off
   styles. Cite the pattern to follow.
4. **Security & data safety**: trust boundaries, injection (SQL/command/
   template), authz checks, secrets in code/logs, unsafe deserialization, and
   for any LLM-touching code, prompt-injection / unvalidated model output.
5. **Tests**: do the tests actually prove the change? Do they follow the repo's
   test conventions? Missing edge-case coverage, tests that assert nothing,
   over-mocked tests that pass regardless of the code.
6. **Performance & scale**: N+1 queries, unbounded loops/allocations, work in a
   hot path, payloads that won't hold at real data sizes. Flag only where it
   plausibly bites, don't micro-optimize.
7. **Migration & backward compatibility**: schema changes, data backfills,
   rollback path, API/contract breaks, feature-flag and deploy ordering.
8. **Readability & maintainability**: naming, dead code, stray debug logs,
   commented-out blocks, missing context on genuinely non-obvious code. (Nits,
   unless they obscure correctness.)

## 4. Deliver the review

Output to chat (write a file only if asked). Structure it so the author can act:

- **Verdict**: one line. ✅ approve / 🟡 approve with comments / 🔴 request
  changes, plus a one-sentence summary of the change and its overall quality.
- **What's good**: call out genuinely solid choices. Real, not filler; a staff
  review reinforces good patterns, it doesn't only hunt for faults.
- **Blocking**: issues that must be fixed before merge. Each: `file:line`, the
  problem, why it matters, and the suggested fix. Empty is a fine answer.
- **Non-blocking / nits**: improvements and style that shouldn't gate the merge.
  Label them clearly so they don't read as blockers.
- **Open questions**: things you genuinely can't resolve from the diff; ask the
  author rather than guessing their intent.

## 5. Close the loop (only if a `.plan` doc exists)

A review that finds the plan was wrong and doesn't record it wastes the finding.
When a blocking issue **contradicts the plan**: an acceptance criterion that
isn't actually met, scope that crept past the `Out` list, a convention the plan
prescribed that turned out not to exist: append a dated entry to the doc's
`## Work Log` saying so. Don't rewrite the plan's other sections; the Work Log is
where reality goes.

Ask before writing. If there's no doc, skip this entirely.

## 6. Stay honest

- Don't invent rationale for code you don't understand, say what's unclear and
  ask. A confident-wrong review is worse than a question.
- Don't pad the count. Three real blocking issues beat fifteen nits.
- Severity is the whole point: never let a real bug sit in the same bucket as a
  naming nit. If nothing blocks, say so plainly and approve.
- You review and report; you don't merge. Offer to apply fixes if the user wants,
  but landing the PR is their call.
