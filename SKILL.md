---
name: go-to-luna
description: Orchestrate the preceding or inline task with the current model as planner and final reviewer while GPT-6 Luna workers execute bounded work packages. Use when the user explicitly invokes $go-to-luna and selects low, medium, high, or xhigh effort plus subagent or new-task mode.
---

# go-to-luna

**去月球! · Go To Luna!**

Keep the current session model as coordinator. Delegate the execution-heavy work to `gpt-6-luna` (or `gpt-5.6-luna` when explicitly requested), collect concise evidence, review the combined result, and finish with an honest usage estimate.

## Invocation contract

```text
$go-to-luna [low|medium|high|xhigh] [sub|task] [n=auto|1..4] [model=luna6|luna5.6] [-- <task>]
```

Arguments may appear in any order before `--`:

- Effort selects the Luna reasoning effort. Default to `medium`.
- `sub`, `subagent`, or `子代理` selects subagent mode. This is the default.
- `task`, `thread`, or `新对话` selects user-visible new-task mode.
- `n=auto` lets the coordinator select the worker count. An integer from 1 through 4 requests that exact number of workers.
- `model=luna6` selects `gpt-6-luna` workers. This is the default. `model=luna5.6` explicitly selects `gpt-5.6-luna`, which remains available during the GPT-6 rollout.
- Text after `--` is the task. Without `--`, treat unparsed ordinary language as an inline task only when it is unambiguous.

Reject multiple effort levels, multiple modes, invalid worker counts, unknown worker models, and unknown flags with one concise correction. Do not silently reinterpret invalid controls as task text.

## Resolve the task

Use the first available source:

1. The task after `--`.
2. A plan, file, link, or deliverable explicitly named in the invocation.
3. The most recent actionable user request before the invocation.

Do not use an assistant message, status update, or the invocation itself as the task. If no actionable task exists, ask one concise question and stop.

## Plan without doing the workers' jobs

The coordinator must not switch its own model or solve the full task before delegation. Create a compact execution contract containing:

```text
Objective:
Acceptance criteria:
Shared constraints:
Relevant inputs and paths:
Work packages and ownership:
Integration order:
```

Choose `n=auto` from meaningful independent work, normally one worker for an indivisible task, two for two independent tracks, and at most three without an explicit worker count. Never add duplicate workers merely to reach a larger number. When an explicit count exceeds the available concurrency, run workers in batches.

Each work package must be self-contained and include only the context needed for that worker:

```text
Goal:
Owned scope:
Required inputs:
Constraints and non-goals:
Deliverable:
Checks:
Return format:
```

Prefer disjoint ownership. For shared files or external systems, appoint one writer and make all other workers read-only advisers or verifiers. Delegation does not expand the user's authorization, sandbox, or external-write permissions.

## Dispatch Luna workers

Use the selected Luna model for every worker — `gpt-6-luna` by default, `gpt-5.6-luna` only when the user passed `model=luna5.6` — and pass the selected reasoning effort explicitly. Do not silently fall back to the coordinator model, Astra, Sol, Terra, or another higher-cost model. If the selected Luna model or the requested orchestration mode is unavailable, report the missing capability and stop before doing the delegated work with an expensive fallback.

- For `sub`, read and follow [references/subagent-mode.md](references/subagent-mode.md).
- For `task`, read and follow [references/task-mode.md](references/task-mode.md).

Require every worker to return:

```text
Status: complete | partial | blocked
Result or changes:
Evidence and checks:
Files or sources:
Risks and unresolved items:
```

Do not request full transcripts, broad exploration logs, or repeated background. Wait for all requested workers before synthesis unless a worker exposes a genuine blocker that invalidates the remaining work.

## Review and integrate

The current coordinator is the final reviewer. Check the worker results against the original objective and acceptance criteria, resolve conflicts, inspect relevant files or evidence, and run proportionate verification when the user authorized execution.

If a correctable gap remains, send one focused repair request only to the responsible worker. Do not restart the full group or create an unbounded review loop. After one repair round, finish with the verified result and disclose any remaining limitation.

Do not create a separate expensive reviewer. In task mode, do not leave the final answer scattered across child tasks; summarize and deliver it in the invoking task.

## Report usage honestly

Always read [references/usage-estimation.md](references/usage-estimation.md) before the final response. Use runtime token metrics when available. Otherwise provide a range and label it as an estimate.

Distinguish all three concepts:

- Main-model tokens avoided or offloaded to Luna.
- Estimated credit-weighted savings versus doing the same execution on the current model.
- Total raw tokens, which may stay flat or increase because parallel agents add orchestration and duplicated context.

Never claim that total tokens were saved when only main-model workload or weighted usage was reduced. Use `scripts/estimate_usage.py` when input/output token counts are available or can be responsibly estimated.

## Final response

Lead with the completed result, then include this compact receipt:

```text
去月球!: Luna <effort> × <actual workers> · <Subagent|New task>
Main-model work offloaded: ~<tokens or range> (<percent or range>)
Estimated weighted-usage saving: ~<percent or unavailable>
Total raw-token saving: not claimed | <measured value>
Basis: <actual metrics or estimation method>
Verification: <checks performed>
Remaining risks: <none or concise list>
```

Use the user's language unless they request another one.
