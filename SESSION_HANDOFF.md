# SYSTEM CONTEXT — Sensilnet ATPE (Automated Trading & Prediction Engine)
*Condensed handoff for fresh session continuity. Verified against actual repo state on 2026-07-24 — not generated purely from chat memory. Paste relevant sections into a new session, or point a new session at this file directly.*

---

## 1. CORE OBJECTIVE

Building **Sensilnet ATPE**: a daily-batch, Point-In-Time (PIT) compliant multi-task Temporal Fusion Transformer system generating probabilistic return + directional forecasts for 5 SGX blue-chip equities. Research/paper-trading phase only — no live capital, no broker credentials exist.

Most of this session was **not** trading-system implementation — it was **iteratively designing the AI multi-agent team structure and governance process** used to build the system safely (self-review risk, PIT-leakage discipline, review-artifact immutability). That governance design is the primary deliverable so far and is fully committed to the repo as `WORKFLOWS.md` v3.0.

---

## 2. KEY DECISIONS & TECHNICAL CONSTRAINTS

### Team Structure — **`WORKFLOWS.md` v3.0** (current, canonical; supersedes all prior versions)
Clean-slate redesign, re-derived from `docs/INITIAL_PROPOSAL.md` only, prompted by Claude Code (Pro) removing the fresh-session-persona constraint that justified the old PL/PM/PE split.

| Role | Agent/Platform | Authority |
|---|---|---|
| **Sprite** | Human (user) | Business architecture/scope, ADP/ADR approval for protected/business changes, merge approval, credentials, **sole owner of finding disposition** (records directly, no intermediary) |
| **Cola** | Claude Desktop + Local MCP | **Chief Architect** — owns technical architecture/intent, Protected Sections of `ARCHITECTURE.md`, `docs/specs/*`. Periodic check-ins, not continuous. Runs periodic holistic review. |
| **Beer** (Claude Code) | Claude Code (Pro) | **Sole implementation authority** — coding, tests, docs, Git, operational `HANDOFF.md`. Freely edits Implementation Notes; **never** edits Protected Sections without approved ADP. May originate ADPs. |
| **Matcha** | ChatGPT Web UI | **Only genuine cross-model independent check.** Mandatory review for material-risk categories (below). Findings immutable once filed. Advisory only — Sprite decides. |

**Three-Layer Authority Model** (Matcha's contribution, core to v3.0):
`Sprite (business) → Cola (technical/intent) → Beer (implementation)`

**Protected Sections rule** (replaces rejected idea of AI semantic-diff judging "architectural" changes):
Any edit to Vision/Design Principles/Data Contracts/Component Responsibilities in `ARCHITECTURE.md` requires an approved ADP — full stop, no automated judgment call on whether an edit "counts." Gatekeeper only flags *that* a protected section changed, never *whether* it should have.

`docs/ARCHITECTURE.md` section ownership:
- §1 Vision, §2 Math/PIT, §3 Schemas, §4 Subsystems → **Protected (Cola)**
- §5 Roadmap → **Shared** (Beer may propose directly)
- §6 Disposition Matrix → **Append-only historical record**
- §7 Handoff Contract → **Implementation Notes (Beer edits freely)**

**Bounded Disagreement Loop** (unchanged since v2.0):
```
Matcha finding → Beer response (ONE reply, with evidence) → Matcha final reply (ONE) → Sprite decision
```
No re-litigation. Silence ≠ agreement — finding stands as filed.

**Mandatory Matcha review categories** (material-risk, unchanged since v2.0):
Data source/licence decisions; PIT/data contracts; targets & labels; feature availability/known-future-inputs; backtest & execution rules; transaction costs; model-selection changes; major multi-subsystem refactors. Routine/low-risk work exempt.

**Periodic Holistic Review**: every 5 phases (or Sprite-designated milestone) — Matcha checks accumulated architectural drift, not just single-change risk.

**Governing philosophies (both from Matcha, adopted verbatim):**
> "Minimize AI-to-AI conversation. Maximize artifact-to-AI communication."
> "Governance should be enforced by simple, objective rules whenever possible; rely on human judgment only where architectural intent cannot be expressed mechanically."

**Review filing discipline** (`reviews/REVIEW_FORMAT.md`):
- Filename: `reviews/YYYY-MM-DD_<artifact-name>_<reviewer>.md`
- **Rule 6 (critical):** file within the SAME working session as the review, not retroactively — added after a real Matcha review of `pit_adjustment_engine_v1.md` became permanently unrecoverable when the source chat was lost.
- Disposition table in every review is **never filled by Beer** — Sprite decides and records directly (no PM role exists in v3.0).
- Universal append-only attribution: `Author / Timestamp / Content` — never silently overwrite another agent's entry.

### Technical/Domain Facts (carried forward as verification targets, not blindly trusted)
- Pilot universe: **DBS (D05.SI), OCBC (O39.SI), UOB (U11.SI), Singtel (Z74.SI), SIA (C6L.SI)**
- Horizons: $\mathcal{H} = \{1,3,5,10,20,60\}$ trading days
- PIT adjustment: raw prices stored unadjusted; adjusted price computed dynamically via $P^{adj}_{i,s|t} = P^{raw}_{i,s} \times \prod f_{i,\tau|t}$; split factor $=1/S$; dividend factor $=1-D/P^{raw}_{\tau-1}$
- Corporate-action corrections must use **immutable append + supersede**, never in-place UPDATE (preserves backtest reproducibility)
- Same-day split+dividend ordering, and the 15% gap-detection threshold in `pit_adjustment_engine_v1.md` §3.2/§3.4 are **UNRESOLVED** — explicitly flagged, not settled (see Next Steps)
- `market_regime_code` derivation (Bull/Sideways/Bear from ATR percentile + ADX + 3d sentiment avg) — verified logically disjoint, no overlap bug
- Transaction costs: Brokerage 0.08% (min SGD 10), SGX Clearing 0.0075%, Access Fee 0.005%, slippage $=\alpha(V/ADV_{20})^\beta \times ATR_{14}$

### Environment/Security (real findings from this session, not hypothetical)
- **Fixed:** `ClaudeMCP_PAT.txt` (credential file) relocated out of `/mnt/d/Projects/` after being found reachable via `cd ..` traversal from the MCP workspace.
- **Fixed:** `.env` file only contains public MAS API key — explicitly acknowledged as low-risk, no action needed.
- **Verified safe:** `sudo -n true` fails — sudo requires a password neither Cola nor Beer can supply, so no root-escalation path currently exists.
- **Still open, low priority given above:** full container/bubblewrap sandboxing of the MCP server (scoping it to workspace root) not yet done — must be completed before any broker/live-trading credentials ever enter this environment.

---

## 3. CURRENT PROGRESS (verified against repo at `/mnt/d/Projects/sensilnet-atpe`, 2026-07-24)

Commit history (main branch, **4 commits ahead of origin, not yet pushed**):
```
ded9882 Rename TEAM_STRUCTURE.md to WORKFLOWS.md
499c3cc Team Structure v3.0: clean-slate redesign for Claude Code era
d288664 Team Structure v2.0: merge PL into Beer, Matcha as primary checker
1eb0275 Sprite commits
9d0fb55 feat: initialize Sensilnet ATPE workspace and governance structures
```

**Populated/current (committed):**
- `WORKFLOWS.md` (v3.0) — canonical governance doc
- `docs/ARCHITECTURE.md` — full technical blueprint (PIT math, DuckDB schemas, subsystems, 11-row disposition matrix) + Document Governance header mapping sections to Protected/Shared/Implementation-Notes
- `CLAUDE.md` — repo guide for Claude Code sessions (gatekeeper commands, Protected Section awareness, ADP triggers)
- `docs/specs/pit_adjustment_engine_v1.md` (v1.1) — DRAFT, PIT corporate-action contract, 4 open questions with routing plans (see Next Steps)
- `reviews/REVIEW_FORMAT.md` — governs all future review filings

**Still empty / not started:**
- `HANDOFF.md`, `docs/RISK_REGISTER.md`, `docs/KNOWN_LIMITATIONS.md`, `docs/decision_log/`, `docs/phase_logs/`
- No `SPECIFICATIONS.md` split created (deliberate — "don't create unless proven necessary," affirmed by Matcha)
- `requirements.txt` does not exist yet
- No actual Phase 1 implementation code written yet (`src/`, `tests/` are empty scaffolding)

**⚠️ PENDING EXTERNAL CHANGE — needs Sprite's decision, not made by Beer:**
As of this file being written, `git status` shows six files **deleted from disk but not committed**:
```
deleted: .gemini/commands/pe.toml
deleted: .gemini/commands/pl.toml
deleted: .gemini/commands/pm.toml
deleted: .gemini/prompts/pe_system_prompt.txt
deleted: .gemini/prompts/pl_system_prompt.txt
deleted: .gemini/prompts/pm_system_prompt.txt
```
These are the retired PL/PM/PE persona configs (obsolete under v3.0's role structure). Someone deleted them outside this conversation — Beer did not do this. Also, `scripts/generate_context.py` has already been corrected to reference `WORKFLOWS.md` (previously flagged as stale in an earlier summary — that flag is now outdated, the fix already happened externally). **Action needed:** Sprite should either `git rm` to formally stage the persona-file deletions (if intentional) or `git checkout` to restore them (if accidental), then commit. A new session should re-run `git status` to confirm current state before proceeding.

**Untracked, unowned by Beer, not touched:**
- `.gemini/settings.json`
- `scripts/compress_context.py`

---

## 4. NEXT STEPS & ACTIVE TASKS — pick up here

1. **Resolve the pending uncommitted deletions above** — first thing a new session should address, since it's an open working-tree state, not a clean baseline.
2. **Route Q1 in `pit_adjustment_engine_v1.md` §3.2**: same-day split+dividend combined adjustment-factor formula needs independent blind derivation. Assign to Cola — must receive ONLY `ARCHITECTURE.md` §2.1's raw per-event formulas + the same-day scenario description, NOT Beer's proposed formula, to keep the derivation genuinely blind.
3. **Route Q3 in `pit_adjustment_engine_v1.md` §3.4**: 15% gap-detection threshold needs empirical calibration against real historical corporate-action data for the 5 pilot names. Previously assigned to "PE" (role no longer exists under v3.0) — **needs explicit reassignment**, likely to Beer (implementation-level empirical work).
4. **Q2 and Q4** in the same spec (Option B immutability scope-check; PK-change reopening Finding #6) — not yet routed to anyone. Needs assignment.
5. Once Q1–Q4 resolve: file results as real review artifacts in `reviews/` per `REVIEW_FORMAT.md` (same-session filing, not retroactive), update `pit_adjustment_engine_v1.md` §8 Resolution Routing Log, then promote spec content into `ARCHITECTURE.md` §4.1 (Protected Section — requires ADP).
6. Generate `requirements.txt` from the actual `.venv` (exists at project root) rather than hand-typing.
7. Populate `HANDOFF.md` for actual Phase 1 kickoff (branch `feature/phase-1-infrastructure`, Task 1.1 = WSL scaffolding).
8. Decide whether to push the 4 unpushed local commits to `origin/main`.

---

## 5. IMPORTANT REFERENCES

- **Repo path:** `/mnt/d/Projects/sensilnet-atpe` (WSL), accessed via MCP connector `sensilnet-atpe-cola`
- **Governance doc:** `WORKFLOWS.md` (root) — read this first in any new session
- **Repo guide for Claude Code:** `CLAUDE.md` (root)
- **Architecture:** `docs/ARCHITECTURE.md` — has Document Governance header, Protected Section table
- **Open spec:** `docs/specs/pit_adjustment_engine_v1.md` v1.1 — DRAFT, 4 unresolved questions, §8 has routing log table
- **Review template:** `reviews/REVIEW_FORMAT.md`
- **Disposition format** (Matcha's structure):
  ```
  Finding: <what>
  Disposition: Accepted | Deferred | Closed
  Who: Sprite
  Date: YYYY-MM-DD
  Reason: <why>
  ```
- **Confidence-level format** required on all technical findings:
  ```
  Confidence: High | Medium | Low
  Evidence Basis: Verified | Inference | Hypothesis
  Reason:
  ```

---

*This file is a point-in-time snapshot (2026-07-24). Re-run `git log` / `git status` at the start of any new session to confirm nothing has drifted before acting on the "Current Progress" section above.*
