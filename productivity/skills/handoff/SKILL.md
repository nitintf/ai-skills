---
name: handoff
description: Compact the current conversation into a handoff document a fresh agent can pick up.
disable-model-invocation: true
argument-hint: "What will the next session be used for?"
---

Compress this conversation into a document a fresh agent can read cold and
continue from, with no access to what was said here.

Write it to the OS temp directory, never into the workspace. Print the path when
you are done.

If the user passed an argument, it describes what the next session will focus on.
Weight the document toward that and say so at the top.

## What goes in

| Section | Carries |
|---|---|
| **Goal** | What we are trying to achieve, in one or two sentences. |
| **State** | What is done, what is half-done, and what has not started. Name files and paths. |
| **Decisions** | Choices made here and the reason for each. This is the part that is lost if you skip it. |
| **Open questions** | Anything unresolved, with the options considered so far. |
| **Next step** | The single concrete thing to do first. |
| **Suggested skills** | Which skills the next agent should reach for, and why each. |
| **Traps** | What was already tried and failed, so the next agent does not repeat it. |

## What stays out

Reference other artifacts by path or URL rather than copying them. PRDs, `.plan`
docs, ADRs, issues, commits, and diffs are all already durable. A handoff that
restates them will go stale against them.

Cut the narrative of the session. What we tried at 2pm and abandoned at 3pm is
noise unless it belongs under **Traps**.

Redact API keys, tokens, passwords, and personal data. Name the secret and where
it lives instead of quoting it.

## Done when

- Every claim about state names a real path the next agent can open.
- Every decision carries its reason.
- **Next step** is one action, not a list.
- Nothing in the doc is a copy of something already on disk.
- No secret appears in the text.
- The path is printed.
