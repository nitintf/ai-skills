---
name: migrate
description: >-
  Plan and run a data or schema migration without losing data. Characterizes the
  real data first, picks a strategy, writes the rollback before the migration,
  and verifies with queries rather than hope.
disable-model-invocation: true
---

# migrate: change the data without losing any of it

The riskiest change an engineer makes. Code that is wrong can be reverted; data
that is gone is gone. This skill exists because the eng pipeline says anything
touching data runs the full track, and nothing owned that work until now.

**Never run a destructive step until the rollback is written and the backup is
verified.** That ordering is the whole discipline.

## Step 1: Characterize the real data

Not the schema. The data. Query production (or the most recent restore) and
write down actual numbers:

- Row count. The migration plan for 10k rows is not the plan for 500M.
- Null counts on every column you touch. The column you are about to make `NOT
  NULL` almost always has nulls.
- Distinct counts and duplicates on anything you are about to make `UNIQUE`.
- Value ranges, outliers, and the encoding on text columns.
- Rows that already violate the invariant you are about to enforce.

That last one decides the whole plan. **Find those rows before you write the
migration, not when it fails at 3am.** Ask the user what to do with them:
fix, drop, quarantine, or relax the constraint.

Record the numbers in the doc. They are the baseline you verify against later.

## Step 2: Pick the strategy

| Change | Strategy |
|---|---|
| Add a nullable column | Direct. Safe, no lock on most engines. |
| Add a non-null column | Add nullable, backfill, then add the constraint. Three deploys. |
| Backfill a large table | Batch it, with an indexed cursor, a sleep between batches, and a resumable checkpoint. Never one statement. |
| Rename a column or table | Expand and contract: add new, dual-write, backfill, switch reads, stop writing old, drop old. |
| Change a column type | Same expand and contract. Never an in-place `ALTER TYPE` on a large hot table. |
| Drop a column or table | Stop writing, deploy, wait a full retention window, then drop. Never in the same release. |
| Add an index | Concurrently, where the engine supports it. Check the lock behavior for your specific engine and version. |
| Split or merge tables | Dual-write with a reconciliation job, then cut over. |

**Expand and contract** is the default for anything a running app reads. Old code
and new code are live at the same time during a deploy, so every intermediate
state must work for both.

## Step 3: Write the rollback first

Before the forward migration. If you cannot write a rollback, that is the
finding: say so and stop, rather than proceeding and hoping.

The rollback answers three things:

1. **What undoes it.** The exact statements, or the restore procedure where the
   step is not reversible.
2. **What is lost by rolling back.** Writes that landed after the migration.
   Name them.
3. **The point of no return.** The step after which rollback stops being
   possible, usually a drop or an overwrite. Everything before it is cheap,
   everything after it is not.

Confirm a backup exists and is **restorable**, not merely present. An untested
backup is a guess.

## Step 4: Write the verification

Queries that prove the migration worked, written before it runs:

- Row counts reconcile: source count equals destination count, or the difference
  is a number you predicted.
- No nulls where nulls are now illegal.
- A sample of rows compared field by field, old against new.
- The invariant you were enforcing actually holds.
- Nothing outside the intended scope changed. Checksum or count the neighbours.

"It ran without an error" is not verification. A migration that silently touched
zero rows also runs without an error.

## Step 5: Dry run

Run the whole thing against a restored copy of production, not a seeded dev
database. Dev data will not have the nulls, the duplicates, or the 2019 rows
with the broken encoding.

Time it. A backfill that takes four minutes on a copy takes longer under
production load, and you need to know whether it fits the window.

## Step 6: Execute

Staged, with a checkpoint at each step:

1. Take the backup. Verify it restores.
2. Run the forward step.
3. Run the verification queries. Compare against the Step 1 baseline.
4. Watch error rates and latency before moving to the next step.

Stop at the first surprise. A number that differs from the baseline by an amount
you cannot explain is a stop, not a rounding difference.

## Step 7: Record it

Write the baseline numbers, the strategy, the rollback, the verification results,
and anything surprising into the `.plan` doc's Work Log where one exists. The
next person doing this to the same table needs your numbers.

## Done when

- Baseline counts from real data are recorded.
- Rows that violate the new invariant were found and their handling was agreed
  with the user.
- The rollback is written, and the point of no return is named.
- A backup exists and has been restored successfully at least once.
- The verification queries are written, and were run after the migration.
- Counts reconcile against the baseline, or every difference is explained.
- The dry run was against a production restore, not seed data.
