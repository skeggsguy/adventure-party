# CLAUDE.md

This is the source repo for **Adventure Party** (`party` plugin) — a
fantasy-flavored agent-party and experience-system framework for Claude
Code, aimed at smart, driven users who weren't full-stack devs before
2024. Everything is markdown skills/agents plus one shell script; there
is no build. The repo doubles as its own marketplace
(`.claude-plugin/marketplace.json`).

## Commands

- Validate manifests: `jq . .claude-plugin/plugin.json` and
  `jq . .claude-plugin/marketplace.json`
- Dogfood locally: `claude --plugin-dir .` (agents `party:fighter/cleric/wizard`,
  skills `/party:session-zero`, `/party:setup`, `/party:config`,
  `/party:level-up` should all list)
- Test the XP script offline: `sh scripts/xp.sh statusline` /
  `sh scripts/xp.sh banner` against fixture `.claude/learnings.md` and
  `CHRONICLE.md` files

## Layout

- `.claude-plugin/` — plugin + marketplace manifests
- `agents/` — the party: fighter (builder), cleric (reviewer/fixer),
  wizard (read-only advisor)
- `skills/` — session-zero, setup, config, level-up (the Long Rest)
- `memory/` — the experience-system shells `/party:setup` copies into a
  user's project, incl. `CLAUDE.md.template`
- `scripts/xp.sh` — statusline + level-up banner (POSIX sh, zero tokens)

## Conventions

- Prose is the product: skills and agents are instructions executed by a
  model. Keep them unambiguous, honest about cost, and plain-language
  first — theme labels mechanics, never replaces them ("experience
  (your project's memory files)").
- Shipped-text changes ripple: the muster-rule bullets exist in
  `memory/CLAUDE.md.template`, this file, and README — keep them in
  sync, and remember old shipped variants become migration fingerprints
  in `skills/setup/SKILL.md` step 5a.
- Naming: no trademarked tabletop terms in anything shipped. Check:
  `git grep -riE 'd[&]d|dunge[o]n|\bD[M]\b' -- README.md agents skills memory .claude-plugin LICENSE`
  must return zero hits (pattern is self-escaping; the repo's own
  `.claude/` memory may name the terms when recording why we avoid
  them). The main session is "the Guide".
- `*.sh` stays LF (`.gitattributes` enforces); xp.sh must degrade
  gracefully on every failure path — it runs on every prompt render.
<!-- party@0.5.0 -->
- **The party musters on command, not by default.** The main session
  (the Guide) does the ordinary work itself — including substantial
  work. The party rides out only when: (a) the user explicitly summons
  it, (b) a plan-mode plan is approved (plans muster by default — next
  bullet), or (c) the user accepts the Guide's muster suggestion. The
  Guide MAY suggest, once and in one line, when work looks party-sized
  ("this looks party-sized — summon them?") — and takes no for an
  answer. Once mustered: fighter builds, and when fighter finishes,
  ALWAYS spawn `party:cleric` with its build report — not conditional
  on the build looking clean. `party:wizard` (read-only) is on call
  when explicitly asked, or after two failed attempts at the same
  problem. When spawning a party member, check `.claude/party.json`
  for a `models` override and pass it as the Agent tool's `model`
  parameter (absent = the member's default).
- **Plan-mode plans muster the party by default.** Entering plan mode
  is the signal that work is party-sized. Every plan ends with an
  Execution section naming who runs each phase — by default fighter
  builds, and the final step is always "spawn `party:cleric` with
  fighter's build report." A plan silent on execution is a party plan.
  Work stays at the table only when the user asked for that during
  planning, and the plan must say so explicitly. A plan may name wizard
  at a specific checkpoint when a consult should be guaranteed rather
  than left to fighter's judgment — allowed, never required. Approving
  the plan is approving the muster; the user can strike the delegation
  and keep the rest.
- Party mechanics: fighter and cleric spawn their own read-only helpers
  (recon before, verification after) and call wizard mid-encounter, while
  writing every edit themselves; wizard never delegates. Nesting is capped
  at depth 2, so those helpers are leaves. Where nesting is off, fighter
  and cleric degrade to the relay — the agent ends its turn with a
  `NEEDS_WIZARD:` block, the Guide puts that question to wizard and
  resumes the agent via SendMessage with the answer (context preserved).
  `/party:setup` writes the setting that enables nesting
  (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH: "2"` in
  `.claude/settings.json`); it takes effect on the next session start.
<!-- party@0.6.0 -->
- Session Zero (`/party:session-zero`): exploration and chat mode —
  invoke when scoping work, weighing approaches, or explaining what a
  tool or framework actually is, BEFORE plan mode. Iterative dialogue:
  options + recommendation, plain-language trade-offs, terms defined on
  first use, tables/diagrams where they carry structure, YAGNI over
  speculative abstraction, the user makes the calls. Depth tracks stakes
  × reversibility. Never move to plan mode on your own initiative — the
  dialogue ends when the user says so.

<!-- party@0.5.0 -->
## Project memory — the party's experience

@.claude/architecture.md
@.claude/gotchas.md
@.claude/decisions.md

Curated files above are auto-loaded every session — keep them small; remove
stale entries. Append-only log: .claude/learnings.md (NOT imported — read it
when context suggests a past learning is relevant; distilled into the
curated files by the Long Rest, `/party:level-up`).

When a session surfaces something non-obvious — a trap hit and diagnosed, a
wrong assumption corrected, a design insight, user feedback on approach —
append it to .claude/learnings.md (dated, append-only) without being asked.
New gotchas discovered in the codebase also get a 1–2 line entry in
gotchas.md. Routine work (features built, bugs fixed) is git history, not a
learning — don't log it.

Experience points: each dated entry in learnings.md is one XP, and the
party levels up at thresholds (see `/party:level-up`). XP counts entries,
but junk entries are dead weight the party carries — a padded log
distills into bloated curated files that cost context every session.
Log genuine learnings; let the level come.
