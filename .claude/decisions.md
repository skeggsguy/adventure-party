# Decisions

Why A over B, for choices below plan level. Loaded into every session —
keep entries short, newest first.

Format: `YYYY-MM-DD — decision — why`

- 2026-07-25 — embrace nested delegation at depth 2 (pinned in
  `.claude/settings.json`, written into user projects by `/party:setup`)
  instead of designing around "subagents can't spawn each other" — the
  wall isn't real, and cleric had already routed around the relay by
  spawning a helper itself. Fighter and cleric delegate; wizard
  deliberately does not (`disallowedTools: Agent`) — one deep context on
  the real code is its entire value, and a layer-2 wizard couldn't spawn
  anyway. Rejected parallel writers/worktrees: `isolation: worktree` only
  auto-cleans *unchanged* trees, so parallel builders leave live trees to
  merge by hand and degrade the build report from a first-hand account
  into a summary of summaries — the exact failure the party exists to
  prevent. Parallelism goes to the read-only side only (recon before,
  verification after). Rejected depth 3 — bounded and predictable beats
  maximally flexible. `NEEDS_WIZARD:` kept as the degradation path, not
  deleted: the plugin ships to installs we don't control (nesting off,
  older Claude Code, `/party:setup` skipped).
- 2026-07-25 — ship as a Claude Code plugin (`party`) inside a
  single-plugin marketplace (`adventure-party`), with the repo root as
  the plugin root — one-command install and a real update path, versus
  copy-paste install which froze users on a snapshot with no way to pull
  fixes.
- 2026-07-25 — deliver the memory system through a user-invoked
  `/party:setup` skill rather than shipping it as plugin files — a plugin
  can't write into a user's `.claude/`, and half the product is exactly
  those files plus a CLAUDE.md merge. Rejected plugin-only (drops the
  memory system, which is what makes the agents useful) and staying pure
  copy-paste (no updates, and forced this repo to hand-mirror
  `agents/`/`skills/` into `.claude/`).
- 2026-07-25 — dogfood via `claude --plugin-dir .` and delete
  `.claude/agents/` + `.claude/skills/` — project-level agents override
  same-named plugin agents, so keeping the copies would mean the mirrors
  silently win and drift. Rejected installing the plugin from the local
  marketplace for development: `--plugin-dir` picks up edits live via
  `/reload-plugins`, an install does not.

<!-- Record the decision AND the rejected alternative with the reason —
     future sessions re-litigate choices whose "why" isn't written down. -->
