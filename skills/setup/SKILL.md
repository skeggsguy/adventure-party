---
name: setup
description: Install the Adventure Party memory system into the current
  project — copies the four memory files into .claude/, enables nested
  delegation in .claude/settings.json, and wires the party protocol,
  Session Zero, and project-memory sections into CLAUDE.md. Run once per
  repo, by hand.
disable-model-invocation: true
---

# Party Setup

The agents and skills arrive with the plugin. The memory system cannot —
a plugin ships its own files, it never writes into a project's `.claude/`.
This skill closes that gap: it seeds the memory files and the CLAUDE.md
wiring that the party reads its law from, and turns on the nested
delegation the party members use to call for aid.

Run it once per project. It is **additive only** — it never overwrites or
rewrites anything that already exists.

## Source files

Everything is copied out of the installed plugin:

- `${CLAUDE_PLUGIN_ROOT}/memory/architecture.md`
- `${CLAUDE_PLUGIN_ROOT}/memory/gotchas.md`
- `${CLAUDE_PLUGIN_ROOT}/memory/decisions.md`
- `${CLAUDE_PLUGIN_ROOT}/memory/learnings.md`
- `${CLAUDE_PLUGIN_ROOT}/memory/CLAUDE.md.template`

If any of those paths cannot be read, stop and say so — do not
reconstruct the file contents from memory.

## Steps

### 1. Confirm the target

The target is the current project's root — the directory holding (or about
to hold) `CLAUDE.md` and `.claude/`. State it before writing anything. If
the working directory is clearly not a project root (no repo, no source
tree), ask before proceeding.

### 2. Seed the four memory files

For each of `architecture.md`, `gotchas.md`, `decisions.md`,
`learnings.md`:

- If `.claude/<file>` already exists → **skip it**, record it as skipped,
  and do not read or modify it.
- Otherwise copy the plugin's copy verbatim into `.claude/<file>`.

Create `.claude/` if it does not exist. Never merge into an existing
memory file — a project that already has one has its own content there.

Writes under `.claude/` are treated as sensitive and will normally raise a
permission prompt. That is expected for an installer — ask for the
approval, don't route around it. If approval isn't available, stop and say
so plainly; do not silently continue to the CLAUDE.md wiring in step 4,
because a `CLAUDE.md` with `@.claude/*.md` imports and no files behind
them is worse than no install.

### 3. Enable nested delegation

The party's members call for aid mid-encounter — fighter and cleric spawn
helpers and consult `party:wizard` directly. That needs nested subagents
enabled, which is a setting in the project's own `.claude/settings.json`
(committed settings, not `settings.local.json`). The block:

```json
{
  "env": {
    "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "2"
  }
}
```

Additive, same as everything else here — read the file first, then apply
exactly one of these:

- **No `.claude/settings.json`** → create it with the block above.
- **Exists, no `env` key** → add the `env` object, leaving every other
  key untouched.
- **`env` exists without `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`** → add
  just that key alongside the existing ones.
- **The key is already set to any value at all** → leave it exactly as
  it is and report it. Never lower a value the user chose deliberately,
  and don't raise one either.

Preserve the file's existing formatting and key order; the result must be
valid JSON. If the existing file isn't valid JSON, don't try to repair
it — leave it alone and say so in the report.

This step is optional in the sense that the party still works without it:
with nesting off, fighter and cleric fall back to ending their turn with
a `NEEDS_WIZARD:` block for the main session to relay. If the write is
refused, note that and carry on — unlike step 2, it isn't a reason to
stop.

### 4. Wire up CLAUDE.md

**If the project has no `CLAUDE.md`:** copy
`${CLAUDE_PLUGIN_ROOT}/memory/CLAUDE.md.template` to `CLAUDE.md`
unchanged. It is a skeleton with `<angle-bracket placeholders>` the user
fills in — leave them in place and list them in the summary rather than
guessing at project details.

**If the project already has a `CLAUDE.md`:** add only what is missing.
Three blocks matter; check for each independently and insert only the
absent ones, taking the text verbatim from the template:

1. **The agent-party bullet** — the "Agent party" bullet from the
   template's Conventions section. Consider it present if the file already
   mentions `party:fighter` or otherwise documents the fighter/cleric/
   wizard protocol.
2. **The Session Zero bullet** — likewise from Conventions. Present if the
   file already mentions `/party:session-zero`.
3. **The Project memory section** — the whole `## Project memory` block,
   including the `@.claude/architecture.md`, `@.claude/gotchas.md`, and
   `@.claude/decisions.md` imports and the paragraphs about curated files
   vs. the append-only log. Present if the file already imports
   `@.claude/architecture.md`.

Placement:

- The two bullets go at the end of the existing `## Conventions` section.
  If there is no such section, create one at the end of the file.
- The `## Project memory` section is appended at the end of the file.

Do not reword, reorder, reformat, or delete a single line of the existing
CLAUDE.md. If a section exists but looks stale or partial, leave it alone
and flag it in the summary — the user decides.

### 5. Report

Print a short summary:

- **Created** — each file written, with its path.
- **Skipped** — each file left alone because it already existed, and for
  CLAUDE.md, which of the three blocks were already present.
- **Nested delegation** — which of the four cases step 3 hit: created
  `.claude/settings.json`, added the `env` object, added the depth key,
  or left an existing value alone (say what it is).
- **Your turn** — what the user still has to do by hand:
  - **Restart the session** if step 3 changed `.claude/settings.json`.
    An `env` setting is read at session start; until the restart, fighter
    and cleric will still fall back to the `NEEDS_WIZARD:` relay.
  - Fill the template's `<placeholders>` (project description, commands,
    layout, conventions), and seed the memory files with the project's
    real architecture notes, gotchas, and decisions. Empty memory files
    are wired-up but worthless; the party is only as good as what the
    project tells it.

Also confirm what is already live without any setup: the `party:fighter`,
`party:cleric`, and `party:wizard` agents and the `/party:session-zero`
skill come from the plugin itself and need no per-project installation.
