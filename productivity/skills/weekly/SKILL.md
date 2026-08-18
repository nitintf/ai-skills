---
name: weekly
description: >-
  Friday review built from the week's daily notes plus real evidence — commits,
  PRs merged and reviewed, tickets closed, meetings attended. Shows what shipped,
  what slipped and why, where the week actually went versus where you planned it,
  and what to pull into next week. Doubles as your accomplishments log, so at
  review time you have twelve months of evidence instead of trying to remember
  March. Writes to `Daily/Weekly/<YYYY>-W<ww>.md`. Triggers: "weekly", "weekly
  review", "wrap up the week", "what did I do this week", "friday review".
---

# weekly — what the week actually was

A week of shutdowns tells a story no single day can: which work kept sliding,
how much of your time was never yours to plan, and what you actually shipped.
That last one matters more than it seems — **at performance-review time, nobody
can remember March.** This is the record that fixes that.

Not a productivity report card. A factual account, useful to him and directly
reusable in a 1:1 or a self-review.

**Read `${CLAUDE_PLUGIN_ROOT}/DAILY-NOTE.md`** for the daily note schema you're
reading from and the weekly file's location.

## Step 1 — Read the week

Load every `$VAULT/Daily/<date>.md` from Monday to today. From each:

- `## Plan for today` — what he intended, and which boxes are ticked.
- `## Shutdown → ### Done` — what landed.
- `### Didn't get to` — and, crucially, **whether the same item appears across
  several days**. A task carried Monday through Friday is the week's most
  important finding.
- `### Also happened` — unplanned work. Add it up; this is usually the answer to
  "why didn't I get to my actual work".
- `## Notes` — read for context only. **Never edit.**

Missing days are normal (leave, no shutdown run). Note the gap and carry on;
don't treat an absent file as a zero-output day.

## Step 2 — Get the hard evidence

Daily notes record intent and self-report. Cross-check against what's provable —
GitHub MCP if connected, else `gh` and local `git`:

- **Commits** authored this week, grouped by repo.
- **PRs opened, merged, closed.** Merged PRs are the cleanest possible unit of
  "shipped".
- **Reviews given.** Consistently under-counted, genuinely part of the job, and
  the thing most likely to be missing from a self-review.
- **Tickets closed**, and anything that moved to done.
- **Meeting hours** from the calendar — the number that explains most weeks.

Where evidence and notes disagree, trust the evidence and note the discrepancy.

## Step 3 — Find the pattern, not just the list

A list of commits is a log, not a review. Look for what a week reveals that a day
can't:

- **What actually shipped** — the two or three things worth naming.
- **What kept slipping, and why.** A task carried four days isn't a discipline
  problem; it's usually mis-scoped, blocked on someone, or not really the
  priority. Say which.
- **Planned vs unplanned split.** Roughly what share of the week went to work
  that was never on any plan? If it's most of it, that's the finding of the week.
- **Where the time went** — meetings vs focused work.
- **Commitments made and kept**, from the meeting notes. Anything promised and
  not delivered goes into next week rather than quietly disappearing.

## Step 4 — Write it

Write `$VAULT/Daily/Weekly/<YYYY>-W<ww>.md`. New file each week; never overwrite
a previous one.

```markdown
---
week: 2026-W33
range: 2026-08-10 → 2026-08-14
created: <YYYY-MM-DD>
---

# Week 33 — 10-14 Aug

## Shipped
- CSV import for assets — merged (PR 412), live Thursday
- Retry backoff on the payment webhook — merged (PR 418)

## Also did
- Reviewed 7 PRs across `spinquest-frontend` and `zaars-backend`
- Prod incident Wednesday, ~3h — root-caused and fixed

## Slipped
- Migration plan for Raj — carried 4 days. Blocked on the schema decision,
  which only landed Thursday. Not a scoping problem.

## How the week went
- 14 commits across 3 repos, 4 PRs merged, 7 reviews
- ~11h in meetings
- Roughly 40% of the week was unplanned work (incident + urgent reviews)

## Carrying into next week
- [ ] Send Raj the migration plan
- [ ] ACME-244: idempotency keys

## Worth remembering
<For the self-review. The things you'd otherwise forget by December: a hard
problem solved, a decision you drove, someone you unblocked, a fire you put out.
Be concrete and take the credit — this is the section that pays off later.>
- Root-caused the Wednesday payment outage — bad connection pool config under
  load. Fixed and added the alert that would have caught it.
```

## Step 5 — Report

A few lines: what shipped, the one thing that slipped and why, and what's
carrying. Then offer, without pushing:

- Pull the carry-over into Monday's `/daily`.
- Use `## Worth remembering` as 1:1 material.

## Guardrails

- **Evidence over self-report.** Cross-check the notes against commits and PRs.
- **No grading.** No "productive week", no "room for improvement", no score. He
  can read the numbers.
- **Slippage gets a reason, not a shrug.** "Carried 4 days" is half a finding;
  *why* is the other half, and usually it's blocked-on-someone or mis-scoped
  rather than anything about effort.
- **`## Worth remembering` is not bragging** — it's the section that makes the
  whole habit pay off six months later. Fill it honestly and specifically, and
  never leave it empty on a week where something real happened.
- **Read `## Notes`; never edit them.**
- **Don't invent a narrative.** Some weeks are maintenance and meetings. Say so.
