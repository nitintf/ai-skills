---
name: prd
description: >-
  Write a Product Requirements Document at a staff bar: problem, measurable
  goals and non-goals, success metrics, prioritized requirements, risks, and
  rollout.
disable-model-invocation: true
---

# prd: staff-level Product Requirements Document

Produce a PRD at the standard of a senior/staff engineer or PM at a top-tier org.
A great PRD is **about the what and the why, not the how**. It is crisp,
falsifiable, and decision-forcing, not a wall of prose. Ruthless about goals vs
non-goals, honest about risks, and every success metric is measurable.

This skill is **independent of the `eng` plugin.** Its output is a polished PRD
document; `/scope` can later read it to generate tickets, but you do NOT format
it in the eng doc schema.

## Process

### 1. Gather context (don't write yet)
- Understand the idea from the user. Pull in any existing material (linked docs,
  the codebase, prior art).
- **If a personas skill is installed** (check the available skills for one, some
  orgs ship their own, e.g. a `*-personas` skill), load it so the PRD references
  real personas rather than invented ones. If there isn't one, ask the user who
  the actual users are instead of inventing a persona; a fabricated persona is
  worse than a plainly-described user segment.

### 2. Grill the gaps before writing
A PRD is only as good as its inputs. Ask the user: in small batches, one topic
at a time, with your recommended answer for each: about whatever is unclear:
- **Problem**: whose problem, how painful, how do we know it's real (evidence)?
- **Goal & success**: what does winning look like, and what metric proves it?
- **Scope**: what's explicitly out? what's the smallest valuable version?
- **Constraints**: deadlines, platforms, compliance, dependencies.
Don't invent answers to material questions: get them, or list them as Open
Questions.

### 3. Choose the format
Default to the **standard PRD** below. Offer the **Amazon PR/FAQ** style (a mock
press release + anticipated FAQ) when the user is pitching a new product/feature
and wants to "work backwards." Ask only if it's ambiguous.

### 4. Write the PRD
Save to `<project>/.plan/<feature-slug>/PRD.md` by default (so `/scope` can find
it as a sibling), or wherever the user prefers (e.g. `docs/prd/`). Use this
structure:

```markdown
# <Product / Feature name>: PRD

| Field | |
|-------|---|
| **Author** | <name> |
| **Status** | Draft / In Review / Approved |
| **Last updated** | <YYYY-MM-DD> |
| **Reviewers / Stakeholders** | <eng, design, PM, …> |

## TL;DR
<3-5 sentences a busy exec can read: what, for whom, why now, expected impact.>

## Background & Context
<What exists today, what changed, why this is worth doing now. Evidence/data.>

## Problem Statement
<The user/business problem in one sharp paragraph. Who hurts and how much.>

## Goals
<Outcome-oriented and measurable. Each goal ties to a success metric.>
- G1: …

## Non-Goals
<Explicitly out of scope. This section prevents creep and is as important as Goals.>
- NG1: …

## Success Metrics
<Each metric: name, baseline (today), target, how/when measured. No vanity metrics.>
| Metric | Baseline | Target | How measured |
|--------|----------|--------|--------------|
| … | … | … | … |

## Target Users & Personas
<Who this is for. Reference real personas. Their context, jobs-to-be-done.>

## User Journeys / Use Cases
<The key flows, before vs after. Walk the primary journey end to end.>

## Requirements
<Prioritized. P0 = must-have for launch, P1 = should, P2 = nice-to-have.>
### Functional
| ID | Priority | Requirement | Rationale |
|----|----------|-------------|-----------|
| FR1 | P0 | … | … |
### Non-Functional
<Performance, scale, security/privacy, accessibility, reliability, i18n.>

## Proposed Solution (high level)
<The what, not the detailed how. A sketch of the approach, key UX, system shape.
Leave detailed design to an eng design doc / the eng pipeline.>

## Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| … | … | … | … |

## Dependencies
<Teams, services, data, third parties this relies on.>

## Rollout / Phasing
<Milestones, phased delivery (MVP → v1 → v2), flagging, migration/backfill,
launch plan, how we de-risk.>

## Open Questions
<Honest list of unresolved decisions, owners, and needed-by dates.>

## Appendix / References
<Links to data, designs, prior docs, related ADRs.>
```

(If PR/FAQ format: lead with a one-page mock **press release**, headline, dated
dateline, customer quote, problem→solution narrative, followed by an
**anticipated FAQ** for customers and for internal stakeholders.)

### 5. Quality bar before you finish
- Goals are outcomes, not features; each has a metric.
- Non-goals are real and specific.
- Every success metric has a baseline and a target.
- Requirements are prioritized; P0 is genuinely minimal.
- Risks are honest (include the ones that could kill it).
- No solution detail masquerading as requirements.

### 6. Hand off
Tell the user the path and summarize. If they'll build it, suggest:
"Run `/user-stories` to break this into stories, or `/scope` to turn it into
eng tickets."
