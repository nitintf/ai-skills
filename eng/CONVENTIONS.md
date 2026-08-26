# House Conventions: what to extract, and the cache format

Almost every `eng` skill needs the same thing: *how does THIS repo already do
the kind of work I'm about to plan, review, or write?* This file is the single
definition of what that means, so ten skills don't answer it ten different ways.

- **`/conventions` writes** `.plan/_conventions.md` using the format in §2.
- **Every other skill reads** that file first, then explores only the gaps
  (the protocol is in `SPEC.md` §6).

The bar for everything here: **coordinates, not adjectives.** "Errors are handled
consistently" is worthless. ``errors are wrapped with `AppError`: see
`src/lib/errors.ts:14`, used at `src/api/users.ts:63``` is the deliverable. Every
entry cites at least one real `file:line` a reader can open.

---

## 1. The checklist: what counts as a convention

Not every repo has all of these, and a repo may have several answers for one row
(e.g. two API styles mid-migration). **Record what's actually there, including
the inconsistency**: "new code uses X, legacy uses Y, prefer X" is one of the
most useful things this file can say.

### Toolchain & layout
- Language(s), runtime versions, package manager, build tool.
- Top-level directory layout and what each major folder is for.
- How the app is run, built, linted, type-checked, and tested (the actual
  commands, from `package.json` / `Makefile` / `justfile` / CI config).
- Formatter and linter config, and whether it's enforced in CI or a hook.

### Backend / API
- How endpoints, handlers, routes, or RPC methods are **defined and registered**.
- Request validation: what library, where it runs, what a schema looks like.
- The service/domain layer: does one exist, or do handlers talk to the DB?
- Data access: ORM/query builder/raw, where queries live, transaction handling.
- Auth: how a request is authenticated and how authorization is checked.

### Frontend / UI
- Component file structure: one per file? co-located styles/tests? index barrels?
- Props typing, state management, and the data-fetching pattern.
- Styling approach (CSS modules, Tailwind, styled-components, a design system).
- Shared primitives that already exist, the button, the modal, the form field.
  Reinventing one of these is the single most common house-style violation.

### Cross-cutting
- **Error handling**: custom error types, wrap-vs-throw, what reaches the user.
- **Logging**: the logger, its levels, what gets structured fields, what's
  never logged (PII, secrets, tokens).
- **Config & secrets**: where env vars are read, whether they're validated at
  boot, how a new setting gets added.
- **Async**: promises vs async/await, concurrency limits, retry/backoff,
  cancellation, queue or job system.
- **Types**: shared type location, `any` policy, generated types (OpenAPI,
  Prisma, GraphQL codegen).

### Naming & style
- File naming (kebab? camel? PascalCase for components?), directory naming.
- Symbol naming: booleans, handlers, hooks, constants, test names.
- Import ordering and whether path aliases (`@/…`) are used.
- Comment culture, sparse and load-bearing, or heavily documented?

### Tests
This row matters more than the others, because it's where generated code most
visibly fails to match a team.
- Framework and runner, plus the exact command to run one file.
- Location: co-located `*.test.ts` or a `tests/` tree? Naming convention?
- Structure: `describe`/`it` vs flat, AAA vs given/when/then phrasing.
- Fixtures, factories, and builders that already exist, use them, don't hand-roll.
- Mocking approach and how the boundary (DB, HTTP, clock) is faked.
- What the repo does **not** test: a team that never unit-tests controllers is
  telling you something; don't fight it in a single PR.

### Git & delivery
- Branch naming, commit message convention (Conventional Commits? ticket prefix?).
- PR conventions: template, size norms, required checks, review expectations.
- Release/deploy mechanics and feature-flagging, if visible.

---

## 2. The cache format

`/conventions` writes exactly this shape to `.plan/_conventions.md`:

```markdown
---
generated: <YYYY-MM-DD>
commit: <short SHA the scan was run against>
scanned: <one line on breadth, e.g. "full repo" or "apps/web + packages/core">
---

# House Conventions: <repo name>

<2-4 sentences: what this codebase is, its architecture in one breath, and the
single most important thing to know before writing code in it.>

## Toolchain
| Thing | Answer | Evidence |
|-------|--------|----------|
| Language / runtime | TypeScript 5.4, Node 20 | `package.json:12` |
| Test command | `pnpm vitest run <file>` | `package.json:31` |
| … | … | … |

## <Area: e.g. API, Components, Errors, Logging, Config, Tests, Git>
**Pattern:** <one sentence stating the rule.>
**Canonical example:** `path/to/file.ts:42`
**How to add a new one:** <the concrete steps someone follows.>
**Watch out:** <the legacy variant, the deprecated helper, the trap.>

<repeat per area from §1 that this repo actually has>

## Existing primitives: check here before writing a new one
| Need | Already exists | Where |
|------|----------------|-------|
| HTTP client with auth | `apiClient` | `src/lib/api.ts:8` |
| … | … | … |

## Inconsistencies
<Places the repo genuinely disagrees with itself, and which way is winning.
Say which one new code should follow, and why you think so.>

## Not determined
<Honest list of things you looked for and could not establish. A gap named is
worth more than a convention invented.>
```

---

## 3. Rules for whoever writes or consumes this

- **Describe reality, not best practice.** If this repo puts business logic in
  route handlers, that's the convention. Note it as a smell if you like, but
  record what's true. A conventions file full of what the code *should* do makes
  every downstream skill generate code that doesn't fit.
- **Prefer recent code as the source of truth.** When old and new disagree, look
  at what the last few months of commits actually did (`git log --since`), and
  say "new code does X" explicitly.
- **Never invent an entry to fill a row.** Empty is fine. "Not determined" is
  fine. A fabricated convention propagates into every plan and every PR after it.
- **Consumers append, they don't rewrite.** If a skill discovers a convention the
  cache lacks, add the entry. Only `/conventions` regenerates the file wholesale.
- **A stale cache is worse than none.** Consumers check `commit:` against
  `git log -1` and flag drift rather than trusting it blindly.
