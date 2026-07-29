# Decisions

Why A over B, for choices below plan level. Loaded into every session —
keep entries short, newest first.

Format: `YYYY-MM-DD — decision — why`
Budget: 3–5 lines. The argument lives in learnings.md; point at it by
date. This file is paid for every session, the argument is read once.

2026-07-29 — The plugin serves its instructions from a SessionStart hook
and copies nothing into a user's repo; `/party:setup`, `/party:config`
and `/party:level-up` are deleted, `learnings.md` becomes an inbox that
`/party:long-rest` empties, and levels are one per rest. Rejected
keeping the template plus better migration tooling — the drift it
manages is created by the copying, and every piece of the machinery that
manages it can fail silently. Cost accepted: the hook is now a hard
dependency, and its Windows-native path is unverified. See learnings
2026-07-29.

2026-07-29 — The hook ships as one SessionStart block, two one-line `cat`
commands, plain stdout, matcher omitted — not JSON `additionalContext`,
not one entry per file, not an enumerated matcher. The spike proved
stdout injects verbatim and a 21.9k payload survives whole, so both
elaborations bought nothing, and plain `cat` keeps python3 out of the
plugin's runtime requirements. See learnings 2026-07-29.

2026-07-28 — The XP statusline and SessionStart banner are dropped
outright; the level-up nudge moves to the moment the Guide appends a
learning, counting with the Grep tool (no shell, no stored counter).
Rejected patching the probe (runtime `||` chain, slot-2 discovery,
re-probe on `/party:config`) and shipping `xp.sh` unwired for manual
setup — ~70 lines of the repo's most bug-prone shipped instruction
existed to render one line, and every fix round has landed in it. See
learnings 2026-07-28.

2026-07-27 — Decisions entries get a 3–5 line budget: choice, rejected
alternative, one-clause why, plus a pointer to the learnings entry
holding the full argument — over pruning old decisions at the Long Rest
(smaller edit, but leaves the write-time habit intact) or leaving it.
Decisions was the one curated file with an inflow and no outflow: the
Long Rest's prune gate tests *truth*, and a decision never stops being
true, only stops being load-bearing. See learnings 2026-07-27.

2026-07-27 — Session Zero becomes a **phase work passes through by
default**, not a mode the Guide has to recognise — and the bullet is
rewritten to decide the case rather than describe the mode. Forced by a
live 0.6.0 misfire (see learnings 2026-07-27): the always-loaded
CLAUDE.md bullet was in context the whole time and did not help, because
the Guide never disputed "scoping turns get Session Zero" — it decided
"this isn't a scoping turn." The failure is classification, upstream of
anything the skill contains, which is precisely why every more-text fix
was rejected: `@`-importing SKILL.md (~2.3k tokens every session,
forever, including typo-fix sessions), growing the bullet, or adding
trigger examples all describe a mode already excluded. Removing the
recognition step is the only fix that touches the failing step, and
ambiguity now resolves toward talking ("when it is unclear whether there
is a real choice to make, assume there is") where 0.6.x resolved it
toward building. The gate is Option A — approach decisions, "if writing
code means choosing how, talk first" — over Option B, no edit without a
preceding exchange: B removes the judgement entirely but trains the user
to bypass it, and a rule routinely bypassed is worse than a narrower one
that holds. A typo fix contains no architecture, so it is outside the
gate's scope rather than an exemption from it. Three explicit releases
(approach settled earlier in the thread, approved plan, "just build it")
stop it re-litigating agreed work; the depth clause is what stops it
becoming the ceremony tax. Honest cost accepted — some one-turn tasks
become two, which is the trade being bought, since the complaint was the
Guide picking an architecture silently and presenting it finished.
Muster rules untouched; this governs only what happens before pen
touches paper. The `PreToolUse` hook that would make the failure
mechanically impossible stays deferred — it needs an unblock mechanism
and would fight legitimate work; revisit only with evidence the prose
rule doesn't hold.

2026-07-27 — `<!-- party@X.Y.Z -->` markers version the block's *text*,
never the release, and the legibility problem is fixed with a one-line
legend rather than a second number — setup's step 5a already reads them
that way ("a block preceded by a 0.5.0 marker is already current"),
while `skills/setup/SKILL.md` separately told setup to stamp the current
plugin version; that contradiction is deleted. Rejected restamping at
release (a manual per-release step, and 5a loses its cheap signal) and
the two-field `party@0.6.2 (block last changed 0.5.0)` middle ground —
the current-version field goes stale the same way the moment a user
upgrades without that block changing, unless setup rewrites markers in
blocks it has no reason to touch, which is diff noise in the user's repo
and against setup's own "never touches your content" promise. The
freak-out ("0.5.0 in a 0.6.2 repo — has this rotted?") was the author's
own reaction and is real, but it is a labelling problem: the legend
answers it where it is asked, at zero fingerprint cost. Same rule
governs xp.sh's header, which is therefore correct at 0.6.1.

2026-07-27 — Dogfooding runs the source via `claude --plugin-dir .`; the
installed `party` plugin on this machine exists only to test the
*released* install path, and the release routine is push → marketplace
update → plugin update → restart. Sitting in the source repo does not
mean running it: install snapshots the marketplace clone into a
version-keyed cache, so three copies of the same bytes drift
independently, and `${CLAUDE_PLUGIN_ROOT}` points at the oldest of them.
Diagnosed after `/plugin install` here served 0.6.0 while HEAD was
0.6.1 — which would have re-wired the statusline with the weak probe
0.6.1 exists to fix. The user-facing half is a README fix, not a code
change: auto-update is off by default for third-party marketplaces, so
Install now says to enable it and Upgrading names both halves of the
chain (marketplace, then plugin) instead of only the `/party:setup`
re-run.

2026-07-27 — The interpreter probe's success predicate gains **empty
stderr** alongside exit 0 and non-empty stdout, and each Git for Windows
location is tried `bin\sh.exe` before `usr\bin\sh.exe` — amending, not
reversing, the 2026-07-26 probe decision below, which still governs
(prove, never detect). What was wrong was the strictness, not the shape:
`usr\bin\sh.exe` is the bare shell binary, so it runs xp.sh without
Git's coreutils, yet passed the old predicate because xp.sh guards its
`grep`/`tail`/`sed` calls and a project with an empty `learnings.md`
therefore still exits 0 with plausible output. The bug surfaced only
later, as a wrong XP count plus `command not found` on every prompt
render. Exit status measured that the shell started; stderr is what
measures that it worked. The `usr\bin\` candidates stay in the ladder
below their `bin\` siblings — on some installs they are all there is,
and the strengthened predicate now rejects them when they're crippled.

2026-07-26 — The manifest check swaps `jq` for `python3 -m json.tool`,
and the frontmatter check keeps PyYAML with an install note — rather
than a probe-and-run wrapper or a stdlib-only `scripts/validate.py`.
`jq` is preinstalled on no mainstream platform, while python3 was
already a hard dependency of the frontmatter check, so one interpreter
covers both and `json.tool` is stdlib everywhere python3 is real. The
xp.sh probe pattern was rejected deliberately: probing earns its
complexity in shipped code that runs on users' machines every prompt
render, not in a hand-run pre-commit check. A stdlib-only validator was
rejected too — replacing a real YAML parser with regex to dodge one
`pip install` trades a stronger check for a new shipped artifact.
Portability floor recorded in gotchas: stdlib is free, everything above
it needs an install note.

2026-07-26 — Wizard stays read-only with no `Bash` (turn cap raised
15 → 25 instead), and callers paste the diff and error output — a shell
is a write primitive, so granting one would downgrade "READ-ONLY" from a
structural guarantee to a promise, and that guarantee is why fighter and
cleric can call wizard mid-encounter without risk. A wizard that can run
tests also drifts toward iterating instead of reasoning, which is the
opposite of what xhigh effort is bought for. The real constraint on its
depth was never the toolset but the turn cap, so that is what moved; the
number is named in Method step 5 as well, since a model can't read its
own `maxTurns`. Diff-blindness is fixed at the caller's end, where a
shell already exists. `memory: project` went the same way and for the
same reason — the docs have it auto-enable Read/Write/Edit, so it either
falsified READ-ONLY or was inert, and it would have written a checked-in
`.claude/agent-memory/wizard/`: a second un-curated project memory store
competing with the experience files, invisible to the Long Rest.

2026-07-26 — The party reaches the experience system through a `LEARNED:`
line in each member's report, not by writing memory files itself — a
subagent's context dies with its turn, so the final message is the only
carrier, and the Guide's existing "append what surfaced" rule already
fires on it (matching wording deliberately, so no `CLAUDE.md.template`
change and no new migration fingerprint in setup step 5a). Keeping the
Guide as sole writer keeps the append-only log single-voiced and puts
every candidate in front of the user before it counts as XP; "usually
none" and "not routine work" are the governors against three reports a
session padding the log.

2026-07-26 — Cleric's repair scope is the change and its blast radius,
with `NEEDS_REBUILD:` as a high bar that does not excuse it from fixing
what is separably fixable — an unbounded "fix everything you find" lets
a reviewer redo working code to taste and triple the user's diff, while
an easy rebuild verdict would quietly turn cleric back into the
findings-report agent its file says it isn't. Defect vs. preference is
the gate, never size: "a defect is a defect however large, and 'large' is
never why you leave one."

2026-07-26 — session-zero's `description` is a router, not a summary:
cut to 689 chars (from 1083) by dropping every behavior clause (options
+ recommendation, user makes the calls, never self-initiate plan mode)
and keeping only routing — every-turn re-evaluation, mid-conversation
drift, trigger phrases, and the fact-vs-decision tie-break. The dropped
clauses are already in the shipped `memory/CLAUDE.md.template` Session
Zero bullet, which is always-loaded in any set-up project, so the
description was paying twice. Not cut to sibling length (~250) — the
other three skills are `disable-model-invocation: true` and are invoked
by name, so their descriptions route nothing; symmetry with them is a
false target. A compact identity clause stays because the plugin ships
nothing project-specific: in a repo that never ran `/party:setup` there
is no CLAUDE.md bullet to lean on.

2026-07-26 — `/party:setup` ships party.json with a `"//"` comment key
and an empty `"models": {}`, rather than snapshotting the real defaults
or leaving the file silent — the file is the one thing users are told
to edit, and it said nothing about `models`, so the key was
undiscoverable from it (the author hit this). Empty means what absent
means, so the no-stale-pins rule survives intact; snapshotting
`"cleric": "fable"` would silently outlive any future default change.
Cost accepted: `/party:config`'s unknown-top-level-key stop — which
exists to catch `experiance` typos — now carves out exactly the literal
`"//"`. Note `models` takes stable tiers (opus/sonnet/haiku/fable), not
model IDs, so new model releases never require a config edit.

2026-07-26 — The XP display's shell is chosen by probing candidates and
requiring exit 0 + non-empty output (`/bin/sh`, then Git for Windows
locations, bare `sh` last), never by platform detection — one probe
covers macOS/Linux/WSL/Windows-native with no OS branch, and it replaces
two wrong beliefs at once: that Windows-native has no POSIX shell (Git
Bash works, verified, even from a UNC cwd) and that `bash` resolving
proves one exists (it's the WSL shim). Windows gets the *absolute* path
even when `sh` is on PATH, because there PATH reflects the launch chain,
not the machine. Declining names what was tried and the fix — an
unactionable "unsupported platform" is the failure being fixed.

2026-07-26 — Session Zero is exploration/chat mode with no exit
condition but the user's word (plan mode never Guide-initiated), and
explainability is calibrated by stakes × reversibility rather than
always-loud — the old "then hand off to plan mode" clause was what made
the Guide race to converge; uncalibrated depth is its own failure
(burying a naming question stops the user asking a second one).

2026-07-26 — Session Zero stays a single SKILL.md (no `references/`
progressive disclosure, no separate explain skill) and teaches its
visual idioms via ~5-line skeletons rather than a worked example
dialogue — there is no bulky lookup material to defer (the tech
explanations are per-question research, not a shippable catalogue), so
splitting would be the premature abstraction the skill now argues
against; and models imitate examples strongly, so a full transcript
would leak its topic and length into unrelated Session Zeros while a
skeleton leaks only shape.

2026-07-26 — Install scope stays the installer's choice (user-level
default for solo/trial, project-level for team repos), with
`/party:setup` as the real per-project opt-in gate — all project state
is written by setup, never the plugin, so a user-level install is inert
until a repo opts in; forcing project-level installs would add reinstall
friction with no benefit, while checked-in
`extraKnownMarketplaces`/`enabledPlugins` gives teams a shared party.
README documents both paths (verified against Claude Code docs
2026-07-26).

2026-07-26 — Plan-mode plans muster by default (mandatory Execution
section; table only on user request; no Guide discretion) — plan silence
previously meant solo execution and the muster silently didn't fire; the
plan text is what the executor reliably follows, so the instruction
rides inside the plan; plan-mode entry is the party-sized signal,
preserving the ceremony-tax decision (approval remains the consent
gate).

2026-07-25 — The fighter → cleric handoff is unconditional, never
gated on "the build looks clean" (and the same holds for Guide solo
builds) — dogfooded: a feature that passed a headless pixel smoke test
with zero JS errors still had 4 real bugs cleric found and fixed, two
visible in the first minute of play. Automated UI checks measure
rendering, not behavior, so "it looks verified" is precisely the
condition an independent reviewer exists for.

2026-07-25 — Model overrides apply at spawn time (Agent tool `model`
param, wired into the muster bullet) instead of generated
`.claude/agents/` override files — live test proved project agent files
do NOT shadow `party:<name>` (they coexist; namespaced spawns get the
plugin copy), so generation could never work; the param outranks
frontmatter and needs no files that rot.

2026-07-25 — Level-ups trigger the Long Rest (`/party:level-up`):
distill learnings into curated experience files, prune stale gotchas,
append a plain-language CHRONICLE.md entry, award a seeded title/badge —
recognition alone is the sub-10-star-graveyard pattern; bolting the
level-up to the distillation chore nobody otherwise does makes the
metaphor literally true (a leveled party is a better-informed party).
Token cost is real, so it is user-invoked only, never automatic.

2026-07-25 — Party musters only on explicit command, approved plan, or a
Guide *suggestion* (reverses the auto-summon rule) — the ceremony tax is
the single most documented failure mode of workflow plugins (Superpowers,
Spec Kit); the human decides when the party rides.

2026-07-25 — Main-session role renamed "the Guide"; scrub the tabletop
brand name and its trademarked game-master title from all shipped copy —
those two terms are protected; generic archetypes (fighter/cleric/
wizard/party/XP/session zero) are not; "Guide" matches the teaching
role for the non-engineer audience. User model config lives in
`.claude/party.json`, applied by `/party:config`; defaults unchanged
(fighter=Opus, cleric/wizard=Fable).

2026-07-25 — Memory rebranded "experience"; XP = dated entries in
learnings.md ONLY (append-only, so XP never decreases and survives
distillation); surfaced via statusline + SessionStart banner, both
shell-script-only and opt-in at setup — theme must label real mechanics
(the XP number is literally the health of project memory); always-on
token-costing hooks are a named plugin failure pattern.

<!-- Record the decision AND the rejected alternative with the reason —
     future sessions re-litigate choices whose "why" isn't written down. -->
