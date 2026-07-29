# Architecture notes

Deeper wiring than the one-line layout map in CLAUDE.md. Keep curated and
current — this file is loaded into every session. Remove entries that stop
being true.

- **What loads when is the real architecture of this repo.** Four tiers,
  and every design trade-off here is paid in one of them:
  `hooks/instructions.md` plus the project's three curated experience
  files load on *every* session, in every project the plugin is installed
  for — that tier is the expensive one, hence the ~4k budget;
  `learnings.md` is read on demand only; a skill's body costs nothing
  until it is invoked, but its frontmatter `description` is always in the
  model's list — which is why triggers live there and detail lives in the
  body; `hooks.json` itself costs nothing, it is plumbing.
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
