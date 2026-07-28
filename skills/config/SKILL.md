---
name: config
description: Apply the settings in .claude/party.json — per-member model
  overrides, validated here and applied at spawn time via the Agent
  tool's model parameter. Run by hand after editing party.json.
disable-model-invocation: true
---

# Party Config

`.claude/party.json` is the one file a user edits to tune the party.
This skill makes it true: it reads the config, checks it, and reports
what will actually take effect — a typo surfaces here rather than days
later when an agent spawns. It writes nothing, so it is safe to re-run
as often as you like.

## The config file

```json
{
  "//": "To change a party member's model, add it under \"models\" — fighter, cleric, or wizard, set to opus, sonnet, haiku, or fable — then run /party:config. Empty or absent means the plugin's default.",
  "models": {
    "fighter": "opus",
    "cleric": "fable",
    "wizard": "fable"
  }
}
```

Every key is optional. **An absent key means "plugin default"** — the
defaults live in the plugin's agent files, never snapshotted into
party.json, so a plugin update can change a default without stale pins
here. `{}` is a valid config meaning "all defaults", and so is
`"models": {}` — which is what `/party:setup` ships, since JSON has no
comment syntax and an empty block plus the `"//"` note is how the file
documents itself without pinning anything.

The `models` values above are illustrative of the *shape*, not text to
write into a user's file. `models` accepts model **tiers**, not model
IDs — `opus`, `sonnet`, `haiku`, `fable`. Those four names are stable
across model releases: a config saying `opus` follows whatever the
current Opus is. There is nothing here for a user to keep up to date.

## Validation — before reporting anything

Read `.claude/party.json`. If it is missing, treat it as `{}`. If it is
not valid JSON, stop and report — never guess or repair it.

- `models.*` values must be one of: `opus`, `sonnet`, `haiku`, `fable`
  (the Agent tool's `model` parameter accepts exactly these tiers).
  Anything else (e.g. `opsu`): stop and report the exact key and
  value — the error surfaces here, when the config is read, not days
  later when an agent spawns.
- `models` keys must be `fighter`, `cleric`, or `wizard`.
- Unknown top-level keys (e.g. `modles`): stop and report them.
  Silent-inert config is how typos hide. **Exactly two exceptions**,
  handled differently:
  - `"//"` is the file's comment (JSON has no comment syntax) — ignore
    it by name and never report it. Do not rewrite or "correct" a
    `"//"` whose text has drifted from the shipped wording; it is the
    user's file.
  - `experience` is a leftover from the XP display that 0.7.0 removed.
    It does nothing. Do not stop for it — say in one line that it is
    inert and can be deleted, then carry on with the rest of the run.
- Neither exception is fuzzy — each is that literal key name and
  nothing else. `"///"`, `"//models"`, `experiance`, or a `"//"` nested
  inside `models` are unknown keys and stop the run like any other.

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
   bullet (no mention of `party:fighter`, and no "The party musters on
   command" either — the same two-part test `/party:setup` step 5b
   uses), note that overrides won't be picked up until `/party:setup`
   runs.
3. **Flag bare-name doubles**: if `.claude/agents/fighter.md` (or
   cleric/wizard) exists, warn — it does not override the party member;
   it appears as a separate, unnamespaced agent that can confuse
   delegation. Recommend deleting it (but never delete it yourself).

**Team note**: party.json is a committed project file — a model choice
made here applies to everyone who clones the repo. That's a team-level
decision; a solo user can ignore this.

## Report

- **Models**: the effective lineup per member — plugin default, or
  override configured (applied at spawn time); any bare-name doubles
  flagged; whether the CLAUDE.md muster wiring is present.
- **Config problems**: any validation stop, with the exact key; and any
  inert leftover key the user could delete.
