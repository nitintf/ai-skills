---
name: pr-walkthrough
description: >-
  Understand a pull request you did not write, before you judge it. Takes a PR
  number, URL, or branch, pulls the author's stated intent and the linked ticket,
  then maps how the touched subsystem works TODAY on main so the diff is readable,
  names a "start here" file and a dependency-ordered reading path, traces one
  concrete runtime path before vs after, and lists what only the author can
  answer. Explains, it does not judge: no verdict, no blocking list. Hands off to
  `/eng:pr-review` when you want the actual review. Use when a PR is large,
  unfamiliar, or someone else's. Triggers: "explain this PR", "walk me through
  this PR", "help me understand this PR", "what does PR #123 do", "onboard me to
  this change", "I need to review someone else's PR". Do NOT use for: judging a
  change (that's `/eng:pr-review`), a quick re-entry summary of work you already
  know (that's `/catchup`), or your own uncommitted diff (that's `/eng:review`).
---

# pr-walkthrough: understand the change before you have an opinion

Reviewing a diff you don't understand produces nit-picking, because nits are the
only thing visible without context. This skill buys the context. You come out
able to say what the change does, why the author shaped it that way, and where
it touches the rest of the system, **without having formed a verdict yet.**

The bar is the same as the rest of `eng`: **coordinates, not adjectives.** "It
refactors the scheduler" is worthless. ``it moves the guard from
`scheduler.ts:88` into `canWrite()` at `permissions.ts:31`, so every caller now
gets it`` is the deliverable.

**This skill never judges.** No approve, no blocking list, no "should have". The
moment you catch yourself grading, stop and note it as an open question instead.
Judgment is `/eng:pr-review`'s job and it does it better with this in hand.

## 1. Target the PR and decide how you'll read it

The input is a PR number, a URL, a branch name, or nothing (then it's the current
branch's PR). Resolve it first:

```sh
gh pr view <n> --json number,title,body,author,headRefName,baseRefName,labels,\
additions,deletions,changedFiles,comments,reviews,url
gh pr diff <n>
gh pr checks <n>
```

Then pick a mode and **say which one you picked**:

- **Checked out** (`gh pr checkout <n>`): you can open surrounding files, follow
  callers, and run the tests. Required if the user wants to run anything. Only
  do this if `git status` is clean; if it isn't, say so and ask rather than
  stashing someone's work.
- **Read-only** (`gh pr diff` plus reading the base branch): no local state
  touched. Fine for understanding, but you cannot follow a caller into a file the
  diff doesn't include unless it exists on the base branch too.

If `gh` can't see the PR (wrong repo, no auth), stop and say so. Don't guess at
the contents of a PR you can't read.

## 2. Get the intent from outside the diff

A diff tells you what changed. It never tells you what the author was trying to
do. Gather that first, because everything downstream reads differently once you
have it.

- **PR body**: the author's own claim. Note it verbatim-ish; you'll check the
  diff against it later.
- **The commits**: `git log <base>..<head> --stat`. Their grouping and messages
  are the author's own decomposition of the problem. That is usually the best
  reading order anyone will give you.
- **The linked ticket**, which is where the real "why" lives:
  - A ticket key in the branch, title, or commits (`BR-1234`, `PROJ-88`) means a
    Jira-style tracker. Fetch it through the Atlassian MCP tools if they're
    available (`getJiraIssue`), otherwise ask the user to paste it.
  - `Closes #12` / `Fixes #12` means GitHub issues: `gh issue view 12`.
  - Say plainly if there's no ticket and the body is thin. That's a real finding
    about the PR, and it means your open-questions list will be longer.
- **Existing review threads**: `gh pr view --json comments,reviews`. Someone may
  have already answered the question you're about to ask.
- **CI**: red checks are context. Note what's failing; don't diagnose it yet.

## 3. Orient: how does this area work *today*?

**This is the step everything else depends on, and the one people skip.** Before
reading a single changed line, understand the code being changed as it exists on
the base branch. You cannot tell a deliberate choice from a mistake without it.

Bound it to what the PR actually touches. For each area the diff lands in:

- What is this module for, and who calls it? Follow the callers on the base
  branch, not just the file itself.
- Where does state live and what mutates it?
- What are the existing patterns here? **Read `.plan/_conventions.md` if the repo
  has one** (protocol in `${CLAUDE_PLUGIN_ROOT}/SPEC.md` §6), so you're not
  re-deriving house style. For anything the cache doesn't cover, look at a
  neighbouring file that does the same kind of work.

Deliver this as a few lines of "here's the shape of it today", each with a
`file:line`. If the subsystem is genuinely large, say what you covered and what
you left alone.

## 4. Order the diff by dependency, not by filename

GitHub shows you the diff alphabetically, which is close to the worst possible
order for understanding it. Re-order it yourself:

1. **Schema / data model / types**: migrations, table definitions, shared types.
   Everything else is downstream of this shape.
2. **Core logic**: the functions where the new behavior actually lives.
3. **Callers and wiring**: routes, handlers, jobs, components, DI, exports.
4. **Config, flags, infra**: env vars, feature flags, terraform, CI.
5. **Tests**: read them as the author's own spec for the change.
6. **Docs, generated files, lockfiles, snapshots**: skim, note volume, move on.

Name a single **start here** file: the one where the change's intent is clearest.
Then give the reading path as an ordered list of `file:line` entries, each with
one line on why it's next.

Call out the noise explicitly. A 4,000-line diff that's 3,700 lines of generated
client and lockfile churn is a 300-line change, and saying so is most of the
value of a walkthrough.

## 5. Trace the spine

Pick the one path where the behavior actually changes, and walk it end to end
with concrete values. Real inputs, real function names, real files.

> Before: request hits `routes/rental.ts:44`, which calls `assertOwner()` at
> `guards.ts:12`, so a distributor user gets a 403.
> After: `routes/rental.ts:44` calls `assertCanWrite()` at `guards.ts:31`, which
> also passes for a distributor with the `rental:write` scope.

Where the change is data-shaped rather than request-shaped, trace the record
instead: what gets written, by whom, and what reads it afterwards.

If the change has more than one interesting path (a happy path plus a migration
path, say), trace both. Two is usually the limit before this stops being a spine
and starts being a transcript.

## 6. Find the seams

The bugs in someone else's PR live where their change meets code they didn't
open. Enumerate those edges, without judging them:

- Callers of every changed signature, including ones the diff didn't touch.
- Anything reading the same data the change writes, or writing what it reads.
- Ordering constraints: deploy order, migration vs code, feature-flag state,
  background jobs mid-flight.
- Contracts that cross a boundary: API responses, events, queue payloads, shared
  types consumed by another service or the frontend.

For each, say what it is and where. `/eng:pr-review` turns these into findings;
your job is to make sure none of them go unnoticed.

## 7. Deliver the walkthrough

Output to chat. Write a file only if asked; if the user wants it kept, save to
`.plan/_research/pr-<n>-walkthrough.md`.

- **What this PR does**: two or three sentences, in your words, not the author's.
- **Why**: the ticket's problem statement, and the author's stated approach.
  Flag it if the body and the diff disagree, as an observation, not a verdict.
- **The area today**: the §3 orientation, a few lines with `file:line`.
- **Start here**, then the **reading path**: ordered, each entry one line.
- **The spine**: the before/after trace from §5.
- **Seams and blast radius**: §6, as a list.
- **Size, honestly**: real lines vs generated noise; CI state.
- **Open questions for the author**: things the diff genuinely cannot answer.
  Phrase them as questions ("what happens if this runs twice?"), never as
  accusations. These are the highest-value output of the whole skill.

Close with the handoff, one line: *"Want the actual review? Run `/eng:pr-review`
and it'll pick up from here."*

## 8. Stay honest

- Never explain code you didn't read. "I didn't open the migration" is a fine
  sentence; inventing what it does is not.
- Don't launder the PR description into a summary. If your walkthrough could have
  been written from the body alone, you skipped §3 and §5.
- Resist the verdict. Every time you want to write "this is wrong", write "does
  this handle X?" in Open questions instead and let the review stage settle it.
- The author is not in the room. Assume competence and missing context on your
  side, not theirs.
