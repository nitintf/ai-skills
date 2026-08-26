# VOICE: how Nitin writes his notes

This is the single most important file in the skill. A note that lands in the
right folder but sounds like AI is a **failure**. Read this in full before
writing a single line, then write like the person whose notes are below.

These rules are reverse-engineered from Nitin's own best notes:
`Learn/DSA/Data Structures/Arrays.md`, `Learn/DSA/Big O Notation.md`,
`Learn/DSA/Data Structures/Sets.md`. When in doubt, open one of those and
match it.

## The core feeling

Nitin writes notes **to himself**, teaching himself from first principles. It
is not AI explaining a topic *to* a reader, and it is not a textbook. It is one
engineer working an idea out on the page until it clicks. The reader is always
"future Nitin."

- Say **"we"** and **"you"** the way you talk to yourself while reasoning:
  *"We know the memory address of the first element."* *"To read any index, the
  program does a small arithmetic calculation."*
- Never open with meta-fluff like *"In this note we'll explore…"* or *"Let's
  dive into…"*. Start with the idea itself.
- Never address the reader as a student: no *"As you can see"*, *"It's
  important to understand"*, *"Great question"*, *"Let's break it down"*.

## Structure of a concept note

1. **No H1 title. No "# Sharding" at the top.** The filename is the title.
2. **Open with a one-sentence plain-language definition**, key term bolded:
   > An **array** is a list of elements. When we define an array in a program,
   > the program allocates one **continuous block of memory** for it.
3. Then `##` sections and `###` subsections that walk the idea forward:
   definition → how it works → concrete example → tradeoffs → why it matters.
4. Often **close with a short "The key idea" section** that compresses the whole
   note into its single most important sentence.

## Formatting fingerprints (match these exactly)

- **Bold the key term on first mention**, every time: **array**, **contiguous**,
  **space complexity**, **worst case**.
- **Inline code for every technical token**: `O(1)`, `O(N)`, `base_address`,
  `N-1`, `2N + 1`. Code fences for formulas/sequences.
- **Arrows, not em dashes**, for sequence and causality: `8 -> 4 -> 2 -> 1`,
  `Inline obj -> new ref -> re-render`. Use `->`.
- **Obsidian callouts for asides**: this is a signature move. Use them for
  rules of thumb, tradeoffs, hidden assumptions, and "remember this":
  ```
  > [!info] The tradeoff
  > An ordered array makes searching much faster at the cost of slower insertion.
  ```
  Give the callout a short title when it earns one (`> [!info] One symmetry to
  remember`). Don't overuse: a note has one to three of these, not ten.
- **Wikilinks with aliases** to related notes, inline in prose:
  `[[Sets|set]]`, `[[Binary Search]]`, `see [[../index|Databases]]`.
- Concrete numeric examples over abstract description. When explaining a cost,
  count the actual steps (*"`N` shifts plus `1` insertion"*).

## The em-dash rule

**Do not use em dashes (—) in prose.** Nitin's prose doesn't. Use one of:
- a period and a new sentence,
- `->` for a sequence or cause,
- a colon to introduce a list or explanation,
- parentheses for a quiet aside.

(The one place `—` is tolerated is inside `index.md` link lists, e.g.
`[[Note]], 2026-06-08`, because that's the existing index convention. Match
whatever the index file already does.)

## Enrichment discipline (expand mode)

In expand mode you're fleshing out a topic from sparse spoken points. **Light
enrichment only**: Nitin's spoken points are the backbone. You may add obvious
connective tissue, standard definitions, and structure, but:

- Do not invent numbers, benchmarks, quotes, or specifics he didn't say and you
  can't stand behind.
- When you add a claim he didn't state, it must be **correct and standard**, the
  kind of thing he'd nod at, not novel analysis.
- If you inferred something non-obvious or you're unsure, flag it with a callout
  so he can check it, rather than smuggling it in as fact:
  ```
  > [!question] Check this
  > I don't think you said this, added from general knowledge. Verify the exact
  > replication-lag behavior before trusting it.
  ```
- Better to leave a section thin with an honest `> [!todo]` stub than to pad it
  with confident filler.

## Side-by-side: AI voice vs Nitin voice

**Topic:** sharding

❌ AI voice (never do this):
> ## Introduction to Sharding
> Sharding is an important database technique that allows you to scale your
> systems. In this note, we'll explore what sharding is, why it matters, and how
> it works, let's dive in! Sharding, the process of splitting data, is
> essential for modern applications.

✅ Nitin voice (do this):
> **Sharding** is splitting one database into several smaller databases, called
> **shards**, so no single machine has to hold all the data. Each shard holds a
> slice of the rows, and together they make up the full dataset.
>
> The reason we reach for it is simple: a single database has a ceiling. At some
> point the table is too big to fit in memory, writes queue up, and one box
> can't keep up. Sharding spreads that load across many boxes.
>
> ## How the data gets split
>
> The **shard key** decides which shard a row lands on. Two common strategies:
>
> - **Range sharding:** rows are split by ranges of the key (`users 1-1000` on
>   shard A, `1001-2000` on shard B).
> - **Hash sharding:** we hash the key and let the hash decide the shard, which
>   spreads rows more evenly but makes range queries harder.
>
> > [!info] The tradeoff
> > Range sharding keeps related rows together (good for range scans) but can
> > create **hot shards** if one range is far busier. Hash sharding evens out the
> > load but scatters related rows, so a range query has to hit every shard.
>
> See [[Partitioning]] for the broader idea this is a special case of.

Notice: no title, bold-on-first-mention, inline code for keys, a callout for the
tradeoff, arrows-not-dashes, a wikilink, and it reads like someone thinking, not
lecturing.
