# ADP-006: Pilot UI Universe vs. Broader Research Universe, and Data Rights

**Status:** OPEN (amended post-Matcha-review, still pending Sprite disposition)
**Author:** Cola (Claude Desktop + Local MCP)
**Date:** 2026-07-26 (original); amended 2026-07-26 in response to Matcha review Finding 6
**Protected sections affected:** `docs/ARCHITECTURE.md` §1 (Vision — Pilot Universe section), §6 (Disposition Matrix — **new row required, not an edit to Finding #3**)
**Business-layer impact:** YES, significantly — vendor cost/selection, data-licensing budget, and this ADP explicitly **reopens a previously Resolved, independently-audited finding**. **Route to Sprite for explicit approval; this is not a routine technical ADP.**
**Material-risk category (WORKFLOWS.md §6):** YES — "Data source and licence decisions" directly, plus this specific ADP reopens Finding #3 which was itself independently reviewed by Matcha and signed off by Sprite in the original disposition round. **Mandatory Matcha review required before Sprite disposition — treat with more scrutiny than a routine ADP, not less, given it reopens settled work.**

---

## Problem

`docs/ARCHITECTURE.md` v1 §6, Finding #3: *"Pilot Universe... Resolved... Consolidated pilot watchlist to 5 STI stocks: DBS, OCBC, UOB, Singtel, SIA."* This was independently red-team reviewed (Matcha) and signed off (Sprite) per the existing Review Sign-off block.

However, `INVESTMENT_PHILOSOPHY.md` §5.4 (Relative Value, a Core Philosophy) requires dynamic peer analysis across SGX's naturally concentrated sectors — explicitly named: *"Banks, REITs, Telecommunications, Property Developers, Shipping, Industrial Conglomerates."* Of the current 5-name pilot, only DBS/OCBC/UOB form a real peer cohort (banks). Singtel (Telecom) and SIA (Transport) are each the sole representative of their sector in the pilot — meaning Relative Value, a Core Philosophy, is architecturally unimplementable for 2 of the 5 pilot names as currently scoped. This is a genuine conflict between an approved Core Philosophy and a previously-resolved architectural decision, not a preference for more data.

## Proposed Change

**Recommended: two-tier universe, not one.**

1. **Dashboard/UI pilot universe**: unchanged — DBS, OCBC, UOB, Singtel, SIA. Preserves the original proposal's "under 5 minutes on a home PC" lightweight constraint and keeps the dashboard focused.
2. **Research/training universe**: broader, sector-grouped (Banks, REITs, Telcos, Property, Shipping, Industrial Conglomerates per `INVESTMENT_PHILOSOPHY.md` §5.4), used to train models and compute dynamic peer groups, so Relative Value is actually implementable as designed — even for dashboard names outside a well-populated sector.

This is explicitly **not** a silent replacement of Finding #3. If approved, Finding #3 remains untouched (append-only per `WORKFLOWS.md` §6) and a **new** disposition-matrix row is added: *"Finding #3 superseded by ADP-006 — pilot universe (dashboard) unchanged; research/training universe expanded for Relative Value coverage."*

## Data-Rights Discipline (see also ADP-003)

- **yfinance: personal, disposable proof-of-concept only** — not used to source the expanded research universe in production. Its documentation is explicit that it is research/education-oriented and defers to Yahoo's own terms for actual data rights.
- **No SGXNET scraper as a default production source** — SGX's website terms restrict automated storage/reuse without permission.
- **Before this ADP can be dispositioned as Accepted**, the following must be confirmed via trial/quote from SGX Data Direct, EODHD, and FMP (a documented 30–50-name coverage test spanning banks, REITs, telecoms, transport, property, industrials):
  - Symbol and delisted-name coverage
  - 10-year EOD price history depth
  - Financial-statement completeness (see ADP-003)
  - `published_at`/`available_at` availability (see ADP-002)
  - NIM/CET1, DPU/NAV, margin/leverage coverage (see ADP-003)
  - Corporate-action and earnings-calendar accuracy
  - API latency, rate limits, failed-response rate
  - Licence rights for internal research use **and** any future display/dashboard use

**Expectation, not a result (to be confirmed by trial):** SGX Data Direct as strongest candidate for authoritative prices/announcements/corporate actions/structured issuer data; EODHD/FMP as rapid-development candidates for generic fundamentals; PDF extraction as a controlled fallback only, never the primary source.

**This ADP's schema/design shape (the two-tier universe structure) can be approved now. The specific sector list, name count, and provider selection are blocked on the Phase 0 trial closing** — this ADP does not ask Sprite to approve a specific expanded list today, only the two-tier design and the requirement that Finding #3 be superseded via a new row, not edited.

## Rationale

Resolves a genuine conflict between an approved Core Philosophy (Relative Value) and a previously-resolved scoping decision, without violating the disposition matrix's append-only discipline. Keeps the lightweight dashboard constraint from `INITIAL_PROPOSAL.md` intact by not conflating "what the UI shows" with "what the model trains on."

## Open Questions for Matcha Review

1. Given this reopens an already-audited finding, does the original review process require anything beyond a standard Matcha review — e.g., should Matcha's review explicitly reference and respond to the original Finding #3 reasoning, not just evaluate the new proposal in isolation?
2. Is the two-tier (dashboard vs. research universe) split itself sound, or does training on a broader universe than the dashboard displays introduce any distributional-shift risk between what the model learns and what it's ultimately evaluated/displayed on? — **Answered by Matcha Finding 6: yes, a real risk exists if model-selection is tuned against dashboard-name performance. See Amendment 1 below.**
3. Should minimum peer-group size (e.g., "no sector with fewer than N names") be an explicit, checkable requirement in `ref_sector_classification` (see `ARCHITECTURE_v2_PROPOSED.md` §3.7) rather than an implicit expectation? — **Still open; recommend Sprite decide a minimum N as part of Phase 0 universe scoping, informed by whatever coverage the vendor trial actually returns per sector.**

---

## Amendment 1 (post-Matcha-review — responds to Finding 6)

**Trigger:** Matcha review, `reviews/2026-07-26_sensilnet-atpe-adps_matcha.md`, Finding 6 — "The two-tier universe is justified, but evaluation must guard against dashboard-name overfitting." Accepted in full; Matcha's recommendation to accept the Finding #3 reopening as justified is noted and welcomed — this amendment addresses only the validation-hazard half of the finding.

**Gap:** The two-tier design solves the Relative Value coverage problem, but nothing in the original ADP prevented the small, preselected dashboard universe from silently becoming the de facto target of model tuning — feature selection, hyperparameters, peer-group definitions, or promotion decisions could all be adjusted repeatedly against how well the model happens to perform on DBS/OCBC/UOB/Singtel/SIA specifically, while the broader research universe gives a false impression of a large, robust sample size behind that tuning.

**Fix — explicit separation rule, added to `ARCHITECTURE_v2_PROPOSED.md` §4.3 and §5 (Research Baseline / TFT Promotion gates):**

- **Dashboard-universe performance is reported, never used as a selection criterion.** All model-selection, hyperparameter-tuning, feature-inclusion, and champion/challenger promotion decisions (ADP-005's gates) are made exclusively using research-universe validation metrics — computed and locked in before any dashboard-specific breakdown is generated or inspected.
- Concretely: the evaluation pipeline (§4.5 of the proposed architecture) produces two separate, clearly labeled report sections — **"Research Universe Validation"** (used for all gating decisions) and **"Dashboard Universe Display Performance"** (informational only, generated after model selection is finalized, never fed back into model iteration).
- This ordering is enforced procedurally, not just by convention: the Phase 3/4 implementation spec should generate the dashboard-performance report as a downstream, read-only step that runs strictly after a model has already been promoted per the research-universe gates — not as a parallel report generated during development, which would make it too easy to peek at and informally tune against.
- This directly parallels standard train/validation/test separation discipline, extended to a "trained-on vs. displayed-on" distinction specific to this project's two-tier universe design.

## Disposition

*(Pending Matcha final reply, then Sprite recording per WORKFLOWS.md §10. Given this reopens Finding #3, recommend Sprite review the original Finding #3 reasoning alongside this ADP before dispositioning. Note Matcha's Finding 6 explicitly recommends accepting the Finding #3 reopening as justified — this should be weighed in Sprite's final decision.)*
