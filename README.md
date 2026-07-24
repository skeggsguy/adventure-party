# Adventuring Party

A D&D-themed agent party and project-memory framework for
[Claude Code](https://claude.com/claude-code). You bring the quest; the
party ships it.

## Why a party

One agent doing everything means one context doing everything: the model
that wrote the code reviews the code, believes its own report, and moves
on. Splitting the work across specialized agents buys real separation —
the reviewer reads the actual diff instead of trusting the builder's
summary (on this framework's first-ever smoke test, the reviewer caught a
genuine parsing bug the builder had shipped green).

Claude Code subagents can't spawn each other — nesting is one level deep.
The party is designed around that wall instead of fighting it: the main
session is the **DM**, relaying between party members who each end their
turn with a structured handoff.

## The party

| Agent   | Role                    | Model | Effort | Access                |
| ------- | ----------------------- | ----- | ------ | --------------------- |
| Fighter | Builder                 | Opus  | high   | full tools            |
| Cleric  | Reviewer + fixer        | Fable | high   | full tools            |
| Wizard  | Advisor (deep judgment) | Fable | xhigh  | read-only + own memory|

**Fighter** takes a substantial implementation task and ships it
end-to-end — implementation and tests, running the project's suite as it
goes. Deliberately loose instructions: it's a powerhorse, not a
checklist-follower. It ends with a build report.

**Cleric** always runs after fighter. It reviews the actual diff (never
just the report), then directly fixes what it finds — bugs, pinned-invariant
violations, test gaps, convention drift, needless complexity — and leaves
the tree green. If the change has a user-facing surface, cleric drives it
the way a user would before calling it done.

**Wizard** is the party's high-effort judgment: deep review, hard
debugging (2+ failed attempts), and which-approach calls. Read-only — it
diagnoses and advises; the caller implements. It keeps its own memory of
traps diagnosed and verdicts proven right or wrong.

## The protocol

1. The DM (main session) sends substantial builds to **fighter**; small
   fixes stay at the table.
2. When fighter finishes, the DM **always** spawns **cleric** with
   fighter's build report.
3. Any party member that gets stuck ends its turn with a `NEEDS_WIZARD:`
   block (problem, attempts, hypotheses, file paths). The DM relays the
   question to **wizard**, then resumes the stuck agent with the answer
   via SendMessage — its context is preserved, so it picks up where it
   left off.

Planning is deliberately **not** a party member: planning is a dialogue
with the human, and subagents can't talk to the human. The quest gets
written at the DM's table; the party executes it.

## Session Zero

How quests get written at that table is itself part of the framework: the
**session-zero** skill (in `skills/`). It encodes a collaborative
quest-shaping dialogue for the DM to run *before* plan mode or code —
built for users who are smart and opinionated but didn't grow up in app
development. Its core moves: options **with** a recommendation (and the
strongest case against it), trade-offs taught in plain language where
they're used, clarifying questions batched early and only when the answer
changes the plan, musings answered with assessment rather than action —
and every landed decision recorded with its why in the project's
decisions file, so the learning compounds. The user makes the calls,
informed.

## The memory system

Agents are only as good as what the project tells them. The party reads
its law from the project's memory files, so `memory/` ships a shell of a
four-file system that keeps a repo's hard-won knowledge loaded and current:

- `architecture.md` — how the system actually fits together (curated,
  auto-loaded every session)
- `gotchas.md` — non-obvious traps, 1–2 lines each, deleted when fixed
  (curated, auto-loaded)
- `decisions.md` — why A over B, dated, newest first (curated, auto-loaded)
- `learnings.md` — append-only surprise log; never imported, distilled
  into the curated files periodically
- `CLAUDE.md.template` — a project-instructions skeleton wiring it all
  together, including the party protocol

The split matters: curated files stay small because they cost context on
every prompt; the append-only log can grow forever because it's read on
demand.

## Install

Into any Claude Code project:

1. Copy `agents/*.md` into your repo's `.claude/agents/`.
2. Copy `memory/architecture.md`, `gotchas.md`, `decisions.md`, and
   `learnings.md` into `.claude/`.
3. Copy `skills/session-zero/` into `.claude/skills/`.
4. Adapt `memory/CLAUDE.md.template` into your repo's `CLAUDE.md` (or
   merge the party-protocol, session-zero, and project-memory sections
   into an existing one).

New sessions in that project will list fighter/cleric/wizard as available
agents and load the memory files automatically.

## Requirements & caveats

- Claude Code with subagent support; `model:`/`effort:` frontmatter values
  are Anthropic model tiers (`opus`, `fable`) — adjust to what your plan
  offers.
- The agents discover project specifics (test command, pinned invariants,
  verification method) from your CLAUDE.md. A well-documented repo gets
  their best behavior; a bare repo gets honest judgment and honest
  reports about what wasn't verified.
- The relay protocol is convention, not enforcement — the DM's CLAUDE.md
  section is what keeps it followed.

## Roadmap

- Graduate the party to user level (`~/.claude/agents/`) for zero-setup
  availability across all local projects.
- Possible **Rogue**: a dedicated UI-verification specialist (headless
  browser driving) as a lighter standalone alternative to cleric's
  built-in behavioral check.
- Stored delegation profiles for recurring quests.

## License

MIT — see [LICENSE](LICENSE).
