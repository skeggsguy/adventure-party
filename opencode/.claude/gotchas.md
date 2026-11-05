# Gotchas

- OpenCode does NOT hot-reload an EDITED command/agent markdown file (new files register instantly, edits are stale) — after `git pull`, run `opencode service restart` or edits to commands/agents silently don't apply.
- `opencode run "/cmd"` expands the command template but IGNORES its frontmatter (`agent`/`model`); the TUI and `POST /api/session/{id}/command` apply them — smoke-test command model hand-offs via the API, never via CLI `run`.
- The command POST needs `name`, `arguments` AND `text` (the raw `/name args` line) — a payload without `text` 400s with "Missing key at [text]".
- `opencode api get /api/agent` returns agent models as `{id, providerID, variant}` under `data` — useful ground truth for "which model/variant did this agent actually resolve to?".
- Anthropic models via OpenRouter do NOT cache unless the model has `"settings": { "cache_control": { "type": "ephemeral" } }` — OpenCode 2.0.20 skips cache breakpoints on OpenRouter routes. Any new `openrouter/anthropic/*` model needs that line; DeepSeek caches without it. Check: `cache.read`/`cache.write` in `session_message.data`.
- `opencode api --standalone get /api/agent` (and `/api/model`) returns `data: []` on 2.0.20 — it answers before config loads. To see what a fresh load resolves without restarting the user's service, run a private `opencode serve --hostname 127.0.0.1 --port N`, take the password from its stdout, poll `curl -u opencode:<pw> …/api/agent` until agents appear, then kill it.
