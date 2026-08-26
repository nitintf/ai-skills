---
name: research
description: >-
  Investigate a question against primary sources and return a cited answer.
  Reads specs, RFCs, official docs, changelogs, and library source rather than
  blog posts and summaries, weighs each source by trust, and says plainly where
  the sources disagree or go silent. Every claim carries a link. Can be saved as
  a durable doc under `.plan/_research/`. Use when the user asks about something
  outside this codebase: how a third-party API behaves, whether a library
  supports something, what changed in a release, what a spec actually requires,
  or how other people solve a problem. Triggers: "research this", "look this up",
  "what does the spec say", "does X support Y", "find out how", "check the docs".
---

# research: answer from primary sources, with citations

Answer a question about the world outside this repo. Use
[`/understand`](../understand/SKILL.md) for questions about this codebase; the
two never overlap.

The whole value here is **provenance**. An uncited answer from you is worth less
than a search result, because the reader cannot check it. Never answer from
memory: your training has a cutoff, and this question is being asked precisely
because someone needs the current truth.

## Step 1: Frame the real question

Restate what is actually being asked, and say what a good answer would let the
user decide. "Does Stripe support partial refunds on subscriptions" is a
question. "Tell me about Stripe" is not.

Write down what would settle it: a spec line, an API reference page, a changelog
entry, a maintainer's answer. That target is what you go looking for.

Where the question is really two questions, split it and answer both.

## Step 2: Rank sources before you read them

| Tier | Source | Weight |
|---|---|---|
| 1 | The spec, RFC, or standard itself | Settles the question |
| 1 | Official API reference and official docs | Settles the question |
| 1 | The library's own source code, tests, and types | Settles the question, and beats its docs when they disagree |
| 2 | Changelog, release notes, migration guide | Settles "what changed" and "since when" |
| 2 | Maintainer statement in an issue, PR, or RFC discussion | Strong, especially for intent and roadmap |
| 3 | Reputable engineering blog, conference talk, book | Useful for approach, never for a fact |
| 4 | Stack Overflow, tutorials, aggregator posts, AI-written listicles | Use to find tier 1 sources, never as the citation |

Read down the list, not up. A tier 4 page that names an API method is a pointer
to the tier 1 page that documents it. Follow it, then cite the tier 1 page.

**Check the date on everything.** A correct answer from 2021 is a wrong answer
now. Note the version a claim applies to.

## Step 3: Read, do not skim

Open the actual page. A search-result snippet is not a source, and a snippet
that appears to answer the question is the most common way to get this wrong,
because snippets drop the qualifying sentence.

Where the question is about a library's behavior and the docs are thin, read the
source. `node_modules`, the GitHub repo, and the test suite all beat prose.

## Step 4: Weigh what you found

Report disagreement rather than resolving it silently. If the docs say one thing
and the source does another, that is the finding, and it is more valuable than
either source alone.

Say when the sources are silent. "The docs do not state the rate limit; the only
figure I found is in a 2023 support thread" is a real, useful answer. Inventing a
number is not.

Separate what is **documented** from what is **observed** from what is
**inferred**. Label each.

## Step 5: Answer

Lead with the answer to the question asked, in the first sentence. Then the
evidence.

Every factual claim carries an inline link to the source it came from. A
paragraph with no link is either your own reasoning (say so) or an uncited claim
(remove it).

Close with:

- **Confidence**, and what would raise it.
- **What I could not establish**, where anything is still open.

## Saving it

Offer to save when the answer took real work, will be needed again, or informs a
decision. Write to `.plan/_research/<slug>.md` with the question, the date you
ran it, the answer, the sources, and the open questions. Say the path.

Skip the file for a quick lookup. A one-line answer does not need a document.

## Done when

- The first sentence answers the question that was asked.
- Every factual claim links to the source it came from.
- Every source is tier 1 or 2, or is explicitly flagged as weaker.
- Every version-dependent claim names the version, and every source names its date.
- Disagreements between sources are reported, not resolved silently.
- What you could not establish is stated, not skipped.
