# Architecture notes

Deeper wiring than the one-line layout map in CLAUDE.md. Keep curated and
current — this file is read before planning and before any change to how the
parts fit. Remove entries that stop being true.

- **What loads when is the real architecture of this repo.** Four tiers,
  and every design trade-off here is paid in one of them:
  `hooks/instructions.md` alone loads on *every* session, in every project
  the plugin is installed for — the expensive tier, hence a 9,000-char soft
  budget set as a tripwire below the hard 10,000-char-per-hook-entry cap it
  must stay under (see gotchas); the project's `.claude/` experience files are
  injected nowhere and cost nothing until an agent reads one against a
  trigger in the instructions, so their bill is per read, not per session;
  a skill's body costs nothing until it is invoked, but its frontmatter
  `description` is always in the model's list — which is why triggers live
  there and detail lives in the body; `hooks.json` itself costs nothing, it
  is plumbing.
- **Trading an injected file for a read trades a cost for a trigger.**
  Reading the experience files on demand (2026-07-30) retires a silent cap
  failure and makes the bill proportional to use, but it converts one
  unmissable moment into per-file triggers — and a trigger that doesn't fire
  is indistinguishable from a file with nothing to say. So each trigger
  names an observable moment ("before your first edit"), never "when
  relevant", and the triggers themselves live in `hooks/instructions.md`,
  the one tier still guaranteed to be in context.
- **An instruction only fires if it is in context at the moment it must
  fire.** Session-start text — hook payload or CLAUDE.md alike — competes
  with everything else by the time execution begins, which is why the
  muster rule also rides *inside* plan text (the mandatory Execution
  section). Corollary for every default we set: silence must mean the
  behavior we want, because silence is the most common case.
- **The plugin writes nothing into a user's repo; it serves its
  instructions live at session start.** That is the whole 0.8.0 bet:
  copied text drifts from shipped text, so we stopped copying —
  install scope is the only gate (user-level = every repo, project-level
  = that repo), upgrading the plugin upgrades every project at once, and
  the only project state left is what the *user's own* sessions write
  (`.claude/` experience files, `party.json`). The cost is that the hook
  is now a hard dependency: no POSIX shell, no instructions.
- **The party is one builder, an unconditional reviewer, and a third
  member held in reserve.** Deliberate, not arbitrary: the consensus
  failure mode of workflow plugins is the ceremony tax, and a reviewer
  earns its cost only where it isn't ceremonial. Hence fighter → cleric
  always, and wizard only on request or after two failed attempts — an
  advisor pushed by default stops being an advisor.
- **When an always-loaded rule doesn't fire, establish whether the model
  disputed the rule or the case.** Only the second is fixed by rewriting
  the rule, and it is fixed by making the rule *decide the case* rather
  than describe the behavior — every more-text fix feeds the step that was
  already working. See learnings 2026-07-27.
- **Derived values get recomputed; events get stored.** The inbox count is
  `^## YYYY-` headings counted live and must never be cached — a stored
  counter drifts on hand edits, merges and Long Rest rewrites. A level is
  an event, so `CHRONICLE.md` stores it as `## Level N`, which the next
  rest parses. See learnings 2026-07-28.
- **A text budget only holds where the argument is no longer in context.**
  `decisions.md` has inflow from two rules and an outflow gated on "stopped
  being true", which a decision never does — and a write-time budget is no
  fix either: that shipped 2026-07-27 and was violated the same day, in the
  file defining it, because a writer still holding the argument finds every
  clause load-bearing. So the bound is the Long Rest's compact step, which
  moves the entry to `learnings-archive.md` verbatim before cutting it to
  its claim; its gauge is the only thing that makes the read cost of the
  curated three visible. See learnings 2026-07-27, 2026-07-29.
