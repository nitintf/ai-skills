#!/usr/bin/env bash
# Symlink every skill in this repo into ~/.claude/skills so edits are live in the
# next session, with no push, marketplace refresh, or plugin update.
#
# Re-run after adding, removing, or renaming a skill.
#   ./scripts/link-skills.sh          link everything
#   ./scripts/link-skills.sh --unlink remove the links again
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
MARKER=".linked-from-$(basename "$REPO")"

mkdir -p "$DEST"

# Drop links this script made previously, so renames and deletions propagate.
removed=0
for existing in "$DEST"/*; do
  [ -L "$existing" ] || continue
  target="$(readlink "$existing")"
  case "$target" in
    "$REPO"/*) rm "$existing"; removed=$((removed + 1)) ;;
  esac
done

if [ "${1:-}" = "--unlink" ]; then
  echo "unlinked $removed skill(s) from $DEST"
  exit 0
fi

linked=0
conflicts=()
for skill in "$REPO"/*/skills/*/; do
  [ -f "$skill/SKILL.md" ] || continue
  name="$(basename "$skill")"
  if [ -e "$DEST/$name" ]; then
    conflicts+=("$name")
    continue
  fi
  ln -s "${skill%/}" "$DEST/$name"
  linked=$((linked + 1))
done

echo "linked $linked skill(s) into $DEST"
[ "$removed" -gt 0 ] && echo "replaced $removed stale link(s)"

if [ ${#conflicts[@]} -gt 0 ]; then
  echo
  echo "skipped, a real file or foreign link is already there:"
  printf '  %s\n' "${conflicts[@]}"
  echo "move or delete those, then re-run."
fi

echo
echo "Uninstall the plugins while these links are active, or every skill appears twice."
