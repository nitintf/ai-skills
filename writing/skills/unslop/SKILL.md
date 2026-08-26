---
name: unslop
description: >-
  Rewrite text so it reads like a person wrote it: plain, direct English with the
  filler, hedging, and AI tells removed, and every fact, number, and technical
  term left intact. Also runs as an audit that names the tells in a draft without
  rewriting it. Works on chat replies, commit messages, PR descriptions, docs,
  READMEs, and release notes. Use when the user says "unslop this", "rewrite
  this", "this sounds like AI", "make this sound human", "less corporate", "too
  wordy", "cut the fluff", or when you have just drafted prose and want it to
  clear the house style before it ships.
---

Take a piece of text and make it read like a competent engineer wrote it in one
pass: leading with the point, specific, finished when the point is made.

The style itself lives in [`RULES.md`](../../RULES.md), which is the single
source of truth. This plugin's `SessionStart` hook normally loads it already. If
it is not in context, read it before doing anything else.

## Pick the mode

| The user handed you | Mode |
|---|---|
| Text and an instruction to fix it | **Rewrite** |
| Text and a question about whether it reads badly | **Audit** |
| A file path plus "clean this up" | **Rewrite**, in place, via Edit |
| Nothing (you just drafted prose yourself) | **Rewrite**, silently, before you send it |

When it is genuinely ambiguous, audit first. An unwanted rewrite destroys the
original; an unwanted audit costs one paragraph.

## Rewrite

1. **Read for the load-bearing content.** Facts, numbers, names, file paths,
   code, quoted errors, the actual claim. This set survives untouched. Everything
   else is negotiable.
2. **Find the real first sentence.** It is often the third or fourth sentence of
   the draft, sitting behind a preamble. Move it to the front and delete what was
   in front of it.
3. **Apply the targets in `RULES.md`,** in order, top to bottom.
4. **Sweep the guardrails.** This pass is mechanical: hunt each banned
   construction by name and remove it.
5. **Read the result cold.** If a sentence could be said in fewer words without
   losing a fact, say it in fewer words. If a paragraph could be a sentence, make
   it a sentence. Stop when nothing further comes out without a fact going with
   it.
6. **Check the length claim.** A rewrite that grew is a rewrite that failed.

Return the rewritten text and nothing else. Add a short note on what you cut only
when the user asks, or when a cut changed meaning and they need to confirm it.

## Audit

Report the tells you found, each as: the quoted phrase, which rule it breaks, and
the replacement you would write. Order by how badly each one gives the text away,
worst first. End with a one-line verdict on whether the draft needs a rewrite or
a few edits.

Say plainly when a draft is already clean. Manufacturing findings on good prose
is its own kind of slop.

## What survives

Preserve exactly: technical terms, code blocks, file paths, identifiers, quoted
error messages, numbers, names, and URLs. Preserve the claim: if the draft says
the migration is risky, the rewrite says the migration is risky.

Preserve the author's voice when the text is theirs. Their sentence rhythm,
their vocabulary, their level of formality. You are removing what the machine
added, not replacing them with your own register.

Never quietly resolve an uncertainty. "This might be caused by the cache" becomes
"I think the cache is causing this, but I have not confirmed it", not "The cache
is causing this."

## Not caveman

`/caveman` compresses: it drops articles, uses fragments, and trades grammar for
tokens. This does not. Full sentences, normal grammar, ordinary English. The
target reader is a colleague, not a telegraph operator.

## Done when

- The first sentence carries the answer.
- Every banned construction in `RULES.md` is absent.
- Every fact, number, code block, and quoted error in the original is present and
  unchanged in the rewrite.
- The text is shorter than the draft.
- No sentence can lose a word without losing a fact.
