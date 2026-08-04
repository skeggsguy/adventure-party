# Learnings (inbox)

Append-only dated entries (`## YYYY-MM-DD — title`), distilled into the
curated experience files and archived by `/party:long-rest`. Never injected;
read on demand.

## 2026-08-02 — The hire smoke test proves launch, not endurance

First live firing of the mid-quest repair path: codex (luna, max effort)
launched cleanly on a real build task, did ~25s of recon, then died silently
— no edits, nothing on stdout/stderr, exit swallowed, its own session rollout
ending mid-turn. The hire-time smoke test cannot catch this failure mode: it
proves launch, auth and write on a trivial prompt, not survival minutes into
real work. The "hire breaks → finding → `/party:hire` is the repair" path
exists for exactly this and worked as designed — hireling reported, tree
proven byte-identical, quest ended at the table. (Fighter's LEARNED line,
hired-out build of the hire-flow rework.)

## 2026-08-02 — What openai/codex-plugin-cc knows that our hireling doesn't

Studied OpenAI's own Claude Code plugin after today's silent codex death. It
never runs `codex exec` — it drives a long-lived `codex app-server` over
JSON-RPC, so a mid-task death is structurally unswallowable: process exit
rejects every pending request with the captured stderr. We can't ship that
(no-scripts rule), but the portable prose techniques are: (1) bake exit-code
and stderr capture into the run command string itself (`2>errfile; echo
EXIT=$?`) and treat a missing completion marker as death, not silence; (2)
require a completion sentinel at the end of the foreign prompt — absence
means died-mid-task, never summarize; (3) capture the session id from codex's
header BEFORE the work starts, so `codex resume <id>` survives a death; (4) a
`timeout <s>` prefix is the scriptless 80% of their 15-min watchdog; (5)
their skill's hardest rule matches ours: a run never invoked returns nothing
— no substitute answer; (6) their setup gate is two-tier version+auth checks
(`--version`, subcommand `--help`, auth status via RPC), no smoke test at
all — cheap checks we could add alongside ours. Clone studied at scratchpad/
codex-plugin-cc, full analysis in session 2026-08-02.

## 2026-08-02 — The silent death diagnosed: it was our background launch

The discriminating test settled it: the same codex command that "died
silently at 25s" under the hireling ran healthily for 9.5 minutes in the
foreground until our own `timeout` cut it (EXIT=124, caught cleanly) — the
original failure was the adapter backgrounding the process and ending its
turn, not codex crashing. Run-discipline facts learned on the way: codex
streams progress to *stderr* (a stdout watcher sees silence and infers
death); `codex exec resume <id>` takes its options BEFORE the subcommand
(after it → clap error); the session id printed in the header is the
recovery handle — a timeout-killed run resumed mid-task and completed. All
of this belongs in `agents/hireling.md`: foreground only, capture EXIT and
stderr, harvest the session id first, generous timeout for real builds.

## 2026-08-02 — A guided-flow rewrite quietly deletes escape hatches

Cleric's find: "every choice is clickable" got over-applied to the one input
with no enumerable options — the unknown-CLI user-supplied-command fallback,
a standing decision (2026-08-01) — and the builder deleted it as
non-conforming. When a rule bans an interaction *shape*, check each deleted
path for whether any other shape could serve it. (Cleric's LEARNED line,
hire-flow rework review.)

## 2026-08-02 — A hireling that waits for a notification has ended its quest

The hireling adapter launched its foreign CLI in the background and ended its
turn "waiting for the completion notification" — but a subagent's final
message is the only carrier back to the party, and nothing resumes it
automatically. The quest continued only because the Guide noticed and resumed
it via SendMessage. Candidate fix in `agents/hireling.md`: run the hired
command in the foreground (or poll it to completion) and never end the turn
while the command is still running.

## 2026-08-02 — Codex's sandbox makes "curl X and commit it" an adapter job

First fully clean hired build (chess app quest): codex under `--sandbox
workspace-write` blocks both network and `.git` writes, so any plan step of
the shape "fetch artifact, commit result" must be split — the adapter
pre-fetches the artifact before launch and runs the commit after verifying
the diff, with the hired run command itself unaltered. Budget for that at
launch, not as a mid-run rescue. Corollary: a `QUEST_FAILED` sentinel can be
honest about the *sandbox* (blocked socket bind, read-only `.git`) rather
than the build — read the named reason before treating the run as a failed
build; here the diff was complete and every blocked check passed when re-run
outside. (Hireling's LEARNED lines, chess build.)

## 2026-08-02 — No-runtime review: audit call shapes against the vendored source

Cleric's find on the same quest: with no node/deno on the box and installs
off-limits, the highest-value substitute for executing client code against a
vendored library is (1) auditing every call's shape — signatures and return
fields, not just method names — against the vendored source itself, and (2)
an independent sha256 check against the upstream artifact. The audit caught a
real bug greps missed: en passant's destination square is empty, so
occupancy-based capture highlighting lies — `Move.captured` is the truth.
(Cleric's LEARNED line, chess build review.)

## 2026-08-03 — `pgrep -f` wait loops deadlock on their own watchers

Running a hired codex fighter in `~/projects/ai`, the wait pattern was
`until ! pgrep -f "codex exec -s workspace-write"; do sleep 10; done`. `pgrep`
excludes its own process but not sibling watchers, and each watcher shell's
`/bin/bash -c ...` argv contains the search string verbatim — five watchers
alive meant each matched the other four and no condition ever went false.
Codex exited at ~19:41; the quest stayed blocked 30+ minutes until the
watchers were manually killed. The general shape: any "wait until this
command-line pattern disappears" loop is self-referential, because the waiter
is a process whose command line holds the pattern. Wait on a captured PID
(`tail --pid=$PID -f /dev/null`, which works for non-children) or match the
binary exactly (`pgrep -x`); and give every wait a bounded backstop so a
future variant can't hang a turn indefinitely. Fixed in `agents/hireling.md`
run mechanics.
