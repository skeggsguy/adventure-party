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
