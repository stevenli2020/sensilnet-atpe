# ADP-005: Champion-Challenger Model Governance

**Status:** APPROVED (per Sprite disposition, `reviews/2026-07-26_sensilnet-atpe-adps_matcha.md`, 2026-07-26 — all six bundle findings Accepted)
**Author:** Cola (Claude Desktop + Local MCP)
**Date:** 2026-07-26 (original); amended 2026-07-26 in response to Matcha review Findings 4 and 5; amended again 2026-07-26 to fold Matcha's final-reply numeric threshold (Amendment 2)
**Protected sections affected:** `docs/ARCHITECTURE.md` §4.3 (Model Architecture Subsystem), §5 (Roadmap — gate definitions; Shared section, included here for completeness since gates are referenced by Protected §4.3)
**Business-layer impact:** Timeline — this ADP recasts the roadmap from a fixed 6-week plan to a gated ~11-week plan (see `ARCHITECTURE_v2_PROPOSED.md` §5). **Route to Sprite** for timeline/effort acknowledgment, per `WORKFLOWS.md` §12 (business-layer: cost/schedule tradeoff).
**Material-risk category (WORKFLOWS.md §6):** YES — "Model-selection changes (architecture, loss function, output heads)" directly. **Mandatory Matcha review required before Sprite disposition — complete; see disposition above.**

---

## Problem

`docs/ARCHITECTURE.md` v1 §4.3 specifies a multi-task TFT as the only model — there is no baseline, no comparison, no promotion criterion. A five-name pilot (or even the expanded research universe under ADP-006) provides limited justification for defaulting straight to a deep Temporal Fusion Transformer as the sole modeling backbone. This conflicts with `INVESTMENT_PHILOSOPHY.md` Principle 3: *"Complexity carries the burden of proof... New ideas should only be adopted when they produce measurable prediction improvement, significantly better explainability, materially simpler design, or clear institutional value. Interesting ideas alone are insufficient."* Nothing in v1 establishes that TFT clears this bar relative to a simpler model.

## Proposed Change

See `docs/decision_log/ARCHITECTURE_v2_PROPOSED.md` §4.3 and §5.

- **Champion**: regularized logistic regression (directional) + quantile regression / gradient-boosted trees (return range), one per horizon, trained on Core-lens features (see ADP-001 for lens hierarchy).
- **Challenger**: TFT via `pytorch-forecasting` (retained from v1/`INITIAL_PROPOSAL.md` §5) — introduced only after the champion and data foundation are proven, not as the default day-one model.
- **Promotion rule**, recorded in `validation_results` (schema in `ARCHITECTURE_v2_PROPOSED.md` §3.9), not asserted in prose: challenger replaces champion only if it beats it out-of-sample, after transaction costs (per the retained cost model in v1/proposed §4.5), calibrated by horizon, and stable across at least 2 of 3 historical regime buckets **as defined by the frozen Research Regime Classifier — see Amendment below, not by any model-input feature.**
- **Regime-stability reporting caveat**: given the SGX universe's finite size and backtest window, the number of independent regime episodes available for the "≥2 of 3" check is small. The gate must report a confidence interval or regime-count denominator alongside the pass/fail result — a single lucky or unlucky regime period should not silently flip the gate without that being visible to whoever reviews the promotion decision. **See Amendment 2 — this is now a concrete numeric floor, not a qualitative caveat.**

### Gate Definitions (full table, referenced from roadmap §5 of proposed architecture — updated post-amendment)

| Phase | Gate |
|---|---|
| PIT/data foundation | Historical as-of replays reproduce the same approved feature dataset within stated numerical tolerance, with full source/version lineage, and no not-yet-available events admitted (see ADP-002, incl. Amendments 1–2) |
| Feature registry | Every engineered feature has one primary lens, formula/version, source, availability lag, and passing PIT validation (see ADP-001) |
| Research baseline | Baseline models beat **named** naive benchmarks — persistence (last-value carry-forward) and buy-and-hold STI/E17.SI — **and** the named single-lens baselines defined in Amendment 1 below, out-of-sample, calibrated by horizon. All benchmark names fixed at ADP-approval time, not decided later, so the gate is falsifiable rather than argued about at review time. |
| TFT promotion | TFT outperforms the baseline champion after costs and remains stable across ≥2 of 3 historical regimes **as defined by the frozen Research Regime Classifier (see Amendment below)**, subject to the minimum-evidence floor in **Amendment 2** — below that floor the gate reports `INCONCLUSIVE`, not pass/fail |
| Daily publication | Data-quality, source-freshness, model-version, and confidence checks all pass; otherwise the system publishes a withheld/failed status, not a prediction |

## Rationale

Directly implements Principle 3's "burden of proof" requirement as an enforceable, falsifiable gate rather than a stated intention. The named-benchmark and confidence-interval refinements close two gaps identified during design review: an unnamed "naive benchmark" is not falsifiable at review time, and a bare pass/fail on regime stability hides how much evidence actually backs a promotion decision.

## Dependency

Requires ADP-001 (Core/Supporting feature hierarchy) and ADP-002 (PIT-validated feature foundation) to be implemented first — the champion cannot be meaningfully trained or gated without them.

## Open Questions for Matcha Review — Resolved

1. Is "beats named naive benchmarks" a sufficiently high bar for champion promotion, or should the research-baseline gate also require beating a simple single-factor regression? — **Resolved by Matcha Finding 4 and Amendment 1: yes, additional named single-lens benchmarks are required.**
2. What is an appropriate minimum regime-episode count/confidence-interval width below which the TFT-promotion gate should be treated as inconclusive rather than pass/fail? — **Resolved by Matcha's final reply and Amendment 2 below: a concrete numeric floor is now specified.**
3. Should model-governance promotion decisions be logged as immutable review artifacts per `reviews/REVIEW_FORMAT.md`? — **Not resolved within this ADP; Cola's recommendation (that this become a standing rule in `WORKFLOWS.md` §11 rather than a per-ADP decision) stands. Recommend Sprite consider this separately, outside this ADP's scope.**

---

## Amendment 1 (post-Matcha-review — responds to Finding 4)

**Trigger:** Matcha review, Finding 4 — "Champion baseline gates are too weak to prove the TFT challenger earns its complexity." Accepted in full.

**Gap:** Persistence and buy-and-hold STI/E17.SI are necessary sanity checks but do not test whether the Core-lens baseline champion — or, further up the chain, TFT — is doing anything beyond rediscovering a single well-known factor. On a dataset the size of the SGX research universe, a model with more degrees of freedom can appear to add value while actually just overfitting incremental noise around a simple factor exposure.

**Fix — additional named benchmark rung, added to the Research Baseline gate above:**

Before the Core-lens baseline champion (logistic/quantile regression over all Core-lens features combined) is trusted as the champion, it must also beat two additional, named single-lens models, fixed now rather than chosen later:
- **Pure Momentum model**: same model family (regularized logistic/quantile regression), trained using only Momentum-lens features.
- **Pure Quality model**: same model family, trained using only Quality-lens features.

These are distinct from the Core-lens champion itself (which combines all five Core lenses — Momentum, Quality, Macro, Relative Value, Event-Driven — not a single one), so there is no redundancy between this new rung and the existing champion definition. If the multi-lens Core champion cannot beat either single-lens model out-of-sample, that is itself a finding worth surfacing before any further model complexity (TFT) is considered — it would suggest the lens-combination approach itself isn't adding value yet, independent of whether TFT eventually would.

## Amendment (cross-ADP, post-Matcha-review — responds to Finding 5, shared with ADP-004)

**Trigger:** Matcha review, Finding 5 — "Regime-stability validation lacks a PIT-safe regime definition after `market_regime_code` removal." Accepted in full; identified as the sharpest catch in the review. Full technical fix specified in `ADP-004-macro-regime-redesign.md` §"Amendment (cross-ADP, post-Matcha-review)" — summarized here for how this ADP's promotion gate consumes it.

**Gap:** This ADP's stability check ("stable across ≥2 of 3 historical regime buckets") had no specification for how those validation-time regime buckets get constructed once `market_regime_code` — removed by ADP-004 — is gone. Left unspecified, a researcher could define or adjust the regime buckets after seeing model results, or compute them from revised/full-sample macro data, either of which would leak future information into what's supposed to be an out-of-sample stability check.

**Fix:** The TFT-promotion gate now explicitly consumes the **Research Regime Classifier** defined in ADP-004's amendment — a component built once, before any model training, from PIT-available macro data only, with its bucketing methodology frozen in the Phase 3 implementation spec before any model is evaluated against it. This classifier is validation-only metadata, never a model input, keeping it fully separate from ADP-004's removal of the fused `market_regime_code` feature. Every promotion decision recorded in `validation_results` (§3.9) references the specific classifier version used, so a reviewer can always trace which frozen regime definition a given promotion was tested against.

## Amendment 2 (post-Matcha-final-reply — numeric threshold for Open Question 2)

**Trigger:** Matcha final reply (`reviews/2026-07-26_sensilnet-atpe-adps_matcha.md`), responding to Finding 5 — proposed a concrete numeric floor for the regime-stability gate rather than leaving it to the implementation spec. Accepted; folds Matcha's recommendation directly into the ADP text rather than leaving it as a review-file note only, per Sprite's disposition.

**Rule, added to the TFT-promotion gate:** The regime-stability check ("stable across ≥2 of 3 historical regime buckets," per the Research Regime Classifier defined above) is **`INCONCLUSIVE`, not pass/fail**, unless each of the 3 regime buckets has:
- at least **3 independent historical episodes**, **and**
- at least **30 symbol-episode observations**

in the relevant validation window. If this floor is not met, the stratified per-regime results are still recorded in `validation_results`, but the 2-of-3 rule cannot be cited as promotion evidence for that model run — the gate records `INCONCLUSIVE`, and TFT cannot be promoted on the strength of that stability check alone until enough evidence accumulates (e.g., a longer backtest window or an expanded research universe under ADP-006 that yields more independent episodes).

Confidence-interval width remains metric-specific and is set at implementation time (Phase 3/4 spec), but per Matcha's final reply, the interval must at minimum be reported for the **after-cost incremental metric versus the champion** — not only for standalone TFT performance in isolation.

## Disposition

**Accepted.** See `reviews/2026-07-26_sensilnet-atpe-adps_matcha.md` Disposition section, Finding 5 entry, recorded by Sprite 2026-07-26. This ADP's `Status` is updated to `APPROVED` accordingly.
