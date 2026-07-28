# CLAUDE.md

This is the source repo for **Adventure Party** (`party` plugin) — a
fantasy-flavored agent-party and experience-system framework for Claude
Code, aimed at smart, driven users who weren't full-stack devs before
2024. Everything shipped is markdown skills and agents — no runtime
code, no build. The repo doubles as its own marketplace
(`.claude-plugin/marketplace.json`).

## Commands

- Validate manifests (stdlib only — no `jq`, which is absent on stock
  macOS/Linux/WSL): `python3 -m json.tool .claude-plugin/plugin.json` and
  `python3 -m json.tool .claude-plugin/marketplace.json`
- Validate frontmatter (agents + skills; silence means valid, and a
  broken description silently unloads the file; needs PyYAML —
  `pip install pyyaml`, not bundled with python3 on Debian/Ubuntu):
  `python3 -c "import re,glob,yaml;[yaml.safe_load(re.match(r'^---\n(.*?)\n---\n',open(p,encoding='utf-8').read(),re.S).group(1)) for p in glob.glob('agents/*.md')+glob.glob('skills/*/SKILL.md')]"`
- Check detection sentinels (silence means valid): every string
  `/party:setup` step 5b and `/party:config` test for must actually
  appear in the shipped template, or a wired project reads as unwired
  and setup appends a duplicate —
  `for s in 'party:fighter' '/party:session-zero' '@.claude/architecture.md'; do grep -q -- "$s" memory/CLAUDE.md.template || echo "MISSING SENTINEL: $s"; done`
- Dogfood locally: `claude --plugin-dir .` (agents `party:fighter/cleric/wizard`,
  skills `/party:session-zero`, `/party:setup`, `/party:config`,
  `/party:level-up` should all list)

## Layout

- `.claude-plugin/` — plugin + marketplace manifests
- `agents/` — the party: fighter (builder), cleric (reviewer/fixer),
  wizard (read-only advisor)
- `skills/` — session-zero, setup, config, level-up (the Long Rest)
- `memory/` — the experience-system shells `/party:setup` copies into a
  user's project, incl. `CLAUDE.md.template`

## Conventions

- Prose is the product: skills and agents are instructions executed by a
  model. Keep them unambiguous, honest about cost, and plain-language
  first — theme labels mechanics, never replaces them ("experience
  (your project's memory files)").
- Shipped-text changes ripple: the muster-rule bullets exist in
  `memory/CLAUDE.md.template`, this file, and README — keep them in
  sync, and remember old shipped variants become migration fingerprints
  in `skills/setup/SKILL.md` step 5a. A `<!-- party@X.Y.Z -->` marker
  versions the *block's text*, not the release — bump one only when you
  change the block beneath it, never at release time.
- Naming: no trademarked tabletop terms in anything shipped. Check:
  `git grep -riE 'd[&]d|dunge[o]n|\bD[M]\b' -- README.md agents skills memory .claude-plugin LICENSE`
  must return zero hits (pattern is self-escaping; the repo's own
  `.claude/` memory may name the terms when recording why we avoid
  them). The main session is "the Guide".
- `*.sh` stays LF (`.gitattributes` enforces) — `party.sh` is executed
  by a POSIX shell, which chokes on CRLF from a Windows checkout.
<!-- Party-authored blocks below. A marker's version is when that block's
     text last changed — not your installed plugin version. Leave them. -->
<!-- party@0.7.0 -->
- **The party musters on command, not by default.** The main session
  (the Guide) does the ordinary work itself — including substantial
  work. The party rides out only when: (a) the user explicitly summons
  it, (b) a plan-mode plan is approved (plans muster by default — next
  bullet), or (c) the user accepts the Guide's muster suggestion. The
  Guide MAY suggest, once and in one line, when work looks party-sized
  ("this looks party-sized — summon them?") — and takes no for an
  answer. Once mustered: spawn `party:fighter` to build, and when
  fighter finishes, ALWAYS spawn `party:cleric` with its build
  report — not conditional on the build looking clean. `party:wizard`
  (read-only) is on call when explicitly asked, or after two failed
  attempts at the same problem. When spawning a party member, check
  `.claude/party.json` for a `models` override and pass it as the Agent
  tool's `model` parameter (absent = the member's default).
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
<!-- party@0.6.4 -->
- **Session Zero comes before pen touches paper.** Work that involves
  choosing an approach starts as dialogue, not edits — options +
  recommendation, plain-language trade-offs, terms defined on first use,
  YAGNI over speculative abstraction — and the Guide builds only once
  the user says go. When it is unclear whether there is a real choice to
  make, assume there is. Depth tracks stakes × reversibility — a small
  choice gets a line, not a dialogue. Not gated — pure facts, mechanical
  edits with one obvious form, executing an approach already agreed in
  this thread, and approved plan-mode plans. "Just build it" ends the
  dialogue immediately. Never move to plan mode on your own initiative.
  `/party:session-zero` loads the full method when the exploration is
  more than a line.

<!-- party@0.7.0 -->
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

Experience points: each dated entry in learnings.md is one XP. The party
starts at level 1 and gains one at 10, 25, 50 and 100 XP, then one per
100 beyond that. Straight after appending a learning — and at no other
time — the Guide counts the entries with the Grep tool in count mode
(`^## [0-9]{4}-` over .claude/learnings.md; never read the whole log to
count it) and works out the level that count has earned. If it is above
the level in the last `## Level N` heading of CHRONICLE.md (no chronicle
means level 1), say so in one line and suggest `/party:level-up`. Then
let it go: once per session, however many learnings follow, and take no
for an answer. A session that appended nothing says nothing — the Guide
never raises XP unprompted otherwise. XP counts entries, but junk
entries are dead weight the party carries — a padded log distills into
bloated curated files that cost context every session. Log genuine
learnings; let the level come.
