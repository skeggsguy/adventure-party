# CLAUDE.md

This is the source repo for **Adventure Party** (`party` plugin) — a
fantasy-flavored agent-party and experience-system framework for Claude
Code, aimed at smart, driven users who weren't full-stack devs before
2024. Everything shipped is markdown (agents, skills, one hook payload)
plus a one-command `hooks/hooks.json` — no runtime code, no build. The repo
doubles as its own marketplace (`.claude-plugin/marketplace.json`).

Dogfooding this repo loads the shipped instructions through the plugin's
own SessionStart hook, so the party protocol arrives that way rather than
from this file. This project's `.claude/` experience files are NOT loaded
by anything — read `gotchas.md` before your first edit, `architecture.md`
before planning or changing how parts fit, `decisions.md` before choosing
between approaches.

## Commands

- Validate manifests (stdlib only — no `jq`, which is absent on stock
  macOS/Linux/WSL): `python3 -m json.tool .claude-plugin/plugin.json`,
  `python3 -m json.tool .claude-plugin/marketplace.json` and
  `python3 -m json.tool hooks/hooks.json`
- Validate frontmatter (agents + skills; silence means valid, and a
  broken description silently unloads the file; needs PyYAML —
  `pip install pyyaml`, not bundled with python3 on Debian/Ubuntu):
  `python3 -c "import re,glob,yaml;[yaml.safe_load(re.match(r'^---\n(.*?)\n---\n',open(p,encoding='utf-8').read(),re.S).group(1)) for p in glob.glob('agents/*.md')+glob.glob('skills/*/SKILL.md')]"`
- Check the hook payload against the 9,000 soft budget and the 10,000
  *character* hard cap (past the cap the whole entry is silently relocated
  to disk; counts code points, so `wc -c` is wrong here):
  `python3 -c "import sys;n=len(open('hooks/instructions.md',encoding='utf-8').read());print('FAIL' if n>10000 else 'WARN' if n>9000 else 'OK',n,'chars');sys.exit(n>10000)"`
- Hook smoke test (the sentinel phrase is `the lantern is lit`, in
  `hooks/instructions.md`; anything else means the hook didn't inject):
  `claude --plugin-dir . -p 'Quote the sentence containing "lantern" from your instructions, or say NONE.'`
- Dogfood locally: `claude --plugin-dir .` (agents
  `party:fighter/cleric/wizard/hireling`, skills `/party:session-zero`,
  `/party:long-rest` and `/party:hire` should list)

## Layout

- `.claude-plugin/` — plugin + marketplace manifests
- `agents/` — the party: fighter (builder), cleric (reviewer/fixer),
  wizard (read-only advisor), hireling (adapter that runs a hired
  foreign coding CLI in a party role)
- `hooks/` — `hooks.json` (SessionStart) and `instructions.md`, the
  party protocol injected into every session; it is also where the rules
  for reading the `.claude/` experience files live (the files themselves
  are not injected)
- `skills/` — session-zero, long-rest (distills the learnings inbox),
  hire (hires a foreign coding CLI into a party role, or releases one)

## Conventions

- Prose is the product: skills, agents and the hook payload are
  instructions executed by a model. Keep them unambiguous, honest about
  cost, and plain-language first — theme labels mechanics, never
  replaces them ("experience (your project's memory files)").
- `hooks/instructions.md` is loaded into every session of every project
  the plugin is installed in: soft budget 9,000 characters — a tripwire
  leaving ~1k of margin under the hard cap, not a cost target, so crossing
  it means "you are close to the wall", not "you overspent". Every line
  added there is still paid forever, so weigh each one on its merits rather
  than against the headroom. Shipped-text changes still ripple, and two
  rule sets are duplicated across shipped files — keep both in sync: the
  muster rules (`hooks/instructions.md`, README) and the per-file
  experience-read triggers (`hooks/instructions.md`, README,
  `agents/fighter.md`, `agents/cleric.md`, `skills/session-zero/SKILL.md`,
  and this file's intro).
- A SessionStart hook entry's stdout is injected verbatim only up to
  **10,000 characters, inclusive, per entry**; at 10,001 the whole thing is
  replaced by an `Output too large … saved to …/tool-results/` marker plus a
  ~2k preview. That is the hard cap the 9,000 soft budget above guards. It
  counts characters, not bytes, so **every size check here uses `wc -m`,
  never `wc -c`** (bytes overstate this repo's prose by ~1%). Measured
  2026-07-30; see `.claude/gotchas.md`.
- Shipped hook commands stay one line each, with no logic beyond
  `cd`/`cat`/`exit` — no `.sh` file ships (the 0.7.0 xp.sh lesson: a
  shipped script that runs on every user's machine is the most
  bug-prone thing in the repo).
- Naming: no trademarked tabletop terms in anything shipped. Check:
  `git grep -riE --untracked 'd[&]d|dunge[o]n|\bD[M]\b' -- README.md agents skills hooks .claude-plugin LICENSE`
  must return zero hits (pattern is self-escaping; `--untracked` because
  plain `git grep` skips not-yet-added files — exactly the new agents and
  skills a feature adds; the repo's own `.claude/` memory may name the
  terms when recording why we avoid them). The main session is "the Guide".
- `*.sh` stays LF (`.gitattributes` enforces) — `party.sh` is executed
  by a POSIX shell, which chokes on CRLF from a Windows checkout.
