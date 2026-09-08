---
name: shutdown
description: >-
  Close the day: tick off this morning's plan using real evidence from commits,
  PRs, and tickets, record what slipped, set tomorrow's first thing, then commit
  and push the Obsidian vault.
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
- **Note exists** → read the whole file first, top to bottom. Then take
  `## Plan for today` as the list you're grading.

**Read every section, not just the plan and `## Notes`.** He annotates in place:
a `SKIP THIS` on a `## Needs you` line, a correction after a meeting bullet, a
reason typed beside a carried task. Those lines are evidence and they are his,
and reading only the two sections you care about throws them away.

An annotation changes the grade:

| He wrote, in any section | What it means tonight |
|---|---|
| `SKIP THIS`, `does not depend on me` | Not a failure. It leaves the loop: not in `### Didn't get to`, not carried. Say once in chat that he dropped it. |
| `keep it in notes, not in plan for today` | If it was in the plan anyway, that is the reason it did not move. Record the reason, not just the miss. |
| A correction to something you wrote | Goes into `### Also happened` if it changes what actually happened. Never argue with it. |
| `needs to be done on the last day, 4 Sep` | Not late. It has a date, and the date is not today. |

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
isn't pushed still happened.

**Check `gh auth status` before you conclude anything about `gh`.** One failing
`gh` call is not an auth verdict, and a sandboxed shell with no network looks
exactly like a logged-out one. If `gh` is genuinely unusable, local `git` still
covers commits and branches: say which of the two you used, in chat, and quote
the error rather than diagnosing it.

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
`## Carried over`, or, above all, `## Notes`. That includes his annotations
inside those sections: they stay byte-identical.

**No em-dashes in anything you write** (`DAILY-NOTE.md` §1). Comma, colon,
period, or parentheses.

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

## Step 7: On a Friday, archive the week

Only on Fridays, and only after the `## Shutdown` section is written.

`Daily/` holds the current week; everything older belongs in
`$VAULT/Daily/Archive/` (`DAILY-NOTE.md` §7). `git mv` every note dated before
this week's Monday into it, creating the directory if it does not exist. Today's
note stays put: the week is not over until it is filed, and it gets archived by
next Friday's run.

Do it before Step 8 so the moves and tonight's note land in one commit.

Never delete and never rename. If Friday is missed, the next `/daily` picks it
up as a catch-up, so a skipped Friday costs nothing.

---

## Step 8: Commit and push the vault

The day's record is written. Now make it exist somewhere other than this laptop.
This is the last write of the day and the only git operation in the whole loop:
`/daily`, `/standup` and `/weekly` never do this (`DAILY-NOTE.md` §6).

From the vault root:

1. `git status --short` and `git log --oneline -10`. The log is the style guide.
2. **Stage everything**, his own edits and the Obsidian workspace file included.
   The vault is his; a half-staged vault is worse than an unstaged one.
3. Write the message **in the voice the log already uses**. This one is terse and
   lowercase (`sync`, `changes`, `database index`). Match it. Do not introduce a
   `feat:` prefix, a body, or a bullet list into a log that has never had one.
   Name what actually changed when you can: `2026-09-02 shutdown`, `daily notes
   + db internals`.
4. **No `Co-Authored-By` trailer. No mention of Claude, Claude Code, or any model
   anywhere in the message.** These are his notes.
5. Push to the tracked remote.

Failure handling, in one pass:

- **Nothing to commit** is a normal outcome. One clause in the summary, move on.
- **Push rejected**: `git pull --rebase`, push once more. If that fails, report
  it and stop. Never force, never reset, never discard.
- **Conflict during the rebase**: stop and tell him. Do not resolve conflicts in
  his notes on his behalf at the end of the day.

## Step 9: Tell him, briefly

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
- **Read-only on every external account**: no marking read, replying, or closing
  tickets. The one write you make is the vault commit in Step 8, to his own repo.
- **Never sign his commits as Claude.** No `Co-Authored-By`, no model name in the
  message, in this repo or any other.
- **Don't pad `### Done`.** Three real things beat nine with "attended standup"
  in the list.

## Done when

- Today's `## Notes` was read in full before any item was graded.
- Work that appears only in his notes, with no commit or ticket behind it, is in
  `### Also happened`.
- Every item in `### Didn't get to` that his notes explained carries the reason.
- Every disagreement between his notes and the hard evidence is reported as both,
  not silently resolved.
- `## Notes` is byte-identical to how you found it, and so is every annotation he
  made elsewhere in the file.
- Anything he marked skip is out of the loop, not sitting in `### Didn't get to`.
- Every tick in `### Done` traces to evidence or to his own note.
- Nothing you wrote contains an em-dash.
- On a Friday, every note older than this week's Monday is in `Daily/Archive/`
  and moved with `git mv`, not copied or deleted.
- The vault is committed and pushed, or you said plainly why it isn't. The commit
  message matches the repo's existing style and names no model.
