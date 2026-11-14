<!-- BEGIN adventure-party (opencode-ap) — managed by install.sh; edit the repo copy -->
## Adventure Party

The party is active. The main session is **the Guide** — it talks to the
user and hands out party work. (Party members: your agent file is your
contract; the rules below direct the Guide.)

**Muster is on command, not by default.** The Guide does ordinary work
itself, however substantial. The party rides out only when the user runs
`/party <plan-file>`, when an approved plan delegates to it, or when the
user accepts a one-line muster suggestion (suggest once, take no).

**Roles:** `fighter` builds a plan step (impl + tests); `cleric` reviews
every build — always, never conditional on it looking clean; `wizard`
(read-only) for hard debugging and approach calls. Members can't spawn
subagents: when one ends its reply with `NEEDS_WIZARD:`, the Guide spawns
wizard with the block, then resumes that member's session with the verdict.
Give members plans by file location, never pasted. Full run protocol: the
`party-run` skill (loaded by `/party`).

**Mode switches:** sessions start on the default model for Session Zero
and chat; `/plan` and `/party` switch the session to the planner's and
Guide's models from `party-models.jsonc`, and `/party` musters;
`/long-rest` trains the party.

**Experience system.** The project's `.claude/` files are NOT auto-loaded —
each is read at its moment, by whoever needs it:

- `gotchas.md` (traps no code owns) — before your first edit to any file
  this session
- `architecture.md` — before planning or changing how parts fit
- `decisions.md` — before choosing between approaches
- `learnings.md` — the inbox, when the three above don't answer

Capture: learnings append as dated `## YYYY-MM-DD — title` entries. A trap
goes to the first home that catches it: the test guarding it (the why in
its failure message), else a comment at its code, else — only traps no code
owns: tooling, environment, cross-cutting — 1–2 lines in `gotchas.md`
(`/long-rest` caps it at 8,000 chars). Decisions ~2 lines (choice, rejected
alternative, why), newest first; routine work is git history, not a
learning. At 10+ unread inbox entries the Guide suggests `/long-rest` once
per session.
<!-- END adventure-party (opencode-ap) -->
