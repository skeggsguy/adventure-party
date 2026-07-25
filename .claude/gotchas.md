# Gotchas

Non-obvious traps. Loaded into every session — keep each entry to 1–2 lines
and delete entries once the underlying cause is fixed.

- Skill frontmatter `description` is the ONLY trigger guidance the main
  session sees before loading a skill — instructions inside the skill body
  can't influence whether it fires. Phrase triggers continuously ("every
  turn", drift included) plus an explicit not-this-case, or the skill misses
  conversations that *become* its use case. See 2026-07-25 in learnings.md.
- A plugin can ship agents/skills but can NEVER write into a user's
  `.claude/` — anything the user's repo must own (the memory files, the
  CLAUDE.md merge) has to come from a user-invoked skill reading
  `${CLAUDE_PLUGIN_ROOT}`.
- A project-level `.claude/agents/<name>.md` silently overrides a
  same-named plugin agent — no warning, no error. Never leave a copy of a
  plugin agent in `.claude/agents/`.
- An agent definition with no `tools`/`disallowedTools` inherits the full
  toolset including `Agent` — prose in the body saying "you cannot spawn
  agents" enforces nothing, it's a suggestion the model can and does route
  around. Only frontmatter is enforcement.
- Whether nested subagents are on by default is version-dependent and the
  docs currently disagree with observed behaviour (fired on 2.1.220 with
  `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` unset everywhere). Pin it
  explicitly in `.claude/settings.json`; it's read at session start, so
  `/reload-plugins` won't pick up a change.
- The marketplace's `source: "./"` only resolves when users add the
  marketplace from a git repo (`owner/repo`) or local dir — adding via a
  direct URL to marketplace.json downloads just that file, and the
  relative plugin source fails. Only ever document the `owner/repo` form.

<!-- Each entry: the trap, why it bites, and where it's pinned (a test that
     locks the invariant in place, if one exists). Example shape:

- Library X silently ignores option Y unless Z also rides the call — don't
  "simplify" the pairing. Pinned in tests/test_x.py.
-->
