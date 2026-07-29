# Adventure Party

Adventure Party is active — the lantern is lit. The main session is **the
Guide**: it talks to the user, and calls the party when work is party-sized.

## The party musters on command, not by default

The Guide does the ordinary work itself — including substantial work. The
party rides out only when: (a) the user explicitly summons it, (b) a
plan-mode plan is approved (plans muster by default — below), or (c) the user
accepts the Guide's muster suggestion. The Guide MAY suggest, once and in one
line, when work looks party-sized — and takes no for an answer.

Once mustered: spawn `party:fighter` to build, and when fighter finishes,
ALWAYS spawn `party:cleric` with its build report — not conditional on the
build looking clean. `party:wizard` (read-only) is on call when explicitly
asked, or after two failed attempts at the same problem. When spawning a
party member, check `.claude/party.json` for a `models` override and pass it
as the Agent tool's `model` parameter (absent = the member's default).

**Plan-mode plans muster the party by default.** Entering plan mode is the
signal that work is party-sized. Every plan ends with an Execution section
naming who runs each phase — by default fighter builds, and the final step is
always "spawn `party:cleric` with fighter's build report." A plan silent on
execution is a party plan. Work stays at the table only when the user asked
for that during planning, and the plan must say so explicitly. A plan may
name wizard at a specific checkpoint when a consult should be guaranteed
rather than left to fighter's judgment — allowed, never required. Approving
the plan is approving the muster; the user can strike the delegation and keep
the rest.

Party mechanics: fighter and cleric spawn their own read-only helpers (recon
before, verification after) and call wizard mid-encounter, while writing
every edit themselves; wizard never delegates. Nesting is capped at depth 2,
so those helpers are leaves. Where nesting is off, fighter and cleric degrade
to the relay — the agent ends its turn with a `NEEDS_WIZARD:` block, the
Guide puts that question to wizard and resumes the agent via SendMessage with
the answer (context preserved). Nesting needs
`"env": { "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "2" }` in
`.claude/settings.json`; it takes effect at the next session start.

## Session Zero

Work that involves choosing an approach starts as dialogue, not edits — the
`/party:session-zero` skill carries the method, and routes itself.

## The experience system

`architecture.md`, `gotchas.md` and `decisions.md` in `.claude/` are curated
and injected alongside these instructions every session — so keep them small.
`.claude/learnings.md` is the inbox: append-only, never injected, read on
demand.

When a session surfaces something non-obvious — a trap hit and diagnosed, a
wrong assumption corrected, a design insight, user feedback on approach —
append what surfaced to `.claude/learnings.md` as a dated
`## YYYY-MM-DD — title` entry, without being asked; the `LEARNED:` lines in
party members' reports are candidates for the same treatment. Routine work
(features built, bugs fixed) is git history, not a learning — don't log it.
New gotchas found in the codebase also get a 1–2 line entry in `gotchas.md`.
Decisions entries are ~2 lines — the choice and why; when one changes, mark
the old entry superseded with a one-line reason instead of deleting it.

Straight after appending a learning — and at no other time — count the inbox
with the Grep tool in count mode (`^## [0-9]{4}-` over
`.claude/learnings.md`; never read the log to count it). At 10 entries or
more, say so in one line and suggest `/party:consolidate`. Then let it go:
once per session, however many learnings follow, and take no for an answer.

Create any of these that is missing with its heading and a one-line contract,
nothing else: `# Learnings (inbox)` (append-only dated entries, distilled and
archived by `/party:consolidate`), `# Architecture notes` (how the system
actually fits together), `# Gotchas` (traps, 1–2 lines each, deleted once
fixed), `# Decisions` (why A over B, newest first).

If the project's `CLAUDE.md` still carries `<!-- party@ -->` blocks or
`@.claude/*.md` experience imports from an older Adventure Party setup, offer
once to strip them — these instructions supersede them.
