#!/bin/sh

# Link local agent guidance into a linked worktree without touching tracked files.
set -u

worktree_root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
git_dir=$(git rev-parse --path-format=absolute --git-dir 2>/dev/null) || exit 0
common_dir=$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null) || exit 0

# The main checkout already owns the source files.
[ "$git_dir" != "$common_dir" ] || exit 0

source_checkout=$(dirname "$common_dir")

for name in AGENTS.md CLAUDE.md; do
  source_file="$source_checkout/$name"
  target_file="$worktree_root/$name"

  [ -f "$source_file" ] || continue
  [ ! -e "$target_file" ] && [ ! -L "$target_file" ] || continue

  ln -s "$source_file" "$target_file" || exit 0
done

exit 0
