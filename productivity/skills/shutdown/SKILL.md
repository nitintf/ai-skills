---
name: shutdown
description: >-
  Close the day: tick off this morning's plan using real evidence from commits,
  PRs, and tickets, record what slipped, and set tomorrow's first thing.
disable-model-invocation: true
---

# shutdown: close the loop on the day you actually had

`/daily` opened the day with a plan. You close it with the truth. The gap between
those two is the most useful thing this pair produces: not as a scolding, but
because **the reason you didn't finish is usually more interesting than the fact
that you didn't**. An incident ate three hours. Two "quick" reviews weren't. A
task was never really a one-day task.

You are also the memory. Anything left undone here is what tomorrow's `/daily`
picks up, so an honest shutdown is what keeps the loop from leaking.

**Read `${CLAUDE_PLUGIN_ROOT}/DAILY-NOTE.md` first**: the daily note schema,
and specifically §2, which says exactly what you may and may not edit.

## Step 1: Load this morning's plan

Read `$VAULT/Daily/<today>.md`.

- **No note for today?** `/daily` never ran. Don't fail: reconstruct the day
  from evidence (Step 2) and write a Shutdown section anyway, noting there was
  no plan to compare against. A day without a morning brief still deserves a
  record.
- **Note exists** → take `## Plan for today` as the list you're grading, then
  read `## Notes` in full before grading a single item.

### `## Notes` is evidence, and it is first-hand

Read the whole section, every run, even when it reads like scratch. Commits and
tickets tell you what landed; his notes tell you what happened. Only one of those
sources knows a task died because a meeting ran long.

Use it for:

| What you find there | How it changes the Shutdown |
|---|---|
| Work with no commit and no ticket (a call, a doc, a decision, unblocking someone) | Goes in `### Also happened`. This is the single biggest source of invisible work. |
| The reason a planned task stalled | Goes beside the task in `### Didn't get to`. A reason beats a bare carry-over. |
| A task done outside the tools (verbally agreed, done in a dashboard) | Grounds for ticking it in `### Done`, even with no commit. |
| Something he flagged for tomorrow | A strong candidate for `### Tomorrow's first thing`. |

Where his notes and the hard evidence disagree, **report both** rather than
picking. "Notes say the migration plan went to Raj; no message or commit found"
is the useful output. Silently trusting either one is not.

Never edit the section. What you learn from it goes into your own Shutdown
sections.

## Step 2: Gather evidence of what actually happened

Don't ask him to recite his day. Go find it.

### Code: the strongest evidence
Prefer the **GitHub MCP** if it's connected; otherwise `gh` CLI and local `git`
work fine and are usually faster. Cover both remote and local, because work that
isn't pushed still happened:

- **Commits you authored today**, across the repos you actually touched. Locally:
  `git log --author=<you> --since=midnight --oneline` in each recently-modified
  repo under your code directory. Remotely: `gh search commits --author=@me`.
- **PRs**: opened, merged, or closed today (`gh pr list --author @me`).
- **Reviews you gave**: easy to forget, real work, and often the thing that
  unblocked someone else.
- **Uncommitted work in progress**: `git status` on repos with changes. This is
  frequently where "what I didn't finish" actually lives.

### Tickets
Issues you moved, closed, or commented on today. **Your own actions only** here:
the inverse of `/daily`, which filters those out.

### Meetings
From the calendar, and from Wispr Flow if connected: what you actually attended,
and **new commitments you made today**. Those are tomorrow's obligations: catch
them tonight while there's a transcript, not next week.

## Step 3: Grade the plan honestly

For each item in `## Plan for today`, decide from the evidence:

- **Done** → tick the checkbox `[ ]` → `[x]`. Tick it only when there's real
  evidence, or he confirms it. Don't tick optimistically.
- **Not done** → leave it unchecked, and it goes under `### Didn't get to` with
  its day count incremented.
- **Partly done** → this is the common case and deserves care. Leave it
  unchecked, but record the actual state: "Migration plan, drafted, not sent."
  Tomorrow's carry-over is far more useful when it says where you stopped.

**Never rewrite a task's text**, only its checkbox (`DAILY-NOTE.md` §2). If the
task was wrongly worded or turned out to be three tasks, say so in
`### Also happened`: the plan is a record, not a draft.

Ask him about anything the evidence can't settle. One short batch, not an
interrogation: "Did the Raj migration plan go out? I see no email."

## Step 4: Capture what wasn't on the plan

`### Also happened` is the section that makes the day explicable. Unplanned work
is the usual reason a reasonable plan didn't land:

- Incidents, production fires, urgent pulls.
- Reviews, pairing, and help you gave someone else.
- Meetings that appeared during the day.
- Rabbit holes, the "quick fix" that took two hours.

Rough time cost where you can tell. **Don't editorialize.** "Prod incident, ~2h"
is the finding. "Unfortunately the day was derailed" is noise.

## Step 5: Name tomorrow's first thing

One item, not a list. The single thing to start with before the day fills up.

Pick it from carry-over, a commitment made today, or whatever's genuinely most
urgent: and prefer the thing that's been carried longest, since that's the one
most likely to keep sliding. Tomorrow's `/daily` will put it at the top of the
plan.

## Step 6: Write it back to the same file

Edit `$VAULT/Daily/<today>.md` in place, **the file `/daily` wrote this
morning**. Never create a second file for today.

Per `DAILY-NOTE.md` §2, you may:
- toggle checkboxes in `## Plan for today` (text unchanged),
- write the whole `## Shutdown` section,
- set frontmatter `shutdown:` to the current time.

You may **not** touch `## Today`, `## Needs you`, `## From yesterday's meetings`,
`## Carried over`, or, above all, `## Notes`.

```markdown
## Shutdown

### Done
- Reviewed PR 412: approved, unblocked Ankit
- ACME-231 retry backoff, 3 commits, pushed to `feat/retry-backoff`

### Didn't get to
- Send Raj the migration plan, drafted, not sent  *(2nd day)*

### Also happened
- Prod incident in `spinquest-backend`, ~2h: hotfix merged (PR 118)
- Unplanned design sync, 45m

### Tomorrow's first thing
- Send Raj the migration plan, before standup
```

## Step 7: Tell him, briefly

Three or four lines, not a report. What landed, what's carrying, and the one
thing for tomorrow. He's finishing his day, respect that.

If something's worth flagging, flag it once and plainly:
- A task carried **3+ days**: "this has moved four days; it's not going to
  happen in this form."
- A day where unplanned work exceeded planned work, worth him noticing, said
  once, without commentary.
- Uncommitted work sitting in a repo overnight.

## Guardrails

- **Evidence before assertion.** Tick a box because there's a commit, a PR, a
  sent email, or he said so, never because it seemed likely.
- **Report, don't judge.** No "you should have", no productivity coaching, no
  encouragement. A day where one thing shipped and an incident ate the rest was
  a fine day. State it flat.
- **Read `## Notes` before grading anything, and never edit it.** It is the only
  section he wrote himself, and it routinely explains a task the evidence cannot.
- **Never rewrite task text**, only checkboxes.
- **Read-only on every external account**: no marking read, replying, closing
  tickets, or pushing anything.
- **Don't pad `### Done`.** Three real things beat nine with "attended standup"
  in the list.

## Done when

- Today's `## Notes` was read in full before any item was graded.
- Work that appears only in his notes, with no commit or ticket behind it, is in
  `### Also happened`.
- Every item in `### Didn't get to` that his notes explained carries the reason.
- Every disagreement between his notes and the hard evidence is reported as both,
  not silently resolved.
- `## Notes` is byte-identical to how you found it.
- Every tick in `### Done` traces to evidence or to his own note.
