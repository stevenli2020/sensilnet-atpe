# ADP-004: Macro Regime Redesign — Removal of the Hard-Coded `market_regime_code` Label

**Status:** OPEN
**Author:** Cola (Claude Desktop + Local MCP)
**Date:** 2026-07-26
**Protected sections affected:** `docs/ARCHITECTURE.md` §3.5 (`features_sgx_daily` schema — remove `market_regime_code` column), §4.2 (Feature Engineering — remove derivation protocol), §4.3 (Model Architecture — remove `market_regime_code` from Observed Past Inputs)
**Business-layer impact:** None directly.
**Material-risk category (WORKFLOWS.md §6):** YES — this reopens Disposition Matrix Finding #10 ("Market Regime Semantics," currently marked Resolved) and touches "Model-selection changes" and "Feature availability... encoding." **Mandatory Matcha review required before Sprite disposition.** Note: per `WORKFLOWS.md` §6 Disposition Matrix append-only rule, Finding #10 is **not edited** — this ADP, if approved, adds a **new** disposition-matrix row noting supersession, per the same discipline already applied to Finding #3 in ADP-006.

---

## Problem

`docs/ARCHITECTURE.md` v1 §4.2 defines `market_regime_code` as a categorical state `{0, 1, 2}` derived from:
- 20-day ATR percentile and ADX trend strength (technical/Momentum-lens signals), **combined with**
- rolling 3-day mean FinBERT news sentiment (Market Perception-lens signal)

...and labels the result "Bull/Sideways/Bear" — i.e., **Macro Regime**.

This is a specific, identifiable conflict with `INVESTMENT_PHILOSOPHY.md` §5.3, which defines Macro Regime exclusively in terms of macroeconomic data: *"interest rates, inflation, GDP growth, Purchasing Managers' Index (PMI), exchange rates, government bond yields, central bank announcements, money supply, market indices, sector indices."* No technical indicator or sentiment score appears anywhere in that definition.

The current implementation does not merely violate Principle 5 ("AI learns relationships rather than rules" — a hard-coded threshold rule) — it violates §5.7's non-overlap requirement more fundamentally: it fuses a Momentum-lens signal and a Market-Perception-lens signal into a single feature, then mislabels the result as a third, unrelated lens (Macro Regime). This is worse than a naming issue: any model trained on `market_regime_code` cannot distinguish "the market is trending with rising ADX" from "the actual macroeconomic backdrop has changed" — exactly the ambiguity `INVESTMENT_PHILOSOPHY.md` §5.3's Failure Modes section warns about (*"Unexpected Shocks... Historical macro relationships may temporarily break down. The model should learn these situations rather than assuming historical stability"* — impossible if macro conditions are never actually represented as a distinct input).

It is worth noting the prior disposition matrix (Finding #10) treated this as *resolved* by adding an aggregation protocol and verifying the Bull/Bear conditions are logically disjoint. That verification was correct on its own terms (the thresholds genuinely don't overlap) — but it verified internal consistency of the rule, not whether the rule measures what it claims to measure. Both things can be true: the rule is disjoint, and it is still the wrong rule.

## Proposed Change

See `docs/decision_log/ARCHITECTURE_v2_PROPOSED.md` §4.2.

- Remove `market_regime_code` entirely from the schema and pipeline — no categorical fused label is computed anywhere.
- ADX, ATR remain as separately-tagged Momentum-lens features (`feature_definitions.primary_lens = 'MOMENTUM'`).
- FinBERT sentiment (`news_sentiment_avg_3d` or equivalent) remains as a separately-tagged Market Perception-lens feature.
- **New, currently-missing** Macro Regime features are added using actual macroeconomic data: SORA/Fed rate levels, US10Y, inflation, PMI, FX (USD/SGD, DXY), commodities (Brent, Gold, Copper), regional indices (Nikkei, Hang Seng), BDI — per `INITIAL_PROPOSAL.md` §4's own Macro & Cross-Asset feature list, which v1's schema only partially implemented (only `sora_3m_rate` survived into the actual `features_sgx_daily` table; the rest of the proposal's macro list was dropped somewhere between proposal and v1 architecture, a second instance of the same drift pattern as ADP-003's fundamentals gap).
- The model (§4.3 of the proposed draft) learns interactions among Momentum, Macro, and Market Perception features directly, rather than having those interactions pre-decided by a fixed threshold rule.

## Rationale

This is the single clearest Principle 5 + Principle 4 (explainability) violation identified in the current architecture. Removing the fused label, restoring the dropped macro feature set, and letting the model learn the interaction is the direct, minimal fix.

## Priority

Should be sequenced after ADP-002/ADP-003 (foundation) but does not itself require new raw data sources beyond what `INITIAL_PROPOSAL.md` already specified for Macro & Cross-Asset — this is largely a restoration of dropped scope plus a removal, not new build. Lower implementation risk than ADP-002/003; can proceed in parallel with ADP-001.

## Open Questions for Matcha Review

1. Does removing `market_regime_code` require any retraining/compatibility consideration for downstream consumers (dashboard, evaluation reports) that may have referenced it, or is this purely a Phase-1/pre-implementation change with no live consumers yet? (Current understanding: no model has been trained yet — `src/models/` is empty scaffolding per `SESSION_HANDOFF.md` — so no compatibility risk exists in practice.)
2. Is there any legitimate use for a categorical regime label as a human-readable dashboard summary (distinct from a model input), or should regime communication to the end user also be redesigned as a lens-attribution display rather than a single Bull/Sideways/Bear tag?

## Disposition

*(Pending Matcha review, then Sprite recording per WORKFLOWS.md §10.)*
