# Learnings archive

Processed entries, verbatim and in order. Written by `/party:long-rest`
when it empties the inbox; read on demand, never injected.

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

## 2026-07-28 — An absolute interpreter path is machine-state, and nothing re-probes it

The XP statusline and SessionStart banner went silent in this repo. Every
part of the experience system was intact — `party.json` had
`experience.enabled: true`, `.claude/party/xp.sh` was byte-identical to
`scripts/xp.sh`, and running it by hand printed `📜 Party Lv.2 · 20/25 XP`.
What was wrong was the interpreter: `settings.local.json` invoked
`"C:\Program Files\Git\bin\sh.exe"`, written by a `/party:setup` run under
Windows-native Claude Code. The same project directory reached from WSL
has no such path, so the statusline command failed on every render and
Claude Code showed nothing rather than an error.

This is the bill for the 2026-07-26 probe decision, and the decision is
still right — a PATH-dependent interpreter dies silently when the user
launches differently, which is worse. But an absolute path records where
the interpreter was *at setup time*, and setup runs once. The probe has no
re-run trigger, so any move of the environment under a project — WSL to
Windows-native, a Git for Windows uninstall, a repo copied between
machines — leaves a stale absolute path with no self-heal and no
diagnostic. `settings.local.json` being gitignored hides it further: the
breakage lives in the one file nobody reviews.

Diagnostic order that worked, and should be the default for "feature X
shows nothing": run the script by hand *first*. It printed correct output
immediately, which eliminated XP counting, the opt-in gate, the file copy,
and the level thresholds in a single command, and left only the wiring.
Debugging from the payload outward beats reading the config first, because
a working payload converts a vague "it's broken" into "the caller is
wrong."

Second trap, in the same session: the banner was *also* silent, and that
one is correct behavior. Banner exits 0 unless a level-up is pending, and
Lv.2 chronicled equals Lv.2 computed at 20 XP. Two silent things with one
real cause — say which is which when reporting, or the user re-fixes the
half that was never broken.

Open, not fixed: setup could re-validate the stored interpreter on a later
run, or the statusline could fall back rather than vanish. Both are real
designs and neither is chosen yet; the cost of the current behavior is
that the failure is invisible exactly where the theme promises visibility.

## 2026-07-28 — The display was machinery disproportionate to its payload

Started as "why is my statusline blank" and ended as a decision to delete
the statusline. Worth recording the path, because the first four turns
solved the wrong problem well.

The presenting bug: `settings.local.json` invoked xp.sh through
`"C:\Program Files\Git\bin\sh.exe"`, written by a `/party:setup` run under
Windows-native, while the session was WSL. Claude Code renders nothing
when a statusline command fails, so it failed invisibly, in a gitignored
file nobody reviews.

The design work that followed was real and mostly wasted. A runtime
`cmd1 || cmd2` chain looked right on a good argument — it is not
"guessing with a safety net", it is the setup-time probe moved to
run-time, which is where it belongs when the bug is that setup-time facts
go stale. Wizard killed it on a point the dialogue had missed entirely:
xp.sh's banner mode uses **exit 2 as its success signal**, so in a `||`
chain a *successful* banner fires the fallback and the deliberate exit 2
gets mangled. A chain covers the statusline and not the banner — half a
fix at full complexity, resting on an unverified per-platform assumption
about whether the harness shell-parses the command string at all.

Wizard also found a live bug nobody was looking for: `/party:config`
declines to touch an existing `statusLine`, and on a re-run the plugin's
*own previous wiring* is an existing statusLine — so the repair path
promised in its Report section is forbidden by its own pre-check.

What actually settled it was a ratio, not any of that. To display one
line of text the plugin ships a 9-rung probe ladder, an exit-0 +
non-empty-stdout + empty-stderr predicate, a settings mutation, a
per-repo script copy, and a repair path — ~70 lines of the densest
model-executed instruction in the repo. Three fix rounds have now landed
in that same block. **When repeated fixes cluster in one place, suspect
the mechanism is disproportionate to the payload rather than that you are
one fix away.** The script itself was never implicated; it ran correctly
every time it was invoked by hand.

The structural error underneath: the design **polls** a rarely-changing
state through the most fragile channel available (an external interpreter
resolved from a settings file in an environment we cannot see) on the
highest-frequency trigger available (every prompt render). XP changes a
handful of times per session, and at the exact moment it changes the
Guide is already there, already in context, already writing the file.
The trigger was free and sitting unused. Poll-to-event is the fix, and
the fragile channel disappears with it.

Corollary that made the delete easy: while the statusline is *also* the
mechanism, its silent failure is intolerable — a plugin themed on making
memory visible cannot have an invisible failure. Demote it to ornament
and the same failure becomes acceptable. That is the tell that it should
not have been load-bearing.

Two mechanism notes for the build. Count with the **Grep tool**, not
Bash — whether Claude Code's Bash tool has a POSIX shell on
Windows-native is precisely the class of thing this repo has now been
wrong about twice, and Grep is harness-provided and platform-independent.
And keep the count *derived*: XP is `^## YYYY-` headings in learnings.md
and must never be cached, because a counter drifts on hand edits, merges,
and Long Rest rewrites, and the drift would land in the one number that
gates the level-up. The celebrated level is the opposite case — not
derivable, a record of an event — and CHRONICLE.md already stores it as
`## Level N`. Derived values get recomputed; events get stored.

Process note: the reframe came from the user, not from the analysis. Four
turns of increasingly clever fixes inside the probe never questioned
whether the probe should exist, and the question "why are we keeping
xp.sh if we're removing the display" caught a real inconsistency I was
carrying. Wizard, asked to review, attacked the options as framed and
found genuine flaws in them — but also did not challenge the frame. Both
the subagent and the Guide optimised within the given box.

## 2026-07-28 — Removing a shipped feature leaves residue the orphan grep cannot see

Executing the 0.7.0 display removal turned up a class of breakage neither
the plan nor the token grep (`xp.sh|statusLine|statusline|SessionStart`)
would ever catch, because the residue contains none of those words.

**Deleting a config key silently converts it into a *fatal* one.**
`experience` was dropped from `party.json`, which made it an *unknown*
top-level key — and `/party:config` stops the run on unknown keys, by
design, because that strictness is what catches `experiance`. The same
rule then rejects the file the previous version's own setup wrote,
including this repo's. A removal is only complete when the validator is
told the removed key is **inert** rather than **wrong**; the two look
identical to a schema and opposite to a user.

**Bumping a `party@` marker ripples past the block it marks.** Prose
elsewhere that *enumerates what a version marked* goes false silently.
Setup step 5a said 0.5.0 also marked the muster and experience blocks
"which are current" — true until the bump, after which a 0.5.0-marked
experience block is exactly the outgoing legacy variant, and calling it
current tells setup to skip the migration it should offer. The shipped-
text ripple convention in CLAUDE.md should be read as covering
fingerprint *cross-references*, not just bullet bodies.

**A deleted section is still referenced in words.** `skills/setup/SKILL.md`
pointed at the deleted config section as "that skill owns the wiring" —
no grepped token in it. Deleting a numbered step also invalidates every
internal step cross-reference; one was already wrong before the edit.
After removing a section, read the referring files end to end. The grep
proves the *name* is gone, never that the *promise* is.

Method note worth keeping: fighter's build report flagged four open
items it had deliberately not acted on, and three were real — the
orphaned `Bash(sh scripts/xp.sh …)` permissions in the committed
`.claude/settings.json` were out of its brief's scope but in cleric's.
An agent naming what it did not do is what makes the next reviewer
useful; a report claiming completeness would have buried all three.

## 2026-07-28 — A detection string is a contract, and the archive hides the breach

`/party:setup` step 5b and `/party:config` both decided "is the muster
bullet already wired?" by testing the project's CLAUDE.md for the string
`party:fighter`. `memory/CLAUDE.md.template` had not written that string
since 0.4.0, when the rewrite replaced the "Summon the party" bullet
(which did name it) with the muster bullet (which namespaces cleric and
wizard, but writes the fighter as prose — "fighter builds"). The
heuristic wasn't updated to match. So for three minor versions every
correctly wired project read as unwired: re-running setup appended a
*second* copy of the muster block, and `/party:config` warned that model
overrides wouldn't be picked up on projects where they already were. The
only flow that showed the bug is the one users are told is safe to
repeat.

What kept it invisible is worth more than the fix. `git grep
party:fighter` returns hits — because `memory/legacy-blocks.md` archives
the 0.2.x and 0.3.x blocks verbatim, and those name it three times. The
repo greps clean while the shipped file is broken. An archive of old
shipped text is, to grep, indistinguishable from current shipped text,
so any question of the form "do we still ship this string" has to name
the shipped file and never the repo.

The fix class is the durable part. Keying on a different string
(`party:cleric`, which sits inside the bullet) would have been one word
and would have drifted again at the next rewording. Naming
`party:fighter` in the template costs a real migration — marker bump,
outgoing block archived, new 5a fingerprint — but is independently more
correct, since the Guide must spawn the namespaced id and the other two
members were already namespaced in that same sentence. Neither prevents
recurrence: what does is the sentinel loop now in CLAUDE.md Commands,
asserting that every string 5b tests for exists in the template. The
detection string was a contract between a skill and a shipped file, and
nothing was checking it.

One more, found while fixing: repairing the sentinel would have left the
bug's worst path open. 5a legitimately refuses to migrate in two cases —
the user declines the diff, or the block was hand-edited — and in both,
a single-string test then sends 5b on to append the duplicate anyway.
5b's presence test therefore accepts the bullet's opening phrase as well
as the sentinel. When a fix depends on a migration having run, check what
happens on every path where it deliberately doesn't.

## 2026-07-29 — The drift machinery was the product's largest surface, so we stopped copying text

Six of the repo's gotchas, three skills, an entire `memory/` directory and
every `<!-- party@X.Y.Z -->` marker existed for one reason: text copied into
a user's repo at setup time drifts from the text the plugin later ships.
Nothing in that machinery *fixed* the drift — it managed it, with migration
fingerprints, archived legacy blocks, detection sentinels, and a sentinel
loop to check the detection sentinels. The cost was not the tokens, it was
that each of those pieces could fail silently and several already had.

0.8.0 removes the cause instead: a SessionStart hook `cat`s
`hooks/instructions.md` out of the plugin and the project's own curated
experience files out of `.claude/`, into every session. Nothing is copied,
so nothing can drift; updating the plugin updates every project at once;
install scope becomes the only gate. `/party:setup`, `/party:config` and
`/party:level-up` all die with it — setup because there is nothing to write,
config because a JSON file the user edits by hand never needed a skill to
validate it, level-up because levels no longer have to be derived from a
counter that has to survive distillation.

The thing that made it possible was the inbox reframing. XP-as-entry-count
forced `learnings.md` to be append-only forever, which forced a watermark to
bound each rest, which is where the whole level arithmetic came from. Make
the log an inbox that `/party:consolidate` empties and all of it collapses:
"time to consolidate" is `inbox >= 10`, and the level is just the last
chronicle level plus one. Two numbers that had to agree became one file that
is either full or empty.

What replaces the drift risk is a hard dependency: no POSIX shell, no
instructions at all. That is a worse failure mode than drift (silent and
total, versus stale) and it is unverified on Windows-native — which is why
the README now names it as the thing to report.

## 2026-07-29 — Spiking the hook rails first answered five questions the docs disagreed on

Every design fork in the re-architecture rested on plugin-hook behavior the
documentation is contradictory about, so nothing shipped until a scratch
plugin under `/tmp` had been driven headless with `claude --plugin-dir`.
Five runs, five answers, all cheap: `--plugin-dir` does load a plugin's
hooks; `hooks/hooks.json` auto-registers with no `hooks` key in
`plugin.json`; plain stdout is injected verbatim, so the planned fallback to
a `python3 -c json.dumps` one-liner was never needed — and python3 therefore
never became a runtime requirement of the plugin; a 21.9k-char payload
arrived intact head *and* tail, so one entry per file was unnecessary; and
the `matcher` field is honored, with alternation working (`startup|compact`
fired, `clear|compact|resume` did not).

The last one is the trap worth keeping: a matcher that doesn't match fails
by silently never firing, and the omitted-matcher case can only be *proved*
for the source you can reach headless. `startup` is provable; `compact` and
`clear` are interactive-only, so "fires on all sources" remains an
assumption the shipped file rests on, not a tested fact.

The generalisable half: the spike cost five tiny headless prompts and
retired two variants of the design before a line of shipped text existed.
The alternative — build on the docs, discover at dogfood time — is how the
xp.sh probe consumed three releases.

One finding landed after the shipped text was written, and it is the
sharpest of them: hook-injected context does **not** reach subagents. A
spawned Explore agent, asked whether its own context contained the sentinel
word or the repo's gotchas, answered "NO, NO." CLAUDE.md and its
`@`-imports do propagate — that is how party members have been receiving the
curated experience files all along — so 0.8.0 quietly moves the experience
files from "auto-loaded for everyone" to "auto-loaded for the Guide, and the
agents must read them." The agents' own instructions already tell them to
consult the project's experience files, so this degrades rather than breaks,
but it is a real cost of the re-architecture and it was invisible until
tested. The general shape: when you move where an instruction is *served
from*, re-ask who was receiving it before.

## 2026-07-29 — Nothing in the system watches the size of the files the system loads every session

Asked whether the muster instructions were in context, the Guide confirmed
they were, noticed the injected experience files came to 24.8KB against a
~4k-character budget, and suggested `/party:long-rest`. Wrong lever, and
wrong in a way that is built into the design rather than a slip of
attention.

The Long Rest is triggered by *inbox* volume: count `^## [0-9]{4}-` over
`learnings.md`, suggest at 10+. The ceremony then distills those entries
*into* `architecture.md` / `gotchas.md` / `decisions.md`. Its prune step
removes what has stopped being true — verifiably-fixed gotchas, stale
tombstones — which is correctness hygiene, not size hygiene. So the net
effect of a rest on the curated tier is to make it **bigger**. Reaching for
it to shrink that tier is reaching for the thing that grows it.

The measurements that made it visible: `decisions.md` 17.4KB against a
contract of "~2 lines each"; `gotchas.md` 6.0KB against "1–2 lines each";
`architecture.md` 2.2KB, the only one living inside its budget. Every one of
those loads on every session of every project the plugin is installed for —
the expensive tier, by this repo's own architecture note. The budget is
written down in three places and enforced in none.

The generalisable half, and the reason this is worth a curated line rather
than just a fix: **a budget with no meter is a wish.** We wrote "~4k
characters" into CLAUDE.md, "keep them small" into the hook payload, and
per-file length contracts into the skill — then built the one ceremony that
touches those files around a counter pointed at a *different* file. The
quantity that governs the cost is the only quantity nothing counts.

Two candidate fixes, unresolved: give the Long Rest a size check over the
curated tier (report the byte counts, prune-to-budget when over), or accept
that distillation is inherently additive and make budget enforcement a
separate, explicitly-invoked pass. The first keeps one ceremony; the second
keeps the ceremony honest about what it is for.

## 2026-07-29 — Decision arguments, archived at compaction

`.claude/decisions.md` was compacted on 2026-07-29 from 12,380 chars to
its claim tier: each live entry now carries only its date, its choice,
the rejected alternative, one why-clause and any tombstone. The full
argument every entry was carrying is preserved verbatim below — all 23
entries as the file stood immediately before that compaction, oldest
first, so that state is recoverable from this section alone. (That
baseline is the post-Level-3 working tree, not `HEAD`: the Level 3 rest
had already pruned three entries and rewritten several, and those edits
were still uncommitted. For anything older, read git history.) A `see
learnings YYYY-MM-DD` pointer in `decisions.md` resolves here as well as
to the dated learnings entries above.

### 2026-07-25 — Memory is rebranded "experience" (decision argument, verbatim)

2026-07-25 — Memory is rebranded "experience" — theme must label real
mechanics, never replace them, because the files are literally the
project's memory. *Amended 2026-07-28:* the XP number and its statusline
/banner display are gone; progress is the inbox count and the chronicled
level. See learnings 2026-07-28.

### 2026-07-25 — Main-session role renamed "the Guide" (decision argument, verbatim)

2026-07-25 — Main-session role renamed "the Guide"; scrub the tabletop
brand name and its trademarked game-master title from all shipped copy —
those two terms are protected, generic archetypes (fighter/cleric/wizard/
party/session zero) are not, and "Guide" matches the teaching role for
the non-engineer audience. Model overrides live in `.claude/party.json`;
defaults unchanged (fighter=Opus, cleric/wizard=Fable).

### 2026-07-25 — The party musters only on explicit command (decision argument, verbatim)

2026-07-25 — Party musters only on explicit command, approved plan, or a
Guide *suggestion* (reverses the auto-summon rule) — the ceremony tax is
the single most documented failure mode of workflow plugins (Superpowers,
Spec Kit); the human decides when the party rides.

### 2026-07-25 — Recognition is bolted to the distillation chore (decision argument, verbatim)

2026-07-25 — Recognition is bolted to the distillation chore nobody
otherwise does, so a leveled party is literally a better-informed one —
recognition alone is the sub-10-star-graveyard pattern. Token cost is
real, so the rest is user-invoked only, never automatic. *Amended
2026-07-29:* the trigger is `/party:long-rest`, and a level is one per
rest rather than derived from an XP threshold.

### 2026-07-25 — Model overrides apply at spawn time (decision argument, verbatim)

2026-07-25 — Model overrides apply at spawn time (Agent tool `model`
param, wired into the muster bullet) instead of generated
`.claude/agents/` override files — live test proved project agent files
do NOT shadow `party:<name>` (they coexist; namespaced spawns get the
plugin copy), so generation could never work; the param outranks
frontmatter and needs no files that rot.

### 2026-07-25 — The fighter to cleric handoff is unconditional (decision argument, verbatim)

2026-07-25 — The fighter → cleric handoff is unconditional, never
gated on "the build looks clean" (and the same holds for Guide solo
builds) — dogfooded: a feature that passed a headless pixel smoke test
with zero JS errors still had 4 real bugs cleric found and fixed, two
visible in the first minute of play. Automated UI checks measure
rendering, not behavior, so "it looks verified" is precisely the
condition an independent reviewer exists for.

### 2026-07-26 — Plan-mode plans muster the party by default (decision argument, verbatim)

2026-07-26 — Plan-mode plans muster by default (mandatory Execution
section; table only on user request; no Guide discretion) — plan silence
previously meant solo execution and the muster silently didn't fire; the
plan text is what the executor reliably follows, so the instruction
rides inside the plan; plan-mode entry is the party-sized signal,
preserving the ceremony-tax decision (approval remains the consent
gate).

### 2026-07-26 — Install scope stays the installer's choice (decision argument, verbatim)

2026-07-26 — Install scope stays the installer's choice: user-level for
solo/trial, project-level (checked-in
`extraKnownMarketplaces`/`enabledPlugins`) for team repos. Forcing
project-level would add reinstall friction with no benefit. *Amended
2026-07-29:* scope is now the **only** gate — there is no per-project
opt-in step, so a user-level install is live in every repo.

### 2026-07-26 — Session Zero stays a single SKILL.md (decision argument, verbatim)

2026-07-26 — Session Zero stays a single SKILL.md (no `references/`
progressive disclosure, no separate explain skill) and teaches its
visual idioms via ~5-line skeletons rather than a worked example
dialogue — there is no bulky lookup material to defer (the tech
explanations are per-question research, not a shippable catalogue), so
splitting would be the premature abstraction the skill now argues
against; and models imitate examples strongly, so a full transcript
would leak its topic and length into unrelated Session Zeros while a
skeleton leaks only shape.

### 2026-07-26 — Session Zero is exploration/chat mode with no exit condition (decision argument, verbatim)

2026-07-26 — Session Zero is exploration/chat mode with no exit
condition but the user's word (plan mode never Guide-initiated), and
explainability is calibrated by stakes × reversibility rather than
always-loud — the old "then hand off to plan mode" clause was what made
the Guide race to converge; uncalibrated depth is its own failure
(burying a naming question stops the user asking a second one).

### 2026-07-26 — `party.json`'s `models` takes stable tiers, never model IDs (decision argument, verbatim)

2026-07-26 — `party.json`'s `models` takes stable tiers
(opus/sonnet/haiku/fable), never model IDs, so new model releases never
require a config edit; absent or empty means "member's default", so no
snapshotted pin can outlive a future default change.

### 2026-07-26 — session-zero's `description` is a router, not a summary (decision argument, verbatim)

2026-07-26 — session-zero's `description` is a router, not a summary: cut
to 689 chars (from 1083) by dropping every behavior clause and keeping
only routing — every-turn re-evaluation, mid-conversation drift, trigger
phrases, the fact-vs-decision tie-break. Not cut to sibling length
(~250): the other skills are `disable-model-invocation: true` and route
nothing, so symmetry with them is a false target.

### 2026-07-26 — Cleric's repair scope is the change and its blast radius (decision argument, verbatim)

2026-07-26 — Cleric's repair scope is the change and its blast radius,
with `NEEDS_REBUILD:` as a high bar that does not excuse it from fixing
what is separably fixable — an unbounded "fix everything you find" lets
a reviewer redo working code to taste and triple the user's diff, while
an easy rebuild verdict would quietly turn cleric back into the
findings-report agent its file says it isn't. Defect vs. preference is
the gate, never size: "a defect is a defect however large, and 'large' is
never why you leave one."

### 2026-07-26 — The party reaches the experience system through `LEARNED:` lines (decision argument, verbatim)

2026-07-26 — The party reaches the experience system through a `LEARNED:`
line in each member's report, not by writing the files itself — a
subagent's context dies with its turn, so the final message is the only
carrier. Keeping the Guide as sole writer keeps the inbox single-voiced
and puts every candidate in front of the user; "usually none" and "not
routine work" are the governors against three reports a session padding
the log.

### 2026-07-26 — Wizard stays read-only with no `Bash` (decision argument, verbatim)

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

### 2026-07-26 — The manifest check swaps `jq` for `python3 -m json.tool` (decision argument, verbatim)

2026-07-26 — The manifest check swaps `jq` for `python3 -m json.tool`,
and the frontmatter check keeps PyYAML with an install note — `jq` is
preinstalled on no mainstream platform, while python3 was already a hard
dependency of the frontmatter check. Rejected a stdlib-only validator:
replacing a real YAML parser with regex to dodge one `pip install` trades
a stronger check for a new shipped artifact.

### 2026-07-27 — Dogfooding runs the source via `claude --plugin-dir .` (decision argument, verbatim)

2026-07-27 — Dogfooding runs the source via `claude --plugin-dir .`; the
installed `party` plugin exists only to test the *released* install path
(push → marketplace update → plugin update → restart). Sitting in the
source repo is not running it: install snapshots the marketplace clone
into a version-keyed cache and `${CLAUDE_PLUGIN_ROOT}` points at the
oldest copy. Auto-update is off by default for third-party marketplaces,
so README's Install says to enable it. See learnings 2026-07-27.

### 2026-07-27 — The `<!-- party@X.Y.Z -->` marker scheme is dead (decision argument, verbatim)

2026-07-27 — *Superseded 2026-07-29:* `<!-- party@X.Y.Z -->` markers
versioned block *text* and were legended rather than restamped at
release. The whole marker scheme died with the copied-text machinery.

### 2026-07-27 — Session Zero becomes a phase work passes through by default (decision argument, verbatim)

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

### 2026-07-27 — Decisions entries get a length budget (decision argument, verbatim)

2026-07-27 — Decisions entries get a 3–5 line budget: choice, rejected
alternative, one-clause why, plus a pointer to the learnings entry
holding the full argument — over pruning old decisions at the Long Rest
(smaller edit, but leaves the write-time habit intact) or leaving it.
Decisions was the one curated file with an inflow and no outflow: the
Long Rest's prune gate tests *truth*, and a decision never stops being
true, only stops being load-bearing. See learnings 2026-07-27.

### 2026-07-28 — The XP statusline and SessionStart banner are dropped (decision argument, verbatim)

2026-07-28 — The XP statusline and SessionStart banner are dropped
outright; the level-up nudge moves to the moment the Guide appends a
learning, counting with the Grep tool (no shell, no stored counter).
Rejected patching the probe (runtime `||` chain, slot-2 discovery,
re-probe on `/party:config`) and shipping `xp.sh` unwired for manual
setup — ~70 lines of the repo's most bug-prone shipped instruction
existed to render one line, and every fix round has landed in it. See
learnings 2026-07-28.

### 2026-07-29 — The hook ships as one SessionStart block of plain `cat`s (decision argument, verbatim)

2026-07-29 — The hook ships as one SessionStart block, two one-line `cat`
commands, plain stdout, matcher omitted — not JSON `additionalContext`,
not one entry per file, not an enumerated matcher. The spike proved
stdout injects verbatim and a 21.9k payload survives whole, so both
elaborations bought nothing, and plain `cat` keeps python3 out of the
plugin's runtime requirements. See learnings 2026-07-29.

### 2026-07-29 — The plugin serves its instructions from a SessionStart hook (decision argument, verbatim)

2026-07-29 — The plugin serves its instructions from a SessionStart hook
and copies nothing into a user's repo; `/party:setup`, `/party:config`
and `/party:level-up` are deleted, `learnings.md` becomes an inbox that
`/party:long-rest` empties, and levels are one per rest. Rejected
keeping the template plus better migration tooling — the drift it
manages is created by the copying, and every piece of the machinery that
manages it can fail silently. Cost accepted: the hook is now a hard
dependency, and its Windows-native path is unverified. See learnings
2026-07-29.

## 2026-07-30 — SessionStart relocation cap (gotcha moved verbatim at Level 4 compaction)

- SessionStart stdout is injected verbatim only up to **10,000 characters,
  inclusive, PER HOOK ENTRY**; at 10,001 the entry is replaced by
  `Output too large … saved to …/tool-results/hook-*.txt` and a ~2k preview,
  while the hook still exits 0 — so it fails silently and every cheap check
  passes. Characters, not bytes or tokens: size checks here use `wc -m`,
  never `wc -c`. Bisected 2026-07-30; this replaces an earlier "not
  truncated at ~22k chars" entry, which aimed at a clipping ceiling an order
  of magnitude above the real relocation threshold.

## 2026-07-29 — Shipped instructions must not name a specific built-in tool

`hooks/instructions.md` tells the session to count the learnings inbox "with
the Grep tool in count mode". That instruction is not always executable: the
tool roster served to a session is decided per-install by server-side rollout
bucketing, not by the user's config, and Grep can simply be absent.

Confirmed on this machine (WSL, 2.1.220) vs the same account's Windows install
(also 2.1.220): Grep is absent from the default roster here but present there.
Ruled out — settings/permission denies (none on either side), version skew
(identical), effort level (absent at low/medium/high), and a broken search
backend (ripgrep is embedded in the binary, and `claude --tools Grep,Read`
loads Grep and runs it successfully). The two installs cache 442 GrowthBook
feature flags each and exactly two differ, `tengu_umber_kestrel` being ON for
Windows and OFF for WSL; bucketing hashes on machineID/userID, which differ
per install even for one account. Not causally confirmed — flipping the cached
flag was blocked by the permission classifier.

The rule this implies for anything we ship: name the *outcome*, not the tool.
"Count the entries without reading the file" survives a roster change; "use
the Grep tool" does not. Same class of failure as assuming `jq` exists.

The blast radius is narrower than it first looked, though: only main-session
*prose* is exposed. An agent's frontmatter `tools:` list is an explicit
naming, and explicit naming resurrects a tool the default roster pruned —
verified twice, by `claude --tools Grep,Read` on the CLI and by spawning
`party:wizard` (frontmatter `tools: Read, Grep, Glob`) in a session with no
Grep, where it reported all three and ran a Grep count successfully. So
wizard needs no defensive change, and its read-only guarantee stands. The
asymmetry to remember: a *declared* tool list is honoured; an *instruction*
to use a tool is only a wish.

## 2026-07-29 — A text budget only holds where the argument is out of context

`decisions.md` reached 12.4k against a shipped "~2 lines per entry" rule that
every one of its 23 entries broke. The rule was not ignored — it was applied
at the only moment it cannot work. At write time the author still holds the
full argument, and every clause of it feels load-bearing; compression is only
possible for someone who no longer has it.

This falsifies the 2026-07-27 decision, which diagnosed `decisions.md` as
"inflow with an outflow gated on stopped-being-true, which a decision never
does" and concluded the bound "has to be a budget at write time, not a test
at prune time." Right about the diagnosis, wrong about the remedy — and the
evidence was immediate: entries written the same day, in the file that
defines the rule, ran 15 and 30 lines.

The general shape: a constraint enforced by the party who is motivated to
break it is a wish. Move it to a moment with different incentives. Here that
is `/party:long-rest`, which now compacts as well as distils — and *measures*
the tier, since the ~4k budget had existed for weeks with nothing weighing
it.

Second-order: the fix is not deletion. Only 5 of 23 entries carried a
`see learnings` pointer, so compressing in place would have destroyed 18
arguments outright. Move-then-shorten, into the archive that already existed.
The drain we needed had already shipped for a different purpose.

## 2026-07-29 — Ask which baseline a helper diffed before believing its diff

A read-only verification agent reported, with specificity and confidence,
that ~9 archived entries were not verbatim and the original held 25 entries
rather than 23. Both false. It had diffed against `HEAD`, but the file was
already modified-uncommitted at session start — the entries it flagged as
"missing" were exactly the ones the previous Long Rest had pruned, which
`CHRONICLE.md` records.

The failure is invisible at the finding level: a wrong-baseline diff produces
findings shaped exactly like real ones, and "fixing" them would have
*reverted* correct work. When a helper's claim is a diff, the first question
is never "is this true" but "against what". A dirty working tree makes `HEAD`
the wrong answer by default, and this repo's `.claude/` files are edited by
sessions, so they are dirty more often than not.

Corollary that made the audit possible: a pre-edit baseline of an uncommitted
file is recoverable from the session transcript's `toolUseResult` entries in
`~/.claude/projects/<proj>/<session>.jsonl`, even when git holds no copy. For
lossy compaction steps that is the only reliable audit path — file-history
directories only cover other sessions.

## 2026-07-29 — Renumbering a ceremony breaks the prose the list sits inside

Inserting a step into `/party:long-rest`'s numbered ceremony was mechanically
clean — renumber 4/5/6 to 5/6/7, update two cross-references. What broke was
prose stated elsewhere in the file: "the archive move happens last" and
"every earlier step is idempotent by design" were both invariants the new
step violated, and a pronoun in the new branch had lost its antecedent.

In a repo where prose *is* the executable, a numbered list is not a data
structure — it is a set of promises made about itself in surrounding text.
After renumbering, re-read the whole file for the claims the list is embedded
in, not just the references that name a number. Grep finds `step 4`; it does
not find "happens last".

## 2026-07-30 — Large hook output is relocated to disk, not injected

Observed directly at this session's start: the SessionStart hook's second
`cat` (`architecture.md gotchas.md decisions.md`, 16,912 B) did not reach
context. It was replaced by `Output too large (16.3KB). Full output saved
to: …/tool-results/hook-<uuid>-stdout.txt` plus the first ~2,048 B inline —
so the session had four bullets of `architecture.md` and none of
`gotchas.md` or `decisions.md`. The first `cat` (`instructions.md`,
4,048 B) arrived verbatim, tail byte-identical to the file.

The mechanism is not hook-specific: the spill path is the generic
`tool-results/` directory, so hook stdout inherits the ordinary per-result
inline cap. The cap is **per result, not per session** — which means the
two-`cat` split chosen on 2026-07-29 for unrelated reasons is load-bearing.
One combined `cat` would put the 21 KB total over the cap and take
`instructions.md` — the party protocol itself — to disk with it, silently
disabling the plugin. Any future consolidation of those `cat`s reintroduces
that failure.

`gotchas.md` recorded the opposite on 2026-07-29: "injected verbatim … not
truncated at ~22k chars (tested)". Growth is not the explanation — the tier
was *larger* that day (25,576 B) than now (16,913 B). The test was aimed at
a hypothesised ~22k clipping ceiling, and the real behaviour is an
order of magnitude lower and works by relocation, so it was outside the
hypothesis space.

Two generalisations, both about the shape of the miss rather than the
number:

Relocation defeats every cheap check, because nothing fails. The hook exits
0, the text is retrievable on disk, and the content still exists — so
"did the hook fire?", "is the file there?" and the `lantern is lit` sentinel
all pass. Only absence *in the model's context* distinguishes the two
states, and no gate in this repo tested for that. Worse, every existing
gate probes `instructions.md`, the one file small enough to fit; the file
that doesn't fit had no gate at all. When a limit degrades by moving data
rather than erroring, the assertion has to name the consumer ("the model
can quote line N"), never the producer.

A budget expressed as one number hid two different limits. `~4k` was a
voluntary cost budget on shipped text with no enforcement behind it, while
the per-project tier — assumed unbounded — is the side with the real
ceiling. `architecture.md` had already blurred the two by attaching the 4k
to "that tier", and `/party:long-rest`'s 50k gauge calls a size "fine" that
is several times past the point where the files stop being injected. A
gauge inherits authority from being a number; it earns none of it unless
its thresholds were measured against the mechanism they claim to bound.

## 2026-07-30 — A read trigger is a capability floor, not a prose problem

Replacing hook injection with per-file read triggers made delivery
conditional on compliance for the first time — injection had no compliance
step at all. Measured on the fixture built for the change: the `gotchas.md`
trigger fired 3/3 on the default model and **0/4 on haiku**.

The useful part is the diagnosis. Asked with tools disallowed which file it
must read before its first change, haiku names `.claude/gotchas.md`
correctly, then edits without reading it. So "the rule didn't fire" splits
three ways — *didn't arrive*, *disputed the rule*, *disputed the case* — and
only the middle one is a wording problem. This was the third. Both documented
remedies were applied and both were null: strengthening the trigger to an
explicit precondition ("one-character changes included … 'too small to need
it' is the case it exists for"), and hoisting the whole section above the
muster protocol. That is this repo's own "every more-text fix feeds the step
that was already working", observed live rather than reasoned about.

Establish which of the three failures you have before writing a single word
of remedy, because two of the three cannot be written around. Shipped anyway:
the alternative was silent non-delivery for *every* model, and the default
party is opus/fable. But the trade is now explicit — the injected design had
a truncation cliff, the referenced design has a compliance floor, and the
floor is the one that varies per session without announcing itself.

## 2026-07-30 — A behavioral fixture can leak its own answer

The first attempt at the trigger test asked the model to edit a
`config.txt` whose *other* lines already carried the `-ZORB` suffix the
hidden rule in `gotchas.md` demanded. A pass proved nothing: the suffix was
inferable from the file being edited, so pattern-matching and rule-following
were indistinguishable. Discarded and rebuilt with a side-effect reachable
only through the file under test.

Same failure class as this repo's `lantern` sentinel, which passed for days
while the experience tier silently wasn't loading — it only ever exercised
the one file small enough to fit. A test of whether something was *consulted*
must make its expected evidence unobtainable by any other route, and the way
to check that is to ask what a model that never opened the file could still
produce.


## 2026-07-31 — A release marker with no distribution role has no feedback loop

0.7.0 and 0.8.0 both shipped untagged. Tags stop at v0.6.4 while
`plugin.json` had been bumped twice in plain commits, and the drift was
visible in the subject lines: 0.6.x read "Release X.Y.Z", 0.7.0/0.8.0 just
"X.Y.Z" — the word and the tagging step fell off together.

Nothing broke, and that is the point. `marketplace.json` sets
`"source": "./"` with no version pin, so `/plugin install` clones `main`
and keys its cache off `plugin.json`'s `version` field. Tags are not on the
distribution path at all: merging to `main` *is* the release, and the tag is
a pure marker. A step whose omission produces no symptom will be omitted,
and no amount of intending to remember it changes that — the only
reliable fix is to attach it to something that does fail loudly, or to
check it at the one moment someone is already looking (the version bump).

Caught only because the user asked "did we do a release" — an audit
question, not a build one. Worth asking directly at each bump instead:
`git tag -l` against `plugin.json`'s version is a two-second check.

## 2026-08-01 — A skill can flip a switch but cannot be one

Session-zero argument for the foreign-CLI ("hireling") design, recorded
before any build. The user's ask — swap a party member for another vendor's
coding CLI (codex, kimi, …) via a skill — hides a timing constraint:
`/party:long-rest`-style skills work because the user invokes them at the
moment the work happens, but the muster happens in a later turn or session,
when the skill body is inert. So the skill can only *write state*
(`party.json`), and something in context at muster time — the muster
sentence, or an agent body — must read it. The skill is a setup wizard whose
real job is the precondition check: verify the binary, probe its
non-interactive/write flags, smoke-test end-to-end at hire time, so failure
surfaces before a quest, not mid-build.

Second shape: wrapping any foreign CLI in any role is one job (read
experience files → build prompt → run binary in background past the 10-min
Bash cap → translate output into that role's handoff contract), so it is one
generic adapter agent parameterized by role at spawn — not an agent per tool
or per role. The role contracts are the party's interfaces; if the hireling
honors them, cleric never knows the hands changed. Per-CLI flag knowledge is
probed at hire time and stored in config, never shipped — a shipped flag
table is xp.sh in prose. Disclosure, not judgment: hiring wizard converts a
structural read-only guarantee (tool grant) into a sandbox flag, said once
at hire time.

## 2026-08-01 — A shipped prohibition gets lawyered at its adjective

Cleric's live find while running the hireling build's behavioral check: with
fighter hired to a broken command, the muster→hireling wire worked (hireling
spawned, refused, reported exit 127), but the Guide then spawned the native
fighter and built anyway — overriding the user's standing config. The first
fix, "never a *silent* fallback", failed the second headless run in the most
instructive way possible: the Guide fell back *loudly*. The prohibition was
obeyed at its adjective and violated at its verb. The wording that went
green bans the act and names whose call it is: "A hire whose command fails
ends the quest — report it and stop; falling back to the native member is
the user's call to make, never yours." Rule for shipped prose: a behavioral
ban must land on the act itself and assign the decision to a person; any
qualifier ("silent", "unnecessary", "routine") becomes the loophole.

## 2026-08-01 — disable-model-invocation skills are headlessly testable

They never appear in the model's skill list (known, correct), which had left
"absent from the list" as their only smoke signal. Fighter found the real
check: `claude --plugin-dir . -p '/party:hire'` invokes the skill and runs
its actual body headlessly — used this release to verify hire's status path
end to end, and it generalizes to long-rest. The list-absence gotcha and the
test technique are two halves: you can't ask *about* the skill, but you can
still *run* it.

## 2026-08-02 — A model tier's public name is not its flag value

First live hire (fighter → codex): the user asked to pin "luna", which is a
real OpenAI tier — and not a valid model string. The API wanted
`gpt-5.6-luna`, and nothing local could say so: codex has no non-interactive
model list, its own error is just `model_not_found`, and the mapping had to
be confirmed on the web (the default smoke test's banner gave the pattern,
`gpt-5.6-sol`). Two things the skill's design got right by ordering alone:
the pin got its own smoke test — the first test only proves the *default*
model, and adding `-m` changes the command under test — and testing before
writing meant the bad name cost one throwaway call instead of a broken
muster in a later session. Worth considering for the skill text: the pin
step could say plainly that a user-supplied model name is a claim to verify
(tier names and API strings diverge), and that the proven banner is the
best local evidence of the naming pattern.

## 2026-08-02 — User feedback: guide hire's choice points with question boxes

Direct feedback after the first live hire: the flow leaned on the user
typing free text where structured choices would have guided better. The
evidence is in the transcript — the free-text "which model?" produced the
unpinnable "luna", while the question boxes (pin/confirm steps) worked, and
one even carried a mid-flow correction through its "Other" field ("confirm
on internet the actual model names"). The skill's prose asks open questions
("ask the user which model to pin"); it could instead direct the executor to
offer concrete options where it has them — the smoke-tested model, don't
pin, other — with free text as the escape hatch, not the default. Same
no-ranking rule as ever: boxes list, never recommend a CLI or model.
