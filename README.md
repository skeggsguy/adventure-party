# Adventure Party

<p align="center">
  <img src="assets/party.png" alt="A fighter, cleric, and wizard gathered around a glowing arcane interface" width="480">
</p>

A D&D-themed agent party and project-memory framework for
[Claude Code](https://claude.com/claude-code), packaged as the **`party`
plugin**. You bring the quest; the party ships it.

## Why a party

One agent doing everything means one context doing everything: the model
that wrote the code reviews the code, believes its own report, and moves
on. Splitting the work across specialized agents buys real separation —
the reviewer reads the actual diff instead of trusting the builder's
summary (on this framework's first-ever smoke test, the reviewer caught a
genuine parsing bug the builder had shipped green).

The main session is the **DM**: it assigns the quests and it's the only
one that talks to you. But party members don't run back to town every
time they need something — mid-encounter, fighter and cleric call for aid
themselves: scouts for recon, verifiers for a suspicion, the wizard for a
judgment call. Each still ends its turn with a structured handoff to the
DM.

## The party

| Agent           | Role                    | Model | Effort | Access                 | May call                                    |
| --------------- | ----------------------- | ----- | ------ | ---------------------- | ------------------------------------------- |
| `party:fighter` | Builder                 | Opus  | high   | full tools             | `Explore` recon, `party:wizard`, verifiers  |
| `party:cleric`  | Reviewer + fixer        | Fable | high   | full tools             | a verifier per finding, `party:wizard`, `Explore` |
| `party:wizard`  | Advisor (deep judgment) | Fable | xhigh  | read-only + own memory | nobody — deliberately                       |

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
traps diagnosed and verdicts proven right or wrong. It is the one party
member that delegates nothing: one deep context reading the real code is
the whole point of calling it.

## The protocol

1. The DM (main session) sends substantial builds to **fighter**; small
   fixes stay at the table.
2. Fighter builds, and calls for aid as it goes: `Explore` for recon on
   an unfamiliar subsystem, **wizard** for an approach call or a problem
   it's failed at twice, an independent agent to verify a claim once the
   build is done. It writes every line of the change itself — the
   parallelism is on the read-only side, so the build report stays a
   first-hand account.
3. When fighter finishes, the DM **always** spawns **cleric** with
   fighter's build report. Cleric reviews the diff and can fan out a
   verifier per finding — one agent per suspicion, confirm or kill it
   against the code — then makes every fix itself and consults **wizard**
   on anything that needs a judgment call.

Nesting is capped at depth 2: the DM spawns party members, party members
spawn helpers, and those helpers are leaves. Where nesting isn't
available the party degrades to the old relay — a stuck agent ends its
turn with a `NEEDS_WIZARD:` block (problem, attempts, hypotheses, file
paths), the DM puts the question to wizard and resumes the agent with the
answer via SendMessage, its context preserved.

Planning is deliberately **not** a party member: planning is a dialogue
with the human, and subagents can't talk to the human. The quest gets
written at the DM's table; the party executes it.

## Session Zero

How quests get written at that table is itself part of the framework: the
**`/party:session-zero`** skill. It encodes a collaborative
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
its law from the project's memory files, so the plugin ships a shell of a
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

These files live in *your* repo, not in the plugin — which is why a plugin
alone can't deliver them. `/party:setup` does: it copies the four shells
into `.claude/`, enables nested delegation in `.claude/settings.json`,
and wires the party-protocol, Session Zero, and project-memory sections
into your `CLAUDE.md`. It never overwrites anything that already exists,
so it's safe to re-run.

## Install

Once, to add the marketplace and install the plugin:

```
/plugin marketplace add skeggsguy/adventure-party
/plugin install party@adventure-party
```

That gives you `party:fighter`, `party:cleric`, `party:wizard`, and
`/party:session-zero` in every project.

Then, once per project you want the memory system in:

```
/party:setup
```

It will ask permission to write into `.claude/` — approve it; that's the
install. Restart the session afterwards so the nesting setting takes
effect. Then fill in the `<placeholders>` it leaves in `CLAUDE.md` and
start seeding the memory files with your project's real architecture
notes, gotchas, and decisions — the party is only as good as what the
project tells it.

## Requirements & caveats

- Claude Code with plugin support and subagents; `model:`/`effort:`
  frontmatter values are Anthropic model tiers (`opus`, `fable`) — adjust
  to what your plan offers.
- Party members calling for aid needs **nested subagents**, gated by the
  `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` environment variable. `/party:setup`
  writes `"2"` into your project's `.claude/settings.json`; it's read at
  session start, so restart after the install. Whether nesting is on by
  default varies by Claude Code version — hence setting it explicitly.
  Without it the party still works: fighter and cleric fall back to the
  `NEEDS_WIZARD:` relay through the main session.
- A project-level `.claude/agents/fighter.md` (or `cleric`/`wizard`)
  overrides the plugin's copy. If you previously installed the party by
  hand, delete those files or they silently win.
- The agents discover project specifics (test command, pinned invariants,
  verification method) from your CLAUDE.md. A well-documented repo gets
  their best behavior; a bare repo gets honest judgment and honest
  reports about what wasn't verified.
- The protocol is convention, not enforcement — the DM's CLAUDE.md
  section and the agent definitions are what keep it followed. Nothing
  stops an agent with tool access from delegating in ways its definition
  doesn't describe.

## Roadmap

- Submit `party` to a community plugin marketplace so it installs without
  adding this repo as a marketplace first.
- Possible **Rogue**: a dedicated UI-verification specialist (headless
  browser driving) — a natural helper for cleric to spawn when a change
  has a user-facing surface, instead of driving the browser itself.
- Stored delegation profiles for recurring quests.

## License

MIT — see [LICENSE](LICENSE).
