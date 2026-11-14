---
name: party-run
description: >-
  The party run protocol — muster rules, step-by-step fighter/cleric loop,
  checkpoint commits, the NEEDS_WIZARD relay, hand-back rounds, set-asides,
  per-step reporting and the debrief. Load when executing a plan with the
  party (the /party command loads it); do not load for ordinary single-session
  work.
---

# Party Run — the Guide's protocol

You are the Guide: you talk to the user and hand out the work. Members run
in child sessions with fresh context and cannot spawn subagents — you are
their only route to each other and to the wizard.

## Muster

The party rides out when the user summons it, when an approved plan
delegates to it (plans muster by default), or when the user accepts your
one-line suggestion. Otherwise do the work yourself. Once mustered, follow
this protocol until the run ends.

## Running the plan

- Give both members the plan by file location — "read it all; step N is
  yours" — never pasted. A plan not yet in a file goes to a file first;
  with no plan, write the task out.
- Per step: spawn a **fresh fighter** subagent (foreground, new session —
  no sessionID) → when it returns, ALWAYS spawn the **cleric** with the
  build report and the step number. Never skip cleric because the build
  looks clean.
- Give members the plan's `Autonomous:` value in the spawn prompt.

### Relay (members can't call the wizard)

A member's reply ending with a `NEEDS_WIZARD:` block means it is stuck.
Spawn the **wizard** with the block's contents verbatim plus file paths;
when the verdict returns, resume the SAME member session (the subagent tool
keeps the child's session id) with "WIZARD VERDICT: <verdict> — implement
it and finish your report". Context preserved; the member continues.

### When to resume a member

Resume a member's session only to relay a wizard verdict (above) or to
recover a missing report (below). Never resume across steps or for fix
rounds — spawn fresh. A resumed session re-reads its whole history before
its first token and starts near the compaction line, where fighters lose
the thread.

Missing report: a member returns `Subagent completed without a text
response.` or nothing → resume it once with exactly "Your last turn ended
without visible text, so no report reached me. Reply now with your
report." Still nothing from a fighter → read `git status` and
`git diff HEAD` yourself, spawn cleric with "fighter's report is missing;
review the diff against step N", and say so in the step's lines to the
user. Still nothing from a cleric → spawn a fresh cleric.

### Cleric fixes, or hands back

Cleric fixes what keeps the build's design and hands back what needs a
redesign or a user decision. On a `HANDED BACK`:

- Plan says `Autonomous: no` → pause, bring it to the user.
- Otherwise → spawn a fresh fighter for the fix round, briefed as in
  "Tell members what they can't see"; a user decision included: fighter
  makes that call itself and records it under DECISIONS — the debrief
  lists every such call. Then cleric again.
- At most two fix-rounds per issue on the same step; still handed back →
  wizard's verdict → one final fresh fighter with the verdict in its
  brief; still stuck → set the issue aside for the debrief, tell every
  later spawn it is set aside, and carry on with steps that don't depend
  on it. Stop only when every remaining step depends on it.

### After your own compaction

A `<conversation-checkpoint>` `<summary>` covers only the planning before
this run: its "Plan mode", "awaiting muster" and "Next Move" lines are stale
— `<recent-context>` is the run's state; carry on from it, never re-plan or
re-offer `/party`. A `[truncated]` member report there was cut by the
compaction, not the member — rebuild from `git status` and `git diff`.

## Checkpoints

After each cleric pass that leaves the tree green, commit — so the next
cleric's diff is one step or one round. Commit on a branch: if the run
starts on the default branch, create `party/<plan-name>` first. Start from
a clean tree; if it isn't, ask the user when presenting the plan. A set-
aside issue's uncommitted rework is stashed
(`git stash push -u -m "set aside: <issue>"`), never discarded. The user
signs off by merging the branch.

## Tell the user what happened

- After each step of a multi-step run: a few lines — what worked, what
  didn't, the step's measure (a number against before, best so far, or the
  check's result; cleric's `MEASURED` when it re-took one, else
  fighter's). Uneventful step: one line with its measure. Repeat the lines
  in the step's commit message, then carry on.
- When the run or the party's work ends: **debrief** — outcome against the
  plan's measures, then only sections with something in them: what didn't
  work, what was found, what was set aside and why, calls fighter made for
  the user, what's next. Went as planned: one line with its numbers. A
  takeaway only when genuinely non-obvious — never a forced lesson.

## Experience capture

Members' `LEARNED:` lines are candidates. Append anything non-obvious to
`.claude/learnings.md` as a dated `## YYYY-MM-DD — title` entry. A trap
goes to the first home that catches it: the test that guards it (the why in
its failure message), else a comment at the code it concerns, else — only
for traps no code owns: tooling, environment, cross-cutting — 1–2 lines in
`gotchas.md` (`/long-rest` caps it at 8,000 characters). Members leave
code-local traps in the code themselves, so their `LEARNED:` lines carry
only the rest. Landed choices get ~2 lines in `decisions.md` (choice,
rejected alternative, why). Routine work is git
history, not a learning. After appending, count `^## [0-9]{4}-` in the
inbox: at 10+, suggest `/long-rest` once per session and take no for an
answer.

## Tell members what they can't see

Every spawn prompt says: the plan's file path and which step is theirs; the
project root; that `.claude/` experience files are NOT injected and they
must read them at their triggers (gotchas before their first edit;
architecture before changing how parts fit; decisions before choosing an
approach); that if stuck they end their turn with `NEEDS_WIZARD:` and you
will relay and resume them; and that their final message is a report for
you, not for the user.

A fix-round fighter's spawn prompt also says: that it is fix round R of
step N; the cleric's `HANDED BACK` items, verbatim; the previous fighter's
`DECISIONS` and `UNVERIFIED` sections, verbatim (reports aren't saved
anywhere, so paste them); and where the step's work so far is, cleric's
fixes included — uncommitted in the tree, or the checkpoint commit's hash.
It reads that diff first and keeps what's there unless the hand-back says
otherwise.
