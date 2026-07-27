# ADP-006: Pilot UI Universe vs. Broader Research Universe, and Data Rights

**Status:** APPROVED (per Sprite disposition, `reviews/2026-07-26_sensilnet-atpe-adps_matcha.md`, 2026-07-26 — all six bundle findings Accepted). Finding #3 in `docs/ARCHITECTURE.md` §6 to be superseded by a new disposition-matrix row referencing this ADP, per the append-only rule — not edited.
**Author:** Cola (Claude Desktop + Local MCP)
**Date:** 2026-07-26 (original); amended 2026-07-26 in response to Matcha review Finding 6; amended again 2026-07-26 to fold Matcha's final-reply numeric threshold (Amendment 2)
**Protected sections affected:** `docs/ARCHITECTURE.md` §1 (Vision — Pilot Universe section), §6 (Disposition Matrix — **new row required, not an edit to Finding #3**)
**Business-layer impact:** YES, significantly — vendor cost/selection, data-licensing budget, and this ADP explicitly **reopens a previously Resolved, independently-audited finding**. **Sprite has explicitly approved this reopening** — see disposition.
**Material-risk category (WORKFLOWS.md §6):** YES — "Data source and licence decisions" directly, plus this specific ADP reopens Finding #3 which was itself independently reviewed by Matcha and signed off by Sprite in the original disposition round. **Mandatory Matcha review complete — see disposition above.**

---

## Problem

`docs/ARCHITECTURE.md` v1 §6, Finding #3: *"Pilot Universe... Resolved... Consolidated pilot watchlist to 5 STI stocks: DBS, OCBC, UOB, Singtel, SIA."* This was independently red-team reviewed (Matcha) and signed off (Sprite) per the existing Review Sign-off block.

However, `INVESTMENT_PHILOSOPHY.md` §5.4 (Relative Value, a Core Philosophy) requires dynamic peer analysis across SGX's naturally concentrated sectors — explicitly named: *"Banks, REITs, Telecommunications, Property Developers, Shipping, Industrial Conglomerates."* Of the current 5-name pilot, only DBS/OCBC/UOB form a real peer cohort (banks). Singtel (Telecom) and SIA (Transport) are each the sole representative of their sector in the pilot — meaning Relative Value, a Core Philosophy, is architecturally unimplementable for 2 of the 5 pilot names as currently scoped. This is a genuine conflict between an approved Core Philosophy and a previously-resolved architectural decision, not a preference for more data.

## Proposed Change

**Recommended: two-tier universe, not one.**

1. **Dashboard/UI pilot universe**: unchanged — DBS, OCBC, UOB, Singtel, SIA. Preserves the original proposal's "under 5 minutes on a home PC" lightweight constraint and keeps the dashboard focused.
2. **Research/training universe**: broader, sector-grouped (Banks, REITs, Telcos, Property, Shipping, Industrial Conglomerates per `INVESTMENT_PHILOSOPHY.md` §5.4), used to train models and compute dynamic peer groups, so Relative Value is actually implementable as designed — even for dashboard names outside a well-populated sector.

This is explicitly **not** a silent replacement of Finding #3. Finding #3 remains untouched (append-only per `WORKFLOWS.md` §6) and a **new** disposition-matrix row is added: *"Finding #3 superseded by ADP-006 — pilot universe (dashboard) unchanged; research/training universe expanded for Relative Value coverage."*

## Data-Rights Discipline (see also ADP-003)

- **yfinance: personal, disposable proof-of-concept only** — not used to source the expanded research universe in production. Its documentation is explicit that it is research/education-oriented and defers to Yahoo's own terms for actual data rights.
- **No SGXNET scraper as a default production source** — SGX's website terms restrict automated storage/reuse without permission.
- **Before implementation begins against this ADP**, the following must be confirmed via trial/quote from SGX Data Direct, EODHD, and FMP (a documented 30–50-name coverage test spanning banks, REITs, telecoms, transport, property, industrials):
  - Symbol and delisted-name coverage
  - 10-year EOD price history depth
  - Financial-statement completeness (see ADP-003)
  - `published_at`/`available_at` availability (see ADP-002)
  - NIM/CET1, DPU/NAV, margin/leverage coverage (see ADP-003)
  - Corporate-action and earnings-calendar accuracy
  - API latency, rate limits, failed-response rate
  - Licence rights for internal research use **and** any future display/dashboard use

**Expectation, not a result (to be confirmed by trial):** SGX Data Direct as strongest candidate for authoritative prices/announcements/corporate actions/structured issuer data; EODHD/FMP as rapid-development candidates for generic fundamentals; PDF extraction as a controlled fallback only, never the primary source.

**This ADP's schema/design shape (the two-tier universe structure, and Amendment 2's peer-floor rule) is approved now. The specific sector list, name count, and provider selection remain blocked on the Phase 0 trial closing.**

## Rationale

Resolves a genuine conflict between an approved Core Philosophy (Relative Value) and a previously-resolved scoping decision, without violating the disposition matrix's append-only discipline. Keeps the lightweight dashboard constraint from `INITIAL_PROPOSAL.md` intact by not conflating "what the UI shows" with "what the model trains on."

## Open Questions for Matcha Review — Resolved

1. Given this reopens an already-audited finding, does the original review process require anything beyond a standard Matcha review? — **Matcha's review directly engaged with the Finding #3 reasoning rather than evaluating in isolation (see Finding 6's description), which satisfies this concern.**
2. Is the two-tier split sound, or does it introduce distributional-shift risk between what the model trains on and what it's displayed/evaluated on? — **Resolved by Matcha Finding 6: yes, a real risk exists absent an explicit separation rule. See Amendment 1.**
3. Should minimum peer-group size be an explicit, checkable requirement rather than an implicit expectation? — **Resolved by Matcha's final reply and Amendment 2 below: Matcha explicitly declined to defer this in full to Phase 0, and specified a concrete mechanical floor now.**

---

## Amendment 1 (post-Matcha-review — responds to Finding 6)

**Trigger:** Matcha review, `reviews/2026-07-26_sensilnet-atpe-adps_matcha.md`, Finding 6 — "The two-tier universe is justified, but evaluation must guard against dashboard-name overfitting." Accepted in full; Matcha's recommendation to accept the Finding #3 reopening as justified is noted and welcomed — this amendment addresses only the validation-hazard half of the finding.

**Gap:** The two-tier design solves the Relative Value coverage problem, but nothing in the original ADP prevented the small, preselected dashboard universe from silently becoming the de facto target of model tuning — feature selection, hyperparameters, peer-group definitions, or promotion decisions could all be adjusted repeatedly against how well the model happens to perform on DBS/OCBC/UOB/Singtel/SIA specifically, while the broader research universe gives a false impression of a large, robust sample size behind that tuning.

**Fix — explicit separation rule, added to `ARCHITECTURE_v2_PROPOSED.md` §4.3 and §5 (Research Baseline / TFT Promotion gates):**

- **Dashboard-universe performance is reported, never used as a selection criterion.** All model-selection, hyperparameter-tuning, feature-inclusion, and champion/challenger promotion decisions (ADP-005's gates) are made exclusively using research-universe validation metrics — computed and locked in before any dashboard-specific breakdown is generated or inspected.
- Concretely: the evaluation pipeline (§4.5 of the proposed architecture) produces two separate, clearly labeled report sections — **"Research Universe Validation"** (used for all gating decisions) and **"Dashboard Universe Display Performance"** (informational only, generated after model selection is finalized, never fed back into model iteration).
- This ordering is enforced procedurally, not just by convention: the Phase 3/4 implementation spec should generate the dashboard-performance report as a downstream, read-only step that runs strictly after a model has already been promoted per the research-universe gates — not as a parallel report generated during development, which would make it too easy to peek at and informally tune against.
- This directly parallels standard train/validation/test separation discipline, extended to a "trained-on vs. displayed-on" distinction specific to this project's two-tier universe design.

## Amendment 2 (post-Matcha-final-reply — numeric floor for Open Question 3)

**Trigger:** Matcha final reply (`reviews/2026-07-26_sensilnet-atpe-adps_matcha.md`), responding to Finding 6 — explicitly declined to defer the entire peer-size question to Sprite/Phase 0, and proposed a mechanical floor now. Accepted per Sprite's disposition, which noted Matcha's explicit recommendation not to defer this specific mechanical minimum.

**Rule, added to `ref_sector_classification`-driven peer-group construction (`ARCHITECTURE_v2_PROPOSED.md` §3.7):** No Relative Value feature may be promoted for a given symbol-date unless the as-of peer group contains:
- at least **3 active comparable securities total** (including the target), **and**
- at least **2 non-target peers**

Below this floor, Relative Value features for that symbol-date are `NULL`/withheld rather than computed from an undersized pseudo-peer set. The broader sector list, name count, and provider selection remain deferred to Sprite pending the Phase 0 vendor trial, per the original ADP — this floor applies regardless of how that broader scoping resolves.

## Disposition

**Accepted.** See `reviews/2026-07-26_sensilnet-atpe-adps_matcha.md` Disposition section, Finding 6 entry, recorded by Sprite 2026-07-26. This ADP's `Status` is updated to `APPROVED` accordingly. Finding #3 supersession row to be added to `docs/ARCHITECTURE.md` §6 disposition matrix as a new append-only entry (not an edit) as part of implementation kickoff.
