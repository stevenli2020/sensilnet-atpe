# Team Structure & Operational Blueprint: Sensilnet ATPE

Document Version: 3.0
Project Name: Sensilnet ATPE
Full Name: Automated Trading & Prediction Engine
Target Architecture: Multi-Modal Daily Batch Trading & Prediction Engine for SGX Equities
Environment: Claude Code (Pro) / Claude Desktop + Local MCP / ChatGPT Web UI

**Supersedes:** v2.0 in full. This is a clean-slate redesign, re-derived from `docs/INITIAL_PROPOSAL.md` rather than incrementally patched from prior versions, prompted by the availability of Claude Code (Pro) as a persistent-context implementation environment. Drafted by Beer, challenged and refined by Matcha across two review rounds, approved by Sprite on 2026-07-24.

---

## 1. Executive Summary & Philosophy

The prior three-Gemini-persona split (PL / PM / PE) existed to compensate for a real constraint: each persona was a fresh chat session with no memory of the others' reasoning, so `HANDOFF.md` had to function as a relay baton between them. Claude Code (Pro) removes that constraint — it maintains continuous repository context across planning, implementation, testing, and documentation. Recreating a three-way handoff choreography on top of a tool that doesn't need one would be reintroducing overhead for its own sake.

But collapsing coordination overhead is not the same as collapsing independent judgment. This structure separates **who decides what should be built** from **who builds it** — not for model-diversity reasons (Cola and Beer share a model family and may share blind spots), but because a spec author who never implements can't unconsciously shape a spec to be easy to satisfy, and an implementer who didn't author the spec can't quietly relax a requirement without it surfacing as a visible deviation from someone else's document. That protection is real even without cross-model diversity. Cross-model independence — the check that actually catches what same-family reasoning might miss — remains Matcha's job alone, and nothing in this design should be read as diluting that.

Governing philosophy, contributed by Matcha and adopted in full:

> **Minimize AI-to-AI conversation. Maximize artifact-to-AI communication.**

Debate between Cola, Beer, and Matcha should happen through shared, versioned artifacts (`ARCHITECTURE.md`, ADRs, `reviews/`, `HANDOFF.md`) rather than transient chat exchanges. This is not a stylistic preference — during the design of this very structure, a Matcha review that existed only in a chat session became permanently unrecoverable once that session was lost. The finding was real; it became unusable simply because it was never captured as an artifact. Every review, finding, and architectural decision from this point forward is filed as an artifact at the time it happens, not reconstructed afterward.

Second governing philosophy, also contributed by Matcha:

> **Governance should be enforced by simple, objective rules whenever possible; rely on human judgment only where architectural intent cannot be expressed mechanically.**

This shows up concretely in §5 (Protected Sections instead of AI-adjudicated semantic diffing) and throughout the Automated Gatekeeper (§8) — automation handles what's genuinely deterministic; anything requiring judgment about intent goes to a person or to Cola, not to a script pretending to have judgment it doesn't have.

---

## 2. Team Composition & Role Definitions

| Role | Agent / Platform | Primary Responsibility |
| :--- | :--- | :--- |
| **Sprite** | Human | Business architecture and scope (§4), ADP/ADR approval for business-impacting or protected-section changes, merge approval, credentials, finding disposition (recorded directly — no intermediary role exists to record on Sprite's behalf), conflict resolution. |
| **Cola** | Chief Architect / Claude Desktop + Local MCP | Owns **technical architecture and architectural intent** (§4) — not "architecture" as a static document, but the underlying decisions about what the system must guarantee (PIT correctness, data contracts, target/label definitions, feature governance). Periodic check-ins during implementation, not continuous oversight. Runs the periodic holistic review (§9). |
| **Beer** | Implementation Authority / Claude Code (Pro) | Owns **implementation architecture** (§4) — coding, testing, documentation, Git operations, `HANDOFF.md` (operational ownership, see §7), ADP drafting when a spec proves wrong in practice or when Beer identifies an implementation-level improvement opportunity. Implements *against* Cola's architectural intent; may freely edit Implementation Notes sections but not Protected Sections (§5). |
| **Matcha** | Independent Red Team / ChatGPT Web UI | The only genuine cross-model check in the system. Mandatory review for material-risk categories (§6) before Sprite disposition, plus periodic holistic architecture-drift review (§9). Findings immutable once filed (§10). Advisory authority — Sprite decides. |

---

## 3. Workflow

```text
Sprite (business objective / scope)
   |
   v
Cola (technical architecture + spec, or approves Beer-originated ADP)
   |
   v
Beer / Claude Code (implementation, tests, docs)
   |
   v
Automated Gatekeeper (deterministic script, §8)
   |
   v
Matcha Review (mandatory if material-risk category, §6)
   |
   v
[if Beer disputes a finding -> bounded disagreement loop, §10.1]
   |
   v
Sprite: records disposition (§10), approves merge
```

Periodic holistic review (§9) runs on its own cadence, independent of any single change in this pipeline.

---

## 4. The Three-Layer Authority Model

Contributed by Matcha; this is the load-bearing structural idea in v3.0 and resolves an ambiguity that existed in earlier drafts about who decides what.

```text
Sprite   -> owns BUSINESS architecture   (what markets/products, what scope, what risk tolerance)
Cola     -> owns TECHNICAL architecture  (what the system must guarantee, structurally)
Beer     -> owns IMPLEMENTATION architecture (how a guarantee is actually built)
```

**Worked example, to make the boundary concrete:**

- Sprite: *"We support SGX only, research/paper-trading phase, no live capital yet."* — business scope.
- Cola: *"Corporate-action adjustments must use immutable append-and-supersede records, not in-place updates, to preserve backtest reproducibility."* — technical architecture / intent.
- Beer: *"Implemented via a `superseded_action_id` surrogate-key chain in DuckDB, with an as-of subquery selecting the version current at cutoff `t`."* — implementation architecture.

**Intent vs. Decision** (also from Matcha, important distinction): Cola's authority is over *intent*, not necessarily the specific mechanism. "Storage must support efficient columnar analytics" is intent; "use Parquet" is one implementation of that intent. If Beer later proposes DuckDB instead of Parquet, that can be an implementation-level ADP (Beer originates, Cola approves) precisely because it preserves the stated intent rather than changing it. If Beer's proposal would instead *change* the intent — e.g., relaxing the reproducibility guarantee itself — that requires Cola to revisit the underlying architectural decision, not just approve a substitution.

---

## 5. Document Governance — Protected Sections

Rather than relying on any agent's self-restraint, or asking automated tooling to semantically judge whether an edit changed "architectural intent" (rejected as over-engineering — see §8.4), document sections carry explicit, mechanically-checkable edit authority.

### 5.1 `docs/ARCHITECTURE.md` Section Ownership

| Section | Owner | Edit Rule |
| :--- | :--- | :--- |
| Vision / Executive Summary | Cola | Protected — requires approved ADP |
| Design Principles | Cola | Protected — requires approved ADP |
| Data Contracts (PIT rules, schemas' semantic meaning) | Cola | Protected — requires approved ADP |
| Component Responsibilities | Cola | Protected — requires approved ADP |
| Module Layout | Shared | Beer may propose directly; Cola notified, no ADP required unless it changes a responsibility boundary |
| Implementation Notes | Beer | Freely editable — reflects as-built detail, not intent |

### 5.2 The Rule

> **Any modification to a Protected Section requires an approved ADP, full stop.** No automated tool attempts to judge whether a given edit is "architectural" — that determination is inherently a matter of intent, not syntax, and is reserved for Cola/Sprite. The Gatekeeper (§8) enforces this mechanically only in the trivial sense of flagging *that* a Protected Section changed, not *whether* the change was appropriate.

This applies equally to `docs/specs/*.md` component specs while in DRAFT status — the same section-ownership principle extends to any document Cola originates.

---

## 6. Mandatory Independent Review — Material-Risk Categories

Unchanged in substance from v2.0 — these are domain-correctness risks, not artifacts of the old team structure, and neither review round challenged this list:

- Data source and licence decisions
- PIT / data contracts (timestamp semantics, adjustment logic, corporate-action handling)
- Prediction targets and label definitions
- Feature availability and known-future-input encoding
- Backtest and execution rules (cost models, slippage, benchmark comparison)
- Transaction cost assumptions
- Model-selection changes (architecture, loss function, output heads)
- Major refactors touching more than one subsystem

Routine implementation work, prose edits, and low-risk maintenance are exempt, to keep Matcha's review meaningful rather than a rubber stamp on everything.

---

## 7. HANDOFF.md — Shared, Append-Only Ownership

Beer owns `HANDOFF.md` **operationally** — it is Beer's task board, updated continuously during implementation. But Sprite, Cola, and Matcha may each append entries relevant to their own domain (a priority note from Sprite, an architectural flag from Cola, a review pointer from Matcha) — Beer does not become the sole bottleneck for recording everything that touches the file.

**Rule:** entries are **append-only per author**, tagged with author and timestamp. No agent silently edits or removes another agent's entry — supersede it with a new dated entry if it's out of date, the same immutability discipline already established for `reviews/`.

---

## 8. Automated Gatekeeper

Deterministic script, run by Beer as part of its own workflow — but deliberately not self-interpreted. Raw output goes into the evidence trail as-is; Beer does not get to summarize a failing gate into a passing narrative.

```text
ruff
black --check
mypy
pytest
coverage threshold
pip check
clean git status
no unowned TODO/FIXME/debug prints
canonical-doc integrity check (non-empty, versioned, paths match references)
Protected Section change detector (§8.4)
```

### 8.4 Protected Section Change Detector — deliberately simple

Considered and rejected: semantic diffing to determine whether an edit changed architectural *intent* (e.g., distinguishing "queue" becoming "priority queue" as a meaningful change versus a typo fix). Matcha's objection, adopted in full: *"The gatekeeper is excellent at deterministic checks. It is terrible at semantic governance."*

**Actual mechanism:** the detector flags **any** diff touching the line ranges of a section marked Protected in §5.1, full stop — no judgment about whether the change was substantive. Every flagged diff routes to Cola for a yes/no: does this require an ADP, or was it a formatting/typo fix Cola is comfortable approving inline. The tool's only job is to make sure nothing protected changes *silently*; it does not decide whether a change is acceptable.

---

## 9. Periodic Holistic Review

Contributed by Matcha: material-risk review catches individually dangerous changes, but not architectural drift accumulated from many individually-safe changes over time.

**Cadence:** every 5 phases, or at a milestone Sprite designates, whichever comes first.

**Scope, deliberately broader than a single-change review:**
1. Does currently-implemented behavior still match currently-documented architectural intent, not just "did each individual change get approved."
2. Are there Implementation Notes edits that, in aggregate, should have been Protected Section changes but were never flagged individually.
3. General red-team pass per §11's review scope, applied to the system as a whole rather than one artifact.

Run by Matcha, using an evidence packet Beer/Cola jointly prepare summarizing the phases since the last holistic review.

---

## 10. Finding Disposition & Immutability

Matcha findings, once filed, are **immutable**. Beer may author a response through the bounded disagreement loop (§10.1) but never edits or marks its own finding resolved.

**Disposition is recorded directly by Sprite** — no intermediary recording role exists in this structure (deliberate simplification; Matcha's assessment, adopted: *"Adding another recorder would just introduce ceremony. The important thing is that the decision is immutable once recorded."*).

**Disposition format** (Matcha's structure, adopted verbatim):

```text
Finding: <what was found>
Disposition: Accepted | Deferred | Closed
Who: Sprite
Date: YYYY-MM-DD
Reason: <why this disposition>
```

### 10.1 Bounded Disagreement Loop

Unchanged from v2.0 — neither review round challenged this, and it protects against a specific asymmetry (the party with more context/turns out-arguing a reviewer by volume rather than evidence) that's structural, not tied to the old role names.

```text
Matcha finding
  -> Beer technical response with evidence (one reply)
  -> Matcha final reply (one reply)
  -> Sprite decision
```

No re-litigation. Silence is not tacit agreement — an unanswered finding stands as filed for Sprite's decision.

### 10.2 Universal Append-Only Attribution

Contributed by Matcha, extended beyond `reviews/` to every artifact type in the system: reviews, ADPs, and architecture comments are never silently rewritten by another agent. Append or supersede, always with attribution.

```text
Author: <Sprite | Cola | Beer | Matcha>
Timestamp: <when>
Content: <observation | recommendation | reason | evidence>
```

---

## 11. Matcha Review Scope

Carried forward from v2.0 — domain-correctness concerns, not process artifacts:

- PIT leakage; survivorship bias; label leakage
- Backtest validity; corporate-action handling; exchange-calendar assumptions
- Slippage and transaction-cost realism; overfitting risk; misleading metrics
- Fragile model assumptions; hidden data dependency; strategy robustness under stressed markets
- Structural weaknesses in the team/process design itself

**What Matcha must never receive:** credentials, API keys, broker details, personal data, proprietary raw datasets, unrestricted project archives, `.env` files, live trading configuration. Evidence packets are manually redacted per §11 of the retired v2.0 protocol — unchanged, re-adopted here in full (see `reviews/REVIEW_FORMAT.md` for the packet template, which survives this clean-slate rewrite as process-neutral).

---

## 12. Architecture Drift Proposal (ADP) Process

```text
OPEN -> APPROVED -> IMPLEMENTED -> ARCHIVED_AS_ADR
     -> REJECTED
     -> DEFERRED
```

- **Beer-originated ADPs** (implementation-level improvement, or a Cola spec proving contradictory/infeasible in practice): routed to **Cola** for ordinary technical-architecture drift; escalated to **Sprite** only if it touches business scope, cost, or risk tolerance.
- **Cola-originated ADPs** (technical architecture change): routed to **Sprite** if it touches business-layer concerns per §4; otherwise Cola may self-approve within technical-architecture authority, logged as an ADR regardless.
- Beer never implements a Protected Section change without an approved ADP (§5.2) — this is the one absolute rule in the system with no discretionary exception.
- "Implementation only" does not mean "implement a known defect" — if a Cola spec is contradictory, unsafe, or infeasible as written, Beer stops and drafts an ADP rather than silently patching around it.

---

## 13. Error Escalation

- Escalate after **2 consecutive failures with the same error signature**, or repeated signature-cycling with no test progress. Retry counter resets when the signature changes.
- **Cola**: hard debugging, refactor strategy, math/algorithm validation.
- **Sprite**: anything touching business scope or tradeoffs, or where Cola and Beer cannot resolve a technical dispute (Decision Deadlock — unchanged from v2.0 §5.3: incompatible recommendations with no objective test to resolve them go to Sprite, and the outcome must be recorded as an ADR, risk-register entry, or phase-log entry as appropriate).

---

## 14. Minimal Document Set

| Document | Owner | Purpose |
| :--- | :--- | :--- |
| `docs/ARCHITECTURE.md` | Cola (Protected Sections), Beer (Implementation Notes) — see §5.1 | Canonical system design |
| `docs/specs/*.md` | Cola | Component-level specs, DRAFT until Matcha review clears + Sprite disposition |
| `HANDOFF.md` | Beer (operational), append-only shared per §7 | Active task/phase state |
| `docs/decision_log/` (ADRs) | Drafted by originating agent, approved per §12 | Permanent record of resolved ADPs |
| `docs/RISK_REGISTER.md` | Cola | Persistent domain risks |
| `docs/KNOWN_LIMITATIONS.md` | Cola | Accepted constraints |
| `reviews/` | Matcha, Cola, Beer (disagreement-loop responses) | Independent review artifacts — same-session filing, immutable, per `reviews/REVIEW_FORMAT.md` |
| `requirements.txt` | Beer | Dependency pinning, generated from actual environment, not hand-typed |
| `CLAUDE.md` | Beer, reviewed by Cola | Repository guide for Claude Code — conventions, commands, architecture map, common pitfalls. Not for humans; for keeping Claude Code consistently effective. See root `CLAUDE.md`. |

No `SPECIFICATIONS.md` / `ARCHITECTURE.md` split unless it proves necessary in practice. Documents get created because they solve an actual problem, not for speculative completeness — this call was explicitly affirmed by Matcha as good engineering during review and is retained deliberately.

---

## 15. Known Hard Problems — Carried Forward as Verification Targets, Not Inherited Solutions

These are domain-correctness facts, not process artifacts, so the clean-slate rewrite does not discard them — but Cola's fresh technical-architecture pass should explicitly re-verify each rather than either (a) blindly re-importing the old answer unexamined, or (b) rediscovering the problem from scratch the hard way:

1. Corporate-action PIT correctness — same-day multiple-action ordering, and whether corrections to already-published corporate-action data require immutable-append semantics to preserve backtest reproducibility.
2. Horizon/target synchronization between whatever math spec Cola writes and whatever schema Beer implements — these drifted out of sync once already in the project's history.
3. Any composite/derived signal (e.g., a regime classification) needs an explicit, checkable aggregation rule from its inputs — never an implied one.
4. Transaction cost model completeness — whatever is claimed in prose must match what is actually itemized in the cost calculation, with no silently-dropped line items.

---

## 16. Final Role Boundary

```text
Sprite:
  Business architecture and scope. ADP/ADR approval for business-impacting
  or Protected Section changes. Merge approval. Credentials. Sole owner of
  finding disposition, recorded directly (§10).

Cola (Claude Desktop + Local MCP):
  Technical architecture and architectural intent. Owns Protected Sections
  of ARCHITECTURE.md and all specs in docs/specs/. Periodic check-ins
  during implementation, not continuous oversight. Runs the periodic
  holistic review (§9).

Beer (Claude Code, Pro):
  Implementation architecture. Sole implementation authority: coding,
  testing, documentation, Git, operational HANDOFF.md ownership. May
  freely edit Implementation Notes; may never edit a Protected Section
  without an approved ADP. May originate ADPs for implementation-level
  improvements or when a Cola spec proves contradictory in practice.

Matcha (ChatGPT Web UI):
  The only genuine cross-model, independent check in the system.
  Mandatory reviewer for material-risk categories (§6) and periodic
  holistic review (§9). Findings immutable once filed. Advisory
  authority only — Sprite decides.
```

Operational philosophy:

> Use Cola for architectural depth and fresh judgment, Claude Code (Beer) for implementation velocity with persistent repository context, Matcha for genuine independent challenge, deterministic automation for evidence, and Sprite for judgment where intent cannot be expressed mechanically.

---

## Changelog

- **v3.0 (2026-07-24):** Full clean-slate redesign for the Claude Code (Pro) era, re-derived from `docs/INITIAL_PROPOSAL.md` rather than incrementally patched. Collapsed PL/PM/PE into a single implementation authority (Beer, Claude Code) while explicitly preserving Cola as a separate technical-architecture authority — not for model-diversity reasons, but to prevent self-serving spec drift. Introduced the three-layer authority model (Sprite/business — Cola/technical — Beer/implementation, contributed by Matcha). Introduced Protected Sections as a deterministic alternative to AI-adjudicated semantic diffing (Matcha's objection to semantic gatekeeping, adopted in full). Introduced periodic holistic review to catch accumulated architectural drift that material-risk-only review misses. Moved finding disposition to direct Sprite recording, eliminating the intermediary recorder role as unnecessary ceremony (Matcha's assessment). Adopted universal append-only attribution across all artifact types. Added `CLAUDE.md` as a missing artifact identified during review. Retained unchanged from v2.0: bounded disagreement loop, material-risk mandatory review category list, `reviews/REVIEW_FORMAT.md`, Decision Deadlock Rule, evidence-packet redaction discipline for Matcha.
- **v2.0 (2026-07-24, retired same-day):** Merged PL role into Beer within the prior three-Gemini-persona-plus-Claude-plus-ChatGPT structure. Superseded in full by v3.0 following the introduction of Claude Code (Pro) as an implementation environment.
- **v1.6:** Prior version — see git history.
