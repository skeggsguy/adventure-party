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
