#!/usr/bin/env bash
set -euo pipefail

ISSUE_KEY="${1:-}"
COMMENT_FILE="${2:-}"

if [[ -z "$ISSUE_KEY" || -z "$COMMENT_FILE" ]]; then
  echo "Usage: $0 <issue-key> <comment-file.md>" >&2
  exit 1
fi

if [[ ! -f "$COMMENT_FILE" ]]; then
  echo "ERROR: comment file not found: $COMMENT_FILE" >&2
  exit 1
fi

cat <<EOF
This is an example wrapper.

Implement this script with your approved Jira access method:
- Jira MCP server
- internal Jira CLI
- REST API wrapper
- company-specific automation

Issue: $ISSUE_KEY
Comment file: $COMMENT_FILE
EOF
