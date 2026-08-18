# Daily brief — filter config

Copied to `~/.claude/daily-brief.config.md` on first run of `/daily`. **Edit it
there, not here** — this is the template, and a plugin update overwrites it.

This file is what makes the brief good. The defaults below are a starting point;
`/daily --tune` will propose real values from your mail history, and you should
keep tightening it for the first couple of weeks. If a brief ever shows you
something you didn't care about, add a rule here — that's the whole loop.

---

## Me

```
email:      nitinpanwar0802@gmail.com
work-email:
slack-handle:
jira-account:
timezone:
```

Add every address you receive at. The To:-vs-CC: rule can't work without them.

## Always surface — people

Mail or messages from these people always make the brief, regardless of other
rules. Your manager, your direct collaborators, anyone whose ask blocks you.

```
- name@example.com          # manager
- name@example.com          # tech lead
```

## Always surface — domains

Whole domains that matter (a key customer, a partner, your own company).

```
- @yourcompany.com
```

## Never surface — senders

Aggressive by default. Everything automated belongs here.

```
- noreply@*
- no-reply@*
- notifications@*
- notifications@github.com
- *@atlassian.net              # Jira's own mail; the Jira section covers it properly
- builds@*
- *@circleci.com
- *@vercel.com
```

## Never surface — subject patterns

```
- "unsubscribe"
- "your receipt"
- "invoice"
- "newsletter"
- "digest"
- "[CI]"
- "deploy"
```

## Slack

```
mute-channels:
  - #random
  - #general
  - #deploys
  - #alerts

always-surface-channels:
  - #eng-platform

include-dms: true
include-thread-replies: true
```

`@channel` / `@here` blasts are excluded everywhere unless the message also names
you directly.

## Jira

```
projects:
  - PROJ

include:
  - assigned-to-me-changed-by-others
  - comments-mentioning-me
  - status-transitions-on-my-issues

exclude:
  - my-own-actions        # you did it, you know
  - sub-task-noise
```

## Calendar

```
source: google           # google | wispr | auto  (auto prefers google, falls back)
include-declined: false
include-all-day: false
flag-prep-needed: true   # organizer/presenter, or no agenda on a >30m meeting
working-hours: 09:00-18:00
```

## Wispr Flow

```
extract:
  - commitments-i-made
  - decisions-reached
  - action-items-assigned-to-me

skip:
  - meeting-summaries      # you were there; a recap is not a brief
  - general-discussion
```

## GitHub — used by /shutdown, /standup, /weekly

Evidence of what you actually did. Prefers the GitHub MCP if connected, else
falls back to `gh` CLI and local `git` (which are usually faster anyway).

```
username:
code-root: ~/code             # scanned for local repos with commits today

repos:                        # leave empty to auto-detect from recent activity
  - spinquest-frontend
  - spinquest-backend
  - zaars-backend
  - ampd

include:
  - commits-authored
  - prs-opened
  - prs-merged
  - reviews-given             # under-counted work; keep this on
  - uncommitted-work          # flags WIP left overnight

exclude:
  - merge-commits
  - dependabot
  - commits-to-my-own-scratch-repos
```

## Standup

```
mention-ticket-ids: false     # "I finished the retry logic" > "I completed ACME-231"
say-no-blockers: false        # only true if your team expects everyone to say it
max-sentences: 5
```

## Brief shape

```
max-items-per-section: 5      # more than this means the filter needs tightening
tasks-per-day: 3-5            # hard ceiling of 5 — a longer list is a wish, not a plan
carry-over-warn-days: 3       # flag a task that's moved this many days
show-empty-sections: false
show-source-status: true      # so a thin brief is never mistaken for a quiet day
```

---

## Tuning notes

Keep a running log of what you cut and why. It's the fastest way to a filter that
actually fits you, and it stops you re-litigating the same rule.

```
2026-08-13  Muted #deploys — never once actionable
```
