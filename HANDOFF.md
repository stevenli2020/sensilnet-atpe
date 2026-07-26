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
