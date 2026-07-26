# Decisions

Why A over B, for choices below plan level. Loaded into every session —
keep entries short, newest first.

Format: `YYYY-MM-DD — decision — why`

2026-07-26 — Session Zero is exploration/chat mode with no exit
condition but the user's word (plan mode never Guide-initiated), and
explainability is calibrated by stakes × reversibility rather than
always-loud — the old "then hand off to plan mode" clause was what made
the Guide race to converge; uncalibrated depth is its own failure
(burying a naming question stops the user asking a second one).

2026-07-26 — Session Zero stays a single SKILL.md (no `references/`
progressive disclosure, no separate explain skill) and teaches its
visual idioms via ~5-line skeletons rather than a worked example
dialogue — there is no bulky lookup material to defer (the tech
explanations are per-question research, not a shippable catalogue), so
splitting would be the premature abstraction the skill now argues
against; and models imitate examples strongly, so a full transcript
would leak its topic and length into unrelated Session Zeros while a
skeleton leaks only shape.

2026-07-26 — Install scope stays the installer's choice (user-level
default for solo/trial, project-level for team repos), with
`/party:setup` as the real per-project opt-in gate — all project state
is written by setup, never the plugin, so a user-level install is inert
until a repo opts in; forcing project-level installs would add reinstall
friction with no benefit, while checked-in
`extraKnownMarketplaces`/`enabledPlugins` gives teams a shared party.
README documents both paths (verified against Claude Code docs
2026-07-26).

2026-07-26 — Plan-mode plans muster by default (mandatory Execution
section; table only on user request; no Guide discretion) — plan silence
previously meant solo execution and the muster silently didn't fire; the
plan text is what the executor reliably follows, so the instruction
rides inside the plan; plan-mode entry is the party-sized signal,
preserving the ceremony-tax decision (approval remains the consent
gate).

2026-07-25 — The fighter → cleric handoff is unconditional, never
gated on "the build looks clean" (and the same holds for Guide solo
builds) — dogfooded: a feature that passed a headless pixel smoke test
with zero JS errors still had 4 real bugs cleric found and fixed, two
visible in the first minute of play. Automated UI checks measure
rendering, not behavior, so "it looks verified" is precisely the
condition an independent reviewer exists for.

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
