#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/template"
TARGET_DIR="${1:-$(pwd)}"
BACKUP_SUFFIX=".bak.$(date +%Y%m%d%H%M%S)"

if [[ ! -d "$TEMPLATE_DIR" ]]; then
  echo "ERROR: Template directory not found: $TEMPLATE_DIR" >&2
  echo "Make sure you run this script from the extracted OpenCode Harness Toolkit package." >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"

copy_file() {
  local src="$1"
  local rel="${src#$TEMPLATE_DIR/}"
  local dst="$TARGET_DIR/$rel"

  if [[ "$rel" == "README.md" ]]; then
    echo "skipped:   $rel (toolkit maintenance documentation)"
    return 0
  fi

  if [[ "$rel" == "AGENTS.md" && -e "$dst" ]]; then
    echo "preserved: $rel (existing project instructions)"
    return 0
  fi

  case "$rel" in
    AGENTS.md|opencode.jsonc|.opencode/command/*.md|.agents/interview/*.md|.agents/interview/topics/*.md|.agents/context/context-loading-policy.md|.agents/context/self-verification-policy.md|.agents/scripts/interview-ranker.py)
      ;;
    *)
      echo "deferred:  $rel (generated selectively by /harness-init)"
      return 0
      ;;
  esac

  mkdir -p "$(dirname "$dst")"

  if [[ -e "$dst" ]]; then
    if cmp -s "$src" "$dst"; then
      echo "unchanged: $rel"
      return 0
    fi

    local backup="$dst$BACKUP_SUFFIX"
    cp -p "$dst" "$backup"
    echo "backup:    $rel -> ${rel}${BACKUP_SUFFIX}"
  fi

  cp -p "$src" "$dst"
  echo "installed: $rel"
}

while IFS= read -r -d '' src; do
  copy_file "$src"
done < <(find "$TEMPLATE_DIR" -type f -print0 | sort -z)

if [[ -d "$TARGET_DIR/.agents/scripts" ]]; then
  find "$TARGET_DIR/.agents/scripts" -type f -name "*.sh" -exec chmod +x {} \;
fi

echo
echo "OpenCode harness toolkit installed."
echo "OpenCode Harness Toolkit version: v41"
echo
echo "Target:"
echo "  $TARGET_DIR"
echo
echo "Next steps:"
echo "  1. Review opencode.jsonc"
echo "  2. Start OpenCode:"
echo "       opencode"
echo "  3. Initialize the project harness:"
echo "       /harness-init"
echo "  4. Audit the generated harness:"
echo "       /harness-check"
echo
echo "Notes:"
echo "  - Existing files are backed up with suffix: $BACKUP_SUFFIX"
echo "  - The target project's README.md is never overwritten."
echo "  - An existing project AGENTS.md is preserved for /harness-init to reconcile."
echo "  - Only bootstrap resources are installed; /harness-init generates the project-specific harness."
