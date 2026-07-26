# HANDOFF.md — Active Task/Phase State

*Operationally owned by Beer (Claude Code); append-only per author, per `WORKFLOWS.md` §7. Beer's granular Phase 1 task breakdown belongs here once the ADP bundle below is approved — this file has been empty until this entry.*

---

**Author:** Cola
**Timestamp:** 2026-07-26
**Content:**

Six ADPs filed in `docs/decision_log/`, all `Status: OPEN`, all requiring mandatory Matcha review before Sprite disposition (every one hits at least one `WORKFLOWS.md` §6 material-risk category):

1. `ADP-001-lens-hierarchy-and-traceability.md` — Core/Supporting model hierarchy, one-lens-per-feature registry
2. `ADP-002-bitemporal-versioning-calendar.md` — source versioning, `available_at`, calendar-tiering. **Foundation-tier, execute first.**
3. `ADP-003-fundamentals-filings-schema.md` — closes the Quality/fundamentals data gap. **Foundation-tier, execute first.** Blocked on Phase 0 vendor trial for loader implementation (schema shape not blocked).
4. `ADP-004-macro-regime-redesign.md` — removes `market_regime_code`, restores dropped macro feature set from `INITIAL_PROPOSAL.md` §4.
5. `ADP-005-champion-challenger-governance.md` — baseline-first model governance, named benchmarks, gate table.
6. `ADP-006-pilot-universe-and-data-rights.md` — two-tier universe (dashboard unchanged, research universe expanded for Relative Value). **Reopens Finding #3 explicitly via a new disposition-matrix row, not an edit.**

Companion draft: `docs/decision_log/ARCHITECTURE_v2_PROPOSED.md` — full proposed replacement for `ARCHITECTURE.md` §1–§4, referenced by all six ADPs. **Not yet merged into canonical `docs/ARCHITECTURE.md`.**

Sequencing recommendation: ADP-002 and ADP-003 first (foundation), ADP-004 and ADP-001 next (can proceed in parallel with each other, depend on 002/003), ADP-005 after 001/002, ADP-006 is business-layer and can be dispositioned by Sprite independent of implementation sequencing but blocks any research-universe-scope work until Phase 0 trial closes.

**Next action:** Sprite to route this bundle to Matcha for the mandatory reviews above before recording any disposition. None of these six ADPs have been Matcha-reviewed or Sprite-dispositioned yet — do not implement against them until that happens, per `WORKFLOWS.md` §5.2 (no Protected Section change without an approved ADP) and §12 (Beer never implements a Protected Section change without an approved ADP — this is the one absolute rule with no discretionary exception).

Phase 0 (data-rights/coverage trial: SGX Data Direct, EODHD, FMP) is in progress externally, run by Sprite — not yet closed as of this entry.

---

**Author:** Cola
**Timestamp:** 2026-07-26 (update 2)
**Content:**

**Matcha review received:** `reviews/2026-07-26_sensilnet-atpe-adps_matcha.md` — Summary Verdict: **Approve-with-conditions.** Six findings filed, all High/Medium confidence. Sharpest catch: Finding 5, a cross-ADP gap between ADP-004 (removes `market_regime_code`) and ADP-005 (regime-stability promotion gate) — neither specified how *validation* regime buckets get constructed once the categorical model-input feature is gone, which could have silently leaked future information into the promotion gate itself.

**Cola response filed:** all six findings accepted in full, no disagreement raised against any of them. Response recorded in the review file's Disagreement Loop section per `WORKFLOWS.md` §10.1 bounded process (one response, not a re-litigation).

**ADPs amended in place** (still `Status: OPEN`, pre-approval revision is normal, not a process bypass):
- `ADP-002`: two amendments — (1) added an immutable, append-only `ingestion_events` log as the actual PIT source-of-truth, with raw tables as a queryable projection over it; (2) `ESTIMATED` calendar rows excluded from precise `days_to_earnings` encoding, restricted to a coarse boolean/bucket signal only; `CONFIRMED` rows required for precise known-future-input use.
- `ADP-003`: one amendment — `raw_sgx_fundamentals` gains a mandatory `data_authority` field; any feature sourced from an `EXTRACTED_LLM` row cannot reach `PROMOTED` status without a populated `reviewer_id`/`review_status`, enforced as a join-based check in the feature-registry gate, not a policy statement.
- `ADP-004` + `ADP-005` (shared cross-ADP amendment): added a **Research Regime Classifier** — separate from any model input, built once before any training using only PIT-available macro data, methodology frozen before model comparison, referenced by version in every `validation_results` row. Resolves Finding 5 without reintroducing anything resembling the removed `market_regime_code` as a model feature.
- `ADP-005`: additional amendment — added named single-lens benchmarks (pure Momentum-only, pure Quality-only) as a required rung below the Core-lens baseline champion, so TFT promotion has to clear more than persistence/buy-and-hold.
- `ADP-006`: one amendment — explicit rule that dashboard-universe performance is reported but never used as a model-selection/promotion input; all gating decisions use research-universe metrics only, with dashboard performance generated as a downstream, read-only report after model selection is finalized.

**Two Matcha open questions remain genuinely unresolved** (not amendable unilaterally by Cola, flagged for Sprite/Matcha final reply):
- ADP-005 Open Question 2: no specific numeric threshold set yet for "minimum regime-episode count/CI width before the stability gate is inconclusive rather than pass/fail." Recommend Matcha propose a number in final reply, or defer to the Phase 3/4 implementation spec.
- ADP-006 Open Question 3: minimum peer-group size per sector not yet set as an explicit checkable rule. Recommend Sprite decide once Phase 0 vendor trial shows actual per-sector coverage.

**Next action:** Awaiting Matcha's final reply (per bounded disagreement loop — one reply, then Sprite dispositions). Once Matcha replies (or is silent, which per `WORKFLOWS.md` counts as the finding standing as filed), Sprite records dispositions for all six findings in the review file's Disposition table. No implementation should begin against any of these six ADPs until Sprite dispositions them as Accepted.