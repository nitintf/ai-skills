---
name: resolve-conflicts
description: >-
  Resolve git merge, rebase, or cherry-pick conflicts hunk by hunk, by tracing
  what each side was trying to do rather than by picking a side. Reads the
  commits behind both branches, keeps both intents where they are compatible,
  flags semantic conflicts that leave no markers, and finishes the operation
  rather than aborting it. Use when a merge, rebase, cherry-pick, stash pop, or
  pull leaves conflicts, when git reports "CONFLICT (content)", "fix conflicts
  and then commit", or "Unmerged paths", or when the user is stuck part way
  through one. Triggers: "resolve conflicts", "merge conflict", "rebase
  conflict", "fix the conflicts", "git conflict", "help me merge".
---

# resolve-conflicts: resolve by intent, not by side

A conflict is two changes that both had a reason. Picking `--ours` or `--theirs`
throws one reason away silently. The job is to find both reasons and produce the
code that satisfies both.

**Never run `--abort` without asking.** The user may have real work in the
resolution already. Aborting is their call, not yours.

**Never resolve a hunk you do not understand.** Ask instead.

## Step 1: Find out what is actually running

```
git status
git diff --name-only --diff-filter=U
```

The operation changes what "ours" and "theirs" mean, and getting it backwards is
the classic way to resolve every hunk wrong:

| Operation | `--ours` / `HEAD` is | `--theirs` is |
|---|---|---|
| `git merge` | the branch you are on | the branch being merged in |
| `git rebase` | the **upstream** you are replaying onto | **your** commit being replayed |
| `git cherry-pick` | the branch you are on | the commit being picked |

During a rebase, ours and theirs are inverted relative to a merge. Say out loud
which is which before you touch a hunk.

Check for an interrupted state you did not create: `.git/MERGE_HEAD`,
`.git/rebase-merge/`, or `.git/CHERRY_PICK_HEAD`. If the user is part way
through, find out how far before doing anything.

## Step 2: Trace the intent of both sides

Per conflicted file, before reading a single marker:

```
git log --oneline --merge -- <file>          # commits from both sides that touch it
git log -p HEAD -- <file> | head -100        # what our side did, and why
git log -p MERGE_HEAD -- <file> | head -100  # what their side did, and why
```

Read the commit messages. They tell you the intent that the diff only implies.
Where a message names an issue or a PR, and `gh` is available, read it.

Write one sentence per side before you resolve: *ours renamed the field for the
v2 API; theirs added retry handling to the same function.* Those two are
compatible, and the resolution keeps both. That sentence is the resolution.

## Step 3: Resolve hunk by hunk

For each hunk, classify it:

| Situation | Resolution |
|---|---|
| The two sides changed different things in the same region | Keep both. This is most conflicts. |
| Both sides made the same change | Keep one. Verify they really are the same, not merely similar. |
| One side is a superset of the other | Keep the superset. |
| The two sides genuinely contradict | Stop. Present both intents to the user and ask which wins. |
| One side is a revert of the other | Stop and ask. A revert is a decision, never a merge artifact. |
| Generated or lock files | Do not hand-edit. Take one side and regenerate: `npm install`, `cargo build`, the codegen command. |

Never leave a marker. Never keep both copies of a function "to be safe". Never
comment one side out.

Where you keep both sides, check the result actually composes. Two correct edits
to the same function can merge into a function that is wrong.

## Step 4: Hunt the semantic conflicts

The dangerous conflicts leave no markers. Git merged cleanly because the two
changes were in different places, and the result is still broken:

- Ours renamed a function, theirs added a new call to the old name. Clean merge,
  build fails.
- Ours changed a function's return type, theirs added a caller expecting the old
  one.
- Ours removed a config key, theirs added a reader for it.
- Both sides added a migration, and now two migrations claim the same version.
- Both sides added a dependency at different versions.

So after resolving markers, **build and run the tests**. A clean `git status` is
not a resolved merge. Where the repo has a type checker or a linter, run those
too: they catch exactly this class.

## Step 5: Finish the operation

```
git add <resolved files>
git merge --continue      # or: git rebase --continue / git cherry-pick --continue
```

Leave the generated merge commit message alone unless it is wrong. Where you made
a real judgment call resolving a hunk, add a line to the message saying which
intent won and why.

Never `git commit -am` your way out of a rebase. Use the operation's own
`--continue`.

## When to stop and ask

- The two sides contradict on purpose.
- Either side is a revert.
- The conflict is in a migration, a lock file, or anything schema-shaped.
- More than roughly 20 files conflict, which usually means the branch should be
  rebased differently or split, not resolved.
- You cannot state both intents in a sentence each.

Presenting the two intents and asking costs one message. Guessing costs a
silently dropped feature that shows up in production a week later.

## Done when

- No conflict marker survives anywhere: `git grep -nE '^(<<<<<<<|=======|>>>>>>>)'` is empty.
- Both intents are stated, and the resolution satisfies both or the user chose.
- The build passes and the tests pass, having actually been run.
- The type checker and linter pass, where the repo has them.
- Generated and lock files were regenerated, not hand-merged.
- The operation is finished, so `git status` is clean.
