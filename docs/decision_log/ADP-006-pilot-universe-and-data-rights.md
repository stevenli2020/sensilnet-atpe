# ADP-006: Pilot UI Universe vs. Broader Research Universe, and Data Rights

**Status:** OPEN
**Author:** Cola (Claude Desktop + Local MCP)
**Date:** 2026-07-26
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
2. Is the two-tier (dashboard vs. research universe) split itself sound, or does training on a broader universe than the dashboard displays introduce any distributional-shift risk between what the model learns and what it's ultimately evaluated/displayed on?
3. Should minimum peer-group size (e.g., "no sector with fewer than N names") be an explicit, checkable requirement in `ref_sector_classification` (see `ARCHITECTURE_v2_PROPOSED.md` §3.7) rather than an implicit expectation?

## Disposition

*(Pending Matcha review, then Sprite recording per WORKFLOWS.md §10. Given this reopens Finding #3, recommend Sprite review the original Finding #3 reasoning alongside this ADP before dispositioning.)*
