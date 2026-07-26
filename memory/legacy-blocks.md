# Legacy party-authored CLAUDE.md blocks

Verbatim copies of every block older plugin versions wired into user
projects' CLAUDE.md files. `/party:setup` step 5a matches against these
to migrate old installs: a block found in a project's CLAUDE.md that
matches one of these **exactly** is unmodified and safe to replace (with
the user's confirmation); a block whose opening line matches but whose
body differs from every variant here was hand-edited — setup must not
touch it. Never edit this file except to append the outgoing versions of
blocks when a new plugin version changes the shipped text.

## 0.2.x — "Agent party" bullet (Conventions)

```markdown
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
  preserved). `/party:setup` writes the setting that enables nesting
  (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH: "2"` in
  `.claude/settings.json`); it takes effect on the next session start.
```

## 0.3.x — the three Conventions bullets

```markdown
- **Summon the party — don't build alone.** Substantial work goes to
  `party:fighter` BEFORE the first Edit or Write: multi-file changes, new
  features, refactors, migrations, executing an approved plan. When
  fighter finishes, ALWAYS spawn `party:cleric` with its build report —
  not conditional on the build looking clean. Small fixes (single file,
  typos, docs, config) stay at the table. Borderline → summon; say which
  way you went in one line. `party:wizard` (read-only) is on call for deep
  review, hard debugging, and approach calls — use it directly whenever a
  second, stronger set of eyes would help.
- **Plans name their executor.** When writing a plan for substantial
  work, the plan's steps must name which party member executes each
  phase — step 1 is "spawn `party:fighter` with …", and the final step is
  always "spawn `party:cleric` with fighter's build report." Approving
  the plan is approving the delegation.
- Party mechanics: fighter and cleric spawn their own read-only helpers
  (recon before, verification after) and call wizard mid-encounter, while
  writing every edit themselves; wizard never delegates. Nesting is capped
  at depth 2, so those helpers are leaves. Where nesting is off, fighter
  and cleric degrade to the relay — the agent ends its turn with a
  `NEEDS_WIZARD:` block, the main session puts that question to wizard and
  resumes the agent via SendMessage with the answer (context preserved).
  `/party:setup` writes the setting that enables nesting
  (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH: "2"` in
  `.claude/settings.json`); it takes effect on the next session start.
```

## 0.2.x–0.3.x — "Project memory" section

```markdown
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
New gotchas discovered in the codebase also get a 1–2 line entry in
gotchas.md. Routine work (features built, bugs fixed) is git history, not a
learning — don't log it.
```

## 0.4.x — the muster + executor Conventions bullets

In installed files these two bullets are preceded by a `<!-- party@0.4.0 -->`
marker line, which is the cheapest fingerprint. The `- Party mechanics:`
companion that follows them is **unchanged** in 0.5.0 — leave it alone; it
needs no migration.

```markdown
- **The party musters on command, not by default.** The main session
  (the Guide) does the ordinary work itself — including substantial
  work. The party rides out only when: (a) the user explicitly summons
  it, (b) an approved plan names party members as executors, or (c) the
  user accepts the Guide's muster suggestion. The Guide MAY suggest,
  once and in one line, when work looks party-sized ("this looks
  party-sized — summon them?") — and takes no for an answer. Once
  mustered: fighter builds, and when fighter finishes, ALWAYS spawn
  `party:cleric` with its build report — not conditional on the build
  looking clean. `party:wizard` (read-only) is on call when explicitly
  asked, or after two failed attempts at the same problem. When
  spawning a party member, check `.claude/party.json` for a `models`
  override and pass it as the Agent tool's `model` parameter (absent =
  the member's default).
- **Plans name their executor when they delegate.** A plan is free to
  keep work at the table. When a plan DOES propose party execution, its
  steps name which member executes each phase — and the final step is
  always "spawn `party:cleric` with fighter's build report." Approving
  such a plan is approving the muster; the user can strike the
  delegation from a plan and keep the rest.
```

## 0.5.0 — the Session Zero bullet (Conventions)

In installed files this bullet is preceded by a `<!-- party@0.5.0 -->`
marker line. Note that marker alone does not identify it: 0.5.0 also
marked the muster and experience blocks, both of which are **unchanged**
in 0.6.0. Match on the body.

```markdown
- Session Zero (`/party:session-zero`): invoke when scoping new work or
  weighing approaches, BEFORE plan mode — collaborative quest-shaping
  dialogue (options + recommendation, plain-language trade-offs, the user
  makes the calls).
```
