---
name: standup
description: >-
  Print your standup update in plain speakable English: what you worked on, what
  you will work on next. Writes nothing.
disable-model-invocation: true
---

# standup: what to say, in words you can just say

Nitin reads this out loud in a meeting. That single fact decides everything about
the output.

So: **short, plain, spoken English.** Simple sentences. Nothing he would not
actually say to his team. If a line sounds like it was written to be read rather
than spoken, rewrite it.

**Two parts only:**
1. What I worked on
2. What I will work on next

That's it. This is the whole skill.

## Never say what did not get done

Important, and the easiest thing to get wrong: **only positive.** No "I could not
finish", no "this is still pending", no "I did not get to it".

If yesterday's task is still going, say it as **present work**, not as a failure:

- ✅ "I am working on the migration plan. I will finish it today."
- ❌ "I did not finish the migration plan yesterday."

Same information, and the first one is what a person actually says in standup.

## Step 1: Get the material

You already have all of it. Read, in this order:

1. **Yesterday's daily note**: the most recent note across `$VAULT/Daily/` and
   `$VAULT/Daily/Archive/` (`DAILY-NOTE.md` §7), the
   `## Shutdown → ### Done` and `### Also happened` sections. This is the best
   source for "what I worked on", because it was written with real evidence.
2. **Today's daily note**: `## Plan for today`. This is "what I will work on
   next".
3. **Commits and PRs**, if the notes are thin or missing: GitHub MCP if
   connected, else `git log --author=<you> --since=yesterday` across the repos he
   touched, plus `gh pr list --author @me`. Commit messages are a good record of
   real work.

Schema for the notes is in `${CLAUDE_PLUGIN_ROOT}/DAILY-NOTE.md`. If no notes
exist at all, build it from git alone, never ask him to recall his day.

## Step 2: Write it the way he will say it

**Three to five short sentences. Twenty to thirty seconds spoken.** Group related
work into one sentence instead of listing every commit.

Use plain, everyday words:

- "I worked on the payment retry logic."
- "I completed the CSV import."
- "I reviewed Ankit's PR."
- "Today I will work on the migration script."
- "I will take up ACME-231 after that."
- "I need one input from Raj on the schema."

Keep it in that register. **Do not use corporate or American idiom**: no
"circled back", "touched base", "bandwidth", "deep dive", "reached out", "synced
up", "low-hanging fruit", "aligned on". Nobody says these out loud, and they make
an update sound written.

Also drop:
- Ticket IDs and PR numbers, **unless the team uses them in standup**. "I
  finished the retry logic" is better than "I completed ACME-231."
- Hedging, "I think", "kind of", "hopefully", "tried to".
- Filler openers, "So basically", "Just wanted to say".
- Any explanation of *why* something took long. Nobody asked.

## Step 3: Blockers, only if real

He did not ask for a blockers section, and most days there isn't one. **Add one
line only when he is genuinely waiting on another person**: not when something
is merely hard or unfinished.

- "I need one input from Raj on the schema."
- "I am waiting for access to the staging DB."

Otherwise say nothing about blockers. Do not write "No blockers" unless his team
expects everyone to say it.

## Step 4: Print it

Chat only. **Write no files.** Give him the update as a small block he can read
straight off the screen:

```
Yesterday I worked on the payment retry logic and finished the CSV import.
I also reviewed Ankit's PR.

Today I will work on the migration plan and send it to Raj.
Then I will take up the retry backoff ticket.
```

Nothing before it, nothing after it. No "Here is your standup update", no offer
to change the tone, no bullet points. Just the words.

If he asks for it shorter or different, adjust and print again.

## Guardrails

- **Two parts. Worked on, will work on.** Nothing else unless there's a real
  blocker.
- **Never mention what did not get done.** Ongoing work is described as ongoing.
- **Speakable or it's wrong.** Read it back in your head. If it sounds like a
  written report, it failed.
- **Never invent work.** If the evidence shows one thing, say one thing. A short
  honest update is completely fine.
- **No files, no side effects.** This skill only prints.
