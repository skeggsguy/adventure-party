# Adventure Party for OpenCode

An adventuring party and experience system for [OpenCode](https://opencode.ai)
V2 — the OpenCode edition of [Adventure Party](https://github.com/skeggsguy/adventure-party)
(a Claude Code plugin), rebuilt around OpenCode's native pieces: file-based
agents, commands, skills, `AGENTS.md`, and model **variants** for reasoning
effort. No plugin needed — everything is markdown plus an installer that
stamps each role's model into the agent files and symlinks the party into
`~/.config/opencode/`.

You bring the quest; the party ships it: **Session Zero** (the
`session-zero` skill) to talk it through, **plan mode** (`/plan`) to write it down, **fighter → cleric**
to build and review each step, the **wizard** for the hard calls, and a
**Long Rest** (`/long-rest`) to turn learnings into the project's curated
memory.

## The party

> **The author's setup.** This was built and dogfooded with
> **Qwen3.8-Flash-Next running locally** in the two seats that use the most
> tokens: the Guide (`/party`), which is in the loop for the whole run, and the
> Fighter, which writes every step. It's a 111 GB model; for running it on a
> 64 GB Mac, see [Flash-next-ssd](https://github.com/skeggsguy/Flash-next-ssd).
> Flash-Next isn't on OpenRouter, so the shipped defaults use its cloud sibling
> `qwen/qwen3.8-flash`, and the party runs without a local server.

- **Guide** — the main session once you run `/party`: it runs the plan,
  hands out the steps and writes the debrief.
- **Fighter** — builds each plan step: implementation and tests.
- **Cleric** — reviews every build, fixes what it can, hands back the rest.
- **Wizard** — read-only; hard debugging and "which approach?" calls.
- **Planner** — `/plan`: writes the plan file that `/party` runs.
- **Long Rest** — `/long-rest`: distills `.claude/learnings.md` into the
  project's curated memory.

## Choosing models

Each role's model is set in [`party-models.jsonc`](party-models.jsonc). The
shipped defaults all run on OpenRouter:

| Role | `party-models.jsonc` key | Model | Effort | Why |
| --- | --- | --- | --- | --- |
| **Guide** (`/party`) | `guide` | `openrouter/qwen/qwen3.8-flash` | `high` | in the loop for the whole run; needs a model that follows rules reliably at volume |
| **Fighter** | `fighter` | `openrouter/qwen/qwen3.8-flash` | `high` | writes every step; most of a run's tokens |
| **Cleric** | `cleric` | `openrouter/~deepseek/deepseek-flash-latest` | `high` | runs every step, so it's kept cheap; the `~…-latest` alias tracks the newest DeepSeek Flash |
| **Wizard** | `wizard` | `openrouter/xiaomi/mimo-v2.6-pro` | model default | rare and critical; gets a strong model |
| **Planner** (`/plan`) | `planner` | `openrouter/xiaomi/mimo-v2.6-pro` | model default | the plan decides the whole run |
| **Long Rest** (`/long-rest`) | `long-rest` | `openrouter/qwen/qwen3.8-flash` | `high` | occasional, mostly reading and condensing |

`party-models.jsonc` itself explains each line and lists the effort choices of
the common OpenRouter models. Two more seats are set in **your own
`opencode.jsonc`**, not here, because they aren't party roles:

| Seat | Setting in `opencode.jsonc` | Example |
| --- | --- | --- |
| **Session default** — chat, Session Zero | root `model`, **and** the same model on `agents.build` | `openrouter/xiaomi/mimo-v2.6-pro` |
| **Helpers** — `explore`, `general`, and title/summary/compaction | `agents.<name>.model` | `openrouter/anthropic/claude-haiku-5.5#low` |

[`opencode.example.jsonc`](opencode.example.jsonc) is a starter config with
both, plus a commented-out local model. Two things in it matter: the `build`
pin must match the root `model` (the TUI starts new sessions on the default
agent's model, so a mismatch wins), and every `openrouter/anthropic/*` model
needs `"settings": { "cache_control": { "type": "ephemeral" } }`, or it never
uses prompt caching. The installer never touches your `opencode.jsonc`.

### Changing a role's model

Don't edit `party-models.jsonc`: `git pull` updates it. Create
`party-models.local.jsonc` beside it instead (git ignores it) and list only the
roles you want to change:

```jsonc
{
  "cleric": { "model": "openrouter/~deepseek/deepseek-pro-latest", "effort": "high" },
  "wizard": { "model": "openrouter/~moonshotai/kimi-latest", "effort": "max" }
}
```

A role you list **replaces** that role's whole entry: effort names belong to
one model, so a new model never inherits the old effort. Leave `"effort"` out
to use the model's own default. A key that isn't one of the six roles is an
error, so typos don't pass silently. Then apply it:

```sh
./install.sh && opencode service restart
```

### Effort

Effort is a model **variant**, written `model#effort` in the files the
installer generates (OpenCode ignores an effort field in agent frontmatter).
Every model has its own variant names; for example `qwen/qwen3.8-flash` has
`none | high | max`, `xiaomi/mimo-v2.6-pro` only `none | thinking`, and
Anthropic models `low | medium | high | xhigh | max`. To list them all, with
OpenCode running:

```sh
opencode api get /api/model > /tmp/models.json   # a file, not a pipe: piped output gets cut off
python3 -c 'import json, sys
for m in json.load(open(sys.argv[1]))["data"]:
    print(m["providerID"] + "/" + m["id"], " ".join(v["id"] for v in m.get("variants", [])))' /tmp/models.json
```

A model you define yourself in `opencode.jsonc` only has the variants you give it.

`./install.sh` checks every role against that same list. A model OpenCode
doesn't know, or an effort the model doesn't have, stops the install with
the role, the model and the variants it does have, and nothing is installed.
If OpenCode isn't running, it warns that it couldn't verify the models and
installs anyway; `./install.sh --no-check` skips the check.

### Running the Guide and Fighter locally

The Guide and the Fighter use by far the most tokens, so they're the two seats
where a local model saves the most. Define your server as a provider in
`opencode.jsonc` (see the commented `local` block in `opencode.example.jsonc`),
then point the two roles at it in `party-models.local.jsonc`, using the
variants you defined:

```jsonc
{
  "guide":   { "model": "local/my-model", "effort": "fast" },
  "fighter": { "model": "local/my-model", "effort": "deep" }
}
```

A local Guide and Fighter share one GPU, so run party steps in the
foreground (the default): a backgrounded fighter competes with the Guide
for it.

## Install

1. **Connect OpenRouter** (one-time): in the TUI run `/connect`, pick
   OpenRouter, paste your API key.
2. **Install the party:**
   ```sh
   git clone https://github.com/skeggsguy/adventure-party && cd adventure-party/opencode && ./install.sh
   ```
   This renders each role's model from `party-models.jsonc` (plus your
   `.local`) into `.generated/`, checks them against OpenCode's model list,
   symlinks the rendered agents and commands and the `skills/` into
   `~/.config/opencode/` (or `$OPENCODE_CONFIG_DIR`), and adds the party
   block to `~/.config/opencode/AGENTS.md` between `adventure-party`
   markers (your file, your other rules untouched).
3. **Optional:** copy what you want from `opencode.example.jsonc` into your
   `~/.config/opencode/opencode.jsonc` (session default and helper models).
4. If OpenCode was already running: `opencode service restart`.
5. **Check:** `/agents` lists `fighter`, `cleric`, `wizard`; `/plan`,
   `/party`, `/long-rest` are offered.

**Updating and editing.** After a `git pull`, or after editing a models file
or anything in `agents/` or `commands/`, run `./install.sh` again, then
`opencode service restart`. The installed agents and commands are generated
copies, so edits to the sources reach OpenCode only through the installer,
and OpenCode picks up new files live but not edited ones. Skills are linked
directly; an edited skill needs only the restart.

**Removing.** `./install.sh --uninstall` removes the links and the
`AGENTS.md` block, and leaves the clone as it is.

## A quest, start to finish

```
<the idea>            → Session Zero on your default model (the skill loads
                        itself): options, trade-offs, decisions
/plan <the quest>     → the session switches to the planner's model, which
                        writes a plan file with steps, measures, an
                        Execution section and an Autonomous: yes/no line
/party ~/.opencode/plan/<file>.md   → the session switches to the Guide's
                        model and the party runs it: fighter builds each
                        step, cleric always reviews, checkpoint commits on a
                        party/<plan> branch, a debrief at the end. Merging
                        the branch is your sign-off.
/long-rest            → distill .claude/learnings.md into the project's
                        curated memory; cap gotchas.md at 8,000 chars by
                        moving traps into the code they concern (comments
                        and test failure messages, never logic; full text
                        archived, tests re-run, every source file touched
                        listed, asks first over uncommitted work); a level
                        and a title in CHRONICLE.md
```

Small change? Skip all of it — the Guide just does it.

## How this differs from the Claude Code plugin

- **No nesting, by design.** OpenCode subagents can't spawn subagents, so
  members never summon helpers or the wizard themselves. They end their
  reply with a `NEEDS_WIZARD:` block; the Guide consults the wizard and
  **resumes the member's child session** with the verdict — the plugin's
  relay, made first-class.
- **Models are named, not tiered.** Like the plugin's `party.json`, one
  file sets every role's model: `party-models.jsonc`, with your changes in
  `party-models.local.jsonc`. But it names real `provider/model` IDs and
  efforts rather than tiers, and the installer stamps them into the agent
  and command files as `model: provider/model#effort`.
- **The protocol is split.** A lean trigger block lives in global
  `AGENTS.md` (it is read every turn by every agent — including subagents,
  which OpenCode *does* give `AGENTS.md`, unlike Claude Code's hook
  injection). The full run mechanics live in the `party-run` skill, loaded
  only when mustered. This keeps the Guide focused, even on a small model.
- **Model hand-offs ride commands.** Selecting an agent does not change a
  session's model in OpenCode, but a command's `model` override beats
  everything — so `/plan` and `/party` *are* the model switches (new
  sessions start on the root `model` of your `opencode.jsonc`).
- **Experience files stay in `.claude/`** so projects shared between both
  harnesses keep one memory. `CLAUDE.md` becomes `AGENTS.md`.

## Layout

```
agents/fighter.md   agents/cleric.md   agents/wizard.md
commands/plan.md    party.md           long-rest.md
skills/party-run/   skills/session-zero/
AGENTS.fragment.md  install.sh
party-models.jsonc  opencode.example.jsonc
tools/party_models.py   (the renderer install.sh runs)
tests/                  python3 -m unittest discover tests
.generated/             (rendered by install.sh; git ignores it)
```

## Caveats

- Needs OpenCode ≥ 2.0: the party relies on model variants and the V2
  config shape (`providers`, `agents`) that `opencode.example.jsonc` uses.
- **In `opencode run` (headless CLI), commands expand as prompt text only**
  — their `model`/`agent` frontmatter applies in the TUI and via the
  session API, not the CLI. Use the TUI for `/plan`, `/party`.
- With the shipped defaults every seat is an OpenRouter call: ordinary chat
  before `/party` runs on your default model, and the Guide and Fighter
  carry most of a run's tokens. Running those two locally (see above) moves
  the bulk of a run off the bill.
