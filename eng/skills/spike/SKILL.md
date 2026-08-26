---
name: spike
description: >-
  Timeboxed investigation that ends in a recommendation: evaluate 2-4 approaches
  against this codebase's real constraints and pick one, with a confidence
  level.
disable-model-invocation: true
---

# spike: buy information, then decide

A spike is a **purchase of information**. You spend a bounded amount of effort to
reduce uncertainty enough to commit, and then you stop. Two failure modes bracket
it: stopping too early and guessing, or sliding into building the thing for real
under the cover of "still investigating".

The output is not a survey. It is a **recommendation you'd defend**, with the
reasoning visible so someone can disagree with it on the merits.

## 1. Frame the actual question

Most spikes are asked badly. "Should we use X?" is not answerable; "can X handle
50k events/sec with our existing Kafka setup, without a rewrite of the ingest
path?" is. Before anything else, pin down:

- **The decision this unblocks.** If nothing changes based on the answer, don't
  spike it. Say so.
- **The real constraints**: scale, latency, budget, deadline, team skills,
  existing infrastructure, compliance, what you can't break. These do the actual
  deciding; a generic comparison ignores them and is therefore useless.
- **The success criteria**: what evidence would settle this? Name it *now*,
  before you're invested in an answer. This is what keeps a spike from becoming
  a rationalization.
- **The timebox.** Agree it explicitly: "a couple of hours of exploration" or
  "read-only, no prototype". Then hold it, and report honestly if you hit it
  without an answer: "I need more time and here's specifically why" is a
  legitimate and useful outcome.

If the question is still fuzzy after this, ask the user before burning effort.

## 2. Ground it in this codebase

The difference between a useful spike and a blog post. Before evaluating
anything, know what you're actually integrating with:

- Read `.plan/_conventions.md` if it exists (see `${CLAUDE_PLUGIN_ROOT}/SPEC.md`
  §6): the stack, the patterns, the primitives already present.
- Find the code the decision touches, with `file:line`. What would each option
  actually require changing?
- **Check what's already there.** Half of all spikes end with "we already have
  something that does this": a dependency already in `package.json`, a helper
  someone wrote, a service already deployed. Look before comparing.
- Look for prior art: has this been tried here before? `git log`, existing ADRs
  in `.plan/_decisions/`, a dead branch, a commented-out experiment.

## 3. Identify the candidates: 2 to 4, including the boring one

More than four and you'll evaluate all of them shallowly. Always include:

- **Do nothing / status quo.** The baseline. Sometimes it wins, and it's the
  option people forget to price.
- **The simplest thing that could work**, even if it feels unambitious. Often the
  right answer, and it calibrates the cost of the fancier options.
- The candidates the user proposed, plus any obvious one they missed.

Say explicitly what you ruled out before evaluating, and why: that's part of the
reasoning, and it stops "did you consider Y?" a week later.

## 4. Evaluate against the criteria, not in the abstract

For each candidate, answer the questions **you defined in §1**, not a generic
feature matrix. What matters:

- **Fit with this codebase**: how much of the existing architecture survives?
  What has to change, with `file:line`?
- **The risky assumption**: every option rests on something unverified
  ("it can handle our volume", "it supports our auth model", "it works with our
  Node version"). Name it. This is what a prototype is for.
- **Cost to adopt and to live with**: migration effort, ongoing maintenance,
  operational burden, licensing, the on-call cost.
- **Reversibility.** How expensive is it to back out in six months? This
  frequently *should* dominate the decision and rarely does. A cheap-to-reverse
  option deserves a much lower evidence bar than a one-way door.
- **What breaks first at scale**, if scale is one of the constraints.

Check real evidence over reputation: read the library's source or issue tracker,
check its release cadence and open-issue profile, verify the version you'd
actually use supports what you need. "It's popular" is not a finding.

## 5. Prototype only the riskiest assumption

If the decision genuinely hinges on something you can't determine by reading,
build the **smallest possible thing that tests exactly that**: not a demo, not a
feature, not an integration. The one assumption.

- Throwaway branch, clearly labelled. Never in the working tree the user is
  building on.
- Timebox it hard.
- **Delete it, or park it on a branch and say so.** Spike code is written to be
  wrong; it must never quietly become production code. If it turns out to be
  useful, that's a fresh, properly-scoped `/scope` ticket.

Record what the prototype actually proved or disproved, including "inconclusive".

## 6. Recommend

Write to `.plan/_research/spike-<slug>.md` (or where the user prefers):

```markdown
# Spike: <the question>

**Recommendation:** <the answer, in one sentence, up top.>
**Confidence:** high | medium | low: <why, in a clause>
**Timeboxed to:** <what you spent> · **Date:** <YYYY-MM-DD>

## The question and why it matters
<What decision this unblocks, and the constraints that bound it.>

## What would settle it
<The success criteria from §1, so a reader can check your work.>

## Options
### <Option>: recommended ✅
<What it is. Fit with our codebase, with `file:line`. Cost to adopt and to
live with. Reversibility. What it costs us.>
### <Option>
<Same treatment, fairly. Then: why not, tied to a specific constraint.>

## Evidence
<What you actually read, ran, or measured. Prototype results, including the
negative ones. `file:line` and links. This is the part that makes it checkable.>

## Recommendation
<The call and the deciding reason. What tradeoff you're accepting, explicitly.>

## What I'd want to verify before committing
<Anything the timebox didn't cover, and how much it would cost to find out.>

## Open questions / risks
<Honest. What could still make this wrong.>
```

Then hand off:
- Decision made and it's significant → **`/adr`** to record it permanently.
- Ready to build → **`/scope`** to turn it into tickets.
- Not settled → say exactly what's still unknown and what it'd take.

## Guardrails

- **A spike ends in a recommendation.** "Here are the tradeoffs, you decide" is
  an abdication. Make the call; the user can overrule you with the reasoning in
  front of them.
- **State confidence honestly.** Low confidence clearly labelled is far more
  useful than false certainty: it tells the user how hard to hold the decision.
- **Hold the timebox.** If you blow through it, stop and report, don't keep
  going silently.
- **Prototype code is throwaway.** Never leave it in the working tree, never let
  it drift into production, never optimize it.
- **Don't strawman the losers.** If you can't state the strongest case for an
  option you're rejecting, you haven't understood it well enough to reject it.
- **You investigate and recommend; you don't implement.** Building it is
  `/scope` → the pipeline.
