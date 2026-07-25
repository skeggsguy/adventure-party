---
name: setup
description: Install the Adventure Party experience system (project
  memory) into the current project — seeds the four experience files
  into .claude/, creates party.json, enables nested delegation, wires
  the party protocol, Session Zero, and experience sections into
  CLAUDE.md (migrating party-authored blocks from older plugin
  versions), and offers the opt-in experience display. Run once per
  repo, by hand.
disable-model-invocation: true
---

# Party Setup

The agents and skills arrive with the plugin. The experience system
(the project's memory files) cannot — a plugin ships its own files, it
never writes into a project's `.claude/`. This skill closes that gap:
it seeds the experience files and the CLAUDE.md wiring the party reads
its law from, and turns on the nested delegation the party members use
to call for aid.

Run it once per project; re-running is safe and is also the upgrade
path. The promise, stated honestly: **setup never touches your
content; it may update party-authored blocks it can fingerprint** (see
step 5a's migration).

## Source files

Everything is copied out of the installed plugin:

- `${CLAUDE_PLUGIN_ROOT}/memory/architecture.md`
- `${CLAUDE_PLUGIN_ROOT}/memory/gotchas.md`
- `${CLAUDE_PLUGIN_ROOT}/memory/decisions.md`
- `${CLAUDE_PLUGIN_ROOT}/memory/learnings.md`
- `${CLAUDE_PLUGIN_ROOT}/memory/CLAUDE.md.template`
- `${CLAUDE_PLUGIN_ROOT}/memory/legacy-blocks.md` (step 5a matches against it)
- `${CLAUDE_PLUGIN_ROOT}/skills/config/SKILL.md` (step 6 references it)

If any of those paths cannot be read, stop and say so — do not
reconstruct the file contents from memory. Read the plugin version from
`${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`; the version markers
below use it.

## Steps

### 1. Confirm the target

The target is the current project's root — the directory holding (or about
to hold) `CLAUDE.md` and `.claude/`. State it before writing anything. If
the working directory is clearly not a project root (no repo, no source
tree), ask before proceeding.

### 2. Seed the four experience files

For each of `architecture.md`, `gotchas.md`, `decisions.md`,
`learnings.md`:

- If `.claude/<file>` already exists → **skip it**, record it as skipped,
  and do not read or modify it.
- Otherwise copy the plugin's copy verbatim into `.claude/<file>`.

Create `.claude/` if it does not exist. Never merge into an existing
experience file — a project that already has one has its own content
there.

Writes under `.claude/` are treated as sensitive and will normally raise a
permission prompt. That is expected for an installer — ask for the
approval, don't route around it. If approval isn't available, stop and say
so plainly; do not silently continue to the CLAUDE.md wiring in step 4,
because a `CLAUDE.md` with `@.claude/*.md` imports and no files behind
them is worse than no install.

### 3. Create `.claude/party.json`

If it doesn't exist, create it as:

```json
{
  "experience": {
    "enabled": false
  }
}
```

If it exists, leave it exactly as it is. This is the user's one config
file — model overrides and the experience display live here; `/party:config`
applies it. Absent keys mean plugin defaults.

### 4. Enable nested delegation

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
a `NEEDS_WIZARD:` block for the main session (the Guide) to relay. If
the write is refused, note that and carry on — unlike step 2, it isn't a
reason to stop.

### 5. Wire up CLAUDE.md

**If the project has no `CLAUDE.md`:** copy
`${CLAUDE_PLUGIN_ROOT}/memory/CLAUDE.md.template` to `CLAUDE.md`
unchanged. It is a skeleton with `<angle-bracket placeholders>` the user
fills in — leave them in place and list them in the summary rather than
guessing at project details.

**If the project already has a `CLAUDE.md`:** first migrate, then add
what's missing.

**5a. Migration — fingerprinted party blocks from older plugin
versions.** Older setups wired their era's protocol text verbatim, and
that text now contradicts the current rules (it commanded auto-summoning,
and its memory section predates the experience/XP system). Because it
was inserted verbatim, it is exact-matchable: the complete legacy blocks
ship in `${CLAUDE_PLUGIN_ROOT}/memory/legacy-blocks.md` — read that
file; do not reconstruct old text from memory. Look for:

- The 0.3.x Conventions bullets (opening `**Summon the party — don't
  build alone.**`, plus the `**Plans name their executor.**` and
  `- Party mechanics:` companions)
- The 0.2.x `- Agent party (from the ` bullet
- The legacy `## Project memory` section (this one matters even though
  5b would count it as "present" — the old text lacks the XP paragraph
  and tells sessions to distill "periodically", which conflicts with the
  Long Rest owning distillation)

For each candidate block: compare it against the legacy-blocks.md
variants. **Exact match** → unmodified: show the user the old text and
the current template's replacement as a diff, and replace on their
confirmation. **Opening matches but body differs from every shipped
variant** → hand-modified: do NOT touch it — print the current template
block and tell the user to merge by hand. Never migrate without showing
the diff first.

**5b. Additive wiring.** Three blocks matter; check for each
independently and insert only the absent ones, taking the text verbatim
from the template. Every block this step inserts is preceded by a
version-marker comment line, `<!-- party@<version> -->`, so future
setups can fingerprint it by lookup instead of forensics:

1. **The muster bullet** — the "The party musters on command" bullet
   from the template's Conventions section (plus its companions "Plans
   name their executor when they delegate" and "Party mechanics").
   Consider them present if the file mentions `party:fighter` — but
   only after 5a has had its chance to migrate old text.
2. **The Session Zero bullet** — likewise from Conventions. Present if
   the file already mentions `/party:session-zero`.
3. **The experience section** — the whole `## Project memory — the
   party's experience` block, including the `@.claude/architecture.md`,
   `@.claude/gotchas.md`, and `@.claude/decisions.md` imports, the
   curated-vs-log paragraphs, and the XP paragraph. Present if the file
   already imports `@.claude/architecture.md`.

Placement:

- The bullets go at the end of the existing `## Conventions` section.
  If there is no such section, create one at the end of the file.
- The experience section is appended at the end of the file.

Beyond 5a's confirmed migrations, do not reword, reorder, reformat, or
delete a single line of the existing CLAUDE.md. If a section exists but
looks stale or partial, leave it alone and flag it in the summary — the
user decides.

### 6. Offer the experience display (opt-in)

Ask one question: *"Want the experience display? A statusline showing
the party's level and XP, plus a one-line level-up banner at session
start. Both are local shell scripts — zero tokens, per-user (not
committed), and removable. [yes/no]"*

- **No** → skip; note in the report that `/party:config` can wire it
  later (set `experience.enabled` to `true` in party.json and run it).
- **Yes** → set `"enabled": true` in `.claude/party.json`, then read
  `${CLAUDE_PLUGIN_ROOT}/skills/config/SKILL.md` and perform its
  "Applying `experience`" section exactly — that skill owns the wiring
  (pre-checks, atomicity, the Windows-native decline, the
  existing-statusline decline). Don't reimplement it from memory here.

### 7. Report

Print a short summary:

- **Created** — each file written, with its path.
- **Migrated** — each CLAUDE.md block replaced in 5a (or refused as
  hand-modified, with what to do).
- **Skipped** — each file left alone because it already existed, and for
  CLAUDE.md, which blocks were already present.
- **Nested delegation** — which of the four cases step 4 hit.
- **Experience display** — opted in or not; what was wired, declined,
  or left for `/party:config`.
- **Your turn** — what the user still has to do by hand:
  - **Restart the session** if step 4 or step 6 changed a settings
    file. Settings are read at session start; until the restart,
    fighter and cleric fall back to the `NEEDS_WIZARD:` relay and the
    statusline stays as it was.
  - Fill the template's `<placeholders>` (project description, commands,
    layout, conventions), and seed the experience files with the
    project's real architecture notes, gotchas, and decisions. Empty
    experience files are wired-up but worthless; the party is only as
    good as what the project tells it.

Also confirm what is already live without any setup: the `party:fighter`,
`party:cleric`, and `party:wizard` agents and the `/party:session-zero`,
`/party:config`, and `/party:level-up` skills come from the plugin itself
and need no per-project installation.
