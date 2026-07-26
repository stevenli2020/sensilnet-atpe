# ADP-003: Fundamentals, Filings, and Earnings-Estimates Schema

**Status:** OPEN (amended post-Matcha-review, still pending Sprite disposition)
**Author:** Cola (Claude Desktop + Local MCP)
**Date:** 2026-07-26 (original); amended 2026-07-26 in response to Matcha review Finding 3
**Protected sections affected:** `docs/ARCHITECTURE.md` §3 (Schemas — new `raw_sgx_fundamentals`, `raw_sgx_announcements` tables), §4.1 (Ingestion responsibility expansion)
**Business-layer impact:** YES — this ADP's scope and timeline are contingent on the Phase 0 data-rights/coverage evaluation (SGX Data Direct / EODHD / FMP trial), which has cost and vendor-selection implications. **Route to Sprite** per `WORKFLOWS.md` §12 (business-layer concerns: cost, vendor selection).
**Material-risk category (WORKFLOWS.md §6):** YES — "Data source and licence decisions" (directly) and "Feature availability and known-future-input encoding." **Mandatory Matcha review required before Sprite disposition.**

---

## Problem

`docs/INITIAL_PROPOSAL.md` §4 ("Comprehensive Feature Matrix") lists a full Company Fundamentals category as a day-one feature source: Quarterly EPS, Debt/Equity, Quick Ratio, P/E, Forward P/E, P/B, Dividend Yield, Share Buybacks, plus Known Future Events (Ex-Dividend Dates, Earnings Release Dates).

`docs/ARCHITECTURE.md` v1's actual schema (§3.1–§3.5) contains **zero tables** for any of this. There is no `raw_sgx_fundamentals` table, no filings table, no earnings-estimates table. Quality is a Core Philosophy (`INVESTMENT_PHILOSOPHY.md` §5.2) built entirely from ROE, ROA, margins, FCF, debt ratios, earnings consistency, capital efficiency — none of which have a data source anywhere in the current architecture. This is not a minor enhancement; it is a Core Philosophy with no implementable data path.

Additionally, `INVESTMENT_PHILOSOPHY.md` §5.7 (Earnings Revision, Supporting Philosophy) requires analyst forecasts, consensus revisions, and target-price revisions as preferred inputs, with management guidance and historical earnings trend as fallback — none of which exist in v1 either.

## Proposed Change

See `docs/decision_log/ARCHITECTURE_v2_PROPOSED.md` §3.4 (`raw_sgx_fundamentals`) and §3.5 (`raw_sgx_announcements`).

Phased approach, sequenced against the Phase 0 vendor trial (not assumed to resolve before this ADP is filed):

**Phase 1 (rapid baseline, once a commercial API trial is confirmed):** generic statement fields only — Revenue, Net Income, Total Assets, Total Liabilities, Operating/Free Cash Flow, Shares Outstanding, dividends, corporate actions. Populate via whichever provider (EODHD/FMP) wins the initial coverage test.

**Phase 2 (SGX-specific depth):** sector-specific fields —
- Banks: NIM, CET1 ratio, loan growth, cost-to-income
- REITs: DPU, NAV per unit, gearing ratio, occupancy rate
- Industrials/Conglomerates: operating margin, leverage, cash conversion

Preferred source for Phase 2: SGX's licensed announcement/reference feeds. Where a structured feed doesn't cover a sector-specific field, `pdfplumber` + structured LLM extraction from issuer reports is permitted as a **source-backed enrichment and reconciliation workflow** — explicitly not the canonical feed. Every extracted value stores: the original source document reference, extraction method/version, source timestamp, and a `reviewer/validation_status` field (not auto-promoted to `PROMOTED` status in `feature_definitions` without review). **See Amendment 1 below — this boundary is now mechanically enforced, not just stated.**

**Earnings estimates** (for ADP-related `Earnings Revision` lens): analyst forecast/consensus data where the winning provider covers it; fallback to management guidance + historical earnings trend extraction where it doesn't, per `INVESTMENT_PHILOSOPHY.md` §5.7's own stated fallback design.

## Data-Rights Discipline (explicit, non-negotiable in this ADP)

- **yfinance: proof-of-concept / personal use only.** Its own documentation frames it as research/education-oriented and defers to Yahoo's terms for actual data rights — not used as a production source for this schema.
- **No SGXNET scraper as a default production source.** SGX's website terms restrict automated storage/reuse without permission. Use SGX Data Direct (licensed) or obtain written permission first. This is a hard constraint on this ADP's implementation, not a preference.
- Before promoting any provider to source-of-record status for this schema: confirm history depth, statement-availability timestamps, restatement/revision handling, internal model-training rights, cloud storage rights, and any dashboard/display rights — not just raw field coverage.

## Rationale

Closes the single largest data gap between `INITIAL_PROPOSAL.md`'s stated feature scope and what `ARCHITECTURE.md` v1 actually implements. Without this, Quality (Core) and Earnings Revision (Supporting) are philosophies in name only.

## Dependency

Blocked on Phase 0 vendor trial results (provider scorecard: symbol/delisted-name coverage, 10-year EOD history, statement completeness, `published_at`/`available_at` availability, NIM/CET1/DPU/NAV coverage, corporate-action/earnings-calendar accuracy, API latency/rate limits, licence rights). **This ADP's schema shape (§3.4–§3.5 of the proposed architecture) is not blocked and can be approved now; the loader implementation and field-population timeline is blocked until Phase 0 closes.**

## Open Questions for Matcha Review

1. Is the "PDF extraction as reconciliation, not canonical feed" boundary sufficiently enforceable, or does it need a stricter mechanical gate (e.g., `feature_definitions.validation_status` cannot reach `PROMOTED` for any feature sourced primarily from extraction without a named human reviewer field populated)?
2. Are the named sector-specific fields (NIM, CET1, DPU, NAV, gearing, occupancy) the right minimum set, or is this list itself something that should go through independent review before being locked into the schema?

## Priority

Foundation-tier, alongside ADP-002 — execute first.

---

## Amendment 1 (post-Matcha-review — responds to Finding 3)

**Trigger:** Matcha review, `reviews/2026-07-26_sensilnet-atpe-adps_matcha.md`, Finding 3 — "PDF/LLM extraction can become canonical by accident." Accepted in full; directly answers Open Question 1 above.

**Gap:** The original ADP stated in prose that extraction is "enrichment, not canonical," but the proposed `raw_sgx_fundamentals` schema (`ARCHITECTURE_v2_PROPOSED.md` §3.4) had no field distinguishing a licensed structured-data row from an extracted one, and `validation_status` lived only at the `feature_definitions` level — meaning a feature could be promoted without the underlying row's provenance being checked at all. Once an extracted value sits in the same table shape as vendor-provided fundamentals, downstream code has no way to know which rows carry which evidentiary weight.

**Fix, applied to `raw_sgx_fundamentals` (`ARCHITECTURE_v2_PROPOSED.md` §3.4):**

```sql
-- Added columns:
    data_authority VARCHAR NOT NULL CHECK (data_authority IN
        ('LICENSED_STRUCTURED', 'EXTRACTED_LLM', 'MANUAL_ENTRY')),
    extraction_method VARCHAR,      -- NULL unless data_authority = 'EXTRACTED_LLM'
    extraction_doc_ref VARCHAR,     -- pointer to the original stored source document
    reviewer_id VARCHAR,            -- NULL unless reviewed
    review_timestamp TIMESTAMP,     -- NULL unless reviewed
    review_status VARCHAR CHECK (review_status IN ('PENDING','REVIEWED','REJECTED') OR review_status IS NULL)
```

**Mechanical enforcement, applied to `feature_definitions` (§3.8):**

Any feature whose `source_tables` includes a `raw_sgx_fundamentals` row with `data_authority = 'EXTRACTED_LLM'` **cannot** reach `validation_status = 'PROMOTED'` unless the corresponding source row has `reviewer_id IS NOT NULL AND review_status = 'REVIEWED'`. This is a join-based check run as part of the Phase 1/2 feature-registry gate (§5 of the proposed architecture), not a documentation convention someone has to remember to apply. `LICENSED_STRUCTURED` and `MANUAL_ENTRY` rows are exempt from this specific gate (manual entry carries its own separate operator-sign-off requirement, unchanged from the original ADP).

This closes the gap directly: extraction-derived data can enter the system and be inspected, reconciled, and even used in draft/unpromoted analysis, but it structurally cannot become a promoted model input without a named human reviewer's sign-off recorded against it.

## Disposition

*(Pending Matcha final reply, then Sprite recording per WORKFLOWS.md §10.)*
