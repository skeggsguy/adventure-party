---
name: config
description: Apply the settings in .claude/party.json — per-member model
  overrides (validated, applied at spawn time via the Agent tool's model
  parameter) and the opt-in experience display (statusline + level-up
  banner). Run by hand after editing party.json.
disable-model-invocation: true
---

# Party Config

`.claude/party.json` is the one file a user edits to tune the party.
This skill makes it true: it reads the config and applies it. It is
safe to re-run — re-running is also how you repair a half-configured
state or refresh stale generated files after a plugin update.

## The config file

```json
{
  "//": "To change a party member's model, add it under \"models\" — fighter, cleric, or wizard, set to opus, sonnet, haiku, or fable — then run /party:config. Empty or absent means the plugin's default.",
  "models": {
    "fighter": "opus",
    "cleric": "fable",
    "wizard": "fable"
  },
  "experience": {
    "enabled": false
  }
}
```

Every key is optional. **An absent key means "plugin default"** — the
defaults live in the plugin's agent files, never snapshotted into
party.json, so a plugin update can change a default without stale pins
here. `{}` is a valid config meaning "all defaults, experience off",
and so is `"models": {}` — which is what `/party:setup` ships, since
JSON has no comment syntax and an empty block plus the `"//"` note is
how the file documents itself without pinning anything.

The `models` values above are illustrative of the *shape*, not text to
write into a user's file. `models` accepts model **tiers**, not model
IDs — `opus`, `sonnet`, `haiku`, `fable`. Those four names are stable
across model releases: a config saying `opus` follows whatever the
current Opus is. There is nothing here for a user to keep up to date.

## Validation — before touching anything

Read `.claude/party.json`. If it is missing, treat it as `{}`. If it is
not valid JSON, stop and report — never guess or repair it.

- `models.*` values must be one of: `opus`, `sonnet`, `haiku`, `fable`
  (the Agent tool's `model` parameter accepts exactly these tiers).
  Anything else (e.g. `opsu`): stop and report the exact key and
  value — the error surfaces here, at write time, not days later when
  an agent spawns.
- `models` keys must be `fighter`, `cleric`, or `wizard`.
- Unknown top-level keys or unknown keys inside `experience` (e.g.
  `experiance`): stop and report them. Silent-inert config is how typos
  hide. **Exactly one exception**: a top-level `"//"` key is the file's
  comment (JSON has no comment syntax) — ignore it by name and never
  report it. The exception is that literal two-character key alone;
  `"///"`, `"//models"`, or a `"//"` nested inside `models` are unknown
  keys and stop the run like any other. Do not rewrite or "correct" a
  `"//"` whose text has drifted from the shipped wording — it is the
  user's file.

## Applying `models` — spawn-time overrides, no generated files

Verified behavior (2026-07-25): a project-level `.claude/agents/<name>.md`
does NOT shadow the plugin's `party:<name>` — the two coexist as
separate agents, and a namespaced spawn always gets the plugin copy. So
file generation cannot override a party member's model. What does work:
the Agent tool's per-invocation `model` parameter, which outranks the
agent definition's frontmatter.

The mechanism is therefore convention, wired into CLAUDE.md: the muster
bullet installed by `/party:setup` tells the Guide to check
`.claude/party.json` for `models` overrides when mustering and pass them
as the Agent tool's `model` parameter. This skill's job for `models` is:

1. **Validate** (above) and report the effective lineup — for each
   member, the plugin default (read from
   `${CLAUDE_PLUGIN_ROOT}/agents/<name>.md` at apply time) or the
   configured override.
2. **Check the wiring**: if the project's CLAUDE.md lacks the muster
   bullet (no mention of `party:fighter`), note that overrides won't be
   picked up until `/party:setup` runs.
3. **Flag bare-name doubles**: if `.claude/agents/fighter.md` (or
   cleric/wizard) exists, warn — it does not override the party member;
   it appears as a separate, unnamespaced agent that can confuse
   delegation. Recommend deleting it (but never delete it yourself).

**Team note**: party.json is a committed project file — a model choice
made here applies to everyone who clones the repo. That's a team-level
decision; a solo user can ignore this.

## Applying `experience` — the display wiring

All writes in this section go to `.claude/settings.local.json` —
**per-user, untracked** — because a statusline is a personal display
preference; committing it would clobber teammates' own statuslines.

**`enabled: false` (or absent)** → nothing to wire. If a previous run
wired the statusline/hook into settings.local.json, offer to remove
those entries.

**`enabled: true`** → this is an atomic block: pre-check everything,
then land all of it or none of it, and report which.

Pre-checks:

- **Shell interpreter**: find one by *proving* it, never by detecting
  the platform — see "Choosing the interpreter" below. If nothing
  proves out, decline the whole block with the exact message given
  there. This runs on macOS, Linux, WSL, and Windows-native alike.
- **Existing statusline**: if the user already has a `statusLine` in
  any settings file, do not replace it — decline that piece, say so,
  and still offer the SessionStart banner alone.

#### Choosing the interpreter

The statusline runs as a subprocess on *every prompt render*, so a
wrong interpreter is an error the user sees continuously. Do not infer
one from the operating system, and do not trust a bare `sh` resolving
in your own shell: on Windows, whether Git Bash is on `PATH` is a
property of how the terminal was launched, not of the machine, so a
statusline that works today dies silently when the user opens Claude
Code a different way tomorrow.

Probe against the plugin's own `${CLAUDE_PLUGIN_ROOT}/scripts/xp.sh`,
not the project copy — the pre-check must be able to fail before
anything has been written. Try these candidates **in order**, and take
the first that genuinely works:

1. `/bin/sh` — POSIX systems (macOS, Linux, WSL) always have it
2. `C:\Program Files\Git\bin\sh.exe` — Git for Windows, default
3. `C:\Program Files\Git\usr\bin\sh.exe` — same install, bare binary
4. `C:\Program Files (x86)\Git\bin\sh.exe` — 32-bit install
5. `C:\Program Files (x86)\Git\usr\bin\sh.exe` — same, bare binary
6. `%LOCALAPPDATA%\Programs\Git\bin\sh.exe` — per-user install
7. `%LOCALAPPDATA%\Programs\Git\usr\bin\sh.exe` — same, bare binary
8. the `bin\sh.exe` then `usr\bin\sh.exe` siblings of whatever
   `where.exe git` reports, resolved from the Git install root
   (`git.exe` may sit in either `cmd\` or `mingw64\bin\`, so walk up to
   the root — don't assume a fixed number of levels)
9. bare `sh` — last resort only

Each Git for Windows location is tried `bin\` first, `usr\bin\` second,
and the order matters: `bin\sh.exe` is a wrapper that puts Git's
coreutils on `PATH` before handing off, while `usr\bin\sh.exe` is the
bare shell binary and runs without them — so `xp.sh` loses `grep`,
`tail`, and `sed`. Keep the `usr\bin\` entries anyway; on some installs
they are all there is.

"Genuinely works" means: run `<candidate>
${CLAUDE_PLUGIN_ROOT}/scripts/xp.sh statusline` from the project
directory with empty input, and require **exit code 0, non-empty
stdout, and empty stderr** — all three. A candidate that exits 0 with no
output has not proved anything, and neither has one that printed
`command not found` on the way. Stderr is not optional here: `xp.sh`
guards its utility calls, so a shell that can't find `grep`/`tail`/`sed`
still exits 0 with plausible output on a project whose `learnings.md` is
empty, and only starts reporting the wrong XP once there are entries to
count. Exit status proves the shell *started*; empty stderr is the only
probe-time evidence it actually *worked*. Give each probe a short
timeout and treat a hang as a failure. Prefer an absolute path over a bare name whenever one proves
out — absolute paths do not depend on the environment the subprocess
inherits.

Write the winning candidate into both commands below, quoted if it
contains spaces. **In JSON, every backslash in a Windows path must be
escaped** (`C:\\Program Files\\Git\\usr\\bin\\sh.exe`); an unescaped
path is either invalid JSON or a silently mangled command.

If every candidate fails, decline the whole block and say exactly what
was tried and what would fix it:

> The experience display needs a POSIX shell to run `xp.sh`, and I
> couldn't find one that works here. I tried `/bin/sh`, the standard
> Git for Windows locations, and the `git` on your `PATH`. Installing
> Git for Windows (which bundles the shell) and re-running
> `/party:config` will wire it up. Everything else in the party works
> without it — the display is cosmetic; the experience files are the
> substance.

Never decline with a bare "unsupported platform": the user cannot act
on that. Name what was tried, name the fix, and say what still works.

Steps:

1. Copy `${CLAUDE_PLUGIN_ROOT}/scripts/xp.sh` to `.claude/party/xp.sh`.
   The file's header comment carries the plugin version — on re-run,
   compare and refresh a stale copy. (The copy exists because settings
   files can't reference `${CLAUDE_PLUGIN_ROOT}`.)
2. In `.claude/settings.local.json` (create if missing; preserve every
   existing key; result must be valid JSON — if the existing file is
   invalid JSON, stop and report rather than repair), add exactly these
   two entries (merging into any existing `hooks` object):

   ```json
   {
     "statusLine": {
       "type": "command",
       "command": "<SH> .claude/party/xp.sh statusline"
     },
     "hooks": {
       "SessionStart": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "<SH> \"$CLAUDE_PROJECT_DIR\"/.claude/party/xp.sh banner"
             }
           ]
         }
       ]
     }
   }
   ```

   `<SH>` is the interpreter the pre-check proved — `/bin/sh` on POSIX,
   or a quoted, backslash-escaped absolute path on Windows, e.g.
   `\"C:\\Program Files\\Git\\usr\\bin\\sh.exe\"`. Never write the
   literal `<SH>`.

   The path forms differ deliberately: the statusline command runs with
   the project as its working directory (and the script falls back to
   `$PWD`), while hooks get the `$CLAUDE_PROJECT_DIR` variable — each
   uses the form guaranteed in its own context.
3. Note: settings are read at session start — the display appears after
   the next restart.

The banner script is opt-in-gated twice: it exits silently unless
party.json says `enabled: true`, so a copied script with no wiring (or
wiring with `enabled` later set false) does nothing.

## Report

- **Models**: the effective lineup per member — plugin default, or
  override configured (applied at spawn time); any bare-name doubles
  flagged; whether the CLAUDE.md muster wiring is present.
- **Experience**: enabled or not; each piece wired, declined (and why),
  or repaired; which interpreter the pre-check proved (name the actual
  path, so a later silent failure is traceable); whether a restart is
  needed.
- **Config problems**: any validation stop, with the exact key.
