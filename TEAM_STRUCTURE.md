# Team Structure & Operational Blueprint: Sensilnet ATPE

Document Version: 2.0
Project Name: Sensilnet ATPE
Full Name: Automated Trading & Prediction Engine
Target Architecture: Multi-Modal Daily Batch Trading & Prediction Engine for SGX Equities
Environment: WSL Ubuntu Terminal / Python venv / Gemini CLI / Claude Desktop + MCP / ChatGPT Web UI

**Supersedes:** v1.6. v2.0 merges v1.6's operational hardening (deterministic gates, evidence-based Matcha review, reproducibility requirements) with the Team Structure v2 role redesign agreed between Sprite, Beer, and Matcha on 2026-07-24. Everything in v1.6 not explicitly changed below remains in force.

---

## 1. Executive Summary & Philosophy

Sensilnet ATPE operates on a flattened multi-agent architecture designed for a solo developer coordinating several AI assistants through explicit local artifacts rather than relying on chat memory.

The system uses **two Gemini operational roles** (PM, PE), **one Claude-based merged Project Leader / Chief Architect role** (Beer), **one Claude-based reserve technical specialist role** (Cola), and **one ChatGPT-based independent review role** (Matcha).

The previous three-Gemini-role design (separate PL, PM, PE, all sharing one underlying model) was consolidated on 2026-07-24: the PL role and the Chief Architect function were merged into a single Claude-based role (Beer), removing a translation layer between architecture decisions and their specification. This consolidation was accepted on the explicit condition that independent review authority does not consolidate alongside it — see §2 and §5.5.

All three Gemini/Claude implementation-and-architecture roles (PM, PE, Beer) may improve workflow discipline and depth, but **none of them are independent validation authorities on their own output**, and Beer and Cola in particular share the same underlying model family and may share the same blind spots. Independent checks must come from deterministic gates, evidence, genuine model diversity (Matcha), and final human judgment (Sprite).

All state and communications between agents are stored in version-controlled local artifacts such as `HANDOFF.md`, `docs/ARCHITECTURE.md`, `docs/SPECIFICATIONS.md`, `docs/decision_log/`, `docs/phase_logs/`, `docs/specs/`, and `reviews/`.

The guiding principle is:

> LLMs may plan, implement, review, and challenge, but deterministic evidence and Sprite control acceptance.

---

## 2. Team Composition & Role Definitions

| Role | Agent / Platform | Primary Responsibility | Work Environment |
| :--- | :--- | :--- | :--- |
| Sprite | Project Owner / Human | Final approvals, business objectives, API credentials, merge approval, live-trading readiness decisions, finding disposition, and conflict resolution. | WSL Terminal / Browser |
| Beer | Project Leader + Chief Architect / Claude Desktop + Local MCP | Owns architecture vision and roadmap, authors and maintains `docs/ARCHITECTURE.md` and `docs/specs/*`, defines phase milestones and module contracts, writes proposal responses in the disagreement loop. Writes zero production code. **Does not own finding disposition** (§5.4) and **is not the independent checker on its own output** — see §5.5. | Claude Desktop App with Local MCP |
| PM | Project Manager / Gemini Gem | Maintains `HANDOFF.md`, decomposes tasks, manages branches, executes deterministic phase gates, archives phase artifacts, converts approved ADPs into ADRs, **records finding disposition status** (never Beer), and verifies canonical-document integrity (non-empty, versioned, paths matching references — see §5.6). | Gemini CLI in WSL |
| PE | Primary Coding Engineer / Gemini Gem | Writes most production Python code, implements features, writes tests, runs local unit tests, escalates when failure rules trigger, and **may raise an ADP and block implementation** when a specification is contradictory, unsafe, or infeasible — "implementation only" does not mean "implement a known defect" (§5.7). | Gemini CLI in WSL |
| Cola | Secondary Engineer / Claude Desktop + Local MCP | Full-access **fresh-context specialist**, not an independent tiebreaker (§5.5.3): complex refactoring, difficult debugging, math validation, architecture stress testing, test-gap analysis, and rescue work when PE reaches escalation criteria. No longer a standing gate on every architecture document — invoked for specialist depth, or by Sprite for a second technical opinion. | Claude Desktop App with Local MCP |
| Matcha | Primary Independent Checker + Technology Advisor / ChatGPT Web UI | **Mandatory independent reviewer** for all material-risk changes (§5.6 risk-tier list) before Sprite disposition. Independent red-team auditor: backtesting logic stress tests, PIT leakage review, strategy risk analysis, edge-case detection, and challenge of weak assumptions. Findings are immutable once filed (§5.4). Advisory authority only — Sprite decides. Receives only manual redacted evidence packets. | ChatGPT Web UI / Isolated Manual Review |

---

## 3. Directory Layout & File Communications

```text
sensilnet-atpe/
|-- .gemini/
|   `-- system prompts and Gemini CLI configuration
|-- docs/
|   |-- ARCHITECTURE.md
|   |-- SPECIFICATIONS.md
|   |-- RISK_REGISTER.md
|   |-- KNOWN_LIMITATIONS.md
|   |-- specs/
|   |   `-- <component>_v<N>.md      (draft specs pending review, e.g. pit_adjustment_engine_v1.md)
|   |-- decision_log/
|   |   |-- ADR-001.md
|   |   `-- ADR-002.md
|   `-- phase_logs/
|       |-- phase_1_handoff.md
|       `-- phase_1_summary.md
|-- reviews/
|   |-- REVIEW_FORMAT.md             (governing template and rules — see §5.6.1)
|   `-- YYYY-MM-DD_<artifact>_<reviewer>.md   (flat, one file per review — supersedes prior inbox/active/completed/rejected subfolder scheme)
|-- scripts/
|   `-- phase_gatekeeper.sh
|-- logs/
|   `-- test_runner.log
|-- src/
|   |-- core/
|   |-- features/
|   |-- models/
|   `-- backtest/
|-- tests/
|-- HANDOFF.md
|-- PROJECT_CONTEXT.md
|-- TEAM_STRUCTURE.md
`-- mcp_server.py
```

**Note on `reviews/`:** v1.6 specified an `inbox/active/completed/rejected` subfolder scheme. As of 2026-07-24 this is superseded by the flat, date-prefixed convention documented in `reviews/REVIEW_FORMAT.md` — one file per review, filed at review time (not as a later cleanup task), named `YYYY-MM-DD_<artifact-name>_<reviewer>.md`. `reviews/REVIEW_FORMAT.md` is the authoritative source for the template and rules; this document defers to it rather than duplicating it.

### File Responsibilities

| File / Folder | Purpose |
| :--- | :--- |
| `HANDOFF.md` | Active operational task board only. Current phase, branch, task assignments, blockers, error fingerprints, next action. |
| `docs/ARCHITECTURE.md` | Master architecture, module boundaries, data flow, major system contracts. Authored by Beer. |
| `docs/specs/` | Draft component-level specifications pending independent review, before promotion into `ARCHITECTURE.md` or `SPECIFICATIONS.md`. Authored by Beer, status explicitly DRAFT until disposition. |
| `docs/SPECIFICATIONS.md` | Feature schemas, math definitions, data contracts, model assumptions once promoted out of draft. |
| `docs/decision_log/` | Permanent Architecture Decision Records. |
| `docs/RISK_REGISTER.md` | Persistent project risks, mitigations, owners, and review dates. |
| `docs/KNOWN_LIMITATIONS.md` | Known constraints that future agents should not rediscover repeatedly. |
| `docs/phase_logs/` | Completed phase handoff archive and concise phase summary. |
| `reviews/` | Independent review artifacts (Matcha, Cola, Beer disagreement-loop responses). Governed by `reviews/REVIEW_FORMAT.md`. |
| `PROJECT_CONTEXT.md` | Local-only project snapshot. Must not be sent wholesale to Matcha. Should be treated as local context only. |

---

## 4. Master Rules & Operational Protocol

| Rule # | Name | Description |
| :--- | :--- | :--- |
| Rule 1 | Active Operational Source of Truth | `HANDOFF.md` holds only active work status, task assignments, normalized error fingerprints, blockers, and next actions. Architecture, specifications, risks, decisions, and history belong in dedicated documents. |
| Rule 2 | Failure Cap & Escalation | PE may make at most two consecutive attempts with the same normalized error fingerprint before marking `BLOCKED` and escalating. |
| Rule 3 | Branch Isolation & Authority | All implementation work occurs on feature branches. `main` changes only after PM gate passes, required Matcha findings have recorded dispositions, and Sprite approves the merge. |
| Rule 4 | No Direct Code by Beer | Beer owns architecture and contracts, not production implementation. (Formerly "No Direct Code by PL" — role merged, rule unchanged.) |
| Rule 5 | Session Flushing | Terminal sessions are terminated at the end of each phase to prevent context degradation. |
| Rule 6 | Cola & Beer Workspace Access Boundary | Cola and Beer may read, edit, create, refactor, and run project files through Claude Desktop MCP inside the project workspace. Neither may access credentials, broker endpoints, live trading systems, or unrelated personal files. **This boundary must be verified as an environment-level control (container/sandbox scoping, credential relocation), not merely a stated policy** — see RISK_REGISTER entry for outstanding sandboxing hardening status. |
| Rule 7 | Strict PIT Compliance | No raw future lookups are allowed in feature matrices, labels, validation logic, or backtests. |
| Rule 8 | Context & Reproducibility | Every experiment must record commit hash, config version, random seeds, data snapshot/version, model version, dependency state, and execution timestamp. |
| Rule 9 | Evidence-Based Matcha Review | Matcha receives only redacted, task-specific evidence packets. No credentials, secrets, proprietary raw data, or unrestricted full-project context. |
| Rule 10 | Review Immutability & Disposition Ownership | Matcha findings, once filed, are immutable. Beer may author a response (§5.5) but never edits or marks a finding resolved. Disposition status (Accepted/Deferred/Closed) is recorded by PM and decided by Sprite only — never by Beer. Filed reviews live in `reviews/` per `REVIEW_FORMAT.md` and must not be silently overwritten. |
| Rule 11 | Research-Only Safety Boundary | Until Sprite approves a separately documented live-trading readiness decision, no agent, MCP tool, script, or environment may access broker credentials, submit orders, alter order limits, or connect to a live trading endpoint. |
| Rule 12 | Critical-Fault Exception | Architecture is normally frozen within a phase. Potential PIT leakage, invalid labels, data corruption, credential exposure, loss of reproducibility, or live-trading behavior bypasses the freeze and blocks the phase until Sprite and Beer formally resolve it. |
| Rule 13 | Disposition Separation (Condition 1) | Beer authors proposals and disagreement-loop responses but never owns finding disposition. PM records status; Sprite alone marks a finding Accepted, Deferred, or Closed. |
| Rule 14 | Bounded Disagreement Loop (Condition 2) | Disputes between Beer and Matcha follow a fixed sequence — see §5.5 — to prevent both silence and unbounded repeated debate from deciding the outcome. |
| Rule 15 | Model-Diversity Framing (Condition 3) | Cola is never described as an independent tiebreaker between Beer and Matcha. Beer and Cola share a model family and may share blind spots; genuine independence comes from Matcha (different model) and deterministic tests, not from a second Claude-based opinion. |
| Rule 16 | PE Block Authority (Condition 4) | PE may raise an ADP and halt implementation when a specification is contradictory, unsafe, or infeasible. "Implementation only" scope does not obligate PE to implement a known defect. |
| Rule 17 | Risk-Tiered Mandatory Review (Condition 5) | Matcha review is mandatory before any material-risk item may be marked Resolved — see §5.6 for the risk category list. Routine prose or low-risk maintenance changes do not require it. |

---

## 5. Governance

### 5.1 Decision Authority Matrix

| Decision Type | Final Authority |
| :--- | :--- |
| Business objective | Sprite |
| Project scope | Sprite |
| System architecture | Beer, unless material scope/risk changes require Sprite |
| Architecture Drift Proposal | Beer or Sprite depending on impact |
| Implementation details | PE |
| Complex refactor strategy | Cola, with Sprite approval if high impact |
| Mathematical correctness (implementation-level) | Cola |
| Mathematical/architectural correctness (material-risk, §5.6) | Matcha independent review required; Sprite decides |
| Backtesting risk / PIT leakage concerns | Matcha advises, Sprite decides |
| Finding disposition (Accepted/Deferred/Closed) | Sprite only — never Beer (Rule 13) |
| Test acceptance | PM via deterministic gate |
| Merge to `main` | Sprite |
| Live trading readiness | Sprite only |

### 5.2 Escalation Matrix

| Problem Type | Escalation Target |
| :--- | :--- |
| Syntax, import, typing, or ordinary unit-test failure | PE |
| Repeated identical failure fingerprint | Cola |
| Complex refactor | Cola |
| Mathematical/algorithmic uncertainty (implementation-level) | Cola |
| Material-risk mathematical or architectural uncertainty (§5.6) | Matcha (mandatory), not Cola alone |
| Library limitation requiring architecture change | Beer |
| Backtesting leakage or strategy-risk concern | Matcha |
| Contradictory, unsafe, or infeasible specification | PE raises ADP and blocks (Rule 16) |
| Conflicting agent recommendations | Sprite |
| Business objective conflict | Sprite |
| Credential, broker, or live-trading concern | Sprite |

### 5.3 Decision Deadlock Rule

If PE, Cola, and Matcha offer incompatible recommendations and an objective test cannot resolve the disagreement, Sprite is the binding decision authority.

The chosen outcome and supporting evidence must be recorded in either:

- an ADR, if it changes architecture;
- the risk register, if it accepts or mitigates risk;
- the phase summary, if it is local to the phase.

### 5.4 Confidence Levels

All architectural, technical, or risk recommendations from agents must include:

```text
Confidence: High | Medium | Low
Evidence Basis: Verified | Inference | Hypothesis
Reason:
```

Examples:

```text
Confidence: High
Evidence Basis: Verified from pytest and supplied diff
Reason: The failing test reproduces the PIT leakage under a minimal fixture.
```

```text
Confidence: Medium
Evidence Basis: Inference from supplied architecture
Reason: The design appears vulnerable to survivorship bias, but the dataset construction code was not included.
```

```text
Confidence: Low
Evidence Basis: Hypothesis requiring experiment
Reason: The claim depends on model behavior that has not yet been benchmarked.
```

### 5.5 Disagreement Loop Protocol (Condition 2)

When Matcha files a finding against a Beer-authored artifact and Beer disputes it, the exchange follows a **fixed, bounded sequence**:

```text
Matcha finding
  -> Beer technical response with evidence (one reply)
  -> Matcha final reply (one reply)
  -> Sprite decision
```

**Rules governing this loop:**

1. **No re-litigation.** Beer gets exactly one response per finding. Matcha gets exactly one final reply. Neither side may re-open the exchange to argue further — if either believes the other's reply introduced a genuinely new point requiring rebuttal, that goes to Sprite as an open question, not as another loop iteration.
2. **Silence is not resolution.** If Beer does not respond within the disposition window, the finding stands unmodified for Sprite's decision — it is not treated as tacit agreement or automatically closed.
3. **Sprite's decision is final** and must be recorded in the finding's Disposition table per `REVIEW_FORMAT.md`.
4. This loop exists in part to prevent an asymmetry where the role with more context and more turns (historically, PL/Beer) can simply out-argue a reviewer by volume rather than by evidence.

#### 5.5.1 Cola Is Not an Independent Tiebreaker (Condition 3)

Cola must never be invoked or described as a tiebreaker between Beer and Matcha. Beer and Cola are both Claude-family reasoners sharing the same underlying training and potential blind spots — a second Claude opinion is not model-independent verification, even though it remains useful as a fresh-context specialist. Genuine independence in this project comes from two sources only: **Matcha** (different model family) and **deterministic tests** (objective, reproducible evidence). Cola's role is specialist debugging and refactor depth, invoked by Sprite or by escalation rules — not as a check on Beer's architecture.

### 5.6 Risk-Tiered Mandatory Review (Condition 5)

Matcha review is **mandatory** before any item in the following categories may be marked Resolved, Accepted, or Closed:

- Data source and licence decisions
- PIT / data contracts (timestamp semantics, adjustment logic, corporate-action handling)
- Prediction targets and label definitions
- Feature availability and known-future-input encoding
- Backtest and execution rules (cost models, slippage, benchmark comparison)
- Transaction cost assumptions
- Model-selection changes (architecture, loss function, output heads)
- Major refactors touching more than one subsystem

Routine prose edits, documentation formatting, and low-risk maintenance changes are exempt from mandatory review to avoid creating an unnecessary bottleneck — PM uses judgment on borderline cases and may escalate to Sprite if uncertain whether an item qualifies.

#### 5.6.1 Documentation Integrity Preflight (PM)

Before any phase gate or disposition is finalized, PM verifies:

- Canonical documents referenced in `HANDOFF.md` and disposition records actually exist and are non-empty.
- Each canonical document carries a version/status header.
- File paths referenced in disposition matrices match actual file locations.
- No duplicate/conflicting sources of truth exist for the same content (e.g., a blueprint duplicated across two files).

This requirement exists because `docs/ARCHITECTURE.md` was found empty (0 bytes) on 2026-07-23 despite an earlier disposition matrix claiming it was populated — the claim and the filesystem state had silently diverged. See `reviews/REVIEW_FORMAT.md` Rule 6 for the equivalent same-session-filing requirement for reviews.

### 5.7 PE Block Authority (Condition 4)

PE's "implementation only" scope (§2) does not mean PE must implement a specification known to be contradictory, unsafe, or infeasible. When PE identifies such a defect:

1. PE raises an ADP in `HANDOFF.md` describing the contradiction/hazard, rather than proceeding.
2. Implementation of the affected task is blocked pending resolution.
3. Resolution follows the standard ADP lifecycle (§7) — Beer or Sprite adjudicates depending on impact.

This is distinct from PE silently redesigning architecture — PE identifies and blocks, it does not unilaterally resolve.

---

## 6. HANDOFF.md Template

```markdown
# Sensilnet ATPE - Active Phase Handoff Board

## Project Phase
[Example: Phase 1 - Ingestion & PIT Data Infrastructure]

## Active Branch
feature/phase-1-ingestion

## Current Status
IN_PROGRESS

---

## Phase Tasks Checklist

- [x] Beer: Generate system architecture document
- [x] PM: Initialize repository structure and test scaffolding
- [ ] PE: Implement PIT data fetcher
- [ ] PE: Write unit tests and pass local test target
- [ ] PM: Run candidate gate
- [ ] Matcha: Conduct mandatory review if item falls under §5.6 risk tiers
- [ ] Sprite: Record disposition and approve merge

---

## Immediate Action Item for Next Agent

Target Agent: PE

Instruction:
Create `src/core/ingestion/sgx_feed.py` following the schema in `docs/ARCHITECTURE.md`.
Run the required unit test target.
If two consecutive failures share the same normalized error fingerprint, mark `BLOCKED` and escalate.
If the specification itself is contradictory, unsafe, or infeasible, raise an ADP and block instead (Rule 16).

---

## Error Fingerprints

### Fingerprint 1
Status: OPEN
Failing Test IDs:
Exception Type:
Relevant Stack Frame:
Attempt Count:
Pass Count Change:
Notes:

---

## Architecture Drift Proposals

### ADP-001
Status: OPEN
Phase:
Raised By:
Problem:
Proposed Change:
Impact:
Risk:
Decision Needed From: Beer / Sprite
Decision:
Evidence:

---

## Blocking Issues / Escalations

Status: GREEN

Escalation Notes:
N/A
```

---

## 7. Architecture Drift Proposal Process

Architecture is frozen during a phase unless an approved ADP or critical-fault exception applies.

### ADP Lifecycle

```text
OPEN -> APPROVED -> IMPLEMENTED -> ARCHIVED_AS_ADR
     -> REJECTED
     -> DEFERRED
```

### Rules

- PE or PM may raise an ADP in `HANDOFF.md`.
- Beer approves ordinary architecture changes.
- Sprite approves material scope, cost, risk, or live-readiness changes.
- PM converts only approved and implemented ADPs into ADRs.
- Rejected ADPs remain in the archived phase handoff but do not become ADRs.
- Deferred ADPs must include owner, rationale, and target phase.

### ADR Template

```markdown
# ADR-XXX: [Decision Title]

## Status
Accepted / Superseded / Deprecated

## Date
YYYY-MM-DD

## Context
What problem forced this decision?

## Decision
What did we decide?

## Alternatives Considered
What else was considered?

## Consequences
Benefits, trade-offs, risks, and future maintenance impact.

## Evidence
Tests, logs, documentation, experiments, or review notes supporting the decision.

## Approved By
Beer / Sprite
```

---

## 8. Phase Gatekeeper

PM acts as a deterministic verifier, not as a second manual coding agent.

### 8.1 Candidate Gate

Run before commit.

```text
ruff
black --check
mypy
pytest
coverage threshold
pip check
git diff --check
secret/unintended-file scan
```

The candidate gate does not require a clean worktree because valid uncommitted changes are expected before commit.

### 8.2 Release Gate

Run after commit and before merge.

```text
candidate checks pass against committed SHA
working tree is clean
branch is based on expected target
commit hash is recorded
phase documentation is updated
approved ADPs are resolved
Matcha findings have dispositions (mandatory for §5.6 risk-tier items)
documentation integrity preflight passed (§5.6.1)
```

### 8.3 Debug Marker Policy

Do not categorically ban every `TODO`, `FIXME`, or `print()`.

Reject:

- accidental debug prints;
- untracked temporary files;
- commented-out experimental code;
- TODO/FIXME markers with no owner or reference.

Allow:

- intentional technical-debt markers linked to an ADR, issue, phase note, or risk-register entry.

---

## 9. Phase Execution Lifecycle

1. Beer creates or updates architecture and specification contracts (draft specs land in `docs/specs/` first, per §3).
2. PM creates a feature branch and initializes `HANDOFF.md`.
3. PE implements the task, writes tests, and runs local test targets. PE may block via ADP if the spec is defective (Rule 16).
4. If PE hits two identical error fingerprints or cycles without increasing pass count, PE marks `BLOCKED`.
5. Cola investigates escalated technical failures using full project workspace access, as a specialist — not as a check on Beer's architecture (§5.5.1).
6. Beer or Sprite resolves any ADP.
7. PM runs the candidate gate and prepares the commit.
8. PM runs the release gate after commit.
9. Sprite prepares a redacted Matcha evidence packet for any item touching §5.6 risk tiers (mandatory) or on request.
10. Matcha performs manual red-team review; findings are immutable once filed.
11. If Beer disputes a finding, the bounded disagreement loop (§5.5) runs.
12. PM records dispositions for Matcha findings — Sprite decides, PM records, Beer never fills this field.
13. Sprite approves or rejects merge to `main`.
14. PM archives `HANDOFF.md` to `docs/phase_logs/phase_N_handoff.md`.
15. PM writes `docs/phase_logs/phase_N_summary.md`.
16. Sprite flushes active LLM sessions before the next phase.

---

## 10. Phase Summary Format

Each phase summary must be concise and limited to three sections.

```markdown
# Phase N Summary

## Key Accomplishments

## Technical Debt / Trade-offs Incurred

## Lessons Learned for Next Phase
```

The phase summary should not merely duplicate the final handoff. If it contains no analysis, it should be shortened.

---

## 11. Matcha Review Protocol

Matcha is the project's **primary independent checker** (§2, §5.6) and red-team reviewer — not a routine implementation agent and not the final approval authority.

### 11.1 What Matcha Reviews

Matcha should focus on:

- PIT leakage;
- survivorship bias;
- label leakage;
- backtest validity;
- corporate actions;
- exchange-calendar assumptions;
- slippage and transaction-cost realism;
- overfitting risk;
- misleading metrics;
- fragile model assumptions;
- hidden data dependency;
- strategy robustness;
- failure modes under stressed markets;
- structural weaknesses in the team/process design itself (e.g., self-certification risk, escalation-authority conflicts).

Review is **mandatory**, not optional, for any item in the §5.6 risk-tier list before it may be marked Resolved.

### 11.2 What Matcha Must Not Receive

Do not send Matcha:

- credentials;
- API keys;
- broker details;
- personal data;
- proprietary raw datasets;
- unrestricted project archives;
- full unredacted `PROJECT_CONTEXT.md`;
- `.env` files;
- live trading configuration.

### 11.3 Matcha Evidence Packet Template

```markdown
# Matcha Review Request

## Request Metadata
Project:
Phase:
Branch:
Commit Hash:
Prepared By:
Date:

## Review Question
What specifically should Matcha challenge?

## Scope
What files, modules, or assumptions are in scope?

## Out of Scope
What should not be reviewed?

## Relevant Architecture / Specification Excerpts

## Relevant Diff Summary

## Test Evidence

## Backtest / PIT Evidence

## Reproducibility Evidence
- Configuration identifier and hash:
- Random seed(s):
- Dataset snapshot/version and retrieval time:
- Dependency lockfile/environment identifier:
- Exact command(s) executed:
- Test/backtest output summary:

## Known Concerns

## Evidence Boundary
Confirm that this request contains no credentials, personal data, proprietary raw data, or unredacted full-project context.
```

### 11.4 Matcha Response Requirements

Each Matcha finding should include:

```text
Finding:
Severity: Critical | High | Medium | Low
Confidence: High | Medium | Low
Evidence Basis: Verified | Inference | Hypothesis
Reason:
Recommendation:
```

A confidence label without evidence is not sufficient. All findings are filed in `reviews/` per `REVIEW_FORMAT.md` **within the same working session as the review** (see `REVIEW_FORMAT.md` Rule 6) — not deferred to later cleanup. A review that exists only in a chat transcript is not yet a review.

---

## 12. Cola Operating Protocol

Cola is allowed full access inside the Sensilnet ATPE project workspace, functioning as a **fresh-context specialist**, not a standing gate and not an independent tiebreaker (§5.5.1, Rule 15).

This includes permission to:

- read project files;
- inspect diffs;
- edit project files;
- create new files inside the project;
- run tests;
- run linting;
- run scripts;
- perform refactors;
- investigate stack traces;
- update documentation when assigned.

Cola must not:

- access `.env` secrets unless Sprite explicitly provides approval for a specific purpose;
- access broker credentials;
- connect to live trading endpoints;
- submit orders;
- modify personal files outside the project workspace;
- make irreversible destructive changes without Sprite approval;
- merge to `main`;
- approve its own work as final;
- **be invoked or cited as an independent check on Beer's architecture** — that role belongs to Matcha (§5.5.1).

When Cola writes or modifies code, PM or PE must still run the deterministic gate afterward.

When Cola proposes an architecture change, Beer or Sprite must approve it through the ADP process.

**Environment boundary note:** As of 2026-07-24, credential relocation (removal of a PAT file previously reachable via parent-directory traversal) has been completed, and sudo access from Cola/Beer sessions requires a password neither role can supply. Full container/namespace-level sandboxing (Docker or bubblewrap scoping the MCP server to the workspace root) remains an open hardening item — see `docs/RISK_REGISTER.md` — and must be completed before any broker or live-trading credentials are introduced to this environment (Rule 11).

---

## 13. Reproducibility Requirements

Every meaningful experiment, model training run, feature-generation run, or backtest must record:

```text
Git commit hash
Branch name
Configuration identifier
Configuration hash
Random seed(s)
Dataset snapshot/version
Data retrieval timestamp
Model version
Dependency lockfile or environment identifier
Execution timestamp
Exact command
Output artifact path
Summary metrics
Known caveats
```

Any result that cannot be reproduced should be treated as exploratory only and must not support a major architecture or trading decision.

---

## 14. Risk Register

`docs/RISK_REGISTER.md` should track persistent risks.

Example format:

```markdown
# Risk Register

## RISK-001: Point-In-Time Leakage

Status: Open
Severity: Critical
Owner: Beer
First Identified: YYYY-MM-DD
Last Reviewed: YYYY-MM-DD

### Description

### Current Mitigation

### Evidence

### Next Review
```

Recommended standing risks:

- PIT leakage;
- survivorship bias;
- corporate-action handling;
- exchange-calendar mismatch;
- stale or revised data;
- label leakage;
- overfitting;
- unrealistic slippage;
- transaction-cost underestimation;
- reproducibility failure;
- dependency instability;
- credential exposure;
- accidental live-trading access;
- **incomplete environment sandboxing (Cola/Beer MCP access broader than workspace-scoped — open as of 2026-07-24).**

---

## 15. Known Limitations

`docs/KNOWN_LIMITATIONS.md` should preserve accepted limitations so future agents do not rediscover the same constraints.

Example:

```markdown
# Known Limitations

## LIMIT-001: Daily Timeframe Only

Status: Accepted
Reason:
The current engine is designed for daily batch research and not intraday execution.

Impact:
Intraday signals, order-book dynamics, and real-time latency are out of scope.

Mitigation:
Revisit only after daily system is stable and reproducible.
```

---

## 16. Final Role Boundary

```text
Claude Beer:
Merged Project Leader + Chief Architect. Architecture, specifications, contracts,
ordinary ADP approval, disagreement-loop responses. Writes zero production code.
Never owns finding disposition.

Gemini PM:
Task board, deterministic gates, phase archives, ADR conversion, branch hygiene,
finding disposition recording, documentation integrity preflight.

Gemini PE:
Routine implementation, tests, local debugging, initial fixes, and ADP-raising
block authority against contradictory/unsafe/infeasible specifications.

Claude Cola:
Full-access fresh-context specialist for hard debugging, refactoring, math
validation, and escalation support. Not an independent tiebreaker.

ChatGPT Matcha:
Primary independent checker. Mandatory reviewer for all material-risk changes.
Manual red-team reviewer using redacted evidence packets only. Findings immutable
once filed. Advisory authority — Sprite decides.

Sprite:
Final decision authority, merge approval, credential control, live-trading
authority, and sole owner of finding disposition.
```

The operational philosophy is:

> Use Gemini for throughput, Claude (Beer) for architecture depth, Claude (Cola) for specialist technical depth, ChatGPT (Matcha) for genuine independent challenge, deterministic tools for evidence, and Sprite for judgment.

---

## Changelog

- **v2.0 (2026-07-24):** Merged PL role into Beer (Claude, Project Leader + Chief Architect). Demoted Cola from standing architecture gate to reserve specialist (Rule 15, §5.5.1). Promoted Matcha to primary independent checker with mandatory review for material-risk categories (§5.6, Rule 17). Added bounded disagreement loop (§5.5, Rule 14). Added disposition-ownership separation (§5.4/§5.6, Rule 13) following the empty-`ARCHITECTURE.md` incident. Added PE block authority (§5.7, Rule 16). Added documentation-integrity preflight (§5.6.1). Updated `reviews/` to flat same-session-filing convention per `REVIEW_FORMAT.md`. Added environment-boundary status note to Cola protocol (§12) following credential-relocation and sudo-lockdown verification.
- **v1.6:** Prior version — see git history. Hardened original three-Gemini-role design with explicit non-independence caveat and deterministic-evidence philosophy.
