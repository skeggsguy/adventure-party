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
  only session-zero; that's correct, not a packaging bug.
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
- Grepping the repo cannot tell you what the plugin *ships*:
  `memory/legacy-blocks.md` archives old blocks verbatim, so
  `party:fighter` looked current for three versions after the template
  dropped it (setup 5b keys on it). Ask the shipped file by name — the
  sentinel loop in CLAUDE.md Commands does exactly that.
- Git Bash on Windows PATH is a property of the *launch chain*, not the
  machine: `Git\usr\bin` is absent from the persistent PATH but present
  in a terminal opened from Git Bash. Wire subprocess commands
  (statusline, hooks) with absolute interpreter paths — a PATH-dependent
  one dies silently when the user launches differently.
- `/plugin install` and `/reload-plugins` never fetch origin — they
  snapshot the local *marketplace clone* into a version-keyed cache, and
  auto-update is off by default for third-party marketplaces. So the
  installed plugin can silently trail a just-pushed release: dogfood this
  repo with `claude --plugin-dir .`, never the installed copy.
- The marketplace clone's `origin/main` ref is not evidence of what it
  has fetched — a marketplace update leaves the ref stale while moving
  the checkout (fetch-to-`FETCH_HEAD` shape). Only its HEAD is truthful.
- `${CLAUDE_PLUGIN_ROOT}` resolves to the *cache snapshot*, not the cwd,
  so `/party:setup` run inside this repo copies the installed version's
  shipped text over the newer text sitting in the working tree.
- `git show HEAD:path` applies working-tree eol conversion, so it cannot
  prove byte-identity with HEAD — it compares converted text to converted
  text. Use `git cat-file blob HEAD:path` wherever the bytes are the
  point (legacy-block fingerprints in `memory/legacy-blocks.md`).
- `grep -c $'\r'` through the Bash tool silently matches every line — the
  `$'...'` quoting doesn't survive to grep. Count line endings in Python
  (`b.count(b'\r\n')`), never by shell pattern.
- `main` is the live distribution channel, not a dev branch: with
  `"source": "./"` the marketplace clones the repo, so merging to `main`
  ships to every end user immediately. Work on a branch; merging is the
  release.
- Deleting a key from `party.json` silently promotes it to an *unknown*
  key, which `/party:config` treats as a typo and hard-stops on — so a
  removal breaks every config the previous version shipped until the
  validator is told the key is inert rather than wrong (0.7.0,
  `experience`).
- Bumping a `<!-- party@X.Y.Z -->` marker ripples past its own block:
  prose that enumerates *what a version marked* (setup step 5a's
  fingerprint notes, `legacy-blocks.md` framing) goes false silently.
  Grep the old version string after any bump.
