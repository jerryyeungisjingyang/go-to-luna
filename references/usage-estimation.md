# Usage estimation

The usage receipt measures workload routing, not a guaranteed reduction in total raw tokens.

## Evidence priority

Use the best available basis:

1. Runtime-reported coordinator and worker input/output tokens.
2. Token counts returned by task or agent APIs.
3. A clearly labeled range estimated from visible prompts, summaries, and tool outputs.
4. Qualitative reporting when no defensible count is available.

Do not invent hidden reasoning-token counts. When estimating from visible text, use a wide range and lower the confidence because file reads, tool schemas, cached input, and hidden reasoning may be absent.

## Metrics

Let coordinator tokens be the input and output handled by the current model for planning, orchestration, review, and final delivery. Let worker tokens be the combined Luna input and output.

- `main-model tokens offloaded = worker input + worker output`
- `main-model workload reduction = worker tokens / (coordinator tokens + worker tokens)`
- `baseline weighted usage = all coordinator and worker tokens priced at the current model's rates`
- `actual weighted usage = coordinator tokens priced at current-model rates + worker tokens priced at Luna rates`
- `weighted saving = baseline weighted usage - actual weighted usage`

The baseline assumes comparable token volume if the current model performed the delegated work. State this assumption. It is a routing comparison, not a counterfactual measurement.

## Deterministic calculator

When counts are available, run:

```bash
python3 scripts/estimate_usage.py \
  --main-model gpt-5.6-sol \
  --coordinator-input 3000 \
  --coordinator-output 1000 \
  --worker-input 24000 \
  --worker-output 8000 \
  --source estimated
```

The bundled rate card is dated `2026-09-12` and represents credits per million tokens. Treat it as a snapshot; if current official rates are available and differ, use current rates or describe only token offload.

## Required wording

Prefer:

```text
Main-model work offloaded: approximately 28k-36k tokens.
Estimated main-model workload reduction: 82%-90%.
Estimated weighted-usage saving versus Sol: 76%-86%.
Total raw-token saving: not claimed; parallel orchestration may increase it.
Basis: visible packet/result sizes; runtime per-agent usage was unavailable.
```

Avoid saying `saved 32k tokens` without the `main-model` qualifier. If the current model is already Luna, report zero model-tier saving while still reporting any organizational benefit.
