---
description: The Long Rest — distill the learnings inbox into the project's curated experience files and hold gotchas.md to its cap (user-invoked ceremony)
agent: build
model: party-models:long-rest
---

# The Long Rest

`.claude/learnings.md` is an inbox, not an archive: entries land there
un-curated as sessions surface them. The Long Rest is where the party
trains — the inbox is distilled into the curated files the party reads at
their triggers, then emptied, so a leveled-up party is a better-informed
party. It is also the only thing that bounds those files: distilling grows
them, so the same ceremony moves gotchas that have a home in the code into
that code, holds `gotchas.md` to its 8,000-character cap, compacts what has
outgrown its budget, and reports what the files now cost to read.

## Before anything: state the plain reading and the price

First check whether the project's source files — everything outside
`.claude/` and `CHRONICLE.md` — have uncommitted changes. The rest may edit
them, and its edits should review as their own diff; mixed into unfinished
work, they can't. If there are any, say so in the opening message and ask
whether to proceed anyway.

Open with (in your own words, both halves mandatory):

> A Long Rest distills your project's learnings inbox into the curated
> experience files (its memory), moves gotchas that belong in the code into
> that code — as comments and test failure messages, never logic — until
> `gotchas.md` is back under its 8,000-character cap, shortens entries that
> have outgrown their budget (the full text of everything moved or
> shortened is kept in the archive), archives the processed entries,
> records the level in the chronicle, and tells you what the curated files
> now cost to read. It uses real tokens, runs your test command, and edits
> `.claude/architecture.md`, `gotchas.md`, `decisions.md`, `learnings.md`,
> `.claude/learnings-archive.md`, `CHRONICLE.md`, and comments and test
> failure messages in your source files — the report lists every source
> file it touched. Proceed?

Wait for a yes. Empty (or nearly) inbox: say so honestly and ask whether to
rest anyway — a small rest still holds `gotchas.md` to its cap. Count the
inbox without reading it: `^## [0-9]{4}-` matches in
`.claude/learnings.md`, via grep in count mode. Never read the whole log
just to count it.

## The ceremony — order matters

The chronicle entry is written **last** and the inbox's archive move happens
with it: the chronicle is the atomic commit-record of the rest. Aborted
early, the inbox is intact and the next rest redoes the same work — every
earlier step is idempotent: the relocate and compact steps skip an archive
append whose text is already there, and never write a code comment or
failure message twice.

1. **Scope.** Every entry in `.claude/learnings.md`. Exception: if
   `CHRONICLE.md` has a `*Distilled through YYYY-MM-DD.*` line, entries on
   or before that date were distilled already — archive them in step 7
   unread, distill only what's newer.
2. **Distill.** For each entry decide where its durable core belongs and
   put it there, **skipping anything already present**. A trap goes to the
   first home that catches it — the order every session captures by: the
   test that guards it (the why in its failure message), else a comment at
   the code it concerns, else — only for traps no code owns: tooling,
   environment, cross-cutting — 1–2 lines in `gotchas.md`. A general coding
   lesson, true in any project, goes in none of them; the archive keeps it.
   How the parts fit goes to `architecture.md`, why A over B to
   `decisions.md` (~2 lines), each in that file's format and within budget.
   Code edits follow step 4's rules (comments and failure messages only,
   never logic) and its test runs (baseline before the first edit, re-run
   in step 4). Distilling = compressing to the durable core and pointing
   back ("see learnings YYYY-MM-DD"), not restating the argument. Many
   entries distill to nothing durable; normal. Never edit an entry's text —
   it moves to the archive verbatim. A curated entry that lands over budget
   is step 5's to cut.
3. **Prune.** Remove gotchas whose cause is verifiably fixed (check the
   tree, not memory), curated entries that stopped being true, and
   superseded decision tombstones that stopped earning their line.
4. **Relocate.** `gotchas.md` is capped at 8,000 characters (`wc -m`), held
   by moving entries into the code they concern — read exactly when that
   code is, free everywhere else. At or under the cap, move no entries: if
   step 2 made code edits, run sub-steps 1 and 3 for them, then step 5;
   if none, skip to step 5. Over it, ask of each entry *would
   an agent still fall into this trap without this line?* and sort it:
   - **A test guards it** (falling in turns it red) — confirm the test
     exists by name in the tree and checks this trap; one the entry names
     but the tree lacks guards nothing. Add the why to its failure message
     if missing.
   - **It concerns one file or function** — a comment of at most two lines
     at that spot, in the file's own comment style, saying the trap and its
     why. Skip the write if one there already says it.
   - **A general coding lesson**, true in any project — archive only.
   - **No code owns it** (tooling, environment, cross-cutting) — it stays.

   Code edits are comments and failure messages only, **never logic**:
   never change what an assertion checks, add or remove a test, or change
   what any line does. A failure message belongs to an existing assertion —
   adding or extending one is the only edit allowed on a line that runs;
   where the framework gives an assertion no message, comment beside it. A
   file that takes no comments (JSON, say) can't hold a trap — that entry
   stays.

   Pick entries to move cheapest first — general lessons, then
   test-guarded, then new comments — until moving them brings the file to
   or under the cap, or only entries no code owns are left. Then, in this
   order, so a re-run picks up where an aborted one stopped:
   1. Unless step 2 already took it, run the project's documented test
      command for a baseline, before any code edit. A test already failing
      is the project's, not the rest's: name it in the report, leave it
      alone. No documented test command: write comments only, no failure
      messages, and report the code edits as untested.
   2. Write each chosen entry's comment or failure message. Code text
      pointing back at `gotchas.md` for a moving entry (a comment, a
      failure message, a test helper's message string) would point at
      nothing once it leaves: repoint it at the new home or drop the
      reference — a comment or message edit, same rules.
   3. Re-run the tests. A test the baseline passed now fails → the rest's
      own edits broke it: find the entry responsible, undo its edits, and
      keep it where it is (a trap from step 2 goes to `gotchas.md` instead).
   4. For each entry still moving, append its **verbatim** text to
      `.claude/learnings-archive.md` under `## YYYY-MM-DD — Relocated
      gotcha: <short title>` (today's date), then one line naming where it
      went — the test by name, the file and function, or "archive only".
      Create the file as step 7 says if missing; skip if already there.
   5. Only then remove the entry from `gotchas.md`.

   Measure again; still over with movable entries left → go round again.
   Never delete a true trap just to fit: if only entries no code owns
   remain and the file is still over, it stays over and the report says so
   with their count.
5. **Compact.** Entries past budget: unless the archive already holds its
   full current text (no pointer, or a pointer whose archived text the
   entry has outgrown, both mean not held), append its verbatim text to
   `.claude/learnings-archive.md` first (under `## YYYY-MM-DD — title` with
   the entry's own date, else today's; create the file as step 7 says if
   missing; skip if already there), then cut the live entry to its claim
   plus a pointer at the heading holding its full text —
   keep the date, the choice, the rejected alternative in one clause, one
   why-clause, and any `*Superseded:*` / `*Amended:*` tombstone. The
   rejected alternative is what stops the next session re-litigating a
   settled call. Never compact an entry whose pointer resolves to nothing —
   skip it and name it in the report.
6. **Flag junk, don't drop it.** Entries that shouldn't have been logged
   (routine work, narration) get a one-line mention in the chronicle notes;
   they still archive. Routine work is git history, not a learning.
7. **Archive and empty the inbox.** Append every processed entry, verbatim
   and in order, to `.claude/learnings-archive.md` (create with a
   `# Learnings archive` heading if missing). Leave `.claude/learnings.md`
   as its bare header only. The empty inbox is the watermark — write no
   watermark line.
8. **Chronicle.** Append to `CHRONICLE.md` (create with `# Chronicle` if
   missing):

   ```markdown
   ## Level 3 — Wardens of the Unbroken Build — YYYY-MM-DD

   <The saga in plain language: what was built this level, what was
   conquered (bugs and traps, from the learnings), what the player learned
   (from the decisions and their whys). A few short paragraphs. Notes: junk
   flagged, anything pruned or relocated.>
   ```

   `N` = last `## Level N` heading plus one (no chronicle or no level
   heading means Level 2). The heading format is load-bearing.

## The title

Deterministic — same repo, same level, same title:

1. `N=$(printf '%s' "<repo-dir-basename>:<level>" | cksum | cut -d' ' -f1)`
2. Title = `<ORDER[N % 16]> of the <ADJ[(N / 16) % 16]> <NOUN[(N / 256) % 16]>`

| i | ORDER | ADJ | NOUN |
|---|-------|-----|------|
| 0 | Wardens | Unbroken | Build |
| 1 | Keepers | Emerald | Spire |
| 2 | Seekers | Iron | Oath |
| 3 | Blades | Silent | Road |
| 4 | Shields | Gilded | Forge |
| 5 | Heralds | Storm-born | Archive |
| 6 | Wanderers | Ember | Gate |
| 7 | Sentinels | Moonlit | Summit |
| 8 | Champions | Thorned | Beacon |
| 9 | Scribes | Azure | Vault |
| 10 | Vanguards | Wandering | Bridge |
| 11 | Pathfinders | Steadfast | Harbor |
| 12 | Lanterns | Hollow | Grove |
| 13 | Banners | Bright | Citadel |
| 14 | Outriders | Ashen | Ledger |
| 15 | Stalwarts | Winter | Star |

## Report

Level reached and title; what was distilled where (counts, files); what was
pruned; what was relocated — how many entries went to a test's failure
message, to a code comment, and to the archive only — and **every source
file touched**, plus any entry kept because its edits turned a test red,
any test already failing before the rest, and whether the code edits went
untested; what was compacted and any entry skipped for an unresolved
pointer; junk flagged; entries archived. Plain language first, flavor
second.

Then the gauge, **every rest**: measure `.claude/architecture.md`,
`gotchas.md` and `decisions.md` in characters (`wc -m`, never `wc -c`).
State all three and the total; read each file on its own, not the total.
`gotchas.md` against its cap:

> **at or under 8,000 — at the cap · over it — only traps no code owns are
> left (say how many)**

`architecture.md` and `decisions.md` against:

> **under 8k fine · 8–15k worth a review · over 15k act on it**

This is a read-cost gauge, not a truncation guard. Say the number even when
it's fine — drift is invisible without a previous reading.
