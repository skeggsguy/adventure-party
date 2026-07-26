# Notes — open follow-ups

Scratch backlog. NOT auto-loaded into sessions, NOT experience (no XP —
these are open items, not learnings). Delete each entry when it's done or
when it stops mattering.

Newest first.

## 2026-07-26 — `xp.sh` hangs when run from a terminal

**What.** `scripts/xp.sh` line 21 is `cat >/dev/null 2>&1 || :`, draining
stdin so the statusline writer never hits EPIPE. It works when Claude
Code pipes JSON and closes the pipe. It hangs forever when stdin is a
terminal, because `cat` waits for EOF.

**Why it matters.** The affected command is the one `CLAUDE.md`'s Commands
section documents for testing the script: `sh scripts/xp.sh statusline`.
Production paths (statusline, SessionStart hook) are unaffected — this is
a broken *documented test*, not a broken feature. Found when the command
timed out during the Level 2 Long Rest.

**Fix, ready to apply** — keeps the EPIPE protection, skips the drain
when stdin is interactive:

```sh
[ -t 0 ] || cat >/dev/null 2>&1 || :
```

Apply to `scripts/xp.sh`; `.claude/party/xp.sh` is the installed copy and
also needs it (or a re-run of setup, see next entry). Workaround
meanwhile: `sh scripts/xp.sh statusline </dev/null`. Consider whether
`CLAUDE.md`'s documented command should carry `</dev/null` regardless, as
belt-and-braces for other harnesses that hold stdin open.

## 2026-07-26 — `/party:setup` doesn't refresh the installed `xp.sh` on upgrade

`.claude/party/xp.sh` says `party@0.4.0` while `scripts/xp.sh` says
`0.5.0`. Only the version comment differs today, so behavior is
identical and nothing is broken — but it proves the copy isn't
re-run/refreshed on upgrade, which will bite the first time the script's
*logic* changes. Look at setup's copy step: does it skip when the file
already exists? If so it needs a version check, or an explicit refresh.

## 2026-07-26 — Session Zero: release chores deferred from the second pass

The shipped Conventions bullet changed in `CLAUDE.md` +
`memory/CLAUDE.md.template`, which by the step-5a convention makes the
0.5.0 variant a migration fingerprint. Cleric confirmed nothing breaks
today (5a's candidate list never included the Session Zero bullet, so no
code path reads its marker; the loss to existing installs is
under-specification, not wrong instructions). Do all three together at
the next version bump:

1. Bump `.claude-plugin/plugin.json` (0.5.0 → 0.6.0).
2. Append a `## 0.5.0 — Session Zero bullet` section to
   `memory/legacy-blocks.md` with the exact outgoing body.
3. Add a Session Zero case to `skills/setup/SKILL.md` step 5a.

**Time-sensitive:** the outgoing bullet text is recoverable from
`git show HEAD:CLAUDE.md` now, and won't be after the next commits land.
Capture it before then if the bump is far off.

## 2026-07-26 — Session Zero: judgement calls cleric left for the author

- **The state diagram is the file's weakest visual.** The sentence above
  it already says "no exit condition except the user's word; loop as long
  as the user is still thinking," so the 14-line sketch largely restates
  prose — which its own "a visual must carry information the sentence
  can't" rule forbids. It also shows one exit while `CLAUDE.md` allows
  three (plan mode, "just build it", accepting a muster suggestion).
  Either add the missing branches or cut it; it's the biggest clean cut
  available if 234 lines feels heavy.
- **The trigger boundary asks the model to infer purpose.** It landed
  both live probes, so it works — but a syntactic form would need no
  mind-reading: "a question with one correct answer that doesn't depend
  on this project (a port number, a flag name, what a function returns)."
- **Undefined jargon in a file that mandates defining terms:** `seam`,
  and arguably `refactor`/`rewrite` in the asymmetry sketch (that sketch
  half-defines them by contrast). Left alone because supplying the
  definitions is authoring in the user's voice.
- **Depth-tier overlap:** "a library" sits in tier 2 while "a dependency
  you'll build on" sits in tier 3 — same noun, split on load-bearingness.
  Works as written; revisit only if real use shows mis-tiering.

## 2026-07-26 — Pre-existing: two agent frontmatters aren't strict YAML

`agents/fighter.md:5` and `agents/cleric.md:7` each have a bare `: `
inside a multi-line plain-scalar `description` (`the default:` and `Not a
standalone reviewer: only`). Claude Code's parser tolerates it and both
agents load — but a stricter validator would trip. Not urgent; worth
fixing before anyone runs a schema check over the plugin.

## 2026-07-26 — Working tree mixes two changes

`README.md`, `.claude/decisions.md`, and `.claude/learnings.md` carried
uncommitted install-scope work *before* the Session Zero pass started,
and the Level 2 Long Rest then added to the same pile. Decide what rides
in which commit before committing.
