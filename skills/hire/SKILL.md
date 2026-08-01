---
name: hire
description: Hires a foreign coding CLI — another vendor's command-line coding
  tool — into a party role, or releases one. Verifies the binary, probes how
  to run it non-interactively with write access, smoke-tests it end to end
  with the user's consent, then records the resolved command in the project's
  party.json. User-invoked only — never run this unprompted.
disable-model-invocation: true
---

# Hire

A **hireling** is a foreign coding CLI — another vendor's command-line coding
tool, on the user's own subscription — standing in for a party member. This
skill hires one into a role or releases it. It ships no code and runs no
quest: it proves a command works, then records it in `.claude/party.json`,
where the muster rule reads it in every later session.

Hiring is standing configuration, not a one-off summons. Once fighter is
hired out, every muster of fighter runs through that command until the user
releases it — and both directions are one command.

The Guide is never hireable; it is the session the user is talking to. The
three hireable roles are `fighter`, `cleric` and `wizard`.

## No arguments — status

Read `.claude/party.json` if it exists. Most projects won't have one; that
is not an error and is **not** the moment to create it. Report one line per
role — hired to what, or the party's own member — and name both commands:
`/party:hire <role> <cli>` to hire, `/party:hire <role>` to release.

## `/party:hire <role> <cli>` — hire

Ask for whatever the user didn't supply. A role outside the three, or the
Guide: say plainly that it can't be hired, and stop.

Then work in this order, stopping at the first step that fails. Each step
exists to make a later, more expensive failure impossible.

1. **Find the binary.** `command -v <cli>`. Not found ends it — offer to
   take a full path instead.
2. **Confirm what it is.** Run its version flag and show the user the
   output. A name on PATH proves nothing about what answers to it: on
   Windows, `bash` is the WSL shim and `convert` is a filesystem tool, and
   `command -v` finds both happily.
3. **Probe how to run it.** Read the CLI's own help output and settle the
   two things that matter — how to run a single prompt non-interactively (no
   TUI, no REPL, exits when done) and how to grant it write access to files.
   Propose the resolved command with a one-line reason for each flag.
   If the help is unreadable or the tool is unfamiliar, say so and ask the
   user for the command that runs it non-interactively with write access.
   Never write a flag from memory or from a table: what a CLI's flags were
   last release is not what they are today. The probe is the source of
   truth, and its result is stored rather than remembered.
4. **Smoke-test, with consent.** Say plainly that this costs a real call on
   their subscription, and wait for a yes. Then run the resolved command on
   a trivial end-to-end prompt in a scratchpad directory — never in the repo
   — one that makes the CLI both write a file and print something, and check
   the file afterwards. Auth failures, missing config and unexpected
   interactive prompts all surface here, which is the whole point of paying
   for them now instead of mid-build.
5. **Disclose, once, before writing anything.** Two things, plainly, not
   dressed up:
   - The party runs this command through the shell, so **what it does in
     the repo happens outside Claude Code's permission prompts**. The
     approval is for the tool, not for each edit it makes.
   - Hiring **wizard** trades a guarantee for a promise. The party's wizard
     is read-only because it holds no write tools at all; a hired wizard is
     read-only because a flag says so and the hireling checks `git status`
     afterwards.

   No opinion on any CLI or model, here or anywhere else — which tool is
   worth hiring for which job is the user's call and only theirs. Meet a
   capability question with an honest "I have no basis for that".
6. **Write the config** once the user confirms. Merge into
   `.claude/party.json`, preserving `models` and any comment keys; create
   the file with both keys if it is absent. Shape:

   ```json
   "hired": {
     "<role>": {
       "cli": "<name>",
       "run": "<resolved command>",
       "probed": "<YYYY-MM-DD> <version string>"
     }
   }
   ```

7. **Close with the undo.** `/party:hire <role>` releases them, and that
   member musters normally again from the next spawn. Re-run the hire after
   upgrading the CLI, so the flags and `probed` are checked afresh.

## `/party:hire <role>` — release

When that role is hired, confirm with the user, then delete its entry from
`hired` and leave the rest of `party.json` untouched. Say that the party's
own member is back on the roster from the next muster. Nothing the hired CLI
wrote is touched — releasing changes who gets mustered, nothing else.

If the role isn't hired, say so and show the status instead.

## What hiring does not change

The party protocol is untouched. A hired fighter still hands its build
report to cleric, a hired member still emits that role's handoff contract,
and the `party:hireling` adapter is what carries the project's experience
files into the foreign prompt and reads the real diff afterwards. If a hired
command breaks mid-quest, the hireling reports it as a finding and points
back here — a re-run of this skill is the repair.
