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
here. `{}` is a valid config meaning "all defaults, experience off".

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
  hide.

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

- **Platform**: `bash` (or `sh`) must be resolvable. On Windows-native
  Claude Code it isn't — decline with one honest sentence ("the
  experience display needs a POSIX shell; on Windows-native Claude Code
  it would error on every prompt, so it was not installed") and skip
  the whole block. WSL is fine.
- **Existing statusline**: if the user already has a `statusLine` in
  any settings file, do not replace it — decline that piece, say so,
  and still offer the SessionStart banner alone.

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
       "command": "sh .claude/party/xp.sh statusline"
     },
     "hooks": {
       "SessionStart": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "sh \"$CLAUDE_PROJECT_DIR\"/.claude/party/xp.sh banner"
             }
           ]
         }
       ]
     }
   }
   ```

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
  or repaired; whether a restart is needed.
- **Config problems**: any validation stop, with the exact key.
