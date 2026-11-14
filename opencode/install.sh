#!/bin/sh
# Adventure Party for OpenCode installer — renders each role's model into the
# agent/command files, symlinks the party into ~/.config/opencode and manages
# the AGENTS.md fragment block. Idempotent.
#
#   ./install.sh              install / refresh
#   ./install.sh --no-check   same, without checking models against OpenCode
#   ./install.sh --uninstall  remove the party's symlinks and fragment
#
# Agents and commands are linked from .generated/, where tools/party_models.py
# stamps the models from party-models.jsonc (+ party-models.local.jsonc) into
# copies of agents/*.md and commands/*.md. Skills are linked directly. After
# editing a models file or an agent/command source, run ./install.sh again;
# OpenCode only picks up edited files after `opencode service restart`.
set -eu

REPO=$(cd "$(dirname "$0")" && pwd)
DEST="${OPENCODE_CONFIG_DIR:-$HOME/.config/opencode}"
MARK_BEGIN="<!-- BEGIN adventure-party (opencode-ap)"
MARK_END="<!-- END adventure-party (opencode-ap) -->"

link() {
  # link <src> <dest-dir>  — -n so an existing symlink-to-dir is replaced, not followed
  ln -sfn "$1" "$2/$(basename "$1")"
  echo "linked $2/$(basename "$1")"
}

strip_fragment() {
  python3 - "$DEST/AGENTS.md" "$MARK_BEGIN" "$MARK_END" <<'PYEOF'
import sys
path, begin, end = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    text = open(path, encoding="utf-8").read()
except FileNotFoundError:
    sys.exit(0)
if begin not in text:
    sys.exit(0)
head, _, rest = text.partition(begin)
_, tail_marker, tail = rest.partition(end)
open(path, "w", encoding="utf-8").write(head.rstrip("\n") + ("\n" + tail.lstrip("\n") if tail.strip() else "\n"))
print("fragment removed from", path)
PYEOF
}

UNINSTALL=0
CHECK=""
for arg in "$@"; do
  case "$arg" in
    --uninstall) UNINSTALL=1 ;;
    --no-check)  CHECK="--no-check" ;;
    *) echo "usage: $0 [--no-check | --uninstall]" >&2; exit 2 ;;
  esac
done

if [ "$UNINSTALL" = 1 ]; then
  for f in fighter cleric wizard; do
    [ -L "$DEST/agents/$f.md" ] && unlink "$DEST/agents/$f.md" && echo "unlinked agents/$f.md"
  done
  for f in plan party long-rest; do
    [ -L "$DEST/commands/$f.md" ] && unlink "$DEST/commands/$f.md" && echo "unlinked commands/$f.md"
  done
  for s in party-run session-zero; do
    [ -L "$DEST/skills/$s" ] && unlink "$DEST/skills/$s" && echo "unlinked skills/$s"
  done
  strip_fragment
  echo "uninstalled (files in $REPO untouched)"
  exit 0
fi

# Render first: if a model doesn't resolve, stop before touching $DEST.
# ($CHECK is unquoted on purpose: empty means no argument.)
if ! python3 "$REPO/tools/party_models.py" $CHECK; then
  echo "install.sh: models not rendered; nothing was installed." >&2
  exit 1
fi

mkdir -p "$DEST/agents" "$DEST/commands" "$DEST/skills"

# Iterate the sources, link their rendered copies: a stale file left in
# .generated/ by a removed or renamed role is never linked.
for f in "$REPO"/agents/*.md;   do link "$REPO/.generated/agents/${f##*/}" "$DEST/agents";   done
for f in "$REPO"/commands/*.md; do link "$REPO/.generated/commands/${f##*/}" "$DEST/commands"; done
for s in "$REPO"/skills/*/;     do link "${s%/}" "$DEST/skills"; done

# AGENTS.md: replace our marker block (or append it) with the repo's fragment.
strip_fragment
python3 - "$DEST/AGENTS.md" "$REPO/AGENTS.fragment.md" <<'PYEOF'
import sys
dest, frag_path = sys.argv[1], sys.argv[2]
fragment = open(frag_path, encoding="utf-8").read().strip()
try:
    existing = open(dest, encoding="utf-8").read().rstrip("\n")
except FileNotFoundError:
    existing = ""
out = (existing + "\n\n" if existing else "") + fragment + "\n"
open(dest, "w", encoding="utf-8").write(out)
print("fragment installed into", dest)
PYEOF

echo
echo "Done. Verify in OpenCode: /agents should list fighter, cleric, wizard;"
echo "/plan, /party, /long-rest should be offered. If OpenCode is already"
echo "running, \`opencode service restart\` loads changed models."
