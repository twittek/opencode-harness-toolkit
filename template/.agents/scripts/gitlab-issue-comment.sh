#!/usr/bin/env bash
set -euo pipefail

ISSUE_ID="${1:-}"
COMMENT_FILE="${2:-}"

if [[ -z "$ISSUE_ID" || -z "$COMMENT_FILE" ]]; then
  echo "Usage: $0 <issue-id> <comment-file.md>" >&2
  exit 1
fi

if [[ ! -f "$COMMENT_FILE" ]]; then
  echo "ERROR: comment file not found: $COMMENT_FILE" >&2
  exit 1
fi

if ! command -v glab >/dev/null 2>&1; then
  echo "ERROR: glab CLI is not installed or not on PATH." >&2
  exit 1
fi

glab issue note "$ISSUE_ID" --message "$(cat "$COMMENT_FILE")"
