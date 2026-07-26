# ADP-001: Investment Framework Traceability, Core/Supporting Hierarchy, and Horizon Metadata

**Status:** OPEN
**Author:** Cola (Claude Desktop + Local MCP)
**Date:** 2026-07-26
**Protected sections affected:** `docs/ARCHITECTURE.md` §1 (Vision), §3 (Schemas — new `feature_definitions` table), §4 (Component Responsibilities — §4.2, §4.3)
**Business-layer impact:** None directly — this is a technical-architecture change within Cola's authority per `WORKFLOWS.md` §4. Logged here for Sprite visibility per §12, not requiring Sprite approval on business grounds alone.
**Material-risk category (WORKFLOWS.md §6):** YES — "Model-selection changes (architecture, loss function, output heads)" and "Major refactors touching more than one subsystem." **Mandatory Matcha review required before Sprite disposition.**

---

## Problem

Two gaps in v1:

1. **No mechanism enforces one-lens-per-feature.** `docs/ARCHITECTURE.md` v1 §4.2 lists technical/macro/sentiment features with no lens tagging at all — nothing prevents a feature from ambiguously serving two philosophies, which `INVESTMENT_PHILOSOPHY.md` §5.7 explicitly warns against: *"If two philosophies answer the same question, one is probably unnecessary."*
2. **All 8 lenses are architecturally flat.** v1 §4.3's TFT input structure (static/known-future/observed-past) treats every feature as an equal-weight input to a single model. This directly contradicts `INVESTMENT_PHILOSOPHY.md` §6: *"The committee deliberately rejected the idea of treating them as equal voting systems. Core Philosophies establish the investment thesis. Supporting Philosophies strengthen, weaken or refine confidence in that thesis."* Value, Earnings Revision, and Market Perception are explicitly Supporting (§5.5, §5.7, §5.8) and should never carry equal architectural weight to Momentum/Quality/Macro/Relative Value/Event-Driven.

A related, smaller gap: v1 has no representation of `INVESTMENT_PHILOSOPHY.md` §7's horizon-tiering (Quality/Value → long horizon; Momentum/Macro/Relative Value → medium; Event-Driven/Market Perception/Earnings Revision → short).

## Proposed Change

See `docs/decision_log/ARCHITECTURE_v2_PROPOSED.md` §3.8 (`feature_definitions` table, with `primary_lens` and `lens_role` `CHECK` constraints) and §4.3 (Core-lens baseline + Supporting-lens learned gating layer).

Concretely:
- Every engineered feature registers into `feature_definitions` with exactly one `primary_lens` (of 8) and one `lens_role` (`CORE` or `SUPPORTING`) — enforced by a database constraint, not a documentation convention.
- Model architecture (§4.3 of the proposed draft) computes a base signal from Core-lens features, then applies a learned, horizon-specific gate from Supporting-lens features to strengthen/weaken/qualify that signal.
- `horizon_weight_prior` field captures §7's tiering as a **modelling prior and evaluation lens**, not a hard filter — the model can still learn to deviate from the prior if evidence supports it, preserving Principle 5 ("AI learns relationships rather than rules").

## Clarification Refinement (from design discussion, incorporated)

One raw input may support multiple lenses through different transforms — e.g. raw ROE → a Quality feature; peer-relative ROE spread → a separate Relative Value feature. The one-lens rule applies to each **derived, engineered feature**, not to raw source data. This preserves conceptual clarity without duplicating ingestion.

## Rationale

Directly closes the gap identified across the design-review conversation: prior architecture revisions (including the one immediately preceding this ADP) proposed a philosophy-mapped feature *table* but did not specify a mechanism differentiating Core from Supporting weight in the model itself — this ADP is what makes that mechanism concrete and queryable rather than a documentation note.

## Open Questions for Matcha Review

1. Is a database `CHECK` constraint sufficient enforcement, or does the lens-tagging discipline need an additional code-level gate (e.g., a CI check that fails if a feature is registered without a lens)?
2. Does the proposed "learned gating layer" for Supporting lenses introduce a new class of overfitting risk (a second learned component beyond the base model) that needs its own validation criteria distinct from the base model's?
3. Is `horizon_weight_prior` as a soft prior (rather than a hard constraint) adequately falsifiable — i.e., can we detect if the model is silently ignoring the prior versus correctly learning to override it with evidence?

## Disposition

*(Pending Matcha review, then Sprite recording per WORKFLOWS.md §10 — not filled by Cola.)*
