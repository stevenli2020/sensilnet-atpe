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

---

**Author:** Cola
**Timestamp:** 2026-07-26 (update 3 — FINAL, bundle approved)
**Content:**

**Matcha's final reply received and Sprite disposition recorded.** All six findings: **Accepted.** See `reviews/2026-07-26_sensilnet-atpe-adps_matcha.md` Disposition section for the full per-finding record. Bounded disagreement loop (`WORKFLOWS.md` §10.1) complete for this review.

Matcha's final reply supplied two concrete numeric thresholds that were open questions, rather than deferring them — both now folded directly into ADP text as a second amendment round (not left as review-file commentary only):
- **`ADP-005` Amendment 2:** TFT-promotion regime-stability gate is `INCONCLUSIVE` (not pass/fail) unless each of the 3 regime buckets has ≥3 independent historical episodes AND ≥30 symbol-episode observations.
- **`ADP-006` Amendment 2:** No Relative Value feature may be promoted for a symbol-date unless the as-of peer group has ≥3 active comparables total (incl. target) AND ≥2 non-target peers; below that floor, withhold as `NULL`.

**All six ADPs now `Status: APPROVED`:**
- `ADP-001-lens-hierarchy-and-traceability.md`
- `ADP-002-bitemporal-versioning-calendar.md` (+ 2 amendments)
- `ADP-003-fundamentals-filings-schema.md` (+ 1 amendment)
- `ADP-004-macro-regime-redesign.md` (+ 1 cross-ADP amendment, shared with 005)
- `ADP-005-champion-challenger-governance.md` (+ 2 amendments, incl. numeric regime-stability floor)
- `ADP-006-pilot-universe-and-data-rights.md` (+ 2 amendments, incl. numeric peer-floor)

**Per `WORKFLOWS.md` §12, ADP lifecycle is `OPEN → APPROVED → IMPLEMENTED → ARCHIVED_AS_ADR`.** These six are now at `APPROVED`. They move to `IMPLEMENTED` as Beer builds against them, and to `ARCHIVED_AS_ADR` once implementation is verified complete.

**Beer: this is your green light.** All Protected Section changes described in these six ADPs (plus the companion `ARCHITECTURE_v2_PROPOSED.md` draft) are now approved for implementation. Recommended sequencing unchanged from the first entry above: ADP-002 and ADP-003 first (foundation, note ADP-003's loader implementation is still blocked on Phase 0 vendor trial closing — schema shape is not blocked), then ADP-004/ADP-001 in parallel, then ADP-005, with ADP-006's broader universe scope also blocked on Phase 0 closing (its two-tier design and peer-floor rule are approved now; the specific expanded name list is not).

One outstanding item not part of this ADP bundle, raised by Cola during the review but explicitly left unresolved within it (see `ADP-005` Open Question 3): whether model-governance promotion decisions should themselves be logged as immutable `reviews/`-style artifacts going forward. Recommend Sprite consider this as a `WORKFLOWS.md` §11 amendment separately, not blocking on it for Phase 1 kickoff.

---

**Author:** Cola
**Timestamp:** 2026-07-26 (update 4 — canonical doc reconciled, granular Phase 1 tasks below)
**Content:**

**`docs/ARCHITECTURE.md` §6 updated.** New append-only row, Finding #12, added — supersedes Finding #3 per `ADP-006`'s approval without editing the original entry. Also added short pointer notes in §1, §4.2, §4.3, §5, §7 (not edits to the Protected Section technical content itself — no formulas, schemas, or DDL were changed) flagging that the six approved ADPs supersede those sections' text in intent pending the actual v2 rewrite. That rewrite is **not** done yet — `docs/ARCHITECTURE.md` §1–§4 still show the pre-ADP v1 design as their literal text. Treat the ADPs and `ARCHITECTURE_v2_PROPOSED.md` as authoritative wherever they conflict with the untouched v1 text, exactly as the new note says.

**Granular Phase 1 task breakdown follows below.** Foundation-tier only (ADP-002, ADP-003 schema shape) — this is deliberately not a full Phase 1–5 breakdown in one shot; later phases get their own HANDOFF entries once foundation tasks are underway, so this list stays actionable rather than speculative.

### Phase 1 Tasks — Foundation (ADP-002 + ADP-003 schema)

Each task lists: what to build, which approved ADP section it implements, and its gate/exit criterion. Work sequentially; do not start a task whose dependency isn't checked off.

**1.1 — WSL Scaffolding & Virtual Environment Initialization**
- Standard project scaffold: `src/`, `tests/`, `data/`, venv, dependency pins (DuckDB, pandas, pytest at minimum for this phase).
- Exit criterion: `pytest` runs (even with zero tests) with no import errors.

**1.2 — `ingestion_events` table + write-path discipline**
- Implements: `ADP-002-bitemporal-versioning-calendar.md`, Amendment 1.
- Build the `ingestion_events` table exactly as specified (append-only, `event_type` CHECK constraint, `payload_snapshot` JSON, `source_response_metadata` JSON).
- Add the CI guard: a script/check that fails the build if `UPDATE`/`DELETE` statements targeting `ingestion_events` appear anywhere in `src/`.
- Exit criterion: table created via migration script; CI guard test written and passing (i.e., it correctly fails on a deliberately-introduced violation, then passes once removed — write both cases as tests).

**1.3 — Raw price table `raw_sgx_ohlcv`, versioned**
- Implements: `ADP-002`, `ARCHITECTURE_v2_PROPOSED.md` §3.1.
- Surrogate-key schema (`record_id`, `source_id`, `source_version`, `content_hash`, `available_at`, `superseded_by`) — no natural-key `PRIMARY KEY (symbol, trade_date)`.
- Adapter interface stub only at this stage (no live vendor call yet — Phase 0 not closed) — write against a fixture/mock payload so the schema and versioning logic can be tested independently of vendor selection.
- Exit criterion: unit test proves that ingesting a "corrected" version of an existing `(symbol, trade_date)` creates a new row with `superseded_by` populated on the prior row, not an overwrite.

**1.4 — Corporate actions table, versioned**
- Implements: `ADP-002`, `ARCHITECTURE_v2_PROPOSED.md` §3.2.
- Same versioning pattern as 1.3.
- Exit criterion: same overwrite-vs-version test pattern as 1.3, applied to a dividend correction scenario.

**1.5 — Corporate calendar table with tiered availability**
- Implements: `ADP-002`, Amendment 2; `ARCHITECTURE_v2_PROPOSED.md` §3.3.
- `event_date_status` (`ESTIMATED`/`CONFIRMED`/`REVISED`), `announced_at`, tiered by event type per the amendment.
- Exit criterion: test proves `days_to_earnings`-equivalent precise encoding is rejected/blocked for `ESTIMATED` rows at the data-access layer (not just documented) — i.e., a query function or view that returns precise day-counts should refuse or return `NULL` for `ESTIMATED`-only rows, only succeeding once a `CONFIRMED` row exists.

**1.6 — PIT resolution logic in `pit_store.py`**
- Implements: `ADP-002` §2.1–§2.2 (bitemporal filtration extended with `available_at`).
- "Latest non-superseded version as of `t`" query logic, filtering strictly on `available_at ≤ t`, not `ingested_at`.
- Exit criterion: PIT-replay test — ingest a sequence of versioned observations with different `available_at` timestamps, then confirm a query as-of an earlier `t` correctly excludes later corrections. **This is the actual gate test for the "PIT/data foundation" row in ADP-005's gate table** — write it now, since it's foundational, not deferred to Phase 3/4.

**1.7 — `raw_sgx_fundamentals` schema (shape only, no loader yet)**
- Implements: `ADP-003`, Amendment 1; `ARCHITECTURE_v2_PROPOSED.md` §3.4.
- Full schema including `data_authority`, `extraction_method`, `extraction_doc_ref`, `reviewer_id`, `review_timestamp`, `review_status`.
- **No vendor loader implementation in this task** — blocked on Phase 0. This task is schema-only, tested against fixture data.
- Exit criterion: schema created; unit test proves a row with `data_authority = 'EXTRACTED_LLM'` and no `reviewer_id` cannot have any feature referencing it reach `validation_status = 'PROMOTED'` in `feature_definitions` (test the constraint/join-check logic directly, even with `feature_definitions` mostly empty at this stage).

**1.8 — `feature_definitions` table + lens `CHECK` constraint**
- Implements: `ADP-001`; `ARCHITECTURE_v2_PROPOSED.md` §3.8.
- Full schema with `primary_lens`, `lens_role`, `horizon_weight_prior`, `validation_status` CHECK constraints.
- Exit criterion: test proves an attempt to register a feature with an invalid lens value, or with no lens at all, is rejected at the database level, not just caught in application code.

**1.9 — Phase 1 gatekeeper run**
- Run full `pytest` suite for tasks 1.1–1.8 together.
- Confirm no `UPDATE`/`DELETE` violations anywhere in the codebase against `ingestion_events` or any versioned raw table's superseded rows.
- **This task itself is a `WORKFLOWS.md` §6 material-risk category** (PIT/data contracts) — log the outcome as a review artifact per §11 once complete, even though the ADP itself already went through Matcha review; the *implementation* verification is a separate check from the *design* review.
- Exit criterion: all tests green; gatekeeper log entry appended to this file (new HANDOFF.md entry, not edited into this one).

### What's Deliberately Not in This Phase 1 Batch

- No vendor adapter implementation (SGX Data Direct / EODHD / FMP) — blocked on Phase 0, tracked separately.
- No `ADP-004` (macro regime) or `ADP-001`'s model-side gating layer — those depend on this foundation existing first, and are their own HANDOFF entry once 1.1–1.9 are green.
- No `ADP-005` baseline models — depends on both the foundation (this batch) and the feature registry (`ADP-001`, next batch).
- No `ADP-006` broader-universe loading — blocked on Phase 0 closing, same as `ADP-003`'s loader.

**Next action:** Beer begins with Task 1.1. Cola available for clarification on any schema/amendment detail; not expected to check in until Task 1.9's gatekeeper run completes or a Protected Section question arises mid-implementation.