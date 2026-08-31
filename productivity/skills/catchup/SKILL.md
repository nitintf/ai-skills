---
name: catchup
description: >-
  Summarize what changed so you can re-enter work fast. Given a branch, PR,
  commit range, file, or "since yesterday", it reads the diff/commits and
  produces a tight summary: what changed, why, risk areas, and what's left.
  Great for resuming after a break, reviewing what a teammate pushed, or before
  picking up a PR. Use when the user asks what changed or wants to get back up to
  speed. Triggers: "catch me up", "catchup", "what changed", "what did I miss",
  "summarize this branch/PR/diff", "since I last looked". Do NOT use for:
  understanding someone else's PR in depth before reviewing it, that's
  `/eng:pr-walkthrough`; this is a fast summary, not a walkthrough.
---

# catchup: get back up to speed fast

Produce a concise, accurate summary of what changed in a scope the user gives
you, so they can resume or review without reading every line.

## Steps

### 1. Determine the scope
Figure out what to summarize from the user's request:
- a **branch** → diff vs its merge-base with the main branch
- a **PR** (number/URL) → use `gh pr diff` / `gh pr view`
- a **commit range** (`abc..def`) or "since \<date>" → `git log` + `git diff`
- a **file/dir** → recent history for that path
- "what did I miss" with no scope → recent commits on the current branch since
  the user's last activity (ask if ambiguous)

### 2. Read the actual changes
Use `git log --stat`, `git diff`, and `gh` as needed. Read enough of the diff to
understand intent, not just file names. Don't guess.

### 3. Summarize: tight and structured
Output to chat (no file unless asked):

- **TL;DR**: 1-2 sentences, the gist of what changed and why.
- **Changes**: grouped by area/feature, each with the *why*, not just the what.
- **Risk / watch-out areas**: anything subtle, breaking, migration-related, or
  worth a closer look in review.
- **What's left / next**: open TODOs, failing checks, unfinished threads (if
  detectable from commits, comments, or `.plan` docs).

### 4. Keep it honest
If something is unclear from the diff alone, say so rather than inventing
rationale. Cite `file:line` or commit SHAs so the user can jump in.
