# Daily Note Schema: the contract `/daily`, `/shutdown`, `/standup` and `/weekly` obey

**One file per day.** `/daily` creates it in the morning, `/shutdown` edits the
*same* file in the evening, `/standup` reads it, `/weekly` reads a week of them.
Nothing here ever creates a second file for the same date.

That only works if every skill agrees on the sections below and, critically,
**edits only the sections it owns**. This file is the agreement.

```
$VAULT/Daily/<YYYY-MM-DD>.md            # the daily note
$VAULT/Daily/Weekly/<YYYY>-W<ww>.md     # the weekly review (different cadence, own file)
```

Resolve `$VAULT` from `$OBSIDIAN_VAULT`, else the directory containing
`.obsidian/`, else ask. **Never write to a guessed path.**

---

## 1. The file

```markdown
---
date: 2026-08-13
brief: 09:12          # set by /daily on first run
shutdown: 18:40       # set by /shutdown
carried: 2            # count of tasks carried in from yesterday
---

# Thursday 13 Aug

## Today
<calendar. Owned by /daily.>
09:30  Standup (15m)
14:00  Design review, Payments   ⚠️ you're presenting, no deck yet

## Needs you
<mail / slack / tickets that need a reply. Owned by /daily.>
- **Sarah** (email), Q3 numbers, wants them by EOD

## From yesterday's meetings
<commitments, decisions, action items from Wispr Flow. Owned by /daily.>
- You told Raj you'd send the migration plan, *Design review, 14:20*

## Carried over
<what yesterday's Shutdown marked as not done. Owned by /daily.>
- Migration plan for Raj  *(2nd day)*

## Plan for today
<THE task list. /daily writes it unchecked; /shutdown ticks the boxes.
This is the spine of the whole loop: see §3.>
- [ ] Send Raj the migration plan
- [ ] Review PR 412
- [ ] ACME-231: implement retry backoff

---

## Notes
<Nitin's own. Every skill READS this. No skill EDITS it: never rewritten,
reformatted, or reordered. Read-and-use, not read-and-ignore.>

---

## Shutdown
<Owned by /shutdown. Absent until the evening run.>

### Done
- Reviewed PR 412: approved
- ACME-231 retry backoff, pushed to `feat/retry-backoff`

### Didn't get to
- Send Raj the migration plan  *(2nd day)*

### Also happened
<unplanned work that ate the day, from git, PRs, meetings. This is what makes
the "why didn't I finish" question answerable.>
- Prod incident, ~2h, hotfix in `spinquest-backend`

### Tomorrow's first thing
- Send Raj the migration plan, before standup
```

---

## 2. Section ownership: who may write what

| Section | Created by | May edit | Never touched by |
|---|---|---|---|
| frontmatter | `/daily` | `/daily`, `/shutdown` |, |
| `## Today` | `/daily` | `/daily` | `/shutdown` |
| `## Needs you` | `/daily` | `/daily` | `/shutdown` |
| `## From yesterday's meetings` | `/daily` | `/daily` | `/shutdown` |
| `## Carried over` | `/daily` | `/daily` | `/shutdown` |
| `## Plan for today` | `/daily` | `/daily` writes items; **`/shutdown` only toggles `[ ]`→`[x]`** |, |
| `## Notes` | `/daily` (empty) | **nobody** | **everyone, every run** |
| `## Shutdown` | `/shutdown` | `/shutdown` | `/daily` |

Hard rules:

- **`## Notes` is read by every skill and edited by none.** Two separate rules,
  and the second one keeps eating the first. Skills have been treating the
  section as a no-go zone and skipping it entirely, which throws away the only
  input in this file that Nitin wrote himself.
  - **Read it, every run.** `/daily` reads yesterday's before planning today.
    `/shutdown` reads today's before grading. `/weekly` reads all five.
  - **Use what is in it.** It outranks inference: a note saying a task is blocked
    beats your guess from the commit log. Where it contradicts the evidence, say
    both.
  - **Never edit it.** No rewriting, reformatting, reordering, or tidying. Add
    what you learned from it to your own sections instead.
- **`/shutdown` never rewrites a task's text**, only its checkbox. If the task as
  written was wrong, say so in `### Also happened`, don't silently edit history.
- **Re-running a skill updates its own sections in place.** `/daily` run twice in
  a morning refreshes Today / Needs you; it does not duplicate them, and it does
  not clear checkboxes the user already ticked by hand.
- **If the file exists, read it fully before writing.** Preserve everything you
  don't own.

---

## 3. The carry-over loop: the reason this schema exists

The point of one file per day, and the thing that makes the pair worth more than
either skill alone:

```
/daily  → writes "## Plan for today", unchecked
          ↓
you work the day
          ↓
/shutdown → ticks what got done
          → lists the rest under "### Didn't get to"
          ↓
next morning
          ↓
/daily  → reads yesterday's "### Didn't get to"
          → puts it in "## Carried over"
          → seeds it into today's "## Plan for today"
```

**Yesterday** means the most recent existing daily note, not literally
`today - 1`. A Monday brief picks up Friday's shutdown; a brief after a week off
picks up the last day you worked, and says how long the gap was.

### Age tracking

Every carried task keeps a day count: `*(2nd day)*`, `*(3rd day)*`.

**At 3+ days, `/daily` must call it out** rather than silently carrying it again:

> "Migration plan for Raj has moved 4 days. Cut it, schedule it, or delegate it:
> carrying it a fifth time isn't a plan."

A task that quietly rolls forever is the exact failure this loop exists to
prevent. Surfacing it is more valuable than moving it.

---

## 4. Task list rules (`## Plan for today`)

- **3-5 items. Five is the ceiling.** A 12-item list is a wish, not a plan, and
  guarantees a demoralizing shutdown. If more is genuinely pending, pick the
  five that matter and say what you left out.
- **Ordered**, most important first. The first item should be the one that would
  make the day a success on its own.
- Carried-over items go **first** unless something today is genuinely more urgent.
- Each item is **concrete and finishable in a day**: "Send Raj the migration
  plan", not "work on migrations". A task you can't tick is a bad task.
- Anchor to the source where there is one: ticket ID, PR number, person's name.
- **`/daily` proposes the list and the user can edit it.** It's their day.

---

## 5. Anchors for editing

Skills find their section by exact `##` heading match. When editing:

1. Read the whole file.
2. Locate your section by heading.
3. Replace only the content between that heading and the next `##` at the same
   level.
4. Write the file back whole.

If a heading is missing, insert it in the schema's order: never append your
section to the bottom of the file.
