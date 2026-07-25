# Gotchas

Non-obvious traps. Loaded into every session — keep each entry to 1–2 lines
and delete entries once the underlying cause is fixed.

<!-- Each entry: the trap, why it bites, and where it's pinned (a test that
     locks the invariant in place, if one exists). Example shape:

- Library X silently ignores option Y unless Z also rides the call — don't
  "simplify" the pairing. Pinned in tests/test_x.py.
-->

- A project `.claude/agents/<name>.md` does NOT shadow the plugin's
  `party:<name>` — they coexist, and namespaced spawns always get the
  plugin copy (verified 2026-07-25). Model overrides must ride the Agent
  tool's per-invocation `model` param instead.
- Skills with `disable-model-invocation: true` don't appear in the
  model's skill list — a headless "list your skills" smoke test shows
  only session-zero; that's correct, not a packaging bug.
