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

if [[ -d "$TARGET_DIR/.agent/scripts" ]]; then
  find "$TARGET_DIR/.agent/scripts" -type f -name "*.sh" -exec chmod +x {} \;
fi

echo
echo "OpenCode harness toolkit installed."
echo "OpenCode Harness Toolkit version: v35"
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
echo "  - This install script is template-based; edit files under template/ to customize the toolkit package."
