# Gotchas

Non-obvious traps. Read before the first edit of a session, a one-line one
included — keep each entry to 1–2 lines and delete entries once the
underlying cause is fixed.

<!-- Each entry: the trap, why it bites, and where it's pinned (a test that
     locks the invariant in place, if one exists). Example shape:

- Library X silently ignores option Y unless Z also rides the call — don't
  "simplify" the pairing. Pinned in tests/test_x.py.
-->

- A project `.claude/agents/<name>.md` does NOT shadow the plugin's
  `party:<name>` — they coexist, and namespaced spawns always get the
  plugin copy (verified 2026-07-25). Model overrides must ride the Agent
  tool's per-invocation `model` param instead.
- Agent AND skill frontmatter descriptions are plain YAML scalars: a
  literal `": "` or a line-ending colon breaks parsing ("mapping values
  are not allowed here") and silently unloads the file. Use em dashes,
  and run the frontmatter check (CLAUDE.md Commands) over `agents/` too
  — scoping this gotcha to skills is why two agents shipped broken.
- An agent's `memory:` scope auto-enables Read/Write/Edit for its memory
  dir, so it silently widens a deliberately read-only `tools:` allowlist
  — or is inert if `tools:` wins; both bad. Wizard dropped it; durable
  insight rides its `LEARNED:` line into the experience files instead.
- Skills with `disable-model-invocation: true` don't appear in the
  model's skill list — a headless "list your skills" smoke test shows
  only session-zero; that's correct, not a packaging bug. But
  `claude --plugin-dir . -p '/party:<skill>'` still runs the body
  headlessly — that's the real smoke test. See learnings 2026-08-01.
- The built-in tool roster varies per install (server-side bucketing), so
  shipped prose names the *outcome*, never a tool — "count without reading
  it", not "use Grep"; a frontmatter `tools:` list IS honored and
  resurrects a pruned tool. See learnings 2026-07-29.
- When a helper reports a diff, ask "against what" before "is it true" — a
  dirty tree makes `HEAD` the wrong baseline, and this repo's `.claude/`
  files are dirty more often than not. See learnings 2026-07-29.
- Renumbering a skill's ceremony breaks prose *outside* the list —
  invariants like "happens last" carry no step number, so grep can't find
  them; re-read the whole file. See learnings 2026-07-29.
- A fixture testing whether a file was *consulted* must make its evidence
  unobtainable any other way — ask what a model that never opened the file
  could still produce. See learnings 2026-07-30.
- Tags are off the distribution path (merging to `main` is the release), so
  an untagged release shows no symptom — check `git tag -l` against
  `plugin.json`'s version at every bump. See learnings 2026-07-31.
- A behavioral ban must land on the act and assign the decision to a person
  — any qualifier ("silent", "unnecessary") becomes the loophole and gets
  obeyed instead of the verb. See learnings 2026-08-01.
- A user-supplied model name is a claim to verify, not config to record:
  marketing tier names ("luna") aren't API strings (`gpt-5.6-luna`), and a
  pinned model needs its own smoke test — `-m` changes the command under
  test. See learnings 2026-08-02.
- No `gh` in this WSL, and git pushes go over SSH (an HTTPS remote can't
  prompt for credentials mid-session).
- A documented dev command is only real if it runs on a stock machine:
  `jq` ships nowhere by default, and PyYAML is a separate package on
  Debian/Ubuntu. Python's *stdlib* (`json.tool`, `re`) is the portable
  floor; anything above it needs an install note.
- Examples in a skill get imitated wholesale, topic and length included
  — ship skeletons of form (`| Option | What it is | Costs you |`), never
  a worked transcript, or a database example turns up in a CSS answer.
- Audit shipped instructions for what they imply about *when to stop*
  and for mandates with no governor — one stray "then hand off to plan
  mode" made a whole exploration skill rush, and "explain everything"
  with no depth ladder buries trivial questions.
- Before building on a platform assumption, read the field reference AND
  sentinel-test it — docs settle what a field *does* (`memory:` quietly
  enables write tools), live tests settle composition (docs claimed
  project agents override plugin ones; only the sentinel showed they
  coexist).
- On Windows, `bash` on PATH is `C:\WINDOWS\system32\bash.exe` — the WSL
  shim, not Git Bash (`uname` says Linux). "Is bash resolvable?" is
  therefore never a valid POSIX-shell check there.
- Same trap, different name: `convert` on Windows PATH is
  `System32\convert.exe` (the filesystem converter), NOT ImageMagick —
  it fails with "Invalid Parameter". `command -v` finding a name proves
  nothing about what it is. PIL is present and is the reliable image
  tool here; note `python3` is win32, so it does not share Git Bash's
  `/tmp`.
- `marketplace.json` sets `"source": "./"`, so the plugin is the whole
  repo and `/plugin install` clones it — `assets/` and every superseded
  binary blob ship to every user. Size binaries at commit time (README
  hero renders at width 480, so 960px is the ceiling); there is no
  package step to catch it later.
- Git Bash on Windows PATH is a property of the *launch chain*, not the
  machine: `Git\usr\bin` is absent from the persistent PATH but present
  in a terminal opened from Git Bash — so a PATH-dependent interpreter in
  a shipped subprocess (the SessionStart hook) dies silently when the user
  launches differently.
- `/plugin install` and `/reload-plugins` never fetch origin — they
  snapshot the local *marketplace clone* into a version-keyed cache, and
  auto-update is off by default for third-party marketplaces. So the
  installed plugin can silently trail a just-pushed release: dogfood this
  repo with `claude --plugin-dir .`, never the installed copy.
- The marketplace clone's `origin/main` ref is not evidence of what it
  has fetched — a marketplace update leaves the ref stale while moving
  the checkout (fetch-to-`FETCH_HEAD` shape). Only its HEAD is truthful.
- `${CLAUDE_PLUGIN_ROOT}` resolves to the *cache snapshot*, not the cwd —
  so the installed plugin serves the snapshot's `hooks/instructions.md`,
  which can trail the working tree even while you sit in this repo.
- `git show HEAD:path` applies working-tree eol conversion, so it cannot
  prove byte-identity with HEAD — it compares converted text to converted
  text. Use `git cat-file blob HEAD:path` wherever the bytes are the
  point.
- `grep -c $'\r'` through the Bash tool silently matches every line — the
  `$'...'` quoting doesn't survive to grep. Count line endings in Python
  (`b.count(b'\r\n')`), never by shell pattern.
- `main` is the live distribution channel, not a dev branch: with
  `"source": "./"` the marketplace clones the repo, so merging to `main`
  ships to every end user immediately. Work on a branch; merging is the
  release.
- SessionStart hook output reaches the MAIN session only — subagents do
  not inherit it (tested 2026-07-29). CLAUDE.md and its `@`-imports do
  propagate, so anything a party member must have either lives in
  CLAUDE.md, is read by the agent itself, or rides the spawn prompt. As of
  2026-07-30 the experience files take the middle route: each agent's own
  read step, not a briefing carried into the spawn prompt.
- A plugin's `hooks/hooks.json` auto-registers — no `hooks` key in
  `plugin.json`, and `--plugin-dir` honors it. Stdout is injected verbatim,
  no JSON wrapper needed; the `matcher` field is honored and accepts
  alternation, so a wrong matcher fails silently by simply never firing —
  and "omitted matcher fires on every source" is proven only for `startup`,
  since `compact`/`clear` are interactive-only.
- SessionStart stdout is injected verbatim only up to **10,000 characters,
  inclusive, per hook entry** — past it the whole entry is relocated to
  `tool-results/` while the hook still exits 0, so every cheap check passes.
  Characters, not bytes: `wc -m`, never `wc -c`. See learnings 2026-07-30.
- `@`-imports do not resolve in hook stdout — relative and absolute alike
  arrive as literal text while the surrounding payload loads fine. A hook
  has no include primitive, so referencing another file must be prose that
  instructs the reader to go read it.
- The experience read triggers fire on the default party models but not on
  haiku, which names `gotchas.md` correctly when asked yet edits without
  reading it — the *case* is disputed, not the rule, and neither stronger
  wording nor hoisting the section moved it (0/4 vs 3/3, 2026-07-30).
- `git grep` searches tracked files only, so a "zero hits" check over a
  change that *adds* shipped files passes vacuously until they're staged —
  CLAUDE.md's trademark grep now carries `--untracked`; any ad-hoc repo
  grep in a session has the same hole.
- A grep proves the *name* is gone, never that the *promise* is: prose
  that describes a removed feature contains none of its tokens. After
  deleting a section, read the referring files end to end.
- An archive of superseded text is indistinguishable from live text to
  `git grep` — `.claude/learnings-archive.md` holds strings this repo no
  longer ships, so "do we still ship this?" must name the shipped file,
  never the repo.
- `/party:long-rest` both grows and drains the curated experience files:
  distilling writes *into* `architecture.md` / `gotchas.md` /
  `decisions.md` and the prune step drops only what stopped being true, so
  its compact step is the sole drain and its gauge the only thing measuring
  what those files cost to read.
- A CLI's effort/reasoning knob can hide behind a generic override flag
  (codex: `-c model_reasoning_effort=<value>`, not a dedicated flag) with no
  enumerable values in `--help` at all — asking the CLI to self-report the
  key name and value list (even as clean JSON) is a fine candidate source
  but silently undercounts: codex's own JSON self-report named
  `model_reasoning_effort` correctly but listed only
  `minimal/low/medium/high/xhigh`, dropping the real `none` and `max`.
  Feeding one deliberately invalid value through the actual probe command
  surfaces the *complete* authoritative list in the resulting error message
  (`"Supported values are: ..."`) — that error text, not the CLI's
  self-report, is the source to record from. Verified 2026-08-03.
