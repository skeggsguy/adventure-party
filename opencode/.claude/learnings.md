# Learnings (inbox)

## 2026-10-11 — the TUI does seed from the default agent's model
The 10-09 "agent model ≠ session model" probe ran headless (API/`opencode run`), where the root `model` wins. The TUI is different: after root `model` became DeepSeek Pro, a fresh TUI in this repo still showed Qwen — the `build` pin (`local/qwen-flash-next#fast`). Keep `agents.build.model` equal to the root `model`.

## 2026-10-09 — agent model ≠ session model; alias is the way
A primary agent's configured `model` does NOT seed new sessions — confirmed with a probe agent set to a `#probe` (none-effort) variant: it still produced a full scratchpad. The session's model comes from the config root `model`. Fix: the `local/qwen-guide` alias (modelID → qwen-flash-next, `settings.reasoningEffort: "low"`), set as root, gives the Guide low effort. Confirmed live: an alias with `reasoningEffort: "none"` suppressed the scratchpad entirely.

## 2026-10-09 — commands ARE the model hand-offs (but only via TUI/API)
A command's `model` override beats the session model — verified: a command fronted `model: local/no-such-model-probe` failed the session on exactly that model, and a fresh command on `qwen-flash-next#fast` landed on it. BUT `opencode run "/cmd"` ignores command frontmatter (template only); the TUI/API honor it. This is why `/zero`, `/plan`, `/party` are the Opus↔Qwen switches, and why smoke tests must use the API.

## 2026-10-09 — OpenCode sends variant effort to the local server
The local provider had no captured `reasoning_effort` in historical corpus traffic, but custom variants DO forward it: variant `#probe` (`reasoningEffort: "none"`) killed the llama.cpp scratchpad, `#fast`/`#deep` behave as low/xhigh. So effort-per-role via `#variant` works end-to-end on `@ai-sdk/openai-compatible`.

## 2026-10-09 — Tab-switch hook: designed, deferred
Auto model swap on Plan↔Build Tab is feasible as one ~50-line V2 plugin (pattern: `~/.config/opencode/plugins/auto-continue.ts`): `ctx.session.hook("prompt", …)` + `ctx.session.switchModel(…)`, acting only when the session's agent changed since its last prompt (so `/zero` on build+Opus and hand-picked models are never stomped). No documented "agent switched" event exists, so the label updates on next message, not on Tab. Unprobed: whether the switch applies to the admitting prompt or only the next. Map (plan→opus#high, build→qwen-guide) belongs in plugin options in opencode.jsonc.

## 2026-10-09 — subagents see global AGENTS.md
Unlike the Claude Code plugin (where hook-injected context is main-session-only), OpenCode gives subagents the global AGENTS.md too — `explore` quoted it verbatim when spawned as a child. So the party fragment must stay lean and phrase rules as "the Guide does X" (members read it, shouldn't act on it).

## 2026-11-06 — Effort reaches a subagent only through a `#variant`
Probed with a request-capturing fake provider (OpenCode 2.0.20, `--standalone`, isolated XDG dirs): a subagent with `model: probe/m#deep` sent `reasoning_effort: xhigh`; the same agent with `reasoningEffort:` flat, under `options:`, or under `settings:` in frontmatter sent nothing — silently ignored. Separately, OpenRouter models ship built-in variants (`qwen/qwen3.8-flash`: none/high/max — it has no effort levels, only a thinking toggle + budget, so OpenCode's `high`/`max` send `reasoning.max_tokens` 65536/131071 and `none` sends `enabled: false`; `~deepseek/deepseek-flash-latest`: none/low/high/max; `xiaomi/mimo-v2.6-pro`: none/thinking), so `model#<variant>` needs no user config when the name matches a built-in. `opencode run --agent X` ignores a primary agent's own model, and `opencode models` printed nothing under isolated dirs — read `opencode api get /api/model` (variants per model) instead.
