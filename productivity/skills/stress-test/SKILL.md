---
name: stress-test
description: >-
  Relentless standalone interview about any plan, design, or decision until you
  reach shared understanding — walking each branch of the decision tree one at a
  time, with a recommended answer for every question. General-purpose and works on
  anything: a design in your head, a doc, an architecture, a business call. NOT
  tied to the eng pipeline's .plan docs — use eng's `/grill` for those, since it
  reads and writes the doc's Open Questions and Decisions. Triggers: "stress-test
  this", "poke holes in this", "challenge my thinking", "interview me about this
  design", "what am I missing".
---

# stress-test — find the holes before reality does

Interview the user relentlessly about every aspect of the plan until you both
reach shared understanding. Walk down each branch of the design tree, resolving
dependencies between decisions one at a time.

**Ask one question at a time**, and give your recommended answer with each — a
question without a recommendation makes the user do all the work, and a
recommendation gives them something concrete to push against.

**If a question can be answered by exploring the codebase, go explore it
instead.** Never make someone answer what the code already decides.

Adapt as you go. Each answer should change what you ask next; a fixed
questionnaire isn't a stress test. Push hardest on the assumptions the whole plan
rests on, the failure modes nobody has named, and the parts the user seems most
confident about — that's usually where the unexamined belief is hiding.

When you're done, summarize what got decided and what's still genuinely open.
Don't pretend everything resolved.

> Working on a `.plan` ticket doc? Use eng's `/grill` instead — it starts from
> the doc's recorded Open Questions and writes answers back into Decisions.
