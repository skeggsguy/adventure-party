# Decisions
Why A over B, ~2 lines each, newest first. Choice — rejected <alternative>, because <why>.

## 2026-11-06 — Publish as an `opencode/` folder on adventure-party's main
The port ships inside `skeggsguy/adventure-party` under `opencode/` (root LICENSE covers it; the plugin README links to it) — rejected a side branch, because visitors and clones only see `main` and a never-merged branch drifts from the shared protocol; rejected a separate repo, because one protocol in one place is less upkeep and each version advertises the other.

## 2026-11-06 — One master models file, stamped in by the installer; users override in `.local`
Each role's model + effort lives in `party-models.jsonc`, with a gitignored `party-models.local.jsonc` on top; `install.sh` writes `model: <id>#<effort>` into the six agent/command files — rejected per-file frontmatter edits, because the files are symlinked from the clone (edits conflict on pull), and rejected effort in frontmatter, because OpenCode ignores it (only `#variant` reaches the model, probed). Partly supersedes "Repo + symlinks": those six files become generated.

## 2026-11-06 — Public defaults run on OpenRouter; local Qwen is an override
Shipped defaults put Guide, Fighter and long-rest on `openrouter/qwen/qwen3.8-flash` — rejected shipping `local/qwen-*`, because a stranger has no local server; the README names Guide + Fighter as the token-heavy seats worth running locally. (Qwen3.8-Flash-Next itself isn't on OpenRouter; 3.8-flash is the nearest.)

## 2026-10-23 — Fresh fighter for every step and every fix round; no resume
Cleric hand-backs spawn a new fighter briefed with the hand-back and the previous fighter's DECISIONS and UNVERIFIED verbatim, plus where the step's diff is (reports aren't saved to files) — rejected resuming the same session, because all 30 logged resumes re-read their history with zero cache hits (median 96k tokens, ~6 min before the first token) and started near the 180k compaction line, where Step 6/7 compacted and went silent. Also rejected a compaction plugin to protect the Guide's latest message: it couples to OpenCode internals and other writers (retry notices, shell notices, nudges) land in the child session too.

## 2026-10-23 — Planner scopes steps by size; the fighter is never told to limit itself
`/plan` aims for steps editing up to ~6 files (tests included) and splits any step expected to edit more than 8 or to need open-ended investigation of unfamiliar code; peaks around 100k context are fine, 180k compaction is the line to stay clear of — rejected budget or "report early" rules in the fighter's prompt or spawn briefs, because the user wants the fighter to work unconstrained and sizing belongs to planning. Rejected a raw tool-call budget, because the planner can't count tool calls in advance; files edited is the visible proxy (0-4 files: 1 of 32 fighters compacted; 5-9: median peak 117k; 10+: 2 of 4 compacted).

## 2026-10-17 — MiMo Pro for session/plan/wizard; cleric on the rolling DeepSeek Flash alias
Root `model`, `build` pin, `/plan` and wizard → `openrouter/xiaomi/mimo-v2.6-pro` (fixed ID, no effort variant: MiMo takes no `reasoning_effort`; OpenRouter has no MiMo `latest` alias). Cleric → `~deepseek/deepseek-flash-latest#high` — rejected a pinned snapshot this time, because the user wants the cheap reviewer to track new Flash releases on its own; the 10-09 "fixed ID" rule still stands for the wizard's seat.

## 2026-10-11 — Sessions default to DeepSeek Pro high; `/zero` dropped
Root `model` is the `openrouter/deepseek-v4-pro-high` alias, and `/plan` uses it too — rejected local Qwen as the default and Opus for planning, because brainstorming wants a snappy strong model while the local GPU is saved for the token-heavy `/party` run. `/zero` removed: the `session-zero` skill triggers itself.

## 2026-10-09 — Tab-switch model plugin deferred; dogfood manual first
Keep Plan→Build model swaps manual (`/party` or `/models`) for now — rejected building the prompt-hook plugin yet, because the friction is unmeasured and the plugin reverses "no code"; revisit after dogfooding (design: see learnings 2026-10-09 "Tab-switch hook").

## 2026-10-09 — Guide low-effort via root-model alias, not agent pin
The Guide defaults through `model: local/qwen-guide` (an alias of the same server model with effort low) — rejected pinning `agents.build.model`, because a primary agent's configured model does not seed new sessions (probed: an agent set to none-effort still produced a full scratchpad; variants proved sent via a `#probe` variant killing thinking).

## 2026-10-09 — Wizard on deepseek-v4-pro (fixed ID), cleric on v4-flash
Split the two DeepSeek seats by tier — rejected same-model-different-effort and the `deepseek-pro-latest` alias, because cleric volume wants cheap while wizard stakes want pro, and a fixed ID stops a silent upstream `latest` swap changing the wizard mid-quest.

## 2026-10-09 — Experience files stay in `.claude/`
Memory lives in the project's `.claude/` — rejected `.opencode/`, because projects worked from both harnesses must share one memory and the folder name is cosmetic.

## 2026-10-09 — Relay is the primary wizard path
Members escalate via `NEEDS_WIZARD:` and the Guide resumes their session with the verdict — rejected plugin-style nesting, because OpenCode V2 subagents cannot spawn subagents and resume-by-session-ID makes the relay first-class anyway.

## 2026-10-09 — Commands are the model hand-offs
`/plan` sets the session to DeepSeek Pro, `/party` to Qwen (was `/zero`+`/plan` → Opus until 2026-10-11) — rejected relying on agent selection to change models, because only a command's `model` override beats the session's stored model.

## 2026-10-09 — Lean AGENTS.md fragment + party-run skill
Trigger rules (~1.9k chars) in global AGENTS.md, run mechanics in a skill loaded on muster — rejected shipping the whole protocol ambient, because AGENTS.md reaches subagents too (probed: explore quoted it verbatim) and a low-effort Guide follows ten crisp rules better than forty dense ones.

## 2026-10-09 — Repo + symlinks as the install
This repo is the source of truth; `install.sh` symlinks into `~/.config/opencode` — rejected copying files in or a plugin, because symlinks give live-reload edits and nothing here needs code.

## 2026-10-09 — Config migrated to V2 native shape in one pass
`providers`/`package`/`settings`, ordered `permissions`, variant arrays — rejected staying on the V1 compat layer, because custom variants and the haiku helper pins configure cleanly in the native shape (V1 backup kept at `opencode.jsonc.v1-backup-20261009`).
