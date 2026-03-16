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
worktree_root="${HOME}/codex-worktrees/palio-board/tasks"
worktree_path="${worktree_root}/${task_branch_slug}"
shared_backlog_target="${worktree_path}/backlog"
worktree_admin_path="${repo_root}/.git/worktrees/${task_branch_slug}"

is_mountpoint() {
  local target="$1"

  if command -v mountpoint >/dev/null 2>&1; then
    mountpoint -q "$target"
    return
  fi

  awk -v target="$target" '$5 == target { found = 1 } END { exit found ? 0 : 1 }' \
    /proc/self/mountinfo
}

if command -v umount >/dev/null 2>&1; then
  umount_cmd=(umount)
  if command -v sudo >/dev/null 2>&1; then
    umount_cmd=(sudo umount)
  fi

  if [ -d "$shared_backlog_target" ] && is_mountpoint "$shared_backlog_target"; then
    printf 'Unmounting bind mount at %s\n' "$shared_backlog_target"
    "${umount_cmd[@]}" "$shared_backlog_target"
  fi
elif [ -d "$shared_backlog_target" ] && is_mountpoint "$shared_backlog_target"; then
  printf 'umount command not found; cannot unmount bind mount at %s\n' \
    "$shared_backlog_target" >&2
  exit 1
fi

if [ -e "$worktree_path" ]; then
  printf 'Deleting worktree folder %s\n' "$worktree_path"
  rm -rf "$worktree_path"
fi

if [ -d "$worktree_admin_path" ]; then
  printf 'Deleting worktree metadata %s\n' "$worktree_admin_path"
  rm -rf "$worktree_admin_path"
fi

printf 'Dismissed worktree for %s\n' "$task_id_upper"
