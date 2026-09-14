# Subagent mode

Use this mode when the current Codex environment exposes native subagent orchestration. Keep the work inside the invoking task and return every result to the coordinator.

## Dispatch

For every worker:

- Set `model` to `gpt-5.6-luna`.
- Set `reasoning_effort` to the parsed `low`, `medium`, `high`, or `xhigh` value.
- With `collaboration.spawn_agent`, set `fork_turns` to `none`; send the self-contained work package instead of the full conversation.
- Give the worker a unique, bounded assignment and the exact required return format.
- Do not let workers create further subagents.

Spawn independent packages in parallel up to the environment's capacity. Queue the remainder without changing the requested worker count. Keep dependent steps sequential.

## Workspace ownership

Subagents may share a filesystem. Assign disjoint files or directories whenever workers can write. When scopes overlap, use one implementation worker and make the others read-only researchers, testers, or reviewers. Tell every worker about the boundary.

The coordinator owns integration and user-facing communication. Workers must not commit, push, publish, deploy, send messages, or mutate external systems unless the underlying user request explicitly authorizes that exact action and the coordinator assigns a single owner.

## Collection and repair

Wait for all active workers with the native wait mechanism. Read concise final results rather than replaying full histories. If one result is incomplete, send one focused follow-up to that worker; do not resample the whole group.
