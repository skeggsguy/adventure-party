# Decisions

Why A over B, for choices below plan level. Loaded into every session —
keep entries short, newest first.

Format: `YYYY-MM-DD — decision — why`

2026-07-26 — Plan-mode plans muster by default (mandatory Execution
section; table only on user request; no Guide discretion) — plan silence
previously meant solo execution and the muster silently didn't fire; the
plan text is what the executor reliably follows, so the instruction
rides inside the plan; plan-mode entry is the party-sized signal,
preserving the ceremony-tax decision (approval remains the consent
gate).

2026-07-25 — Model overrides apply at spawn time (Agent tool `model`
param, wired into the muster bullet) instead of generated
`.claude/agents/` override files — live test proved project agent files
do NOT shadow `party:<name>` (they coexist; namespaced spawns get the
plugin copy), so generation could never work; the param outranks
frontmatter and needs no files that rot.

2026-07-25 — Level-ups trigger the Long Rest (`/party:level-up`):
distill learnings into curated experience files, prune stale gotchas,
append a plain-language CHRONICLE.md entry, award a seeded title/badge —
recognition alone is the sub-10-star-graveyard pattern; bolting the
level-up to the distillation chore nobody otherwise does makes the
metaphor literally true (a leveled party is a better-informed party).
Token cost is real, so it is user-invoked only, never automatic.

2026-07-25 — Party musters only on explicit command, approved plan, or a
Guide *suggestion* (reverses the auto-summon rule) — the ceremony tax is
the single most documented failure mode of workflow plugins (Superpowers,
Spec Kit); the human decides when the party rides.

2026-07-25 — Main-session role renamed "the Guide"; scrub the tabletop
brand name and its trademarked game-master title from all shipped copy —
those two terms are protected; generic archetypes (fighter/cleric/
wizard/party/XP/session zero) are not; "Guide" matches the teaching
role for the non-engineer audience. User model config lives in
`.claude/party.json`, applied by `/party:config`; defaults unchanged
(fighter=Opus, cleric/wizard=Fable).

2026-07-25 — Memory rebranded "experience"; XP = dated entries in
learnings.md ONLY (append-only, so XP never decreases and survives
distillation); surfaced via statusline + SessionStart banner, both
shell-script-only and opt-in at setup — theme must label real mechanics
(the XP number is literally the health of project memory); always-on
token-costing hooks are a named plugin failure pattern.

<!-- Record the decision AND the rejected alternative with the reason —
     future sessions re-litigate choices whose "why" isn't written down. -->
