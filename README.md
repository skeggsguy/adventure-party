# Adventure Party

<p align="center">
  <img src="assets/party.svg" alt="The Party — a Claude Code plugin framework: session zero before the quest, three adventurers, and an experience system that levels up" width="100%">
</p>

An adventuring party and experience system for
[Claude Code](https://claude.com/claude-code), packaged as the **`party`
plugin**. You bring the quest; the party ships it.

## Note from the Creator

This plugin is actively updated from learnings made via a outer harness evaluation blog [Fresh Worktree](https://fresh-worktree.ghost.io/). Check it out if interested!

## Install

One step. Installing the plugin gets you the party, session zero, and the
experience system.

Within the Claude session, add the marketplace and install the plugin:

```
/plugin marketplace add skeggsguy/adventure-party
/plugin install party@adventure-party
```

Pick a scope when `/plugin install` asks:

- **User** (the default) — the party is on call in **every** project on
  this machine. Right for solo work and for trying it out.
- **Project** — the party ships with **this** repo, for team use. Choosing
  "Project" writes it into the repo's `.claude/settings.json`.

  Teammates opening the repo are prompted once to add the marketplace;
  after that the plugin loads automatically for them.

Wherever it is installed, the party is on: the plugin feeds its
instructions into every session as it starts, and those instructions send
the party to read your project's own experience files, if it has any, at the
moments each one matters.

**Upgrading** — Two options either (1) put auto update on within the settings
in Claude marketplace for this plugin. OR (2) periodically refresh the
marketplace directly and then refresh the plugin as a second step.

**Upgrading from 0.10 or earlier** — hirelings are retired. A `hired` entry
in `.claude/party.json` is now ignored and that role's own party member runs
instead; to put a role on another model, see Pinning models below.

## The premise

Adventure Party is built for people who are smart and intellectually
driven, and on the conviction that successful AI development hinges on three things:

1. **The dialogue** — the human conversation with the agent, where you
   learn, brainstorm, and land decisions you actually understand.
2. **Agentic orchestration** — where multiple agents build, test,
   review and ship the plan. Agent instructions are loosely coupled as not to
   constrain better and better models, and compliance enforced through
   unit testing and agentic review.
3. **Leveling up** — You learn, the AI learns. Learnings should be recorded
   and curated into experience, so they compound instead of evaporating.

Other frameworks install process and assume engineering literacy, or
remove decisions and assume expertise. 

Adventure Party installs process **and teaches the literacy as you go**: 
trade-offs explained in plain language where they're used, 
delegation made legible through party roles, and every landed decision 
written down with its reasons. 

You are the main success lever. The system's job is to make you better at
wielding it.

## The workflow

1. **Session Zero** — a real multi-turn conversation shapes every
   change that involves choosing an approach, before any code: what the
   options actually are, plain-language trade-offs, options with a
   recommendation, you make the calls (`/party:session-zero`). At time of writing it is recomended to use either Fable or Opus4.6 for session 0.
2. **Plan mode** — "let's plan mode this." The technical design, where
   you can and should orchestrate adversarial agents to challenge it
   (a UI challenge, a database-design challenge…). The plan also says
   whether the party runs through to the end on its own (the default) or
   checks in with you when cleric hands something back, and each step names
   how we'll know it worked — a number, or a check like a browser test.
3. **The party musters and executes** — on your command or your
   approved plan. Fighter builds, cleric reviews and heals, wizard
   advises on the hard calls.
4. **Results come back to you** — review and feedback before you sign
   off. On a multi-step plan you get a few lines after each step, and the
   party commits each step to a branch as it goes — merging that branch is
   your sign-off. Every run ends with a debrief sized to what happened.
5. **New adventure, new session** — and the experience system carries
   what was learned.
6. **Long rest** — learnings are captured in every session. When enough
   have piled up you take a Long Rest, and they are sorted into
   architecture, decisions and gotchas which are readable by Claude. You
   level up, AI levels up.

## The party

One agent doing everything means one context doing everything: the model
that wrote the code reviews the code, believes its own report, and moves
on. Splitting the work across specialized agents buys real separation —
the reviewer reads the actual diff instead of trusting the builder's
summary.

The main session is **the Guide**: it runs the dialogue, assigns the quests, and 
is the only one that talks to you.

| Agent           | Role                    | Model | Effort | Access                 | May call                                          |
| --------------- | ----------------------- | ----- | ------ | ---------------------- | ------------------------------------------------- |
| `party:fighter` | Builder                 | Opus  | high   | full tools             | `Explore` recon, `party:wizard`, verifiers        |
| `party:cleric`  | Reviewer + fixer        | Fable | high   | full tools             | a verifier per finding, `party:wizard`, `Explore` |
| `party:wizard`  | Advisor (deep judgment) | Fable | xhigh  | read-only (no writes)  | nobody — deliberately                             |

**Fighter** ships a substantial implementation end-to-end —
implementation and tests, running the project's suite as it goes. In
a repo with no suite at all it writes the first test file and records
the command in your CLAUDE.md. When the change has a browser front end
it tests it through a real browser — your project's browser test tool, or
Playwright if there isn't one — as test files you keep. Deliberately loose
otherwise — it's a powerhorse, not a checklist-follower.

**Cleric** always runs after fighter. It reads the plan and checks the
actual diff and fighter's report against it, then heals the bugs whose fix
keeps fighter's design — small or medium — writes any missing tests, and
leaves the tree green. Anything that needs a redesign or a decision from
you it hands back instead of reworking on the spot; style and complexity
it notes rather than fixes.

**Wizard** is the party's high-effort judgment: deep review, hard
debugging (2+ failed attempts), and which-approach calls. Wizard
is expensive and slow but valuable exactly when the repo needs it
most. Solves for try and fail re-attempts.

### The muster protocol

**The party musters on command, not by default.** The Guide does
ordinary work itself. The party rides out only if you summon it,
you accept a suggestion from the guide, or on execution of plan mode.
Fighter and cleric are pointed at the plan file rather than handed a copy,
so each reads the whole plan while the Guide's own context stays lean on
long runs.

**Hand-backs and autonomous runs.** Every plan says `Autonomous: yes` or
`no` — yes by default, and the Guide tells you so when it presents the
plan. When
cleric hands something back:

- `Autonomous: no` — the Guide pauses and brings it to you.
- `Autonomous: yes` — fighter takes it, then cleric again, up to two
  rounds; then wizard gives a verdict and fighter gets one more pass. If
  it's still stuck, it's set aside for the debrief and the run carries
  on with the steps that don't depend on it, stopping only when every
  remaining step does.

In an autonomous run, a hand-back that needs a decision from you goes to
fighter too: fighter makes the call and records it, and the debrief
lists every call made on your behalf so you can reverse any of them.

**Checkpoints.** On a multi-step plan the Guide commits after each step
cleric leaves green — on a `party/<plan-name>` branch if you started on
your default branch — so each cleric reviews just its own step. A set-aside
issue's half-done rework is stashed, not deleted (`git stash list` shows
it), and the tree goes back to the last good step. Start the run from a
clean tree; the Guide asks if it isn't.

**Updates and the debrief.** On a multi-step plan, after each step the
Guide posts a few lines: what worked, what didn't, what was found, and the
step's measure (a number against before and the best so far, or a check's
result — re-taken by cleric if its fixes touched what was measured) — the
same lines go in the commit that closes the step; an uneventful step gets
one line. When the run ends you get a debrief sized to what happened: a
smooth run is a line and its numbers; the rest appears only when there's
something to say — what didn't work, what was found, what was set aside,
calls made on your behalf, what's next. A takeaway only when something was
genuinely non-obvious; never a forced lesson.

### Pinning models

Out of the box — no `party.json` needed — the party runs on these defaults:

| Member  | Default model |
| ------- | ------------- |
| fighter | `opus`        |
| cleric  | `fable`       |
| wizard  | `fable`       |

To change one, pin it per project in `.claude/party.json`, listing only the
members you're changing — anyone left out keeps their default. For example,
moving cleric from Fable to Sonnet:

```json
{ "models": { "cleric": "sonnet" } }
```

What that changes: Sonnet is generally cheaper and faster than Fable, so
each review costs less and a long run finishes sooner — but it is a lighter
reviewer, so expect it to catch fewer of the subtle bugs. A fair trade on
routine work; keep Fable where the review matters most.

Values are tier names — `opus`, `sonnet`, `haiku` or `fable` — never model
IDs, because tier names are all Claude Code's agent-spawning tool accepts.

Running a local or third-party model through a router? Point a tier name
at your model, then pin that tier to the member you want on it. Claude Code
remaps each tier with an environment variable —
`ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`,
`ANTHROPIC_DEFAULT_HAIKU_MODEL` or `ANTHROPIC_DEFAULT_FABLE_MODEL` — set in
your shell or the `env` block of a settings file. For example, to run
cleric on your router's model, in `.claude/settings.json`:

```json
{ "env": { "ANTHROPIC_DEFAULT_SONNET_MODEL": "<your-router-model-id>" } }
```

and in `.claude/party.json`:

```json
{ "models": { "cleric": "sonnet" } }
```

A remapped tier moves everything in the session that uses that tier, not
just the party — and the haiku tier also runs Claude Code's own background
tasks. To put every agent on one model instead, set
`CLAUDE_CODE_SUBAGENT_MODEL` plus `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`;
that overrides `party.json` entirely.

## Session Zero

How quests get written at that table is itself part of the framework:
the **`/party:session-zero`** skill. It is exploration and chat mode — an
iterative dialogue the Guide runs *before* plan mode or code, built for
users who are smart and opinionated but didn't grow up in app
development.

Its core moves: options **with** a recommendation; what a tool or 
framework *actually is* before any verdict on using it — the category, 
the problem it was built for, and which decisions it takes off your plate 
in exchange for its opinions; YAGNI held as the default, because a wrong 
abstraction is a rewrite where duplicated code is only a refactor; 
tables and ASCII sketches where they carry structure prose carries badly; 
every term defined the first time it appears; clarifying questions batched 
early and only when the answer changes something; musings answered with 
assessment rather than action.

## The experience system

Agents are only as good as what the project tells them — so the party's
memory is its **experience**, and it levels up. Four files under
`.claude/` in your own repo hold it:

- `architecture.md` — how the system actually fits together (curated; read
  before planning, or before changing how parts fit)
- `gotchas.md` — non-obvious traps, 1–2 lines each, deleted when fixed
  (curated; read before the first edit, a one-line one included)
- `decisions.md` — why A over B, ~2 lines each, newest first (curated; read
  before choosing between approaches; the full argument lives in the archive)
- `learnings.md` — the **inbox**: an append-only log of surprises, read only
  when the curated three don't answer it, emptied by the Long Rest (below)

Nothing is force-fed into the session — each file is read at the moment it
can change what happens next. The split still matters: the curated three stay
small because they are read often and every read costs context, while the
inbox can grow because nothing opens it until something asks for it.

Nothing here is scaffolded into your repo up front and nothing is copied
out of the plugin: the party's own instructions come from the plugin at
the start of every session — so upgrading the plugin upgrades every
project — and those instructions are what point the party at your curated
files once they exist. The Guide creates each file the first time it has
something to write there.

## Leveling up — the Long Rest

`/party:long-rest` is the ceremony, and it is not fireworks: a Long
Rest is the moment the party *trains*. When the inbox reaches ten
entries the Guide mentions it, once — resting is always your call.

1. It distills the inbox into the curated files the party reads at their
   triggers, prunes what has stopped being true, compacts what has outgrown
   its budget — the full argument moves to `learnings-archive.md`, the live
   entry keeps the claim — then archives the processed entries and leaves
   the inbox empty. It also tells you what those curated files now cost to
   read, every rest: distilling grows them, so the same ceremony is what
   bounds them. A leveled-up party is literally a better-informed party.
2. It appends the level to **`CHRONICLE.md`**: your project's saga in
   plain language — what was built, what was conquered, what *you*
   learned. Every rest is a level; the chronicle is the record of them.
3. It awards the party a title — seeded from your repo's name and the
   level: *your* project's Level 3 party is always, say, the Wardens of
   the Unbroken Build.

The player levels up too: the chronicle plus the decisions file is a
growing, readable record of your own understanding — the thing this
whole framework exists to build.

## Requirements & caveats

- Claude Code with plugin support and subagents; `model:` frontmatter
  values are Anthropic model tiers (`opus`, `fable`) — pin other tiers in
  `.claude/party.json` to match what your plan offers (see Pinning
  models); `effort:` has no per-project override.
- In a project with a browser front end and no browser test tool, the
  first browser test adds Playwright to the project and downloads its
  browsers — a few hundred MB, shared across projects on that machine.
- The session-start hook runs a single one-line `cat` through a POSIX shell.

## Roadmap

- Submit `party` to a community plugin marketplace so it installs without
  adding this repo as a marketplace first.
- **The Thief** — red team: sets up local experiment, plants secrets and
  attempts to steal your app's data and reports how it got in. Test your
  security for real.
- **The Artificer** — refactors, optimizes, and prepares you for production.

## License

MIT — see [LICENSE](LICENSE).
