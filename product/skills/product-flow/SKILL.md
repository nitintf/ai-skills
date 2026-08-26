---
name: product-flow
description: Take a raw idea through PRD, then user stories, then hand off to `/scope`, gating between each. Resumes from whatever is already in `.plan/<feature>/`.
disable-model-invocation: true
---

# product-flow: one idea in, a buildable feature package out

The `product` mirror of `/eng-flow`. You chain the product skills so a raw idea
becomes a PRD, then stories, then engineering tickets: with a gate between each
so the user can redirect before the next stage compounds a bad assumption.

Like `eng-flow`, you are deliberately **dumb**: the files on disk hold the state.
You look at what exists in `.plan/<feature-slug>/` and run the next thing.

## 1. Find or start the feature

Pick the feature slug from the idea (kebab-case), then look at
`<project-root>/.plan/<feature-slug>/` and read what's there:

| what exists | what's next |
|---|---|
| nothing | `/prd` |
| `PRD.md` | `/user-stories` |
| `PRD.md` + `user-stories.md` | hand off to eng's `/scope` |
| `NN-*/doc.md` folders too | already in the eng pipeline, point at `/eng-flow` |

If several features exist, ask which. If the user's idea clearly matches an
existing PRD, resume that one rather than starting a near-duplicate.

## 2. Right-size the run before you start

The full chain is right for a real feature and heavy for a small one. Ask up
front, one question, with a recommendation:

- **Full package**: PRD → stories → tickets. For anything genuinely new, or
  work that needs stakeholder alignment, or where the problem itself is still
  fuzzy.
- **Stories only**: skip the PRD. For a well-understood feature where the *what*
  isn't in doubt and you just need it sliced.
- **Straight to `/scope`**: for a technical task with no real product surface.
  Say so honestly rather than generating ceremony nobody will read. A PRD for
  "add a retry to the webhook sender" is waste.

Recommend the lightest option that fits. Over-documenting is the failure mode
this skill is most likely to cause.

## 3. Run the stages, gating between each

### Stage 1: `/prd`
Produces `.plan/<feature-slug>/PRD.md`. It grills the user on problem, goals,
metrics, and scope before writing.

**Gate:** summarize the PRD's problem statement, goals, and non-goals in a few
lines and ask whether it's right. This is the cheapest possible moment to catch
a wrong problem statement, every artifact after this inherits it.

### Stage 2: `/user-stories`
Reads the PRD, produces `.plan/<feature-slug>/user-stories.md`.

**Gate:** report the story count, the P0s, and the ordering. Ask whether the
slicing is right. Specifically flag any PRD goal with no story covering it:
that gap is the most common defect at this stage.

### Stage 3: hand off to `/scope`
`/scope` (eng plugin) reads both files as inputs and turns them into tickets.

**Gate:** this crosses from product into engineering, and the eng pipeline writes
into the same feature folder. Confirm before crossing, and tell the user what
happens next: `/scope` will propose a ticket breakdown and a track, then
`/eng-flow` can carry it to shipped.

If the `eng` plugin isn't installed, stop here and say the package is ready for
whatever ticketing process they use.

## 4. Keep the artifacts consistent

The stages share a folder, and the failure mode is drift: stories that quietly
contradict the PRD they came from.

- If a later stage surfaces something that invalidates an earlier doc (a story
  that can't be built reveals a non-goal was wrong), **go back and update the
  earlier doc**, don't paper over it downstream. Say what you changed.
- Never let two docs assert different scope. The PRD's Non-Goals and the stories
  must agree.
- If the user changes direction mid-flow, ask whether to revise the PRD or start
  a new feature slug. Don't silently mutate an approved doc.

## 5. Finish

Summarize the package: the paths written, the shape of it (N goals, M stories,
P0 count), and the honest state, what's decided, what's still an open question
in the PRD. Then point at the next step: `/scope` if they're building now,
`/eng-flow` to run the whole thing to shipped.

## Guardrails

- **Don't generate documents nobody asked for.** The lightest artifact that
  unblocks the work is the right one. If the user needs three tickets and not a
  PRD, say that.
- **Gate every stage.** A wrong problem statement propagated into stories and
  then tickets is the expensive failure this orchestrator exists to prevent.
- **You orchestrate; the skills do the work.** No PRD-writing or story-slicing
  logic lives here: that belongs in `/prd` and `/user-stories`, which must keep
  working standalone.
