# CLAUDE.md

Adventuring Party — a shareable agent-party + project-memory framework for
Claude Code (see README.md for the full pitch). The product is markdown:
agent definitions and memory-file templates. This repo also dogfoods its
own framework while developing it.

## Layout

- agents/ — THE PRODUCT: fighter, cleric, wizard agent definitions
- memory/ — THE PRODUCT: memory-system shell (architecture/gotchas/
  decisions/learnings templates + CLAUDE.md.template)
- skills/ — THE PRODUCT: session-zero (quest-shaping dialogue skill)
- .claude/ — live install of the product, used to develop this repo itself

## Dogfood rule

`agents/`, `memory/`, and `skills/` are the shareable artifact; `.claude/`
is a live install of them. Any change to a file in `agents/` or `skills/`
MUST be mirrored to its copy under `.claude/` (and vice versa) in the same
commit — check with `diff -r agents .claude/agents` and
`diff -r skills .claude/skills`. The live memory files in `.claude/`
deliberately DIVERGE from the `memory/` shells: the shells stay clean and
empty of this repo's content; the live copies accumulate this repo's real
notes.

## Conventions

- Keep agent bodies project-agnostic: discovery instructions ("the
  project's test suite", "wherever its CLAUDE.md records pins"), never
  references to any specific repo, tool, or path outside this one.
- Agent party (`.claude/agents/`): `fighter` (Opus high) is the default
  builder for substantial implementation tasks — small fixes stay in the
  main session. When fighter finishes, ALWAYS spawn `cleric` (Fable high)
  with fighter's build report to review, fix, and verify. `wizard`
  (read-only, Fable xhigh) handles deep review, hard debugging, and
  approach calls. Subagents can't call each other; the main session is
  the relay: an agent ending its turn with a `NEEDS_WIZARD:` block gets
  that question packaged off to wizard, then resumed via SendMessage.
- Session Zero (`.claude/skills/session-zero`): invoke when scoping new
  work or weighing approaches, BEFORE plan mode — collaborative
  quest-shaping dialogue (options + recommendation, plain-language
  trade-offs, the user makes the calls).

## Project memory

@.claude/architecture.md
@.claude/gotchas.md
@.claude/decisions.md

Curated files above are auto-loaded every session — keep them small; remove
stale entries. Append-only log: .claude/learnings.md (NOT imported — read it
when context suggests a past learning is relevant; distill durable items
into the curated files periodically).

When a session surfaces something non-obvious — a trap hit and diagnosed, a
wrong assumption corrected, a design insight, user feedback on approach —
append it to .claude/learnings.md (dated, append-only) without being asked.
New gotchas also get a 1–2 line entry in gotchas.md. Routine work is git
history, not a learning — don't log it.
