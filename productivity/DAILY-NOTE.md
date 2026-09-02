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

**Nothing else goes in the file.** No `Sources:` footer, no line about which MCP
server was down, no nag that the config is still the template, no note that `gh`
was unavailable. Those are run diagnostics about the skill, not facts about
Nitin's day. Say them in chat, once, and leave the note clean.

**No em-dashes in anything a skill writes here.** Same rule as the rest of the
repo (`writing/RULES.md`): comma, colon, period, or parentheses, whichever the
sentence wants. It covers section bodies, task text, annotations, and the commit
message `/shutdown` writes, not just chat replies.

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
- **Anything Nitin typed is his, wherever it sits.** He does not confine himself
  to `## Notes`. He edits in place: `- **SKIP THIS PLEASE**` appended to a
  `## Needs you` line, `needs to be done on the last day` after a due date, `no,
  it needs my verdict as well` correcting a line under
  `## From yesterday's meetings`. Those lines live in sections a skill owns and
  they are still his.
  - **Tell his text from yours.** A line a skill wrote is one it can reproduce
    from its own sources. Anything else in that line is his. When in doubt, it is
    his.
  - **Never delete, reword, or reformat one.** Rewriting a section keeps each
    annotation attached to the item it was on.
  - **It outranks your evidence, and it outranks the plan.** `SKIP THIS DOES NOT
    DEPEND ON ME` means the item does not come back tomorrow. `keep it in notes,
    not in plan for today` means it stays out of `## Plan for today`. A
    correction means the corrected version is what carries forward, not the
    original.
  - **If an item genuinely has to go, its annotation goes with it** and gets
    reported in chat, never dropped in silence.
  - See §5 for how each kind of annotation carries into the next day.
- **`/shutdown` never rewrites a task's text**, only its checkbox. If the task as
  written was wrong, say so in `### Also happened`, don't silently edit history.
- **Re-running a skill updates its own sections in place.** `/daily` run twice in
  a morning refreshes Today / Needs you; it does not duplicate them, and it does
  not clear checkboxes the user already ticked by hand.
- **If the file exists, read it fully before writing.** Preserve everything you
  don't own. Fully means every line of every section, not the headings you own
  plus `## Notes`.

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

Every carried task keeps a day count in `## Carried over`: `*(2nd day)*`,
`*(3rd day)*`.

**At 3+ days, add one short callout on that same line.** Cut it, schedule it, or
hand it off:

```markdown
## Carried over
- Review PR #5411  *(6th day)*  six days of chakler waiting. Do it today or tell
  him to find another reviewer.
- Answer Charmaine on BR-7919  *(4th day)*
- Fix the Reshma PR and merge it  *(3rd day)*, blocked on her
```

The count and that one line are the entire treatment. **Do not build a separate
"Aged 3+ days" block**: it repeats items that are already three lines above with
their ages attached, and `## Needs you` is for things that arrived, not for
things that failed to leave.

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
- **Anything he deferred or killed in yesterday's note is not a candidate**, no
  matter how well it scores on urgency. See §5.
- **`/daily` proposes the list and the user can edit it.** It's their day.

---

## 5. Carrying his edits into the next day

§2 says his annotations are his and survive a rewrite. This section says what
`/daily` does with them the following morning, which is the half that keeps
getting dropped.

**Before building anything, re-read the previous note end to end** and pull out
every line he touched, in every section, not just `## Notes`. Then classify each
one:

| He wrote | The next day |
|---|---|
| A kill: `SKIP THIS`, `not mine`, `does not depend on me` | The item does not appear. Not in `## Needs you`, not in `## Carried over`, not in the plan. Propose adding it to the config's "Never surface" list so it stops arriving at all, and say once in chat that you dropped it. |
| A correction: `no, it needs my verdict as well` on *William takes the interview verdict to Sree* | The **corrected** version is what carries: "William takes the interview verdict to Sree, and it needs your verdict too." Never re-emit the original line you wrote yesterday, that is the exact bug this table exists to fix. |
| A deferral: `keep it in notes, not in plan for today`, `wait on this` | It stays out of `## Plan for today`. Keep it in `## Carried over` with the reason attached, or drop it if he said to drop it. |
| A date or constraint: `needs to be done on the last day, 4 Sep` | Becomes the item's deadline. It surfaces on that date, not before. |
| A blocker: `blocked on her` | Rides along with the carried item, every day, until he removes it. A carried task with a known blocker never appears as a bare line. |

Two failure modes to name, because both have happened:

- **Re-emitting a line he already corrected.** You wrote it yesterday, he fixed
  it, and the next morning your regenerated section says the original again. His
  edit is newer than your source. His edit wins.
- **Honoring a skip once, then forgetting.** A skip he had to write twice is a
  skip you failed to record. Put it in the config.

---

## 6. The vault commit (`/shutdown` only)

The vault is a git repo. Uncommitted daily notes are notes that exist on one
machine, which defeats the point of writing them down.

**`/shutdown` commits and pushes the whole vault as its last step**, after the
`## Shutdown` section is written. `/daily`, `/standup` and `/weekly` never touch
git: one write per day, at the end, when the day is actually done.

- Stage everything, his own edits included. The vault is his, and a half-staged
  vault is worse than an unstaged one.
- **Match the repo's existing commit style.** Read `git log --oneline -10` and
  write in that voice. This one is terse and lowercase (`sync`, `changes`,
  `database index`), so match that, do not introduce a conventional-commits
  prefix it has never used.
- **Never add a `Co-Authored-By` trailer, and never mention Claude, Claude Code,
  or any model in the message.** These are Nitin's notes.
- Push to the tracked remote. If the push is rejected, pull with rebase and
  retry once, then report it and stop. Do not force.
- Nothing to commit is a normal outcome. Say so in one clause and move on.

---

## 7. Anchors for editing

Skills find their section by exact `##` heading match. When editing:

1. Read the whole file.
2. Locate your section by heading.
3. Replace only the content between that heading and the next `##` at the same
   level.
4. Write the file back whole.

If a heading is missing, insert it in the schema's order: never append your
section to the bottom of the file.
