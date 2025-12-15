#!/usr/bin/env bash
# Purge sensitive files or patterns from git history using git-filter-repo.
# WARNING: This rewrites git history. Coordinate with collaborators.

if [ -z "$1" ]; then
  echo "Usage: purge_history.sh <path-or-pattern-to-remove>"
  exit 1
fi

TARGET="$1"

echo "Removing $TARGET from history..."

# Ensure git-filter-repo is installed: pip install git-filter-repo
git filter-repo --invert-paths --path "$TARGET"

echo "Run: git push --force --all && git push --force --tags to update remotes (coordinate with collaborators)"
