# CLAUDE.md

This is the source repo for **Adventure Party** (`party` plugin) — a
fantasy-flavored agent-party and experience-system framework for Claude
Code, aimed at smart, driven users who weren't full-stack devs before
2024. Everything shipped is markdown (agents, skills, one hook payload)
plus a two-line `hooks/hooks.json` — no runtime code, no build. The repo
doubles as its own marketplace (`.claude-plugin/marketplace.json`).

Dogfooding this repo loads the shipped instructions through the plugin's
own SessionStart hook, so the party protocol and this project's
experience files arrive that way rather than from this file.

## Commands

- Validate manifests (stdlib only — no `jq`, which is absent on stock
  macOS/Linux/WSL): `python3 -m json.tool .claude-plugin/plugin.json`,
  `python3 -m json.tool .claude-plugin/marketplace.json` and
  `python3 -m json.tool hooks/hooks.json`
- Validate frontmatter (agents + skills; silence means valid, and a
  broken description silently unloads the file; needs PyYAML —
  `pip install pyyaml`, not bundled with python3 on Debian/Ubuntu):
  `python3 -c "import re,glob,yaml;[yaml.safe_load(re.match(r'^---\n(.*?)\n---\n',open(p,encoding='utf-8').read(),re.S).group(1)) for p in glob.glob('agents/*.md')+glob.glob('skills/*/SKILL.md')]"`
- Hook smoke test (the sentinel phrase is `the lantern is lit`, in
  `hooks/instructions.md`; anything else means the hook didn't inject):
  `claude --plugin-dir . -p 'Quote the sentence containing "lantern" from your instructions, or say NONE.'`
- Dogfood locally: `claude --plugin-dir .` (agents
  `party:fighter/cleric/wizard`, skills `/party:session-zero` and
  `/party:consolidate` should list)

## Layout

- `.claude-plugin/` — plugin + marketplace manifests
- `agents/` — the party: fighter (builder), cleric (reviewer/fixer),
  wizard (read-only advisor)
- `hooks/` — `hooks.json` (SessionStart) and `instructions.md`, the
  party protocol + experience rules injected into every session
- `skills/` — session-zero, consolidate (the Long Rest)

## Conventions

- Prose is the product: skills, agents and the hook payload are
  instructions executed by a model. Keep them unambiguous, honest about
  cost, and plain-language first — theme labels mechanics, never
  replaces them ("experience (your project's memory files)").
- `hooks/instructions.md` is loaded into every session of every project
  the plugin is installed in: budget ~4k characters, and every line
  added there is paid forever. Shipped-text changes still ripple — the
  muster rules live in `hooks/instructions.md` and README; keep them in
  sync.
- Shipped hook commands stay one line each, with no logic beyond
  `cd`/`cat`/`exit` — no `.sh` file ships (the 0.7.0 xp.sh lesson: a
  shipped script that runs on every user's machine is the most
  bug-prone thing in the repo).
- Naming: no trademarked tabletop terms in anything shipped. Check:
  `git grep -riE 'd[&]d|dunge[o]n|\bD[M]\b' -- README.md agents skills hooks .claude-plugin LICENSE`
  must return zero hits (pattern is self-escaping; the repo's own
  `.claude/` memory may name the terms when recording why we avoid
  them). The main session is "the Guide".
- `*.sh` stays LF (`.gitattributes` enforces) — `party.sh` is executed
  by a POSIX shell, which chokes on CRLF from a Windows checkout.
