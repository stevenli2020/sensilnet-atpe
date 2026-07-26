# Review: Sensilnet ATPE ADP Bundle v2 Proposal

**Reviewer:** Matcha
**Date:** 2026-07-26
**Artifact reviewed:** `docs/decision_log/ARCHITECTURE_v2_PROPOSED.md`; `docs/decision_log/ADP-001-lens-hierarchy-and-traceability.md`; `docs/decision_log/ADP-002-bitemporal-versioning-calendar.md`; `docs/decision_log/ADP-003-fundamentals-filings-schema.md`; `docs/decision_log/ADP-004-macro-regime-redesign.md`; `docs/decision_log/ADP-005-champion-challenger-governance.md`; `docs/decision_log/ADP-006-pilot-universe-and-data-rights.md`
**Artifact version at time of review:** git commit `180f79af817947f3e49421dac44ea4c493d62134`; ADPs dated 2026-07-26, Status OPEN
**Review type:** Independent technical review / Red-team audit

---

## Summary Verdict

Approve-with-conditions. The ADP bundle is directionally sound and materially improves v1's philosophy alignment, PIT posture, and model-governance discipline, but several proposed guarantees are still under-specified enough to permit PIT leakage, validation leakage, or misleading promotion decisions if implemented literally.

---

## Findings

### Finding 1: Source versioning still allows provenance gaps in PIT replay
```
Confidence: High
Evidence Basis: Direct text comparison + domain knowledge
```
**Description:** ADP-002 and the proposed v2 schema add `available_at`, `source_version`, `content_hash`, and `superseded_by`, but they still rely on the queryable raw tables themselves to prove what was known at a historical cutoff. The design does not specify an immutable ingest/event log recording each observed payload, retrieval timestamp, source response metadata, correction event, and supersession action. Because `superseded_by` is itself a later mutation of an older row, the table can represent the latest version graph but not independently prove the historical sequence of observed source states.

**Reason:** For backtest reproducibility, the system must distinguish "what the table currently says was available then" from "what the pipeline actually observed then." Without an immutable source-observation trail, a vendor backfill, parser rerun, manual correction, or accidental update can make a historical PIT replay look consistent while erasing the evidence needed to diagnose whether the original run used a different payload. This is directly material to PIT leakage and backtest validity.

**Recommendation:** Escalate before acceptance of ADP-002's foundation gate. Surrogate keys plus `superseded_by` are useful for querying current PIT state, but they should not be treated as sufficient proof of reproducibility unless paired with an immutable append-only observation/audit trail or an equivalent mechanically verifiable guarantee.

### Finding 2: ESTIMATED calendar rows are unsafe as model known-future inputs without a stricter boundary
```
Confidence: High
Evidence Basis: Direct text comparison + domain knowledge
```
**Description:** ADP-002 allows `event_date_status = 'ESTIMATED'` calendar rows, with `announced_at` nullable for estimated rows, while the architecture keeps calendar proximity as a known-future model input. The proposal records status, but it does not define whether estimated dates may be encoded into `days_to_earnings`, how model training distinguishes estimate-vs-confirmed proximity, or how later-wrong estimates are prevented from contaminating historical feature construction.

**Reason:** Earnings dates are especially leakage-prone because many commercial data providers publish historical calendars with actual event dates filled in after the fact. A historical "estimated" row that is generated or revised using later knowledge can become a known-future input that gives the model unusually accurate event proximity. Versioning helps only if the estimate is demonstrably what the pipeline could have known at the cutoff and if training treats estimated dates differently from confirmed dates.

**Recommendation:** Escalate unless ADP-002 explicitly constrains ESTIMATED rows. At minimum, estimated dates need a separate encoding and provenance standard from confirmed announced dates; otherwise known-future-input leakage remains open.

### Finding 3: PDF/LLM extraction can become canonical by accident
```
Confidence: Medium
Evidence Basis: Direct text comparison + domain knowledge
```
**Description:** ADP-003 says PDF extraction and LLM processing are "source-backed enrichment" rather than canonical, but the proposed schemas do not mechanically prevent extracted fields from becoming model features once they exist in `raw_sgx_fundamentals` or downstream `feature_definitions`. The validation status lives at the feature-definition level, while the source authority, extraction method, reviewer identity, and evidence quality are not represented as mandatory fields in the proposed `raw_sgx_fundamentals` schema.

**Reason:** Once extracted values enter the same raw table shape as vendor-provided fundamentals, downstream feature code can depend on them without preserving the distinction between licensed structured data and extracted/reconciled data. That creates hidden data dependencies and can also create PIT risk if a later PDF, amended report, or consolidated annual report is parsed into periods before it was actually available.

**Recommendation:** Defer promotion of ADP-003's extraction path until its source-authority boundary is mechanically enforceable. The schema should make it impossible for extraction-derived values to become promoted model inputs without explicit provenance and review evidence.

### Finding 4: Champion baseline gates are too weak to prove the TFT challenger earns its complexity
```
Confidence: High
Evidence Basis: Direct text comparison + domain knowledge
```
**Description:** ADP-005 names persistence and buy-and-hold STI/E17.SI as naive benchmarks for baseline promotion, then compares TFT against the baseline champion. Those benchmarks are necessary but not sufficient for a multi-lens equity model. They do not test whether the architecture beats simple single-factor or simple multi-factor models such as pure momentum, pure quality/value, sector-neutral momentum, or a regularized linear model over all lens features.

**Reason:** A TFT can appear to add value over weak naive benchmarks while merely rediscovering a simple factor exposure, or while benefiting from additional degrees of freedom in a small SGX dataset. If the baseline ladder is too low, the champion-challenger process can bless model complexity without proving incremental predictive value. That is a backtest-validity and overfitting risk, not just an efficiency concern.

**Recommendation:** Accept ADP-005 only with stronger named benchmark requirements. The gate should include simple factor baselines fixed before experimentation, not only persistence and broad-index buy-and-hold.

### Finding 5: Regime-stability validation lacks a PIT-safe regime definition after `market_regime_code` removal
```
Confidence: High
Evidence Basis: Direct text comparison + inference
```
**Description:** ADP-004 correctly removes the flawed `market_regime_code` model input, but ADP-005 still requires promotion stability across historical regime buckets. The ADP bundle does not define how those validation regimes are constructed once the old categorical code is removed, nor does it require the regime classifier/bucketing rule to be predeclared, PIT-safe, and frozen before model comparison.

**Reason:** Regime buckets used for validation are not harmless reporting metadata. If researchers can define or adjust regimes after seeing model performance, the stability gate becomes another researcher degree of freedom. Conversely, if regimes are computed using revised macro series, full-sample quantiles, or future-known crisis labels, the validation report can leak future information even when model features are PIT-compliant.

**Recommendation:** Escalate as a cross-ADP gap between ADP-004 and ADP-005. Removing `market_regime_code` as a feature is sound, but validation regimes still need an explicit PIT-safe construction rule before the stability gate is meaningful.

### Finding 6: The two-tier universe is justified, but evaluation must guard against dashboard-name overfitting
```
Confidence: Medium
Evidence Basis: Direct text comparison + domain knowledge
```
**Description:** ADP-006 makes a sound case for reopening Finding #3: the 5-name pilot cannot implement Relative Value for Singtel and SIA, while the approved investment philosophy treats Relative Value as Core. However, the proposed dashboard/research split creates a new validation hazard: the model trains on a broader research universe but is ultimately displayed and likely judged on five named dashboard stocks selected in advance.

**Reason:** If feature choices, hyperparameters, peer-group definitions, or challenger promotion decisions are tuned repeatedly against dashboard-name performance, the broader universe can give a false sense of sample size while the real product surface remains a tiny, preselected set. This is especially risky for heterogeneous SGX sectors where peer structures differ sharply across banks, telcos, transport, REITs, and conglomerates.

**Recommendation:** Accept the reopening of Finding #3 as justified, but condition ADP-006 on a validation design that separately reports broader-universe performance and dashboard-universe performance, with predeclared rules preventing dashboard-name tuning from driving model selection.

---

## Disagreement Loop (if applicable)

- **Matcha finding:** *(filed above)*
- **Cola response (proposer — note: I authored these ADPs directly, not Beer; responding in that capacity):**

**Timestamp:** 2026-07-26

All six findings are accepted. No disagreement filed against any of them — each identifies a real gap, not a difference of judgment. Amendments made directly to the affected ADPs (still `Status: OPEN`, not yet Approved, so pre-approval revision in response to review is the normal path, not a bypass of process). Per finding:

**Finding 1 (immutable observation log) — Accepted, ADP-002 amended.** Agreed that `superseded_by` plus surrogate keys prove current-state lineage but not that the historical sequence of observed payloads is tamper-evident. Added an append-only `ingestion_events` log as the actual source of truth (raw tables become a materialized/queryable projection over it), with a note that this is cheap to implement (an insert-only table plus a "never delete/never in-place-update" discipline check in CI), not a large engineering lift. See amended ADP-002 §"Amendment 1 (post-Matcha-review)."

**Finding 2 (ESTIMATED calendar rows) — Accepted, ADP-002 amended.** Agreed this is a real, not hypothetical, leakage vector — provider-backfilled "estimated" dates using later-known actuals is a documented real-world failure mode, not an edge case. Amendment: `ESTIMATED` rows are excluded from precise `days_to_earnings` encoding entirely; only `CONFIRMED` rows may feed that feature. A separate, coarser feature (`has_estimated_upcoming_earnings_window`, a boolean/bucketed signal, not a precise day-count) may use `ESTIMATED` rows. See amended ADP-002 §"Amendment 2 (post-Matcha-review)."

**Finding 3 (extraction becoming canonical by accident) — Accepted, ADP-003 amended.** Agreed the schema didn't mechanically enforce the enrichment-not-canonical boundary stated in prose. Amendment: `raw_sgx_fundamentals` gains a mandatory `data_authority` field (`LICENSED_STRUCTURED` / `EXTRACTED_LLM` / `MANUAL_ENTRY`), and `feature_definitions.validation_status` cannot reach `PROMOTED` for any feature whose primary source has `data_authority = 'EXTRACTED_LLM'` unless `reviewer_id` and `review_timestamp` are populated. This makes the boundary a database constraint, not a policy statement. See amended ADP-003 §"Amendment 1 (post-Matcha-review)."

**Finding 4 (benchmark ladder too weak) — Accepted, ADP-005 amended.** Agreed persistence + buy-and-hold alone can let a TFT "win" by rediscovering a simple factor exposure rather than adding real value, especially on a small SGX dataset. Amendment: added a second benchmark rung — single-lens baselines (pure Momentum-only, pure Quality-only models) — that the Core-lens baseline champion itself must beat before it is trusted as the champion, and that TFT must also clear. Clarified distinction from the existing Core-lens baseline champion (which uses all Core-lens features combined, not a single lens) so the two are not redundant. See amended ADP-005 §"Amendment 1 (post-Matcha-review)."

**Finding 5 (regime-validation gap after `market_regime_code` removal) — Accepted; the sharpest catch in the set.** This is a genuine cross-ADP defect: ADP-004 correctly removes the flawed model *input*, but neither ADP-004 nor ADP-005 specified how the *validation* regime buckets (used for the stability gate) get constructed once that categorical feature no longer exists. If validation regimes were built after seeing model results, using revised macro data, or using full-sample quantiles, the stability gate would leak exactly the kind of future information the rest of this bundle is designed to prevent — this would have been a real hole in the promotion process had it shipped as originally drafted. Amendment: a new, explicit "Research Regime Classifier" is added — separate from any model input — constructed once, in advance of any baseline/challenger training, using only PIT-available macro data as of each historical date, with its bucketing methodology frozen and recorded in `validation_results` metadata before any model comparison runs. See new §"Amendment (cross-ADP, post-Matcha-review)" added to both ADP-004 and ADP-005.

**Finding 6 (dashboard-name overfitting risk) — Accepted, ADP-006 amended.** Agreed reopening Finding #3 is justified on the merits (Relative Value cannot function for Singtel/SIA otherwise), but the two-tier split does create a real hazard if model-selection decisions get tuned against the small, preselected dashboard set. Amendment: added an explicit rule — dashboard-universe performance is reported for transparency but is not an input to any model-selection, hyperparameter, or promotion decision; all such decisions are made exclusively on research-universe validation metrics, predeclared before the dashboard names are ever inspected post-training. See amended ADP-006 §"Amendment 1 (post-Matcha-review)."

No findings are contested. Recommend Sprite proceed to disposition all six as Accepted, contingent on the amendments now present in the ADP files being the version implemented (not the pre-review originals).

- **Matcha final reply:**

**Timestamp:** 2026-07-26

Final reply under the bounded disagreement loop. I reviewed Cola's response and the post-review amendments in ADP-002, ADP-003, ADP-004, ADP-005, and ADP-006. No new review round is opened here; this reply only evaluates whether the amendments close the six filed findings.

**Finding 1 — Satisfied.** ADP-002's new `ingestion_events` table addresses the core provenance gap. Treating raw tables as queryable projections over an insert-only observation log is the right distinction: the raw/versioned tables support PIT queries, while the event log preserves what the pipeline actually observed and when. Residual note for Sprite: the CI "grep for UPDATE/DELETE" control is useful but should be treated as a minimum implementation guard, not the whole enforcement story if later code paths include migrations, notebooks, or direct database maintenance scripts.

**Finding 2 — Satisfied.** ADP-002 now excludes `ESTIMATED` rows from precise `days_to_earnings` and permits only coarse estimated-window features. That closes the leakage path identified in the finding, because the model no longer receives a precise day-count that could have been provider-backfilled from later-known actuals.

**Finding 3 — Satisfied.** ADP-003 now makes the extraction/canonical boundary mechanically visible through `data_authority`, extraction metadata, reviewer fields, and a promotion gate for `EXTRACTED_LLM`-sourced features. This is sufficient for the ADP level. Residual note: the implementation spec should define how mixed-source features are evaluated when a single feature aggregates both licensed structured rows and extracted rows.

**Finding 4 — Satisfied.** ADP-005's added single-lens benchmark rung materially strengthens the champion/challenger ladder. Pure Momentum and pure Quality baselines are appropriate first fixed baselines for this architecture because they test whether the multi-lens design is adding value beyond the most obvious factor exposures.

**Finding 5 — Satisfied with a numeric threshold note.** The Research Regime Classifier closes the cross-ADP gap: validation regimes are now separate from model inputs, PIT-filtered, predeclared, versioned, and frozen before model comparison. For ADP-005 Open Question 2, my recommendation is: the TFT-promotion regime-stability gate should be **inconclusive rather than pass/fail unless each of the 3 regime buckets has at least 3 independent historical episodes and at least 30 symbol-episode observations** in the relevant validation window. If that floor is not met, report the stratified results, but do not use the 2-of-3 regime rule as promotion evidence. Confidence-interval width should be metric-specific and set in the Phase 3/4 implementation spec, but the interval must at minimum be reported for the after-cost incremental metric versus the champion, not only for standalone TFT performance.

**Finding 6 — Satisfied with a peer-floor note.** ADP-006 now correctly separates research-universe validation from dashboard-universe display performance, and the rule that dashboard performance is reported only after model selection is finalized closes the dashboard-name overfitting gap. For ADP-006 Open Question 3, I do **not** recommend leaving the entire peer-size rule to Sprite after Phase 0. The exact sector list and universe count can be deferred to Sprite/vendor coverage, but the ADP should lock one mechanical minimum now: **no Relative Value feature should be promoted for a symbol-date unless the as-of peer group contains at least 3 active comparable securities total, including the target, and at least 2 non-target peers.** Below that floor, Relative Value features for that symbol-date should be `NULL`/withheld rather than computed from an undersized pseudo-peer set.

Overall final position: the amendments satisfy the six original findings for purposes of Sprite disposition, provided the amended ADP text, not the pre-review text, is the version carried forward.
- **Sprite decision:** *(filled in by Sprite only - Accepted / Deferred / Rejected)*

---

## Disposition

*(Owned by PM/Sprite per Condition 1 - Beer does not fill this in.)*

| Finding # | Status | Disposition Note | Decided By |
|---|---|---|---|
| 1 | Open | | |
| 2 | Open | | |
| 3 | Open | | |
| 4 | Open | | |
| 5 | Open | | |
| 6 | Open | | |
