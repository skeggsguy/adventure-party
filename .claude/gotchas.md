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
- No `jq` and no `gh` in this WSL — CLAUDE.md's documented manifest
  check can't run as written; validate with `python3 -m json.tool`
  instead. Git pushes go over SSH (an HTTPS remote can't prompt for
  credentials mid-session).
- Examples in a skill get imitated wholesale, topic and length included
  — ship skeletons of form (`| Option | What it is | Costs you |`), never
  a worked transcript, or a database example turns up in a CSS answer.
- Audit shipped instructions for what they imply about *when to stop*
  and for mandates with no governor — one stray "then hand off to plan
  mode" made a whole exploration skill rush, and "explain everything"
  with no depth ladder buries trivial questions.
- Test a load-bearing platform assumption with a live sentinel before
  building machinery on it. Adversarial review called the agent-override
  design "fragile"; only the live test showed it was impossible.
