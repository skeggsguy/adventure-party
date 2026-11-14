---
description: Plan a quest for the party — writes a plan file with an Execution section (session switches to the planner model)
agent: plan
model: party-models:planner
---

Plan this work for the party to run: $ARGUMENTS

Before planning, read the project's `.claude/` experience files if they
exist — `architecture.md`, `decisions.md`, `gotchas.md`. They constrain the
approach; respect pinned decisions.

The plan must include:

1. **Steps**, in order, each with what it touches and how we'll know it
   worked — a number to measure, or a check (e.g. the test suite, a browser
   test). Size each step for one fighter session: list the files it will
   edit, tests included. Aim for up to about 6; split any step expected to
   edit more than 8. Investigating unfamiliar code before changing it is
   its own step. (Steps this size peak around 100k context; a fighter that
   runs past ~180k is compacted and loses its thread.)
2. An **Execution** section: fighter builds each step, cleric reviews every
   build (the party default), wizard only at checkpoints that must be
   guaranteed rather than left to judgment — allowed, never required.
3. A final line: `Autonomous: yes` or `Autonomous: no`. Yes (the default) =
   the party runs to the end on its own and reports every call made on the
   user's behalf in the debrief; no = it pauses whenever cleric hands
   something back.

Write the plan to a file under `~/.opencode/plan/` named after the quest.
Present it to the user, and end that same reply with the exact command on
its own line in a code block, using the plan file's full absolute path,
ready to copy and paste — don't ask for approval or wait for it first:

    /party /Users/<you>/.opencode/plan/<plan-file>.md

Running `/party` is the approval (and the muster). If the user asks for
changes instead, revise the plan file and give the command again.

Never run the plan yourself, and don't start the party — `/party` is what
switches the session back to the Guide's model.
