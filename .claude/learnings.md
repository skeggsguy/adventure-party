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

## 2026-07-25 — Skill triggers must be continuous, not discrete

Session Zero failed to fire during a session that was squarely its use case:
a conversation that opened as a factual lookup ("does Claude read
AGENTS.md?") and drifted, turn by turn, into an architectural comparison
and then a design proposal for this repo's own memory shell. The main
session answered every turn in lookup mode and never re-classified.

The wrong assumption was that a trigger describing a *moment* ("when
scoping new work", "BEFORE entering plan mode") would catch a conversation
that *becomes* scoping — which is the more common shape, since people
arrive with a small question and talk their way into a design decision.

The skill's Method step 1 is "classify the turn", but that instruction
lives inside the skill, so it only runs once the skill is already loaded.
The classification that matters happens earlier, in the main session,
where the only guidance is the frontmatter description. Trigger prose has
to do its work from outside the skill.

Fix: reworded the description to demand re-evaluation EVERY turn, to name
conversational drift explicitly, and to state the negative trigger (a
factual lookup is not Session Zero; the follow-up asking what to DO about
the answer is). The boundary carries more signal than either side alone.

Generalizes beyond this skill: any skill whose activation depends on the
model classifying a turn needs a continuous trigger and an explicit
not-this-case, or it will miss the drift path.

## 2026-07-25 — A plugin can't seed a user's `.claude/`, so a skill does it

The obvious read of "package this as a plugin" was: move `agents/`,
`skills/`, and `memory/` under a manifest and you're done. That is wrong
for a third of the product. Plugins deliver *their own* files to be loaded
— agents, skills, commands, hooks. They have no mechanism to write into
the installing project's `.claude/`, and the memory system is precisely a
set of files that must live in the user's repo (they accumulate that
repo's notes, and `CLAUDE.md` imports them by path).

The way around it is `${CLAUDE_PLUGIN_ROOT}`, which resolves anywhere the
placeholder appears in skill and agent content. So the templates stay in
the plugin at `memory/`, and a user-invoked skill (`/party:setup`) reads
them through that variable and copies them into the target repo. The skill
carries `disable-model-invocation: true` — an installer that writes files
must never fire on the model's own initiative.

Second trap found on the way: project-level `.claude/agents/` **overrides**
same-named plugin agents, silently. This repo's dogfood copies would have
kept winning over the plugin, so every edit would have appeared to work
while actually testing the stale mirror. Deleting `.claude/agents/` and
`.claude/skills/` isn't cleanup, it's a correctness requirement — and it
also retires the hand-mirroring "dogfood rule" in favour of
`claude --plugin-dir .` plus `/reload-plugins`.

That dev loop has its own silent failure: launched without
`--plugin-dir .`, there is no party and no error message. `/context` is
the only tell.

## 2026-07-25 — `source: "./"` ties the marketplace to the `owner/repo` add form

Found while reviewing the repackaging, not while building it. Making the
repo root the plugin root means marketplace.json points at the plugin with
a relative `source: "./"` — elegant, and it works for both documented add
paths we care about (`owner/repo` and a local dir), because both give
Claude Code the whole repo to resolve the path against.

It breaks for a third path: adding a marketplace by direct URL to
marketplace.json fetches only that one file, so there is no repo for `./`
to mean anything. The failure lands at install time, not add time, which
makes it look like a broken plugin rather than a wrong invocation. Nothing
in the manifest can guard against it — the only fix is documentation
discipline: the `owner/repo` form is the sole install path we publish.

## 2026-07-25 — The wall the party was designed around doesn't exist

The framework's founding premise — "Claude Code subagents can't spawn each
other, nesting is one level deep" — was stated flatly in README.md and is
the entire reason the `NEEDS_WIZARD:` relay exists. It's false.

Found by accident, not by reading docs: a `party:cleric` run (session
`ef890073`) made a real `Agent` tool call spawning `claude-code-guide`,
which ran to completion. Confirmed in the transcript — the call in
`~/.claude/projects/…/subagents/agent-a6d2e315a6d337859.jsonl` has no
error result, and the child has its own transcript
(`agent-a611eabda329a5184.jsonl`). Cleric had quietly routed around the
protocol its own CLAUDE.md pins, and nothing flagged it.

The enabling detail: neither `fighter.md` nor `cleric.md` declared `tools`
or `disallowedTools`, so both inherit `Agent` whenever nesting is
permitted. The lesson that generalizes — **a capability an agent should
not have must be removed in frontmatter, not forbidden in prose.** Body
text is a suggestion; the toolset is the enforcement. Wizard was already
safe by accident (its `tools:` allowlist excludes `Agent`); it now says so
explicitly with `disallowedTools: Agent`.

Second surprise, still unresolved: the docs say nesting is default-off
outside Claude Code 2.1.172–2.1.216, yet it fired on 2.1.220 with
`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` absent from user settings, project
settings, `.claude.json`, managed settings, and the session env. Rather
than reverse-engineer which default is really in force, the plan sets the
value explicitly — deterministic under either reading. Don't build on the
accident.

The design fork it opened: given nesting, how much? Rejected parallel
*writers*. `isolation: 'worktree'` only auto-cleans worktrees that were
left *unchanged*, so N parallel builders leave N live trees needing manual
merge and conflict resolution, plus a comprehend pass over code the
fighter didn't write — at which point the build report stops being a
first-hand account and becomes a summary of N summaries. That's precisely
the single-context self-review failure the party exists to prevent, just
moved down a layer. So: parallelism on the read-only side only (recon
before, verification after), every write owned by the agent that reports
on it. Depth capped at 2 because bounded and predictable beats maximally
flexible, and because a layer-2 wizard couldn't spawn anyway.

And the relay survives as a one-line fallback rather than being deleted.
The plugin ships to installs we don't control — nesting off, older Claude
Code, a user who never ran `/party:setup`. Removing the degradation path
would have traded a working-everywhere framework for a slightly tidier
one.
