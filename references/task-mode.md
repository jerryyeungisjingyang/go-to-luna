# New-task mode

Use this mode only when the user explicitly selected `task`, `thread`, or `新对话` and the Codex app exposes task-creation and task-reading tools. New tasks are user-visible and must use `gpt-5.6-luna`.

## Create tasks

Resolve the current project before creation. Keep every prompt self-contained and minimal.

- Set the new task model to `gpt-5.6-luna`.
- Set its reasoning effort to the parsed `low`, `medium`, or `high` value.
- Prefix titles with `Luna i/n` followed by a short assignment name.
- Use the same saved project for repository work and a projectless task only when no repository context is needed.
- For a Git repository, use isolated worktrees when workers need repository access. Include the current working-tree state only when the task depends on uncommitted changes.

Create only the requested number of tasks. Preserve returned task and host identifiers, then use the native wait operation instead of repeatedly polling each task.

## Mutation boundary

New tasks do not share a final working tree automatically. For research, review, planning, and independent artifacts, have them return results directly. For changes that must land in the invoking workspace, keep the invoking task as the single writer and ask workers for bounded patch guidance unless the user explicitly requested isolated branches or commits.

Do not ask child tasks to commit, push, open pull requests, publish, deploy, or send external messages unless the user explicitly authorized that exact action. Never let two child tasks mutate the same external target.

## Collection and repair

Wait until every task completes or needs attention. Read the returned final result and only the minimum additional output needed to verify it. If one task is incomplete, send at most one focused follow-up to that task.

The invoking task performs the final review and delivery. Include links or identifiers for the new tasks when the client supports them, but do not require the user to assemble the answer manually.
