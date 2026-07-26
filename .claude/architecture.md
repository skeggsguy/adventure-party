# Architecture notes

Deeper wiring than the one-line layout map in CLAUDE.md. Keep curated and
current — this file is loaded into every session. Remove entries that stop
being true.

- **What loads when is the real architecture of this repo.** Four tiers,
  and every design trade-off here is paid in one of them: CLAUDE.md plus
  the three curated experience files load on *every* session;
  `learnings.md` is read on demand only; a skill's body costs nothing
  until it is invoked, but its frontmatter `description` is always in the
  model's list — which is why triggers live there and detail lives in the
  body; `xp.sh` costs zero tokens because it is shell. Bloat in the
  always-loaded tier is the expensive kind.
- **An instruction only fires if it is in context at the moment it must
  fire.** CLAUDE.md is loaded once at session start, then competes with
  everything else by the time execution begins — which is why the muster
  rule rides *inside* plan text (the mandatory Execution section) instead
  of relying on CLAUDE.md alone. Corollary for every default we set:
  silence must mean the behavior we want, because silence is the most
  common case.
- **The plugin ships nothing project-specific; `/party:setup` writes all
  project state.** That asymmetry is what makes install scope the
  installer's free choice — a user-level install is inert in any repo
  that hasn't run setup. It also means shipped text and already-installed
  text drift apart across versions, which is why setup carries the
  fingerprinted migration in step 5a and `memory/legacy-blocks.md` holds
  the exact old bodies to match against.
- **The party is one builder, an unconditional reviewer, and a third
  member held in reserve.** Deliberate, not arbitrary: the consensus
  failure mode of workflow plugins is the ceremony tax, and a reviewer
  earns its cost only where it isn't ceremonial. Hence fighter → cleric
  always, and wizard only on request or after two failed attempts — an
  advisor pushed by default stops being an advisor.
