---
name: level-up
description: The Long Rest — the party's level-up ceremony. Distills the
  append-only learnings log into the curated experience files (your
  project's memory), prunes fixed gotchas, and records the level in
  CHRONICLE.md with a seeded title. User-invoked only — never run this
  unprompted, and never suggest it more than once per session.
disable-model-invocation: true
---

# The Long Rest

Levels are earned by experience: every `## YYYY-MM-DD` entry in
`.claude/learnings.md` is one XP. The Long Rest is where the level-up
actually happens — and it is not a fireworks display. It is the moment
the party *trains*: the append-only log gets distilled into the curated
files that load every session, so a leveled-up party is literally a
better-informed party.

## Before anything: state the plain reading and the price

Open with (in your own words, both halves mandatory):

> A Long Rest distills your project's experience files (its memory) into
> shape and records the level in the chronicle. It uses real tokens and
> edits `.claude/architecture.md` / `gotchas.md` / `decisions.md` and
> `CHRONICLE.md`. Proceed?

Wait for a yes. If the party hasn't actually reached a new level
(compute it first — see below), say so honestly and ask whether to rest
anyway; a below-threshold rest is allowed, it just doesn't change the
level.

## Computing XP and level

- XP: count of lines matching `^## [0-9]{4}-` in `.claude/learnings.md`.
- Level: 1, +1 at each threshold 10 / 25 / 50 / 100, then +100 per
  level beyond (200, 300, …).
- Chronicled level: the last `## Level N` heading in `CHRONICLE.md`
  (1 if the file doesn't exist).

Count with the Grep tool in count mode — the log is append-only and
gets long, and there is never a reason to read it just to count it.

## The ceremony — order matters

The chronicle entry is written **last**: it is the atomic commit-record
of the whole rest. If the ceremony is aborted at any earlier step, no
chronicle means no new watermark, and the next Long Rest simply redoes
the same window — every earlier step is idempotent by design.

1. **Find the watermark.** The last `*Distilled through YYYY-MM-DD.*`
   line in `CHRONICLE.md`. Only learnings entries dated AFTER it are in
   scope — this bounds the cost of every rest after the first. No
   chronicle yet → the whole log is in scope.
2. **Distill.** For each in-scope learnings entry, decide where its
   durable core belongs — `architecture.md`, `gotchas.md`,
   `decisions.md` — and add it there in that file's format **and within
   its length budget** (gotchas 1–2 lines, decisions 3–5), **skipping
   anything already present** (idempotent). Distilling means compressing
   to the durable core and pointing back — "see learnings YYYY-MM-DD" —
   not restating the argument in a file that loads every session. Many
   entries distill to nothing durable; that's normal. Never edit or
   delete the learnings entries themselves — the log is append-only, and
   it is the XP record.
3. **Prune.** Remove gotchas whose underlying cause is verifiably fixed
   (check the code/tree, not memory), and curated entries that stopped
   being true. This is the hygiene the curated files' own contract
   demands — it costs XP nothing, because XP counts only the log.
4. **Flag junk, don't delete it.** In-scope entries that shouldn't have
   been logged (routine work, session narration) get a one-line mention
   in the chronicle entry's notes — the log keeps them (append-only),
   the flag teaches the habit. Junk entries are dead weight the party
   carries; routine work is git history, not XP.
5. **Chronicle.** Append to `CHRONICLE.md` (create it with a `# Chronicle`
   heading if missing):

   ```markdown
   ## Level 3 — Wardens of the Unbroken Build — 2026-07-25

   <The saga, in plain language a non-engineer owns: what was built
   this level, what was conquered (the bugs and traps, from the
   learnings), what the player learned (from the decisions and their
   whys). A few short paragraphs. Notes: junk entries flagged, anything
   pruned.>

   *Distilled through 2026-07-25.*
   ```

   The `## Level N` heading and the watermark line are load-bearing —
   the next rest parses them, and so does the Guide's level-up nudge.
   The level recorded is the computed level (unchanged, on a
   below-threshold rest). The watermark
   date is the date of the newest learnings entry distilled; if the rest
   found no in-scope entries, carry the previous watermark forward (or
   use today's date on a first-ever rest).

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

Level reached and title; what was distilled where (counts, files); what
was pruned; junk flagged; the new watermark. Plain language first,
flavor second — the user should know exactly which files changed and
why before they see the trumpets.
