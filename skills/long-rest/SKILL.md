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
*trains* — the inbox is distilled into the curated files that load every
session, then emptied, so a leveled-up party is literally a better-informed
party.

## Before anything: state the plain reading and the price

Open with (in your own words, both halves mandatory):

> A Long Rest distills your project's learnings inbox into the curated
> experience files (its memory), archives the processed entries, and records
> the level in the chronicle. It uses real tokens and edits
> `.claude/architecture.md` / `gotchas.md` / `decisions.md`,
> `.claude/learnings.md`, `.claude/learnings-archive.md` and `CHRONICLE.md`.
> Proceed?

Wait for a yes. If the inbox is empty or nearly so, say that honestly and
ask whether to rest anyway — a small rest is allowed, it just distills less.

Count the inbox with the Grep tool in count mode (`^## [0-9]{4}-` over
`.claude/learnings.md`). Never read the whole log just to count it.

## The ceremony — order matters

The chronicle entry is written **last** and the archive move happens with
it: the chronicle is the atomic commit-record of the whole rest. If the
ceremony is aborted at any earlier step the inbox is still intact, so the
next rest simply redoes the same work — every earlier step is idempotent by
design.

1. **Scope.** Every entry in `.claude/learnings.md`. One exception, for
   projects carried over from the watermark era: if `CHRONICLE.md` contains
   a `*Distilled through YYYY-MM-DD.*` line, entries dated on or before the
   last such date were already distilled by an earlier rest — archive them
   in step 5 without reading or re-distilling them, and distill only what is
   dated after it.
2. **Distill.** For each in-scope entry, decide where its durable core
   belongs — `architecture.md`, `gotchas.md`, `decisions.md` — and add it
   there in that file's format and **within its length budget** (gotchas 1–2
   lines, decisions ~2), **skipping anything already present** (idempotent).
   Distilling means compressing to the durable core and pointing back — "see
   learnings YYYY-MM-DD" — not restating the argument in a file that loads
   every session. Many entries distill to nothing durable; that's normal.
   Never edit the text of an entry itself — it moves to the archive verbatim.
3. **Prune.** Remove gotchas whose underlying cause is verifiably fixed
   (check the code/tree, not memory), curated entries that stopped being
   true, and decision entries whose superseded tombstone has long since
   stopped earning its line. This is the hygiene the curated files' own
   contract demands.
4. **Flag junk, don't drop it.** In-scope entries that shouldn't have been
   logged (routine work, session narration) get a one-line mention in the
   chronicle entry's notes — they still go to the archive, and the flag
   teaches the habit. Routine work is git history, not a learning.
5. **Archive and empty the inbox.** Append every processed entry, verbatim
   and in order, to `.claude/learnings-archive.md` (create it with a
   `# Learnings archive` heading and a one-line note that it is written by
   `/party:long-rest` and read on demand). Then leave
   `.claude/learnings.md` as its bare header and nothing else — the next
   entry starts a fresh inbox. Write no watermark line: the empty inbox is
   the watermark.
6. **Chronicle.** Append to `CHRONICLE.md` (create it with a `# Chronicle`
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
pruned; junk flagged; how many entries were archived. Plain language first,
flavor second — the user should know exactly which files changed and why
before they see the trumpets.
