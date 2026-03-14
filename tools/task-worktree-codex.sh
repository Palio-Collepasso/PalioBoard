#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 1 ]; then
  printf 'Usage: %s TASK_NUMBER\n' "$0" >&2
  exit 1
fi

task_number_raw="$1"

case "$task_number_raw" in
  [0-9]*)
    ;;
  *)
    printf 'Expected a numeric task id like 6, got: %s\n' "$task_number_raw" >&2
    exit 1
    ;;
esac

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
codex_bin="${CODEX_BIN:-codex}"
task_number="$task_number_raw"
task_id_upper="TASK-${task_number}"
mapfile -t task_files < <(
  find "$repo_root/backlog/tasks" -maxdepth 1 -type f \
    -name "task-${task_number} - *.md" | sort
)

if [ "${#task_files[@]}" -ne 1 ]; then
  printf 'Could not resolve a unique backlog task file for %s\n' "$task_id_upper" >&2
  exit 1
fi

task_file_name="$(basename "${task_files[0]}")"
task_slug="${task_file_name%.md}"
task_branch_slug="$(
  printf '%s' "$task_slug" |
    tr '[:upper:]' '[:lower:]' |
    sed -E 's/ - /-/g; s/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/-+/-/g'
)"
branch_name="tasks/${task_branch_slug}"
worktree_root="${HOME}/codex-worktrees/palio-board/tasks"
worktree_path="${worktree_root}/${task_branch_slug}"

mkdir -p "$worktree_root"

existing_branch="$(git -C "$repo_root" branch --list "$branch_name")"
if [ -d "$worktree_path/.git" ] || [ -f "$worktree_path/.git" ]; then
  :
elif [ -n "$existing_branch" ]; then
  git -C "$repo_root" worktree add "$worktree_path" "$branch_name"
else
  git -C "$repo_root" worktree add -b "$branch_name" "$worktree_path" HEAD
fi

printf 'Opening codex in %s\n' "$worktree_path"
cd "$worktree_path"
exec "$codex_bin"
