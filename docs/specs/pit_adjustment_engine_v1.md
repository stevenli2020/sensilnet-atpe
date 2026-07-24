# Specification: PIT Corporate-Action Adjustment Engine (`src/data/pit_store.py`)

**Status:** DRAFT — pending independent resolution of open questions below. Not canonical. Not to be marked Resolved/Accepted by Beer under any circumstance (Team Structure v2, Condition 1).

**Author:** Beer (PL / Chief Architect)
**Risk Category:** PIT / Data Contract (Team Structure v2, Condition 5 — mandatory Matcha review)
**Depends on:** ARCHITECTURE.md §2.1, §3.1–3.3
**Version:** v1.1 — trial round draft, resolution routing added per Sprite approval 2026-07-24

---

## 1. Purpose

ARCHITECTURE.md §2.1 defines the adjustment factor $f_{i,\tau\mid t}$ and the PIT-adjusted price formula at the mathematical level, but does not specify:

- the exact algorithm `pit_store.py` uses to compute $P_{i,s\mid t}^{\text{adj}}$ from the three raw tables,
- ordering/precedence when multiple corporate actions land on the same date,
- behavior when `announced_date` is missing or later than `ex_date`,
- behavior when a corporate-action record is itself corrected or backfilled after other data has already been computed against it,
- what "known at cutoff $t$" means operationally when `raw_sgx_corporate_actions.ingested_at` and `ex_date` diverge.

This spec closes those gaps. It does not change the math in §2.1 — it operationalizes it.

---

## 2. Inputs

| Table | Relevant columns |
|---|---|
| `raw_sgx_daily` | `symbol, trade_date, raw_close, ingested_at` |
| `raw_sgx_corporate_actions` | `symbol, ex_date, action_type, action_value, announced_date, ingested_at` |

## 3. Core Algorithm

### 3.1 PIT eligibility filter (this is the part §2.1 leaves implicit)

A corporate action row is **eligible to affect** $P_{i,s\mid t}^{\text{adj}}$ only if:

```
action.ex_date <= t
AND action.ingested_at <= t
```

**Rationale:** §2.1 says the filtration $\mathcal{F}_t$ includes actions "announced and effective on or before $t$." `ex_date` captures *effective*. But *announced* must be represented by when the system actually learned about it — `ingested_at` — not `announced_date`. `announced_date` is often backfilled by data vendors well after the fact (SGX announcements corrected, re-filed, or vendor lag). Using `announced_date` alone as the PIT gate would silently reintroduce lookahead: a backtest run today could "know" about a dividend announced on `announced_date` that, in real time, the pipeline hadn't ingested yet.

**Edge case — missing `announced_date`:** Treat as `announced_date = ingested_at` for informational purposes only. The eligibility filter uses `ingested_at` regardless, so a missing `announced_date` does not change adjustment-factor computation. It should, however, raise a `DATA_QUALITY_WARNING` (not a hard failure) logged to a `pit_data_quality_log` table (new — see §5) so PM/Cola can audit vendor completeness later.

### 3.2 Same-date multiple-action ordering

If both a `SPLIT` and a `DIVIDEND` action exist for the same `symbol` and `ex_date`:

```
f_combined = f_split × f_dividend_adjusted
```

where `f_dividend_adjusted` uses the **post-split** reference price:

$$f_{\text{div}} = 1 - \frac{D_{i,\tau}}{P_{i,\tau-1}^{\text{raw}} / S_{i,\tau}}$$

**Rationale:** This is a real gap in §2.1's formula — it defines $f$ as a per-event-type cases function but doesn't say what happens when two event types coincide on the same $\tau$. SGX split-then-dividend-same-day is rare but not impossible (e.g. bonus issue + special dividend on the same ex-date). The order matters: dividend yield should be computed relative to the *post-split* price, since that's the price basis the dividend was actually declared against once both events are effective. Split is applied first in the multiplication.

**⚠ STATUS: NOT YET INDEPENDENTLY VERIFIED.** This formula reflects Beer's derivation only. Per resolution plan below, it must not be treated as settled until Cola produces an independent blind derivation.

> **Resolution Plan (approved by Sprite 2026-07-24):**
> Route to **Cola**, blind. Cola is to receive only ARCHITECTURE.md §2.1's per-event $f$ definitions and the same-day split+dividend scenario description — **not** the formula or derivation above — and independently derive the combined factor from first principles, including a worked numeric example (e.g. $S=2$, $P=\$10$, $D=\$0.05$) comparing both possible orderings (split-then-dividend vs. dividend-then-split) to demonstrate why order matters.
> Cola's result will be compared against the formula above. Match → treated as independently confirmed. Divergence → routed through the Team Structure v2 disagreement loop (Beer response → Cola/Matcha final reply → Sprite decision).
> Once settled, the confirmed formula must be encoded as a concrete unit test fixture in `tests/test_pit_adjustment.py`, closing Open Question 1 (§6) with a linked test, not just narrative agreement.
> **Status: PENDING — not yet routed to Cola.**

### 3.3 Late-arriving corrections to already-published corporate-action records

**Scenario:** A dividend amount for `ex_date = 2026-03-15` is ingested as `D = 0.28` on `2026-03-10`. Six weeks later, the vendor issues a correction: the true amount was `D = 0.30`.

**Two options considered:**

**Option A — Mutable correction (in-place UPDATE):**
Update the existing row. All PIT-adjusted prices computed on-the-fly at query time automatically reflect the corrected value going forward, since `pit_store.py` recomputes $P^{\text{adj}}$ dynamically rather than caching it.

**Option B — Immutable append + supersede:**
Never UPDATE `raw_sgx_corporate_actions`. Insert a new row with the corrected value and a `superseded_action_id` reference to the old row. `ingested_at` on the new row is the correction date, not the original.

**Recommendation: Option B.**

**Rationale:** Option A silently changes what "PIT-adjusted price as of $t$" meant for any backtest that already ran between 2026-03-10 and the correction date. If a backtest was executed on 2026-03-20 using the (wrong) $D=0.28$, and someone reruns "the same backtest" after the correction under Option A, they get a *different* result from the same nominal query — which breaks reproducibility and makes it impossible to distinguish "the model changed" from "the data vendor silently fixed a number underneath us." Option B preserves both: `P^adj` computed "as of 2026-03-20" uses the row with `ingested_at <= 2026-03-20` (the wrong value, faithfully reproducing what was actually knowable then), while `P^adj` computed "as of today" uses the corrected row. This is the same PIT discipline §2.1 already applies to prices — it just wasn't extended to corrections-of-corrections.

This is a real design decision, not just an implementation detail, and I want to flag it explicitly as **open question 2** rather than bury it as a settled default — Matcha and Sprite should weigh in on whether Option B's reproducibility guarantee is worth the added schema complexity (see §5) versus whether reproducibility-through-immutability is even required by ARCHITECTURE.md's stated PIT guarantee, or whether that's me adding a requirement that wasn't actually specified.

### 3.4 Missing corporate-action data (gap detection)

If `raw_sgx_daily.raw_close` shows a jump >15% overnight with no corresponding row in `raw_sgx_corporate_actions` for that `ex_date`, this likely indicates a missing/un-ingested corporate action (vendor lag) rather than a genuine price move.

**Behavior:** Do not auto-correct. Raise `PIT_GAP_SUSPECTED` to the data-quality log (§5) and exclude that `(symbol, trade_date)` from `features_sgx_daily` generation until manually reviewed, rather than silently treating an unadjusted corporate action as a genuine 15% return (which would corrupt both technical indicators computed over that window and the return-target labels in §2.2).

**⚠ STATUS: PLACEHOLDER, NOT CALIBRATED.** The 15% threshold is a guess, not a derived value.

> **Resolution Plan (approved by Sprite 2026-07-24):**
> Route to **PE**, with Cola available for statistical methodology support if needed. PE pulls actual historical corporate-action dates for the five pilot-universe names (DBS, OCBC, UOB, Singtel, SIA) across available history and measures the realized overnight price gap on each known ex-date. Compare a flat threshold against a volatility-normalized alternative (gap relative to trailing 20-day ATR, consistent with the ATR-percentile convention already established in ARCHITECTURE.md §4.2's regime derivation). Output — either "15% holds empirically" or a specific replacement rule — must be filed as a `docs/decision_log/` entry with the underlying data referenced, not asserted without evidence.
> **Status: PENDING — not yet routed to PE.**

---

## 4. Pseudocode

```python
def get_pit_adjusted_price(symbol: str, s: date, t: date) -> float:
    """
    Returns P_{i,s|t}^adj: price on date s, using only information
    knowable as of cutoff t.
    Requires s <= t.
    """
    raw = get_raw_close(symbol, s)  # from raw_sgx_daily

    eligible_actions = query(
        """
        SELECT ex_date, action_type, action_value
        FROM raw_sgx_corporate_actions
        WHERE symbol = ?
          AND ex_date > ?          -- s
          AND ex_date <= ?         -- t
          AND ingested_at <= ?     -- t  (PIT gate — see 3.1)
          AND superseded_action_id IS NULL  -- latest known version only, as of t
                                             -- (requires as-of superseded logic, see open Q2)
        ORDER BY ex_date ASC
        """,
        symbol, s, t, t
    )

    factor = 1.0
    # Group by ex_date to handle same-day multi-action case (3.2)
    for ex_date, actions_on_date in group_by_ex_date(eligible_actions):
        factor *= combined_factor_for_date(actions_on_date, prior_raw_close(symbol, ex_date))

    return raw * factor
```

Note: the `superseded_action_id IS NULL` clause as written above is a simplification — under Option B (3.3), correctly reproducing "state as of $t$" actually requires selecting the version of each action that was current *as of $t$*, not just the latest version overall. That needs its own as-of subquery (select the row with the max `ingested_at <= t` per `(symbol, ex_date, action_type)` chain). I've left this as pseudocode-level simplification and flagged it — the real implementation in `pit_store.py` needs this worked out precisely, and I'd want Cola's eyes on the actual SQL/DuckDB ASOF JOIN syntax for it rather than approximating here.

---

## 5. Schema additions required (not yet in ARCHITECTURE.md §3)

```sql
-- Extends 3.2 to support Option B (append-only corrections)
ALTER TABLE raw_sgx_corporate_actions ADD COLUMN superseded_action_id VARCHAR;
ALTER TABLE raw_sgx_corporate_actions ADD COLUMN action_id VARCHAR PRIMARY KEY; -- surrogate key replaces (symbol, ex_date, action_type) as PK

CREATE TABLE IF NOT EXISTS pit_data_quality_log (
    log_id VARCHAR PRIMARY KEY,
    symbol VARCHAR NOT NULL,
    event_type VARCHAR NOT NULL, -- 'DATA_QUALITY_WARNING', 'PIT_GAP_SUSPECTED'
    trade_date DATE,
    detail VARCHAR,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

This is a schema change to an already-approved ARCHITECTURE.md table (3.2's primary key changes from `(symbol, ex_date, action_type)` to a surrogate key). Flagging explicitly since that's a material change to a previously-Resolved item, not just an addition — Sprite/Matcha should treat this as reopening part of Finding #6, not as new scope.

---

## 6. Open Questions (explicitly not resolved by this draft)

1. Is split-then-dividend same-date ordering (§3.2) the correct convention, or does SGX/vendor data provide explicit sequencing? **→ Routed to Cola, blind derivation. See §3.2 Resolution Plan. PENDING.**
2. Does Option B (immutable append+supersede, §3.3) match what ARCHITECTURE.md's PIT guarantee actually requires, or is it Beer over-scoping the requirement? **→ Not yet routed. Candidate for Matcha review alongside §5's PK change.**
3. Is a flat 15% gap-detection threshold (§3.4) adequate, or should it be volatility-normalized per symbol? **→ Routed to PE, historical calibration against pilot-universe data. See §3.4 Resolution Plan. PENDING.**
4. The primary-key change to `raw_sgx_corporate_actions` (§5) touches a previously-Resolved schema (Finding #6) — does this need to go through the disagreement loop as a reopened finding rather than a fresh one? **→ Sprite/Matcha to confirm process treatment.**

---

## 7. What this spec does NOT cover (explicitly out of scope for v1)

- Sentiment/news PIT handling (already specified in ARCHITECTURE.md §4.4, unaffected by this doc)
- Index rebalance date PIT logic (separate from dividend/split adjustment — would need its own spec if not already adequately covered)
- Performance/query-latency of the dynamic ASOF computation at scale (flagged for Cola if this becomes a bottleneck in Phase 1 implementation)

---

## 8. Resolution Routing Log

| Open Question | Routed To | Method | Status | Linked Artifact |
|---|---|---|---|---|
| Q1 — §3.2 combined-factor math | Cola | Blind independent derivation + numeric example | PENDING | *(to be filed in `reviews/` once complete)* |
| Q2 — §3.3 Option B scope | Matcha | Independent review, bundled with §5 PK reopening | NOT YET ROUTED | — |
| Q3 — §3.4 threshold calibration | PE | Historical data analysis, 5 pilot names | PENDING | *(to be filed in `docs/decision_log/` once complete)* |
| Q4 — §5 process treatment (reopened Finding #6) | Sprite / Matcha | Process confirmation | NOT YET ROUTED | — |

---

**Handoff note for PM:** This draft is ready for evidence-packet versioning and routing to Matcha, Cola, and PE per §8. Per Condition 1, I am not marking any section of this Resolved — the open questions in §6 are specifically surfaced for independent judgment, not as rhetorical framing. §8 exists so the routing status is trackable without reconstructing it from chat history.
