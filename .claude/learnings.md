# Learnings (append-only)

NOT imported into CLAUDE.md — this file can grow without limit and is read
on demand, when context suggests a past learning is relevant. Append at the
bottom, never rewrite history. Periodically distill durable items into the
curated files (architecture.md / gotchas.md / decisions.md) and leave the
log itself untouched.

Entry format:

## YYYY-MM-DD — title

A few lines: what surprised you, what the wrong assumption was, what the
correction is. Traps hit and diagnosed, design insights, user feedback on
approach. Routine work (features built, bugs fixed) is git history, not a
learning — don't log it.

## 2026-07-25 — What the plugin-landscape research actually showed

Web research for the adventure-party redesign, verified against the
GitHub API (aggregator sites inflate numbers). Durable findings:
Superpowers (~260k stars) won on credible author + Willison
amplification + one-command install + <2k-token bootstrap with
on-demand skill loading; its #1 documented complaint is the ceremony
tax on small tasks. Amp's oracle pattern works because it is invoked
sparingly and explicitly — Sourcegraph deliberately does NOT push it in
the system prompt. Every RPG-themed Claude Code plugin to date is
cosmetic-only and has <10 stars; nobody has coupled the theme to a real
methodology + memory system. There is abundant *content* for smart
non-engineers using Claude Code but essentially zero *tooling* — that
niche is empty. Consensus on multi-agent shape: one builder plus a
sometimes-invoked reviewer is the sweet spot; unconditional ceremony is
the criticized pattern.

## 2026-07-25 — Project agent files don't shadow plugin agents

Wrong assumption, held since 0.2.x and shipped in the README ("delete
those files or they silently win"), and baked into the approved 0.4.0
plan (/party:config generating override files): that a project-level
`.claude/agents/fighter.md` overrides the plugin's `party:fighter`.
Live test with a sentinel agent proved otherwise — `party:fighter -> PLUGIN`,
`fighter -> OVERRIDE-SENTINEL`: the two coexist as separate agents and
namespaced spawns always resolve to the plugin copy. The docs' "project
agents override plugin agents with the same name" evidently doesn't
cross the namespace. Correction shipped: model overrides ride the Agent
tool's per-invocation `model` parameter (which outranks frontmatter),
wired as one line in the muster bullet; the whole generated-file
mechanism was deleted before it ever shipped. Meta-lesson: the
adversary flagged the override design as fragile, but only the live
sentinel test caught that it was *impossible* — test the load-bearing
platform assumption before building the machinery on it.

## 2026-07-25 — Serving a WSL2 web app to the tailnet (iPad dogfooding)

Tailscale runs on the Windows host, not inside WSL, so tailnet devices
reach Windows only — nothing listening in WSL is directly visible. The
bridge that works with zero config: WSL binds a port (Windows forwards
its own localhost into WSL automatically), then `tailscale.exe serve
--bg <port>` run FROM WSL drives the host daemon and proxies
`https://desktop-cd4mc0o.tail032cd2.ts.net/` → host localhost → WSL.
HTTPS cert comes free; no firewall rules, no netsh portproxy. Turn off
with `tailscale.exe serve --https=443 off`. Also: `gh` and `jq` aren't
installed in this WSL — python3 stands in for jq; git pushes go over
SSH (the HTTPS remote can't prompt for credentials in a session).

## 2026-07-25 — Smoke-testing a canvas game with zero test tooling

This WSL has no node, no pip, no chromium-cli — but google-chrome is
installed. One-shot `--headless=new --dump-dom --virtual-time-budget=N`
can't click, so interaction needs a same-origin harness: a smoke.html
that iframes the app, dispatches synthetic MouseEvents into it, then
verdicts by sampling canvas pixels for known colors (getImageData) and
capturing iframe window.onerror — verdict written into <title> for
grep. Virtual time fast-forwards setTimeout/rAF, so a 2.5s scripted
rally finishes instantly. Top-level `const` in a page script is NOT on
the iframe's window, so state can't be read directly — pixel sampling
is the reliable oracle. Pair with --screenshot and actually look at it.

## 2026-07-25 — First real cleric muster: independent review earns its cost

Dogfood data point. The Guide solo-built the tennis running-players
feature, smoke-tested it green (headless pixel harness, screenshot,
zero JS errors) — and cleric, summoned afterward, still confirmed and
fixed 4 real bugs: a clobbered game-win message, any-tap-fires-the-serve
(broke the receiver-positioning mechanic the feature exists for), a
falsy-zero resize teleport, and portrait rotation playing on blind.
Two were first-minutes-of-play visible. Lesson for the muster
calculus: "the build looks verified" is exactly the condition the
unconditional fighter→cleric handoff was designed for, and it holds
for Guide solo builds too — a passing smoke test measures rendering,
not gameplay. Cleric also modeled good verification: fuzz the real
extracted logic (5000-point scoring fuzz with invariants), not a
reimplementation.

## 2026-07-26 — Instructions that must fire at execution time belong in the plan text

The silent-muster failure: an approved plan was executed solo even
though the party rule lived in CLAUDE.md. Nothing misfired — the old
rule made plan-silence mean "keep it at the table", and CLAUDE.md is
loaded once at session start and then competes with everything else in
context by the time execution begins. The fix that generalizes: an
instruction that must fire at a specific later moment goes into the
artifact that is in context at that moment — here, a mandatory Execution
section in the plan itself. CLAUDE.md sets the default that shapes the
plan; the plan carries the instruction to the point of use. Corollary
for defaults: silence should mean the behavior you want, because silence
is the most common case.

## 2026-07-26 — Plugin install scope: setup is the gate, not the install

Design question ("should the plugin be project-level?") dissolved on
inspection: install scope is the installer's choice in Claude Code, not
the plugin author's, and because every piece of project state is written
by `/party:setup` rather than shipped by the plugin, the install scope
was never the per-project opt-in — setup is. Verified mechanics against
official docs (v2.1.195): `/plugin install` offers user/project/local
scopes (CLI `--scope`, default `user`); team enablement is
`extraKnownMarketplaces` + `enabledPlugins` in a checked-in
`.claude/settings.json`, and teammates get prompted once to add the
marketplace, after which the plugin auto-loads. One honest cost of
user-level install: the agents and session-zero appear in every
project's lists even where setup never ran — inert by the muster rule,
but visible.

## 2026-07-26 — Skill examples should teach form, not content

Deciding whether Session Zero should ship examples surfaced a general
rule for authoring skills: models imitate examples strongly, so whatever
a skill shows becomes the target shape. A full worked dialogue would
have carried its topic and its length into every unrelated invocation —
a CSS question answered in database metaphors, at transcript length. A
5-line skeleton (`| Option | What it is | Costs you | Pick when |`) leaks
only the shape, which is the part we actually want copied. Cost was ~20
lines instead of ~60. Corollary: an instruction like "use diagrams"
without any shape attached reliably produces either nothing or something
bad — the skeleton is what makes the instruction fire.

## 2026-07-26 — A convergence clause is what makes a dialogue skill rush

Session Zero read as an exploration skill but behaved like a funnel, and
the cause was one subordinate clause: "run the dialogue below, then hand
off to plan mode." Everything else in the file invited open-ended
thinking; that half-line set an exit condition, and an exit condition is
what a model optimizes toward. Removing it — and stating explicitly that
the loop ends only on the user's word, with re-opening a settled-looking
question named as the mode working correctly — was the whole fix.
Generalizes: in prose-as-product, check what the instructions imply
about *when to stop*, not just about what to do.

## 2026-07-26 — Explainability needs a governor, not just a mandate

Pushing hard on high explanation (define every term, explain what the
framework actually is, diagram the trade-offs) has an obvious failure
mode the mandate alone doesn't prevent: an 800-word answer to "should
this be `user` or `users`". The fix that kept both halves was a
calibration ladder — depth tracks stakes × reversibility, lean high when
genuinely unsure, one line when the choice undoes in seconds. Also
repositioned the pre-existing "think deep" gate: depth is now the
default for consequential calls, so that phrase became an override for
the cheap tiers rather than the switch that turns depth on.

## 2026-07-26 — "Unsupported platform" was a guess wearing a fact's clothes

`/party:config` declined the XP display on Windows-native, stating that
`bash`/`sh` "isn't resolvable" there. Both halves were wrong. Git for
Windows ships `sh.exe`, and it ran `xp.sh` correctly — exit 0, right
output — including from a `\wsl.localhost\...` UNC working directory,
which is the case MSYS tools are supposed to choke on. Meanwhile `bash`
*is* resolvable on Windows, as `system32\bash.exe`, the WSL shim: the
skill's stated test would have passed while proving nothing about the
POSIX shell it actually needed. A pre-check can be wrong in both
directions at once, and this one was.

The deeper trap took three probes to see. `sh` resolved fine in the live
session, which made the decline look purely spurious — but only because
this PowerShell was opened with a Git-Bash-flavoured PATH.
`Git\usr\bin` is absent from the persistent (machine + user) PATH, so
the same machine, launched from the Start menu, has no `sh` at all.
PATH on Windows describes the launch chain, not the computer. Anything
executed as a subprocess on every prompt render must therefore be wired
with an absolute interpreter path; a PATH-dependent one works until the
user opens their terminal differently, then fails silently and
untraceably.

Fix was to stop detecting and start proving: try `/bin/sh`, then the
known Git for Windows locations, then a git-anchored guess, then bare
`sh` — and require exit 0 *and* non-empty output before writing one in.
One ladder covers all four platforms with no OS branch. Two smaller
things fell out: deriving `sh.exe` from `where git` is unreliable
(`git.exe` lives in `cmd\` or `mingw64\bin\` depending on who asks, so
a fixed number of `..` hops lands nowhere), and the decline message now
has to name what was tried and what would fix it — the original told
the user their platform was unsupported, which is both false and
unactionable.

Method note: the repo's own gotcha — test a load-bearing platform
assumption with a live sentinel — applied cleanly, and was cheap here
because the sentinel *is* the feature. Running `xp.sh` is the whole
test. Worth reaching for that shape whenever the thing in doubt is
already executable.

## 2026-07-26 — A skill description is a router, and prose frontmatter has a YAML trap

Trimming session-zero's `description` (1083 → 689 chars) turned on a
question worth reusing: what is this text *for*? It is the only part of
a model-invocable skill that is always in the model's list, so its job
is to decide whether to fire — not to summarize the skill. Everything
in it that described *behavior* ("options with a recommendation", "the
user makes the calls", "plan mode only when the user asks") was already
in the Session Zero bullet in `memory/CLAUDE.md.template`, which is
always-loaded in any set-up project. The description was paying twice
for the same instruction. Test to apply next time: for each clause, ask
"does this change whether the skill fires?" — if not, the body or
CLAUDE.md owns it.

Corollary about the other three skills: they are
`disable-model-invocation: true`, so they are invoked by name and their
descriptions route nothing. Their 245–394 char length is not a
convention this skill was violating; matching it would have been
cadence copied without its cause.

The YAML trap: a plain (unquoted) scalar cannot contain `": "`. The
first draft opened "Exploration and chat mode: iterative, …" and would
have failed to parse with "mapping values are not allowed here" — the
whole skill silently unloadable. Descriptions here are long prose in
plain scalars, so this is a live hazard: colon-space, and a leading
`- `/`? `/`#` on any line, are the characters to keep out. Parse the
frontmatter after editing rather than eyeballing it.

## 2026-07-26 — A rule stated only in the intro is flavor, and a gotcha's scope decides what gets audited

Reviewing the three agent files turned up two durable things and one
gap.

Fighter was supposed to write tests, and its opening line said so
("implementation and tests, built end-to-end") — but the only operative
bullet under "the few rules that matter" was about *running* the suite.
A model satisfies that by running whatever exists; the intro clause is
flavor, and flavor loses to the rules section. Anything actually
required goes in the rules with a mechanism attached: "write tests" is a
wish, "a test you have never seen fail is not evidence" is an
instruction. The same trap's other half: "run the suite, or find the
obvious runner" had no branch for a repo with no suite at all — the
common case for this plugin's audience — so honest compliance produced
no tests. Fix included a capped ladder (first test file + the `Tests:`
line in CLAUDE.md, "not a testing strategy, not CI") so the escape from
untested code doesn't become a framework install.

The YAML frontmatter gotcha, logged after it bit a *skill*, was written
as "skill frontmatter descriptions…" — so `agents/` was never audited
against it, and two of the three agent files were sitting broken:
cleric on a literal `": "`, fighter on a colon at end of line, which the
gotcha's wording doesn't name either. A gotcha describes a *class* of
mistake; scoping its wording to the file type where you first met it
quietly exempts every other file. Both halves fixed — widen the entry,
and make the check runnable rather than remembered (`python3` + pyyaml,
which this WSL has even though it lacks jq).

The gap: the party had no path into the experience system at all. A
subagent's context dies with its turn, so anything not in its final
message is lost — every trap diagnosed mid-muster evaporated, and
wizard's insights went to a private memory dir the project never sees.
Hence a `LEARNED:` line in all three report contracts, worded to match
the Guide's existing append rule so no new machinery (and no template
migration) was needed. Two members' reports are the transport; the Guide
is still the only writer, which keeps the log single-voiced and puts a
junk entry in front of the user before it becomes XP.

## 2026-07-26 — A capability flag can widen a tool allowlist

Wizard shipped with `tools: Read, Grep, Glob` plus `memory: project`,
which read as belt-and-braces — a narrow allowlist and a private
scratchpad. The docs say otherwise: enabling `memory` "automatically
enables" Read, Write and Edit so the agent can manage its memory files.
So the frontmatter had two possible readings and both were broken.
Either the flag widens the allowlist, and the READ-ONLY guarantee
asserted in the agent's own body was false — the precise failure we had
just rejected `Bash` to avoid — or `tools:` wins and the memory feature
was inert. Nothing was ever written at either scope, so it may have been
inert all along (which also corrects the entry above: wizard's insights
weren't going to a private dir, they were going nowhere). Deleting the
one line resolved it without needing to know which, and that's the
useful shape — when two readings of a config are both bad, the fix is
the line, not the diagnosis.

Generalises past this field: a permission surface is not only what the
allowlist says. A capability flag elsewhere in the same frontmatter can
grant tools as a side effect, so "read-only" is a claim about the union
of everything declared. Read the field docs for anything that sounds
like a feature rather than a permission.

Second-order, and specific to this repo: `memory: project` writes a
checked-in `.claude/agent-memory/<agent>/`, which would have been a
second un-curated project memory store competing with the experience
files this plugin exists to maintain — and invisible to the Long Rest. A
plugin whose product IS a memory system should be suspicious of platform
features that quietly add another one.

## 2026-07-26 — A governor can be cheaper to satisfy than the behavior it governs

Two rounds of user pushback on the same draft, both landing on one
authoring mistake in two forms.

Cleric got a scope governor — stay inside the diff, plus a
`NEEDS_REBUILD:` escape for a build that needs rebuilding rather than
repairing — and the question came straight back: does this stop her
fixing obvious problems? The rule itself didn't; its gate was
defect-vs-preference, not size. The escape hatch did. Declaring
`NEEDS_REBUILD:` was *cheaper* than performing a large repair, so an
agent whose entire job is review-and-repair had been handed a legitimate
way to stop working — and cleric runs on a cheaper tier than fighter,
which is exactly where that incentive bites. Fix was to price it: high
bar, and raising it does not excuse fixing everything separably fixable.
Rule to carry: having added any governor to an agent, ask what the
cheapest way to satisfy it is, and whether that is the behavior you
wanted. Sibling of the convergence-clause learning — same failure, one
verb apart: that one told an agent when to stop, this one told it how.

The second was ordering, not content. Wizard's new paragraph opened with
what it cannot do (no shell, no tests, no `git diff`) before saying it
may read the entire repo unprompted — and was read as a boundary on
everything, which drew "are we hamstringing wizard too?". Nothing in it
said that; the limit simply came first, and in prose-as-product first
means framing. Capability before constraint: "read the whole repo at
will — the paths in the prompt are a starting point, not a boundary" now
leads, and the runtime limits follow. Worth checking on any agent file
whose role is defined partly by a restriction, because the restriction
is the tempting thing to lead with.

## 2026-07-27 — A guarded script is a bad oracle for its own dependencies

The Windows interpreter probe was right in shape and wrong in
strictness. Wiring the XP display into a real project picked
`Git\usr\bin\sh.exe` — it passed the spec's test (exit 0, non-empty
output) and then printed `tail: command not found` / `sed: command not
found` on every prompt render. `usr\bin\sh.exe` is the bare shell
binary; only the `bin\sh.exe` wrapper puts Git's coreutils on PATH
first. The ladder had never listed the wrapper at all.

What let it through is the more transferable half. `xp.sh` guards its
utility calls (`2>/dev/null` on the grep, an empty `CHRON` pipeline
falling through), so on a project whose `learnings.md` is still empty a
coreutils-less shell produces exactly the same exit code and plausible
output as a working one. The probe couldn't fail until the thing it was
protecting had real data — i.e. never at setup time, always later, on
someone's actual repo. Testing a program that swallows its own errors
tells you the program is robust, not that its environment is sound: exit
status proves the interpreter *started*, and stderr is the only cheap
evidence it *worked*. Any probe whose subject has error guards needs a
channel those guards don't cover.

Also worth noting how it was found — not by review, but by running
`/party:setup` project-scoped and watching the statusline. The 2026-07-26
entry above fixed this same area by dogfooding too, and left a subtler
bug behind. One pass of dogfooding finds the failure that fires
immediately; the deferred one needs the second pass.

## 2026-07-27 — Editing a plugin's source is not running it, and the default is stale

`/plugin install` in this very repo served 0.6.0 while HEAD was 0.6.1 —
two commits, including the fix for a statusline bug that fires on every
prompt render. Nothing malfunctioned. Install snapshots the local
*marketplace clone* into a cache keyed by version string, and neither
install nor `/reload-plugins` ever fetches origin. The clone had last
been updated hours before the release. So four copies of the same bytes
sit on this machine with four different refresh rules, and
`${CLAUDE_PLUGIN_ROOT}` — which every skill's file paths resolve
through — points at the oldest one. That is how `/party:setup` run
*inside* the source repo copied a `party@0.4.0` script into a repo whose
working tree held 0.6.1.

Two things generalize past plugins. First: the wizard's reconstruction
was right in outline but I nearly accepted a false detail with it — the
clone's `origin/main` ref was *behind its own checkout*, which a plain
fetch cannot produce. A ref you'd naturally trust as "what it has seen"
was lying, and only running the discriminating test surfaced it. An
analysis worth commissioning is worth the two commands that falsify it.

Second, and the one that cost a user-facing bug: I reasoned about the
mechanism from strong evidence for three exchanges without once checking
whether the platform already solved it. It does — auto-update refreshes
marketplace *and* plugin in the background. But it is enabled by default
only for Anthropic's own marketplaces and **off for third-party ones**,
so every Adventure Party user was pinned at their install version with
no notification, and the README's Upgrading section documented step 4 of
a 4-step process. The defaults that bite are the ones that differ by
who owns the thing; "how does this work" is not the same question as
"what does this do by default for someone who isn't me."

## 2026-07-27 — A rule that describes a mode can't fix a misclassified turn

A downstream project on party@0.6.0 opened with "i want to play snake,
lets build the app. whats the lowest effort way to achieve this on this
pc. i want to play in browser." The Guide wrote the whole game and
opened it in a browser. Session Zero never fired, despite an explicit
approach question sitting in the turn, and the user's next message was
"why didnt you call session 0."

The instinct was to put more Session Zero in front of the model. That
instinct was wrong, and the evidence was already on the screen: the
CLAUDE.md Session Zero bullet is always-loaded, it was in context for
the entire session, and it changed nothing. Because compliance was never
the broken part. The Guide agreed that scoping turns get Session Zero;
it decided this wasn't a scoping turn. Classification failed, compliance
held, and every fix in the more-text family — importing the ~2.3k-token
SKILL.md, growing the bullet, adding trigger examples — feeds the step
that was already working. Generalizes past this bullet: when an
always-loaded rule doesn't fire, first establish whether the model
disputed the rule or the case. Only the second is fixed by rewriting the
rule, and it is fixed by making the rule *decide the case* rather than
describe the behavior.

Two contributing details worth carrying separately. The trigger examples
were all pure questions ("what's your view", "should I…"), so a turn
that mixed an imperative with a question read as an instruction with a
detail attached — examples teach the *shape* of a trigger, not just its
subject, and a list of one shape silently excludes the others. And the
carve-out that got misapplied was written about the triviality of the
*question* ("a one-shot fact"), while the Guide's actual reasoning was
that the *answer* was obvious and the *work* was small. An exemption is
read against whatever nearby thing feels small; if two different things
can be small, name which one you meant.

## 2026-07-27 — The curated file with an inflow and no outflow

Audited the experience system's intent against its actual state at 19
XP. Three of the four files were behaving: gotchas held its 1–2 line
discipline (76 lines), architecture stayed at four entries, learnings
grew freely as designed because nothing imports it. `decisions.md` was
252 lines across 16 entries — ~16 lines each, several past 30 — sitting
in the tier that is paid for on *every* session, including sessions
that only fix a typo.

The cause is structural, not sloppiness. Every other curated file has a
death condition that can be *checked*: a gotcha dies when the code
proves its cause fixed, an architecture note dies when it stops being
true. The Long Rest's prune step tests exactly that — "curated entries
that stopped being true" — and a decision is a historical record, so it
passes the test forever. Meanwhile two separate rules pushed entries
in: Session Zero's "capture decisions durably" fires at decision time,
and the Long Rest's distill step routes learnings cores into the same
file. Inflow from both ends, outflow gated on a condition that can
never fire.

The general shape: **a retention rule that tests truth cannot bound a
file whose entries are permanently true.** What was actually wanted was
"stopped being load-bearing," which is not checkable — so the fix has
to be a budget at write time rather than a test at prune time.

Also worth keeping: the reason a length budget is the right instrument
here at all is that a decision's *conclusion* and its *argument* have
completely different read frequencies — the conclusion is consulted
every session by construction (it's imported), the argument roughly
once, when someone tries to reopen the call. Two read frequencies in
one file means one of them is being overpaid for. Splitting on that
seam is why the pointer ("see learnings YYYY-MM-DD") does real work
rather than being a citation formality.

Corollary noticed while checking who actually reads these: subagents
inherit the project CLAUDE.md, so fighter never *loads* gotchas — the
imports arrive pre-loaded before it reads its task. Only wizard has an
explicit instruction to open the learnings log, which is coherent, since
it's the member you call when the cheap always-loaded context already
failed. So "is this file worth its size" is really a question about
every agent in the party at once, not just the Guide.

## 2026-07-27 — The repo is its own distribution channel, so `assets/` is not free

A 7.5 MB replacement for `assets/party.png` landed in the working tree
and the instinct was "it's not in the plugin, nobody downloads it."
That premise is wrong in a way worth writing down: `marketplace.json`
declares `"source": "./"`, so the plugin *is* the repo root. There is
no packaging step, no ignore list, no artifact build — `/plugin
install` git-clones this whole tree, and every user pays for the full
blob history, not just the checkout.

The general shape: **when the distribution mechanism is a clone, every
tracked byte is a shipped byte, including deleted ones.** That makes
binary assets a one-way door — the superseded 2.6 MB blob is permanent
now, and no future cleanup short of a history rewrite touches it. The
lesson is not "compress images," it's that the usual mental separation
between "source" and "release artifact" doesn't exist here, so the
checks that normally happen at package time have to happen at commit
time instead.

Sizing rule that fell out of it: the README renders the hero at
`width=480`, so 960px is the honest target (2x for retina) and
everything above that is pure freight. 1792px was 3.7x oversampled.
Palette-quantized to 646 KB from 7.5 MB with no visible difference at
render size — checked by cropping a gradient-heavy band from all three
candidates, stacking them 1:1, and actually looking, rather than
trusting the byte count. Worth doing for any lossy step on a visual
asset; the file size tells you nothing about whether it still looks
right.

Process note: the change appeared in the working tree *after* the
user's "commit all" was given against a listed set of files, so it
wasn't covered by that approval. Committing it silently would have been
the easy path and would have shipped the 7.5 MB. A change list the user
approved is a snapshot, not a standing licence — re-check `git status`
between approval and commit, and anything new is a separate ask.
