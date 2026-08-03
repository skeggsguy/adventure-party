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
A bare `/party:hire` then starts the hire flow below with both gaps to
fill, in one clickable interaction; if the user asked only for status, stop
after the report.

## `/party:hire <role> <cli>` — hire

Work in this order, stopping at the first step that fails. Each step
exists to make a later, more expensive failure impossible.

1. **Fill the gaps with choices.** The full `/party:hire <role> <cli>` form
   still works, and an argument already supplied skips the question it
   answers. Put every missing choice to the user as a clickable question
   with options, never a free-typed prompt.

   A role outside `fighter`, `cleric` and `wizard`, including the Guide,
   can't be hired: if one was supplied, say so plainly and stop. When both
   role and CLI are missing, put both questions in the same clickable
   interaction; the role options are `fighter`, `cleric` and `wizard`.

   For a missing CLI, run `command -v` for this short alphabetical list of
   coding-CLI binary names: `aider`, `codex`, `copilot`, `cursor-agent`,
   `gemini`, `opencode`. Offer only the names the sweep actually finds,
   alphabetically, plus `Other`; attach no vendor descriptions and do not
   rank them. A name that is stale or absent simply never appears. `Other`
   accepts a name or full path the sweep missed; if nothing is found, it is
   the only CLI option.
2. **Find the binary and confirm what it is.** Run `command -v <cli>`. Not
   found ends it — offer to take a full path instead. Then run its version
   flag and show the user the output. A name on PATH proves nothing about
   what answers to it: on Windows, `bash` is the WSL shim and `convert`
   is a filesystem tool, and `command -v` finds both happily.
3. **Probe how to run it.** Read the CLI's own help output and settle the
   four things that matter — how to run a single prompt non-interactively
   (no TUI, no REPL, exits when done), how to grant it write access to
   files, how to select a model on the command line, and how to set
   reasoning effort if the CLI has that knob.

   Propose the base command with a one-line reason for each
   probe-confirmed flag. If the help text neither names a dedicated effort
   flag nor enumerates values for a generic override (codex: `-c
   model_reasoning_effort=<value>`, no dedicated flag, no listed values),
   don't conclude the knob is absent — ask, then verify, same shape as
   model discovery in step 4:
   - **Ask** the CLI itself for the config key name and its candidate value
     list, as JSON for clean parsing. Treat the answer as a lead, not a
     fact — asked this way, codex named its own key correctly but its value
     list silently dropped two real values (`none`, `max`); see
     `.claude/gotchas.md`, 2026-08-03.
   - **Verify the key** by running the real probe command with one
     candidate value and confirming the CLI's own output echoes that the
     value took effect — a silently-ignored key is indistinguishable from
     a working one any other way.
   - **Verify the values** by feeding one deliberately invalid value
     through the same real command; many CLIs' resulting error enumerates
     every valid value in the message itself, which is the complete,
     authoritative list — more complete than what the CLI volunteered when
     asked politely. Only fall back to the self-reported list if the error
     doesn't enumerate.
   If the effort knob is absent even after asking, do not offer an effort
   choice later. If the help is unreadable or the tool is unfamiliar, say
   so and ask the user for the command that runs it non-interactively with
   write access — the one choice with no options to click.
   Never write a flag from memory or from a table: what a CLI's flags were
   last release is not what they are today. The probe (plus the ask-then-
   verify fallback above) is the source of truth; use its verified
   spellings and level names below.
4. **Discover model names.** Prefer the CLI's own listing — help text or a
   models subcommand found during the probe. Only when the CLI offers no
   listing, fall back to asking the CLI itself (ask-then-verify, step 3's
   shape) or a web search for current model names. These names populate the
   model menu only. A discovered or user-supplied model name is
   a claim to verify, not configuration to record; the value written later
   is the model string that the smoke test proves runs. Do not rank the
   names.
5. **Smoke-test, with consent.** Put the consent to the user as a clickable
   yes/no question. Say plainly that a yes costs a real call on their
   subscription, and do not run it without that yes. Then run the exact
   base command on a trivial end-to-end prompt in a scratchpad directory —
   never in the repo — that makes the CLI both write a file and print
   something, and check the file afterwards. Auth failures, missing config
   and unexpected interactive prompts all surface here, which is the whole
   point of paying for them now instead of mid-build. A no stops before any
   config is written.
6. **Pin model and effort, then verify the final command.** Put up to two
   questions in one clickable interaction:
   - Which model to pin — the discovered names plus `Don't pin`. If the
     probe found no model-select flag, offer only `Don't pin`.
   - Which reasoning effort to pin — the CLI's own verified level names plus
     `Don't pin`, but only when the probe found an effort knob.

   Which model or effort to choose is the user's call alone; listing what
   the CLI offers is fine, ranking it is not. Pinning is the default shape:
   the selected model and effort flags ride in the stored `run` command so a
   hire means the same thing after the CLI updates itself. Declining a
   choice leaves that flag out; if both are declined, the hire inherits the
   CLI's own config at each muster and neither setting is recorded.

   Any selected model or effort changes the command under test, so the
   smoke test that already ran no longer covers it: get consent again for
   another real call as a clickable yes/no question, then run a fresh
   smoke test of the exact final command. The pinned model-and-effort
   combination, when both are selected, must pass that test before
   anything is written. Never treat a name as verified merely because it
   appeared in a listing or came from the user.
7. **Disclose, once, before writing anything.** Two things, plainly, not
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

   Put a final clickable yes/no confirmation immediately after this
   disclosure; a no stops without writing anything, and only a yes permits
   the next step.
8. **Write the config** after that final yes. Merge into
   `.claude/party.json`, preserving `models` and any comment keys; create
   the file with both keys if it is absent. The resolved command is the exact
   command that passed the final smoke test; any pinned model and effort
   flags are part of its `run` string, like any other flag. The JSON
   shape and schema do not change. Shape:

   ```json
   "hired": {
     "<role>": {
       "cli": "<name>",
       "run": "<resolved command>",
       "probed": "<YYYY-MM-DD> <version string>"
     }
   }
   ```

9. **Close with the undo.** `/party:hire <role>` releases them, and that
   member musters normally again from the next spawn. Re-run the hire after
   upgrading the CLI, so the flags, pinned model, effort and `probed` are
   all checked afresh.

## `/party:hire <role>` — release

When that role is hired, put a clickable yes/no confirmation to the user,
then delete its entry from `hired` and leave the rest of `party.json`
untouched. Say that the party's
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
