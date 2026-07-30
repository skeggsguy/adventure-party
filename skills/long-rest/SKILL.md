---
name: long-rest
description: The Long Rest — the party's level-up ceremony. Distills the
  learnings inbox into the curated experience files (your project's memory),
  prunes what has stopped being true, archives the processed entries, and
  records the new level in CHRONICLE.md with a seeded title. User-invoked
  only — never run this unprompted, and never suggest it more than once per
  session.
disable-model-invocation: true
---

# The Long Rest

`.claude/learnings.md` is an inbox, not an archive: entries land there
un-curated as sessions surface them. The Long Rest is where the party
*trains* — the inbox is distilled into the curated files the party reads at
their triggers, then emptied, so a leveled-up party is literally a
better-informed party. It is also the only thing that bounds those files:
distilling grows them, so the same ceremony compacts what has outgrown its
budget and reports what they now cost to read.

## Before anything: state the plain reading and the price

Open with (in your own words, both halves mandatory):

> A Long Rest distills your project's learnings inbox into the curated
> experience files (its memory), shortens entries that have outgrown their
> budget (their full text is kept in the archive), archives the processed
> entries, records the level in the chronicle, and tells you what the curated
> files now cost to read. It uses real tokens and edits
> `.claude/architecture.md` / `gotchas.md` / `decisions.md`,
> `.claude/learnings.md`, `.claude/learnings-archive.md` and `CHRONICLE.md`.
> Proceed?

Wait for a yes. If the inbox is empty or nearly so, say that honestly and
ask whether to rest anyway — a small rest is allowed, it just distills less.

Count the inbox without reading it: `^## [0-9]{4}-` matches in
`.claude/learnings.md`, via whatever search tool the session has (Grep in
count mode, or `grep -c`). Never read the whole log just to count it.

## The ceremony — order matters

The chronicle entry is written **last** and the *inbox's* archive move
happens with it: the chronicle is the atomic commit-record of the whole
rest. If the ceremony is aborted at any earlier step the inbox is still
intact, so the next rest simply redoes the same work — every earlier step is
idempotent by design, the compact step's own archive appends included.

1. **Scope.** Every entry in `.claude/learnings.md`. One exception, for
   projects carried over from the watermark era: if `CHRONICLE.md` contains
   a `*Distilled through YYYY-MM-DD.*` line, entries dated on or before the
   last such date were already distilled by an earlier rest — archive them
   in step 6 without reading or re-distilling them, and distill only what is
   dated after it.
2. **Distill.** For each in-scope entry, decide where its durable core
   belongs — `architecture.md`, `gotchas.md`, `decisions.md` — and add it
   there in that file's format and **within its length budget** (gotchas 1–2
   lines, decisions ~2), **skipping anything already present** (idempotent).
   Distilling means compressing to the durable core and pointing back — "see
   learnings YYYY-MM-DD" — not restating the argument in a file the party
   re-reads constantly. Many entries distill to nothing durable; normal.
   Never edit the text of an entry itself — it moves to the archive verbatim.
   Anything you write here that lands over budget is fair game for step 4.
3. **Prune.** Remove gotchas whose underlying cause is verifiably fixed
   (check the code/tree, not memory), curated entries that stopped being
   true, and decision entries whose superseded tombstone has long since
   stopped earning its line. This is the hygiene the curated files' own
   contract demands.
4. **Compact.** The prune step drops what stopped being true; this one
   drops what is merely long. Read the three curated files and find every
   entry past its budget — decisions ~2 lines, gotchas 1–2, architecture
   notes one claim plus the evidence for it. For each:
   1. If it carries no `see learnings YYYY-MM-DD` pointer, append its
      **verbatim** text to `.claude/learnings-archive.md` *first*, under a
      `## YYYY-MM-DD — title` heading carrying the entry's own date (create
      the file as step 6 describes if it is missing, and skip the append if
      that text is already there, so a re-run changes nothing). Move, then
      shorten — never shorten in place, or the argument is destroyed rather
      than relocated.
   2. Then cut the live entry to its claim plus a `see learnings
      YYYY-MM-DD` pointer at that heading's date. Keep the date, the
      choice, the rejected alternative in one clause, one why-clause, and
      any `*Superseded:*` / `*Amended:*` tombstone. The rejected
      alternative is the entry's whole job — it is what stops the next
      session re-litigating a settled call.
   3. Never compact an entry whose existing pointer resolves to nothing —
      no entry under that date in the archive, and none in the inbox this
      rest is about to archive. Skip it and name it in the report.

   This step lives here, and not in the rule that writes the entry, for a
   reason worth knowing: whoever writes an entry is still holding the whole
   argument, so every clause feels load-bearing and the budget never bites.
   You are not holding it, which is exactly what makes you able to apply
   the budget.
5. **Flag junk, don't drop it.** In-scope entries that shouldn't have been
   logged (routine work, session narration) get a one-line mention in the
   chronicle entry's notes — they still go to the archive, and the flag
   teaches the habit. Routine work is git history, not a learning.
6. **Archive and empty the inbox.** Append every processed entry, verbatim
   and in order, to `.claude/learnings-archive.md` (create it with a
   `# Learnings archive` heading and a one-line note that it is written by
   `/party:long-rest` and read on demand). Then leave
   `.claude/learnings.md` as its bare header and nothing else — the next
   entry starts a fresh inbox. Write no watermark line: the empty inbox is
   the watermark.
7. **Chronicle.** Append to `CHRONICLE.md` (create it with a `# Chronicle`
   heading if missing):

   ```markdown
   ## Level 3 — Wardens of the Unbroken Build — 2026-07-25

   <The saga, in plain language a non-engineer owns: what was built this
   level, what was conquered (the bugs and traps, from the learnings), what
   the player learned (from the decisions and their whys). A few short
   paragraphs. Notes: junk entries flagged, anything pruned.>
   ```

   `N` is the last `## Level N` heading in `CHRONICLE.md` plus one — no
   chronicle, or no level heading in it, means this rest is Level 2. The
   `## Level N` heading is load-bearing: the next rest parses it.

## The title

Deterministic, so it feels like *this party's* name rather than a slot
machine — same repo, same level, same title, and no randomness needed:

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
pruned; what was compacted, and any entry skipped because its pointer didn't
resolve; junk flagged; how many entries were archived. Plain language first,
flavor second — the user should know exactly which files changed and why
before they see the trumpets.

Then the gauge, **every rest, over budget or not**. Measure
`.claude/architecture.md`, `gotchas.md` and `decisions.md` in *characters* —
`wc -m`, never `wc -c`, or read-and-count; this repo measures text in
characters everywhere. State all three numbers and the total, and read the
line below **per file**, not against the total:

> **under 8k fine · 8–15k worth a review · over 15k act on it**

This is a read-cost gauge, not a truncation guard: nothing clips these files,
but agents re-read them at their triggers, so each one's size is a bill paid
per read. Say the number even when it is comfortably fine: a gauge that only
speaks up in an emergency is a gauge nobody trusts, and drift is invisible
without a previous reading to compare against.
