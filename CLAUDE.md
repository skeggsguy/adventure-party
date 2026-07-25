# CLAUDE.md

Adventure Party — a shareable agent-party + project-memory framework for
Claude Code, shipped as the **`party` plugin** (see README.md for the full
pitch). The product is markdown: agent definitions, skills, and
memory-file templates. The repo root IS the plugin root, and this repo
dogfoods its own framework while developing it.

## Layout

- .claude-plugin/ — plugin.json (the `party` manifest) and
  marketplace.json (the `adventure-party` single-plugin marketplace)
- agents/ — THE PRODUCT: fighter, cleric, wizard agent definitions.
  Loaded live by the plugin as `party:fighter` / `party:cleric` /
  `party:wizard` — not a copy source.
- skills/ — THE PRODUCT: session-zero (quest-shaping dialogue) and setup
  (the memory-system installer). Loaded live as `/party:session-zero` and
  `/party:setup`.
- memory/ — THE PRODUCT: memory-system shell (architecture/gotchas/
  decisions/learnings templates + CLAUDE.md.template). Not auto-loaded;
  `/party:setup` reads it through `${CLAUDE_PLUGIN_ROOT}` and copies it
  into a target project's `.claude/`.
- .claude/ — this repo's OWN live memory files plus settings
  (settings.json pins the subagent spawn depth; settings.local.json is
  gitignored), nothing else

## Dogfood rule

Work on this repo in a session started with `claude --plugin-dir .` from
the repo root. That loads `agents/` and `skills/` directly, so there are
no mirrored copies and no `diff -r` check — edit the real file. After
editing an agent or skill, run `/reload-plugins` to pick it up without
restarting.

**The failure mode is silent**: launched without `--plugin-dir .`, the
party simply isn't there — no error, no warning. Check `/context` for the
`party:*` agents before trusting that a party session is actually running.

`.claude/` holds only this repo's own memory files
(architecture/gotchas/decisions/learnings) plus its settings files. It must
NOT contain `agents/` or `skills/` — a project-level `.claude/agents/`
silently overrides same-named plugin agents, so a stray copy would win and
drift. These live files deliberately DIVERGE from the `memory/` shells:
the shells stay clean and empty of this repo's content; the live copies
accumulate this repo's real notes.

## Conventions

- Keep agent and skill bodies project-agnostic: discovery instructions
  ("the project's test suite", "wherever its CLAUDE.md records pins"),
  never references to any specific repo, tool, or path outside this one.
- Agent party (from the `party` plugin): `party:fighter` (Opus high) is
  the default builder for substantial implementation tasks — small fixes
  stay in the main session. When fighter finishes, ALWAYS spawn
  `party:cleric` (Fable high) with fighter's build report to review, fix,
  and verify the build. `party:wizard` (read-only, Fable xhigh) handles
  deep review, hard debugging, and approach calls — use it directly
  whenever a second, stronger set of eyes would help. Fighter and cleric
  delegate too: they spawn read-only helpers (recon before, verification
  after) and call wizard directly mid-encounter, while writing every edit
  themselves. Wizard never delegates. Nesting is capped at depth 2, so
  those helpers are leaves. Where nesting is off, fighter and cleric
  degrade to the relay: the agent ends its turn with a `NEEDS_WIZARD:`
  block, the main session packages that question off to wizard and
  resumes the agent via SendMessage with the answer (its context is
  preserved). Nesting is pinned here by `.claude/settings.json`
  (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH: "2"`), which needs a fresh
  session to take effect.
- Session Zero (`/party:session-zero`): invoke when scoping new work or
  weighing approaches, BEFORE plan mode — collaborative quest-shaping
  dialogue (options + recommendation, plain-language trade-offs, the user
  makes the calls).
- Bump `version` in `.claude-plugin/plugin.json` when shipping changes
  users should pull — installs update on version, not on commit.

## Project memory

@.claude/architecture.md
@.claude/gotchas.md
@.claude/decisions.md

Curated files above are auto-loaded every session — keep them small; remove
stale entries. Append-only log: .claude/learnings.md (NOT imported — read it
when context suggests a past learning is relevant; distill durable items
into the curated files periodically).

When a session surfaces something non-obvious — a trap hit and diagnosed, a
wrong assumption corrected, a design insight, user feedback on approach —
append it to .claude/learnings.md (dated, append-only) without being asked.
New gotchas also get a 1–2 line entry in gotchas.md. Routine work is git
history, not a learning — don't log it.
