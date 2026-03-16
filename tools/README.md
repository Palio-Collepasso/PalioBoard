# Tools

This directory is reserved for repository-level helper utilities that are shared across backend, web, and infrastructure workflows.

Use this directory only for reusable tooling that does not belong inside one application subtree.

## Scripts
- `task-worktree-codex.sh <task_number>` creates the standard task worktree under `~/codex-worktrees/palio-board/tasks/` for the given numeric Backlog task id and opens `codex` in that worktree. If the branch/worktree already exists, it reuses it.
- `task-worktree-dismiss.sh <task_number>` unmounts the shared `backlog/` bind mount for the task worktree when present, deletes the worktree folder under `~/codex-worktrees/palio-board/tasks/`, and removes the matching git worktree metadata entry.
