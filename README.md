# Adventure Party

<p align="center">
  <img src="assets/party.png" alt="A fighter, cleric, and wizard gathered around a glowing arcane interface" width="480">
</p>

An adventuring party and experience system for
[Claude Code](https://claude.com/claude-code), packaged as the **`party`
plugin**. You bring the quest; the party ships it.

## The premise

Adventure Party is built for people who are smart and intellectually
driven but weren't full-stack developers before 2024 — and on the
conviction that successful AI development hinges on three things:

1. **The dialogue** — the human conversation with the agent, where you
   learn, brainstorm, and land decisions you actually understand.
2. **The orchestration of plan mode** — where the technical design gets
   shaped, challenged (adversarial planning agents are encouraged), and
   written down.
3. **The decisions made there** — recorded with their *why*, so they
   compound instead of evaporating.

Other frameworks install process and assume engineering literacy, or
remove decisions and assume expertise. Adventure Party installs process
**and teaches the literacy as you go**: trade-offs explained in plain
language where they're used, delegation made legible through party
roles, and every landed decision written down with its reasons. You are
the main success lever. The system's job is to make you better at
wielding it.

Your quest stays yours: the plugin brings the party and the experience
system; your project's CLAUDE.md stays part guide to this system, part
blank page to tailor per project.

## The workflow

1. **Session Zero** — a real multi-turn conversation shapes every
   change before any code: what the options actually are, plain-language
   trade-offs, options with a recommendation, you make the calls
   (`/party:session-zero`). It runs as long as you're still thinking.
2. **Plan mode** — "let's plan mode this." The technical design, where
   you can and should orchestrate adversarial agents to challenge it
   (a UI challenge, a database-design challenge…).
3. **The party musters and executes** — on your command or your
   approved plan. Fighter builds, cleric reviews and heals, wizard
   advises on the hard calls.
4. **Results come back to you** — review and feedback before you sign
   off the commit.
5. **New adventure, new session** — and the experience system carries
   what was learned.

## Why a party

One agent doing everything means one context doing everything: the model
that wrote the code reviews the code, believes its own report, and moves
on. Splitting the work across specialized agents buys real separation —
the reviewer reads the actual diff instead of trusting the builder's
summary (on this framework's first-ever smoke test, the reviewer caught a
genuine parsing bug the builder had shipped green).

The main session is **the Guide**: it runs the dialogue, assigns the
quests, and is the only one that talks to you. But party members don't
run back to town every time they need something — mid-encounter, fighter
and cleric call for aid themselves: scouts for recon, verifiers for a
suspicion, the wizard for a judgment call. Each still ends its turn with
a structured handoff to the Guide.

## The party

| Agent           | Role                    | Model | Effort | Access                 | May call                                          |
| --------------- | ----------------------- | ----- | ------ | ---------------------- | ------------------------------------------------- |
| `party:fighter` | Builder                 | Opus  | high   | full tools             | `Explore` recon, `party:wizard`, verifiers        |
| `party:cleric`  | Reviewer + fixer        | Fable | high   | full tools             | a verifier per finding, `party:wizard`, `Explore` |
| `party:wizard`  | Advisor (deep judgment) | Fable | xhigh  | read-only (no writes)  | nobody — deliberately                             |

**Fighter** takes a substantial implementation task and ships it
end-to-end — implementation and tests, running the project's suite as it
goes. Tests are written red-first: a test it has never seen fail isn't
evidence. In a repo with no suite at all it writes the first test file
and records the command in your CLAUDE.md — one file and one command, so
the project ends up more testable than it started. Deliberately loose
otherwise: it's a powerhorse, not a checklist-follower. It ends with a
labeled build report, including what it did *not* verify.

**Cleric** always runs after fighter. It reviews the actual diff (never
just the report), then directly fixes what it finds — bugs, pinned-invariant
violations, test gaps, convention drift, needless complexity — and leaves
the tree green. If the change has a user-facing surface, cleric drives it
the way a user would before calling it done.

Every real bug it fixes gets a test that fails without the fix, and it
checks fighter's tests by inverting the logic they cover rather than by
reading them — a test that passes both ways is a green light wired to
nothing. It stays inside the change and its blast radius: a build that
needs rebuilding rather than repairing comes back as `NEEDS_REBUILD:`
for you to call, not a silent redesign.

**Wizard** is the party's high-effort judgment: deep review, hard
debugging (2+ failed attempts), and which-approach calls. Read-only for
real — it holds no write tools at all, so it diagnoses and advises while
the caller implements. It is the one party member that delegates
nothing: one deep context reading the real code is the whole point of
calling it. Being read-only it can also run nothing — so callers paste
the actual diff and error output, and where the answer turns on
something it can't see, it names the command that would settle the
question instead of guessing. Anything durable it learns leaves in its
`LEARNED:` line, into your experience files rather than a private store.

Default models are set per agent; to change them, put overrides in
`.claude/party.json` and run `/party:config` to validate and apply
them — the Guide passes your choice at spawn time (the Agent tool's
per-invocation model outranks the agent file's default).

## The protocol

**The party musters on command, not by default.** The Guide does
ordinary work itself — including substantial work. The party rides out
only on one of three triggers:

- You explicitly summon it.
- A plan-mode plan is approved — **plans muster by default**: every plan
  ends with an Execution section naming who runs each phase, fighter
  building and cleric reviewing unless you said otherwise while planning,
  and a plan silent on execution is a party plan. Work stays at the table
  only when you asked for that during planning and the plan says so.
  Approving the plan is approving the muster; strike the delegation to
  keep the plan without the party.
- You accept the Guide's suggestion — it may offer, once and in one
  line, when work looks party-sized, and takes no for an answer.

Once mustered: fighter builds and calls for aid as it goes (`Explore`
recon, wizard for approach calls or twice-failed problems, an
independent verifier once the build is done), writing every line of the
change itself — the parallelism is on the read-only side, so the build
report stays a first-hand account. When fighter finishes, the Guide
**always** spawns cleric with fighter's build report; cleric reviews the
diff, fans out a verifier per finding when useful, and makes every fix
itself.

Nesting is capped at depth 2: the Guide spawns party members, party
members spawn helpers, and those helpers are leaves. Where nesting isn't
available the party degrades to the relay — a stuck agent ends its turn
with a `NEEDS_WIZARD:` block (problem, attempts, hypotheses, file
paths), the Guide puts the question to wizard and resumes the agent with
the answer via SendMessage, its context preserved.

Planning is deliberately **not** a party member: planning is a dialogue
with the human, and subagents can't talk to the human. The quest gets
written at the Guide's table; the party executes it.

## Session Zero

How quests get written at that table is itself part of the framework:
the **`/party:session-zero`** skill. It is exploration and chat mode — an
iterative dialogue the Guide runs *before* plan mode or code, built for
users who are smart and opinionated but didn't grow up in app
development.

Its core moves: options **with** a recommendation (and the strongest case
against it); what a tool or framework *actually is* before any verdict on
using it — the category, the problem it was built for, and which
decisions it takes off your plate in exchange for its opinions; YAGNI
held as the default, because a wrong abstraction is a rewrite where
duplicated code is only a refactor; tables and ASCII sketches where they
carry structure prose carries badly; every term defined the first time
it appears; clarifying questions batched early and only when the answer
changes something; musings answered with assessment rather than action.

Depth tracks **stakes × reversibility** — a naming question gets a
sentence, a dependency you'll build on gets the full treatment. The
dialogue has no exit condition except your word: the Guide never moves
to plan mode on its own initiative, and circling back to the same call
from a new angle is the mode working as intended. Every landed decision
is recorded with its why in the project's decisions file, so the
learning compounds. The user makes the calls, informed.

## The experience system

Agents are only as good as what the project tells them — so the party's
memory is its **experience**, and it levels up. The plugin ships a shell
of a four-file system that keeps a repo's hard-won knowledge loaded and
current:

- `architecture.md` — how the system actually fits together (curated,
  auto-loaded every session)
- `gotchas.md` — non-obvious traps, 1–2 lines each, deleted when fixed
  (curated, auto-loaded)
- `decisions.md` — why A over B, dated, newest first (curated, auto-loaded)
- `learnings.md` — append-only log of surprises; never imported,
  distilled by the Long Rest (below)
- `CLAUDE.md.template` — a project-instructions skeleton wiring it all
  together, including the party protocol

The split matters: curated files stay small because they cost context on
every prompt; the append-only log can grow forever because it's read on
demand.

The party feeds this too. A subagent's context dies with its turn, so
every party report ends with a `LEARNED:` line when a muster turned up
something genuinely non-obvious — a trap diagnosed, an assumption
corrected — which the Guide then appends. Without it, the hardest-won
knowledge of a build evaporates inside the agent that earned it.

**Every dated entry in `learnings.md` is one experience point.** XP
never goes down — the log is append-only by law — and the party levels
up at thresholds (10, 25, 50, 100, then every 100). One honest warning,
straight from the files themselves: junk entries are dead weight the
party carries. Routine work is git history, not XP.

Opt in during setup and you get the display, both pieces local shell
scripts costing zero tokens:

- a **statusline** — `📜 Party Lv.3 · 34/50 XP` — that flips to
  `⬆ LEVEL UP — /party:level-up` when the party has earned it, and
- a one-line **banner** at session start when a level-up is waiting.

## Leveling up — the Long Rest

`/party:level-up` is the ceremony, and it is not fireworks: a Long Rest
is the moment the party *trains*. In plain terms (it will tell you this
itself, along with the price — it uses real tokens and edits your
experience files):

1. It distills the learnings log — only entries since the last rest —
   into the curated files that load every session, and prunes gotchas
   that have been fixed. A leveled-up party is literally a
   better-informed party.
2. It appends the level to **`CHRONICLE.md`**: your project's saga in
   plain language — what was built, what was conquered, what *you*
   learned. Half quest log, half learning journal; the chronicle is
   also the system's only level record, so it survives clones, reverts,
   and second machines by riding the same git history as everything
   else.
3. It awards the party a title — seeded from your repo's name and the
   level, so it is deterministic: *your* project's Level 3 party is
   always, say, the Wardens of the Unbroken Build. Their name, not a
   slot machine's.

The player levels up too: the chronicle plus the decisions file is a
growing, readable record of your own understanding — the thing this
whole framework exists to build.

## Install

Once, to add the marketplace and install the plugin:

```
/plugin marketplace add skeggsguy/adventure-party
/plugin install party@adventure-party
```

That installs at the **user level** (the default): `party:fighter`,
`party:cleric`, `party:wizard`, `/party:session-zero`, `/party:setup`,
`/party:config`, and `/party:level-up` become available in every
project. That's the right choice for solo work and for trying the party
out — it's on call everywhere but rides nowhere, because nothing
project-specific exists until you run setup in a repo.

For a **team repo**, install at the project level instead, so the
party ships with the repo: pick "Project" when `/plugin install` asks
for a scope, or check this into the repo's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "adventure-party": {
      "source": { "source": "github", "repo": "skeggsguy/adventure-party" }
    }
  },
  "enabledPlugins": {
    "party@adventure-party": true
  }
}
```

Teammates opening the repo are prompted once to add the marketplace;
after that the plugin loads automatically for them.

Either way, the second step is the same and is **always per-project** —
once per project you want the experience system in:

```
/party:setup
```

It will ask permission to write into `.claude/` — approve it; that's the
install. It also offers the opt-in experience display, and on projects
wired by an older plugin version it migrates the party-authored blocks
in your CLAUDE.md (showing you the diff first). Restart the session
afterwards so settings take effect. Then fill in the `<placeholders>` it
leaves in `CLAUDE.md` and start seeding the experience files with your
project's real architecture notes, gotchas, and decisions — the party is
only as good as what the project tells it.

## Requirements & caveats

- Claude Code with plugin support and subagents; `model:`/`effort:`
  frontmatter values are Anthropic model tiers (`opus`, `fable`) —
  change them via `.claude/party.json` + `/party:config` to match what
  your plan offers.
- Calling for aid mid-encounter needs **nested subagents**, gated by the
  `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` environment variable. `/party:setup`
  writes `"2"` into your project's `.claude/settings.json`; it's read at
  session start, so restart after the install. Whether nesting is on by
  default varies by Claude Code version — hence setting it explicitly.
  Without it the party still works: fighter and cleric fall back to the
  `NEEDS_WIZARD:` relay through the main session.
- A project-level `.claude/agents/fighter.md` (or `cleric`/`wizard`)
  does **not** override the plugin's copy — verified: the two coexist,
  and `party:fighter` always resolves to the plugin agent. If you
  previously installed the party by hand, delete those files; they
  linger as separate bare-name agents that can confuse delegation
  (`/party:config` will flag them).
- The experience display is per-user (written to
  `.claude/settings.local.json`) and needs a POSIX shell — on
  Windows-native Claude Code, setup declines it honestly; WSL is fine.
  `party.json` IS a committed project file — model choices are a
  team-level call.
- On a team repo, most of what `/party:setup` writes is committed —
  the experience files, `party.json`, the spawn-depth setting in
  `.claude/settings.json`, the CLAUDE.md wiring — so run it on a branch
  and let the team review the diff like any other change.
- The agents discover project specifics (test command, pinned invariants,
  verification method) from your CLAUDE.md. A well-documented repo gets
  their best behavior; a bare repo gets honest judgment and honest
  reports about what wasn't verified.
- The protocol is convention, not enforcement — the muster-gated agent
  descriptions, the Guide's CLAUDE.md section, and the
  plans-muster-by-default rule are what keep it followed. It's a
  strong nudge, deliberately not a hard block. Nothing stops an agent
  with tool access from delegating in ways its definition doesn't
  describe, either.

## Roadmap

- Submit `party` to a community plugin marketplace so it installs without
  adding this repo as a marketplace first.
- **The Thief** — red team: attempts to steal your app's data and
  reports how it got in (wrapping Claude Code's security-review
  capability in a party posture).
- **The Artificer** — refactors, optimizes, and generally prepares you
  for production (a natural home for simplification passes).
- Possible **Rogue**: a dedicated UI-verification specialist (headless
  browser driving) — a natural helper for cleric to spawn when a change
  has a user-facing surface.

## License

MIT — see [LICENSE](LICENSE).
