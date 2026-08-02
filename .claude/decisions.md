# Decisions

Why A over B, for choices below plan level. Read before choosing between
approaches — newest first.

Format: `YYYY-MM-DD — decision — why`. Budget ~2 lines: the choice, the
rejected alternative, one why-clause, and `see learnings YYYY-MM-DD`
pointing at the argument. `/party:long-rest` compacts anything over.

2026-08-02 — The hireling runs its CLI foreground-preferred under a timeout
(interrupted → resume via the CLI's own mechanism, discovered from its help
at need), backgrounding only when no resume mechanism exists — over a
probed-and-stored resume command (an unproven stored command, or another
paid call for a failure-path-only mechanism) and over pure foreground,
which the ten-minute cap forbids. See learnings 2026-08-02.

2026-08-02 — `/party:hire`'s choices ride AskUserQuestion (clickable options,
consent gates included); the CLI picker offers what a `command -v` sweep
finds installed, plus Other — over hardcoded vendor names (offers tools the
user may not have; a shipped list that rots visibly) or free-typed commands
(the flow this replaces, where Enter sends the message mid-thought).

2026-08-02 — Model names for the pin menu come from the CLI's own listing
first, WebSearch only as fallback, and search results populate the *menu*
only — the value written to `party.json` is what the smoke test proved runs
— over web-search-first, which reports last month's blog post, not this
install.

2026-08-02 — The probe also settles a reasoning-effort flag, offered at pin
time only when the CLI has one and stored as just another flag in `run` —
over a `party.json` schema field or skipping effort, which benchmarks show
changes real capability rank across vendors; the smoke test validates the
model+effort combo.

2026-08-02 — `/party:hire` pins a model into the stored run command by
default (user's choice of model, decline allowed) — over inheriting the
CLI's own config, under which a CLI update silently changes what a standing
hire means and the party can't see or manage it from `party.json`.

2026-08-01 — Foreign coding CLIs stand in for party members via one generic
hireling agent + `/party:hire` skill + a `hired` map in `party.json` — over
per-tool/per-role agents (duplicate always-loaded descriptions) or
re-skinning fighter (theme lies, mode is global). See learnings 2026-08-01.

2026-08-01 — `/party:hire` probes the CLI's flags at hire time, smoke-tests,
and stores the resolved command in `party.json`; unknown CLIs fall back to a
user-supplied command — over a shipped flag table, which rots as CLIs
change. See learnings 2026-08-01.

2026-08-01 — Hires are standing config state; the Guide is never hireable —
over per-task summons, one more path to explain for marginal gain.

2026-07-30 — The `.claude/` experience files are read on demand against
per-file triggers in `hooks/instructions.md`, not injected — over per-file
hook entries under the 10,000-char cap, a silent failure policed forever.
See learnings 2026-07-30.

2026-07-29 — Instructions are served live from a SessionStart hook and
nothing is copied into a repo — over the template plus better migration
tooling, since the drift that tooling manages is created by the copying.
See learnings 2026-07-29.

2026-07-29 — The hook is one SessionStart block of one-line `cat`s on
plain stdout, matcher omitted — over JSON `additionalContext` or one entry
per file, elaborations the spike proved bought nothing. *Amended
2026-07-30:* one `cat`, not two. See learnings 2026-07-29.

2026-07-28 — The XP statusline and banner are dropped, the level-up
nudge moving to the moment the Guide appends a learning — over patching
the interpreter probe again, because ~70 lines of the repo's most
bug-prone instruction existed to render one line. See learnings
2026-07-28.

2026-07-27 — Decisions entries get a length budget — over pruning them
at the Long Rest, or leaving it: the prune gate tests *truth*, and a
decision never stops being true. *Amended 2026-07-29:* ~2 lines,
enforced at the Long Rest's compact step, because a writer still holding
the argument cannot apply a budget to it. See learnings 2026-07-27.

2026-07-27 — Session Zero becomes a phase work passes through by
default, its bullet deciding the case rather than describing the mode —
over `@`-importing SKILL.md, growing the bullet or adding trigger
examples, which all feed a classification step that was never disputed.
See learnings 2026-07-27.

2026-07-27 — *Superseded 2026-07-29:* `<!-- party@X.Y.Z -->` markers
versioned block *text* and were legended rather than restamped at
release. The whole marker scheme died with the copied-text machinery.

2026-07-27 — Dogfooding runs the source via `claude --plugin-dir .`,
never the installed plugin — install snapshots the marketplace clone
into a version-keyed cache, so sitting in the source repo is not running
it. See learnings 2026-07-27.

2026-07-26 — The manifest check uses `python3 -m json.tool`, not `jq`,
and the frontmatter check keeps PyYAML with an install note — over a
stdlib-only validator, which trades a real parser for regex and adds a
shipped artifact. See learnings 2026-07-26.

2026-07-26 — Wizard stays read-only: no `Bash`, no `memory:`, turn cap
raised 15 → 25 instead — a shell is a write primitive, so granting one
downgrades READ-ONLY from a structural guarantee to a promise. See
learnings 2026-07-26.

2026-07-26 — The party reaches the experience system through a
`LEARNED:` line in each member's report, not by writing the files itself
— a subagent's context dies with its turn, so the final message is the
only carrier. See learnings 2026-07-26.

2026-07-26 — Cleric's repair scope is the change and its blast radius,
`NEEDS_REBUILD:` a high bar — over an unbounded "fix everything you
find", which lets a reviewer redo working code to taste. Defect vs.
preference is the gate, never size. See learnings 2026-07-26.

2026-07-26 — session-zero's `description` is a router, not a summary:
cut to 689 chars by dropping every behavior clause — not cut to sibling
length (~250), since the other skills route nothing. See learnings
2026-07-26.

2026-07-26 — `party.json`'s `models` takes stable tiers
(opus/sonnet/haiku/fable), never model IDs, so a new model release never
forces a config edit; absent or empty means "member's default", so no
snapshotted pin outlives a future default change.

2026-07-26 — Session Zero is exploration/chat mode ending only on the
user's word, explainability calibrated by stakes × reversibility — over
"then hand off to plan mode", the clause that made the Guide race to
converge. See learnings 2026-07-26.

2026-07-26 — Session Zero stays a single SKILL.md teaching its idioms
via ~5-line skeletons — over `references/` disclosure or a worked
dialogue, because a transcript leaks its topic and length where a
skeleton leaks only shape. See learnings 2026-07-26.

2026-07-26 — Install scope stays the installer's choice — forcing
project-level adds reinstall friction with no benefit. *Amended
2026-07-29:* scope is now the **only** gate, so a user-level install is
live in every repo. See learnings 2026-07-26.

2026-07-26 — Plan-mode plans muster by default via a mandatory Execution
section — over plan silence meaning solo execution, under which the
muster silently didn't fire; the plan text is what the executor reliably
follows. See learnings 2026-07-26.

2026-07-25 — The fighter → cleric handoff is unconditional, never gated
on "the build looks clean" — dogfooded: a feature that passed a headless
smoke test with zero JS errors still had 4 real bugs, because such
checks measure rendering, not behavior. See learnings 2026-07-25.

2026-07-25 — Model overrides apply at spawn time via the Agent tool's
`model` param — over generated `.claude/agents/` override files, which a
live sentinel proved could never work: project agent files do not shadow
`party:<name>`. See learnings 2026-07-25.

2026-07-25 — Recognition is bolted to the distillation chore nobody
otherwise does, so a leveled party is a better-informed one — over
recognition on its own, the sub-10-star-graveyard pattern. *Amended
2026-07-29:* the trigger is `/party:long-rest`, one level per rest, not
an XP threshold. See learnings 2026-07-25.

2026-07-25 — The party musters only on explicit command, approved plan,
or an accepted Guide *suggestion*, reversing the auto-summon rule — the
ceremony tax is the most documented failure mode of workflow plugins.
See learnings 2026-07-25.

2026-07-25 — Main-session role renamed "the Guide" and the tabletop brand
name plus its trademarked game-master title are scrubbed from all shipped
copy — over keeping them, because those two terms are protected where the
generic archetypes (fighter/cleric/wizard/party) are not. See learnings
2026-07-25.

2026-07-25 — Memory is rebranded "experience" — theme must label real
mechanics, never replace them, because the files are literally the
project's memory. *Amended 2026-07-28:* the XP number and its
statusline/banner display are gone. See learnings 2026-07-28.

<!-- Record the decision AND the rejected alternative with the reason —
     future sessions re-litigate choices whose "why" isn't written down. -->
