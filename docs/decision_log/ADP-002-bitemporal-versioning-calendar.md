# ADP-002: Bitemporal Data, Source Versioning, and Calendar Availability

**Status:** OPEN
**Author:** Cola (Claude Desktop + Local MCP)
**Date:** 2026-07-26
**Protected sections affected:** `docs/ARCHITECTURE.md` §2 (Data Contracts — PIT filtration extension), §3 (Schemas — `raw_sgx_ohlcv`, `raw_sgx_corporate_actions`, `raw_sgx_corporate_calendar` revisions), §4.1 (Ingestion & PIT Storage Engine responsibility)
**Business-layer impact:** None directly — technical data-contract change within Cola's authority.
**Material-risk category (WORKFLOWS.md §6):** YES — "PIT / data contracts (timestamp semantics, adjustment logic, corporate-action handling)" and "Feature availability and known-future-input encoding." **Mandatory Matcha review required before Sprite disposition.** This is also flagged in `SESSION_HANDOFF.md` §4 as an item requiring "mandatory Matcha review" the moment it's raised — this ADP is that raising.

---

## Problem

Three concrete gaps in v1's PIT design, despite v1's core adjustment-factor math (`ARCHITECTURE.md` §2.1) being independently verified correct in the prior Cola review sign-off:

1. **Silent overwrite risk.** `raw_sgx_daily` uses `PRIMARY KEY (symbol, trade_date)`; `raw_sgx_corporate_actions` uses `PRIMARY KEY (symbol, ex_date, action_type)`. A vendor restatement of historical OHLCV, or a corrected dividend amount, silently overwrites the existing row with no trace of what the system believed before the correction. This undermines reproducibility of any backtest run before the correction was applied.
2. **No `available_at` field distinct from `ingested_at`.** v1's raw tables record only when the pipeline happened to ingest a record, not when that data was actually knowable/available from the source. These can differ (feed latency, batch delays), and PIT correctness requires filtering on availability, not ingestion timing.
3. **Calendar availability is entirely unproven.** `raw_sgx_corporate_calendar` (v1 §3.3) has only `event_date` and `ingested_at`. There is no way to demonstrate that `days_to_earnings` — used directly as a Known Future Input to the TFT encoder (v1 §4.3) — was actually knowable at the historical decision date used in any backtest. This is a real, not hypothetical, PIT-leakage risk in exactly the "Known Future Inputs" category that Finding #5 in the existing disposition matrix already treats as resolved (it is not fully resolved with respect to *provenance*, only with respect to *field existence*).

## Proposed Change

See `docs/decision_log/ARCHITECTURE_v2_PROPOSED.md` §2.2–§2.3 and §3.1–§3.3 for full schema.

- All raw tables gain: `record_id` (surrogate key), `source_id`, `source_version`, `content_hash`, `available_at`, `superseded_by` (nullable self-referencing FK). Natural-key `PRIMARY KEY` constraints removed in favor of surrogate keys plus a "latest non-superseded version as of `t`" resolution rule in `pit_store.py`.
- Corporate calendar table gains `event_date_status` (`ESTIMATED`/`CONFIRMED`/`REVISED`) and `announced_at`, tiered by risk:
  - **Earnings dates: highest priority** — exact dates frequently unconfirmed/revised; every revision is a new versioned row.
  - **Ex-dividend dates: required, lower risk** — still versioned, but typically reliable once announced.
  - **Index rebalance windows: required, lowest risk** — provider-scheduled and most predictable, but still carries the same evidence requirement, no exemption.
- PIT replay validation (Phase 1 gate): re-running feature computation for a historical `as_of` date must reproduce the same feature set **within a stated numerical tolerance**, not byte-identical. Byte-identical is explicitly rejected as the gate criterion — floating-point non-associativity across GPU kernels/BLAS thread counts can shift results at a level unrelated to actual PIT leakage. Tolerance bound to be specified per feature type in the Phase 1 implementation spec (e.g., relative error bound), not left undefined at ADP stage.

## Rationale

Directly resolves `SESSION_HANDOFF.md` §4, item 2 and 3 (Q1/Q3 in `docs/specs/pit_adjustment_engine_v1.md`) by making versioning and calendar-availability structural rather than something resolved ad hoc per-question. Also closes the "silent overwrite" defect surfaced during architecture review discussion, independently of the existing open questions in the PIT adjustment spec.

## Relationship to Existing Open Spec

`docs/specs/pit_adjustment_engine_v1.md` (DRAFT, v1.1) has four unresolved questions (§8 routing log). This ADP does not resolve those questions directly — it changes the schema those questions are asked against. Recommend: resolve this ADP first (schema shape), then re-derive the PIT spec's four open questions against the new schema, since the same-day split+dividend ordering question (Q1) and the PK-reopening question (Q4) may need re-statement once natural keys are removed.

## Priority

Per design-discussion consensus already reached: **this ADP and ADP-003 are the foundation and should be executed first**, before ADP-001, ADP-004, ADP-005 are implemented, since all of them build features/models on top of this schema.

## Open Questions for Matcha Review

1. Is surrogate-key-plus-`superseded_by` sufficient for reproducibility, or does the system additionally need an immutable event log (append-only, separate from the queryable table) as a stronger guarantee?
2. What numerical tolerance is appropriate for the PIT-replay gate, and should it be uniform across feature types or set per-feature-type in `feature_definitions`?
3. Does `event_date_status = 'ESTIMATED'` create a risk that estimated-and-later-wrong earnings dates get used in historical feature construction in a way that's hard to detect after the fact? Should ESTIMATED rows be excluded from Known-Future-Input encoding entirely until CONFIRMED?

## Disposition

*(Pending Matcha review, then Sprite recording per WORKFLOWS.md §10.)*
