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
created_worktree=0

mkdir -p "$worktree_root"

existing_branch="$(git -C "$repo_root" branch --list "$branch_name")"
if [ -d "$worktree_path/.git" ] || [ -f "$worktree_path/.git" ]; then
  :
elif [ -n "$existing_branch" ]; then
  git -C "$repo_root" worktree add "$worktree_path" "$branch_name"
  created_worktree=1
else
  git -C "$repo_root" worktree add -b "$branch_name" "$worktree_path" HEAD
  created_worktree=1
fi

if [ "$created_worktree" -eq 1 ]; then
  shared_backlog_source="${repo_root}/backlog"
  shared_backlog_target="${worktree_path}/backlog"
  shared_backlog_backup=""

  if ! command -v mount >/dev/null 2>&1; then
    printf 'mount command not found; cannot bind-mount %s into %s\n' \
      "$shared_backlog_source" "$shared_backlog_target" >&2
    exit 1
  fi

  mount_cmd=(mount --bind)
  if command -v sudo >/dev/null 2>&1; then
    mount_cmd=(sudo mount --bind)
  fi

  if [ -e "$shared_backlog_target" ]; then
    shared_backlog_backup="${worktree_path}/.backlog.bind-backup.$$"
    mv "$shared_backlog_target" "$shared_backlog_backup"
  fi

  mkdir -p "$shared_backlog_target"
  if ! "${mount_cmd[@]}" "$shared_backlog_source" "$shared_backlog_target"; then
    rmdir "$shared_backlog_target" || true
    if [ -n "$shared_backlog_backup" ] && [ -e "$shared_backlog_backup" ]; then
      mv "$shared_backlog_backup" "$shared_backlog_target"
    fi
    printf 'Failed to bind-mount %s into %s. Check mount permissions.\n' \
      "$shared_backlog_source" "$shared_backlog_target" >&2
    exit 1
  fi

  if [ -n "$shared_backlog_backup" ] && [ -e "$shared_backlog_backup" ]; then
    rm -rf "$shared_backlog_backup"
  fi
fi

printf 'Opening codex in %s\n' "$worktree_path"
cd "$worktree_path"
exec "$codex_bin"
