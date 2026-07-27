# Adventure Party

<p align="center">
  <img src="assets/party.png" alt="A fighter, cleric, and wizard gathered around a glowing arcane interface" width="480">
</p>

An adventuring party and experience system for
[Claude Code](https://claude.com/claude-code), packaged as the **`party`
plugin**. You bring the quest; the party ships it.

## Install

There is a two phase installation process. Installing the plugin
gets you the party and session zero. Running setup gets you the
experience system to improve your party over time.

You can install both onto a new or existing repo.

**Step One** - Within the Claude session, add the marketplace and install 
the plugin:

```
/plugin marketplace add skeggsguy/adventure-party
/plugin install party@adventure-party
```

Pick a scope when `/plugin install` asks:

- **User** (the default) — the party is on call in every project.
  Right for solo work and for trying it out; it stays inert in any
  repo until you run setup there.
- **Project** — the party ships with the repo, for team use. Choosing
  "Project" writes it into the repo's `.claude/settings.json`.

  Teammates opening the repo are prompted once to add the marketplace;
  after that the plugin loads automatically for them.

**Step 2** Then — whichever scope you chose — once per project you want the
experience system in:

```
/party:setup
```

**Upgrading** — after you update the plugin to a newer version, re-run `/party:setup` once in each project that uses it. It is safe to
re-run: it never overwrites your experience files or your edits, it
brings any older CLAUDE.md wiring up to the current version, and it
refreshes the local copy of the experience-display script. Skipping it
leaves the project running the previous version's copy.

## The premise

Adventure Party is built for people who are smart and intellectually
driven but weren't full-stack developers before the genesis of AI — and on the
conviction that successful AI development hinges on three things:

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
6. **Level up** — learnings are captured in every session. On level up
   you long rest and learnings are sorted into architecture, decisions
   and gotchas which are readable by Claude. You level up, AI levels up.

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
the command in your CLAUDE.md. Deliberately loose otherwise — it's a 
powerhorse, not a checklist-follower.

**Cleric** always runs after fighter, it reviews the actual diff
and the report from fighter, then directly heals what it finds — 
bugs, pinned-invariant violations, test gaps, convention drift, 
needless complexity — and leaves the tree green, driving any user-facing 
surface the way a user would. 

**Wizard** is the party's high-effort judgment: deep review, hard
debugging (2+ failed attempts), and which-approach calls. Wizard
is expensive and slow but valuable exactly when the repo needs it
most. Solves for try and fail re-attempts.

### The muster protocol

**The party musters on command, not by default.** The Guide does
ordinary work itself. The party rides out only on one of three triggers:

- You explicitly summon it.
- A plan-mode plan is approved — **plans muster by default**: every plan
  ends with an Execution section naming who runs each phase, fighter
  building and cleric reviewing unless you said otherwise while
  planning.
- You accept the Guide's suggestion — it may offer, once and in one
  line, when work looks party-sized, and takes no for an answer.

Planning is deliberately **not** a party member: planning is a dialogue
with the human, and subagents can't talk to the human. The quest gets
written at the Guide's table; the party executes it.

Default models are set per agent; to change them, run `/party:config` 
— the Guide passes your choice at spawn time, which outranks the agent 
file's default.

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

## Leveling up — the Long Rest

`/party:level-up` is the ceremony, and it is not fireworks: a Long Rest
is the moment the party *trains*.

1. It distills the learnings log — only entries since the last rest —
   into the curated files that load every session, and prunes gotchas
   that have been fixed. A leveled-up party is literally a
   better-informed party.
2. It appends the level to **`CHRONICLE.md`**: your project's saga in
   plain language — what was built, what was conquered, what *you*
   learned.
3. It awards the party a title — seeded from your repo's name and the
   level, so it is deterministic: *your* project's Level 3 party is
   always, say, the Wardens of the Unbroken Build. Their name, not a
   slot machine's.

The player levels up too: the chronicle plus the decisions file is a
growing, readable record of your own understanding — the thing this
whole framework exists to build.

## Requirements & caveats

- Claude Code with plugin support and subagents; `model:`/`effort:`
  frontmatter values are Anthropic model tiers (`opus`, `fable`) —
  change them via `.claude/party.json` + `/party:config` to match what
  your plan offers.

## Roadmap

- Submit `party` to a community plugin marketplace so it installs without
  adding this repo as a marketplace first.
- **The Thief** — red team: sets up local experiment, plants secrets and
  attempts to steal your app's data and reports how it got in. Test your
  security for real.
- **The Artificer** — refactors, optimizes, and prepares you for production.

## License

MIT — see [LICENSE](LICENSE).
