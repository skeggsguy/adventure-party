#!/bin/sh
# xp.sh — Adventure Party experience display. party@0.6.1
#
# Modes:
#   xp.sh statusline   one line: party level, XP, level-up nudge when ready
#   xp.sh banner       SessionStart hook: user-visible banner (stderr,
#                      exit 2) when experience is enabled AND a level-up
#                      is ready; silent exit 0 otherwise
#
# XP  = "## YYYY-MM-DD" entries in .claude/learnings.md — append-only by
#       law, so XP never decreases and survives Long Rest distillation.
# The chronicled level is the last "## Level N" heading in CHRONICLE.md —
# the chronicle is the only level state; there is no state file.
#
# Zero model tokens in both modes. Every failure path must degrade to
# something sane, never an error: this runs on every prompt render.

DIR="${CLAUDE_PROJECT_DIR:-$PWD}"

# Drain stdin (statusline/hook JSON) so the writer never sees EPIPE. Skip it
# when stdin is a terminal: a TTY never reaches EOF, so cat would hang here.
[ -t 0 ] || cat >/dev/null 2>&1 || :

XP=$(grep -c '^## [0-9][0-9][0-9][0-9]-' "$DIR/.claude/learnings.md" 2>/dev/null)
case "$XP" in ''|*[!0-9]*) XP=0 ;; esac

# Level thresholds: 10 / 25 / 50 / 100, then +100 per level forever.
LEVEL=1
NEXT=0
for T in 10 25 50 100; do
  if [ "$XP" -ge "$T" ]; then LEVEL=$((LEVEL + 1)); else NEXT=$T; break; fi
done
if [ "$NEXT" -eq 0 ]; then
  T=200
  while [ "$XP" -ge "$T" ]; do LEVEL=$((LEVEL + 1)); T=$((T + 100)); done
  NEXT=$T
fi

CHRON=$(grep -E '^## Level [0-9]+' "$DIR/CHRONICLE.md" 2>/dev/null \
  | tail -n 1 | sed 's/[^0-9]*\([0-9][0-9]*\).*/\1/')
case "$CHRON" in ''|*[!0-9]*) CHRON=1 ;; esac

READY=0
[ "$LEVEL" -gt "$CHRON" ] && READY=1

case "${1:-statusline}" in
  statusline)
    if [ "$READY" -eq 1 ]; then
      printf '📜 Party Lv.%s · %s XP · ⬆ LEVEL UP — /party:level-up\n' "$CHRON" "$XP"
    else
      printf '📜 Party Lv.%s · %s/%s XP\n' "$LEVEL" "$XP" "$NEXT"
    fi
    ;;
  banner)
    # Opt-in gate: .claude/party.json must say experience.enabled true.
    grep -q '"enabled"[[:space:]]*:[[:space:]]*true' "$DIR/.claude/party.json" 2>/dev/null || exit 0
    if [ "$READY" -eq 1 ]; then
      printf '🎺 Level up! The party has the experience to reach Level %s. Take a Long Rest when ready: /party:level-up — distills your experience files (your project'\''s memory) into shape. Uses real tokens; edits .claude/*.md and CHRONICLE.md.\n' "$LEVEL" >&2
      exit 2
    fi
    exit 0
    ;;
esac
exit 0
