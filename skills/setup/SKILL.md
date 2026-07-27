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
reconstruct the file contents from memory.

A `<!-- party@X.Y.Z -->` marker records when that block's **text** last
changed, not the installed plugin version — so it is copied verbatim
from the template and never restamped. A marker that trails the plugin
version is a block that hasn't changed since, which is exactly what step
5a needs to know.

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
  "//": "To change a party member's model, add it under \"models\" — fighter, cleric, or wizard, set to opus, sonnet, haiku, or fable — then run /party:config. Empty or absent means the plugin's default.",
  "models": {},
  "experience": {
    "enabled": false
  }
}
```

JSON has no comments, so the `"//"` key is the comment: an inert string
`/party:config` ignores by name. It ships because the file was
otherwise silent about `models` — a user with no reason to suspect the
key exists has no way to discover it from the file they're told is the
one they edit.

`"models": {}` is deliberately empty, and empty means exactly what
absent means: every member resolves to the plugin's own default. Never
write the current defaults in as values — a snapshotted `"cleric":
"fable"` is a silent pin that survives a plugin update that changes
that default. The empty object shows the user where an override goes
without committing them to one.

**If it exists**, leave the existing keys exactly as they are. One
additive exception: if the file has neither a `"//"` key nor a `models`
key, it predates this text and is missing the pointer — show the user
the `"//"` line and add it on their confirmation, changing nothing
else. Declining is fine; say `/party:config` reports the lineup either
way. This is the user's one config file — model overrides and the
experience display live here; `/party:config` applies it. Absent keys
mean plugin defaults.

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
that text now contradicts the current rules (the oldest variants
commanded auto-summoning, 0.4.x made plan silence mean solo execution,
and old memory sections predate the experience/XP system). Because it
was inserted verbatim, it is exact-matchable: the complete legacy blocks
ship in `${CLAUDE_PLUGIN_ROOT}/memory/legacy-blocks.md` — read that
file; do not reconstruct old text from memory. Look for:

- The 0.4.x Conventions bullets (opening `**The party musters on
  command, not by default.**` with the old trigger (b), "an approved
  plan names party members as executors", plus its `**Plans name their
  executor when they delegate.**` companion). Fingerprint them by the
  preceding `<!-- party@0.4.0 -->` marker line, or by exact body match
  against legacy-blocks.md. Their `- Party mechanics:` companion is
  unchanged in 0.5.0 — leave it in place. Note this bullet's opening
  line is identical in 0.5.0, so the opening line alone proves nothing:
  a block preceded by a `<!-- party@0.5.0 -->` marker, or whose body
  matches the current template, is already current — skip it silently
  rather than reporting it as hand-modified.
- The 0.5.0 Session Zero bullet — the variant whose body opens "invoke
  when scoping new work or weighing approaches" and calls the dialogue
  "collaborative quest-shaping". The 0.6.0
  replacement describes exploration/chat mode and the no-self-initiated-
  plan-mode rule, which the old three-line body doesn't cover. Its
  `<!-- party@0.5.0 -->` marker is **not** a fingerprint on its own —
  0.5.0 also marked the muster and experience blocks, which are current
  — so match on the body against legacy-blocks.md.
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
   from the template's Conventions section (plus its companions
   "Plan-mode plans muster the party by default" and "Party mechanics").
   Consider them present if the file mentions `party:fighter` — but
   only after 5a has had its chance to migrate old text.
2. **The Session Zero bullet** — likewise from Conventions. Present if
   the file already mentions `/party:session-zero` — again, only after
   5a has had its chance to migrate the old variant.
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
  (pre-checks, atomicity, the proved-interpreter choice and its
  decline, the existing-statusline decline). Don't reimplement it from
  memory here, and in particular don't decline on your own read of the
  platform — the interpreter is chosen by probing, not by detection.

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
