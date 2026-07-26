# ADP-005: Champion-Challenger Model Governance

**Status:** OPEN
**Author:** Cola (Claude Desktop + Local MCP)
**Date:** 2026-07-26
**Protected sections affected:** `docs/ARCHITECTURE.md` §4.3 (Model Architecture Subsystem), §5 (Roadmap — gate definitions; Shared section, included here for completeness since gates are referenced by Protected §4.3)
**Business-layer impact:** Timeline — this ADP recasts the roadmap from a fixed 6-week plan to a gated ~11-week plan (see `ARCHITECTURE_v2_PROPOSED.md` §5). **Route to Sprite** for timeline/effort acknowledgment, per `WORKFLOWS.md` §12 (business-layer: cost/schedule tradeoff).
**Material-risk category (WORKFLOWS.md §6):** YES — "Model-selection changes (architecture, loss function, output heads)" directly. **Mandatory Matcha review required before Sprite disposition.**

---

## Problem

`docs/ARCHITECTURE.md` v1 §4.3 specifies a multi-task TFT as the only model — there is no baseline, no comparison, no promotion criterion. A five-name pilot (or even the expanded research universe under ADP-006) provides limited justification for defaulting straight to a deep Temporal Fusion Transformer as the sole modeling backbone. This conflicts with `INVESTMENT_PHILOSOPHY.md` Principle 3: *"Complexity carries the burden of proof... New ideas should only be adopted when they produce measurable prediction improvement, significantly better explainability, materially simpler design, or clear institutional value. Interesting ideas alone are insufficient."* Nothing in v1 establishes that TFT clears this bar relative to a simpler model.

## Proposed Change

See `docs/decision_log/ARCHITECTURE_v2_PROPOSED.md` §4.3 and §5.

- **Champion**: regularized logistic regression (directional) + quantile regression / gradient-boosted trees (return range), one per horizon, trained on Core-lens features (see ADP-001 for lens hierarchy).
- **Challenger**: TFT via `pytorch-forecasting` (retained from v1/`INITIAL_PROPOSAL.md` §5) — introduced only after the champion and data foundation are proven, not as the default day-one model.
- **Promotion rule**, recorded in `validation_results` (schema in `ARCHITECTURE_v2_PROPOSED.md` §3.9), not asserted in prose: challenger replaces champion only if it beats it out-of-sample, after transaction costs (per the retained cost model in v1/proposed §4.5), calibrated by horizon, and stable across at least 2 of 3 historical regime buckets.
- **Regime-stability reporting caveat**: given the SGX universe's finite size and backtest window, the number of independent regime episodes available for the "≥2 of 3" check is small. The gate must report a confidence interval or regime-count denominator alongside the pass/fail result — a single lucky or unlucky regime period should not silently flip the gate without that being visible to whoever reviews the promotion decision.

### Gate Definitions (full table, referenced from roadmap §5 of proposed architecture)

| Phase | Gate |
|---|---|
| PIT/data foundation | Historical as-of replays reproduce the same approved feature dataset within stated numerical tolerance, with full source/version lineage, and no not-yet-available events admitted (see ADP-002) |
| Feature registry | Every engineered feature has one primary lens, formula/version, source, availability lag, and passing PIT validation (see ADP-001) |
| Research baseline | Baseline models beat **named** naive benchmarks — persistence (last-value carry-forward) and buy-and-hold STI/E17.SI — out-of-sample, calibrated by horizon. Benchmark names are fixed at ADP-approval time, not decided later, so the gate is falsifiable rather than argued about at review time. |
| TFT promotion | TFT outperforms the baseline champion after costs and remains stable across ≥2 of 3 historical regimes, with confidence interval/regime-count reported alongside the pass/fail result |
| Daily publication | Data-quality, source-freshness, model-version, and confidence checks all pass; otherwise the system publishes a withheld/failed status, not a prediction |

## Rationale

Directly implements Principle 3's "burden of proof" requirement as an enforceable, falsifiable gate rather than a stated intention. The named-benchmark and confidence-interval refinements close two gaps identified during design review: an unnamed "naive benchmark" is not falsifiable at review time, and a bare pass/fail on regime stability hides how much evidence actually backs a promotion decision.

## Dependency

Requires ADP-001 (Core/Supporting feature hierarchy) and ADP-002 (PIT-validated feature foundation) to be implemented first — the champion cannot be meaningfully trained or gated without them.

## Open Questions for Matcha Review

1. Is "beats named naive benchmarks" a sufficiently high bar for champion promotion, or should the research-baseline gate also require beating a simple single-factor regression (e.g., pure Momentum or pure Quality) before advancing to Phase 4?
2. What is an appropriate minimum regime-episode count/confidence-interval width below which the TFT-promotion gate should be treated as inconclusive rather than pass/fail?
3. Should model-governance findings (e.g., a promotion decision) themselves be logged as immutable review artifacts per `reviews/REVIEW_FORMAT.md`, given they are exactly the kind of decision `WORKFLOWS.md` §1 warns could become unrecoverable if only discussed in a chat session?

## Disposition

*(Pending Matcha review, then Sprite recording per WORKFLOWS.md §10.)*
