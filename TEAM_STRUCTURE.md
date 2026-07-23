# Team Structure & Operational Blueprint: Sensilnet ATPE

Document Version: 1.6  
Project Name: Sensilnet ATPE  
Full Name: Automated Trading & Prediction Engine  
Target Architecture: Multi-Modal Daily Batch Trading & Prediction Engine for SGX Equities  
Environment: WSL Ubuntu Terminal / Python venv / Gemini CLI / Claude Desktop + MCP / ChatGPT Web UI  

---

## 1. Executive Summary & Philosophy

Sensilnet ATPE operates on a flattened multi-agent architecture designed for a solo developer coordinating several AI assistants through explicit local artifacts rather than relying on chat memory.

The system uses three Gemini operational roles, one Claude-based technical escalation role, and one ChatGPT-based independent review role.

All three Gemini roles use a shared underlying model with different system prompts and operational scopes. They improve workflow discipline, but they are not independent validation authorities and may share the same blind spots. Independent checks must come from deterministic gates, evidence, external model review, and final human judgment.

All state and communications between agents are stored in version-controlled local artifacts such as `HANDOFF.md`, `docs/ARCHITECTURE.md`, `docs/SPECIFICATIONS.md`, `docs/decision_log/`, `docs/phase_logs/`, and `reviews/`.

The guiding principle is:

> LLMs may plan, implement, review, and challenge, but deterministic evidence and Sprite control acceptance.

---

## 2. Team Composition & Role Definitions

| Role | Agent / Platform | Primary Responsibility | Work Environment |
| :--- | :--- | :--- | :--- |
| Sprite | Project Owner / Human | Final approvals, business objectives, API credentials, merge approval, live-trading readiness decisions, and conflict resolution. | WSL Terminal / Browser |
| PL | Project Leader / Gemini Gem | Owns architecture vision, maintains `docs/ARCHITECTURE.md`, approves ordinary Architecture Drift Proposals, defines phase milestones and module contracts. Writes zero production code. | Gemini CLI / Web UI |
| PM | Project Manager / Gemini Gem | Maintains `HANDOFF.md`, decomposes tasks, manages branches, executes deterministic phase gates, archives phase artifacts, converts approved ADPs into ADRs. | Gemini CLI in WSL |
| PE | Primary Coding Engineer / Gemini Gem | Writes most production Python code, implements features, writes tests, runs local unit tests, and escalates when failure rules trigger. | Gemini CLI in WSL |
| Cola | Secondary Engineer / Claude Desktop + Local MCP | Full-access senior technical engineer inside the project workspace: complex refactoring, difficult debugging, math validation, architecture stress testing, test-gap analysis, and rescue work when PE reaches escalation criteria. | Claude Desktop App with Local MCP |
| Matcha | Technology Advisor / ChatGPT Web UI | Independent red-team auditor: backtesting logic stress tests, PIT leakage review, strategy risk analysis, edge-case detection, and challenge of weak assumptions. Receives only manual redacted evidence packets. | ChatGPT Web UI / Isolated Manual Review |

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
|   |-- decision_log/
|   |   |-- ADR-001.md
|   |   `-- ADR-002.md
|   `-- phase_logs/
|       |-- phase_1_handoff.md
|       `-- phase_1_summary.md
|-- reviews/
|   |-- inbox/
|   |-- active/
|   |-- completed/
|   `-- rejected/
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

### File Responsibilities

| File / Folder | Purpose |
| :--- | :--- |
| `HANDOFF.md` | Active operational task board only. Current phase, branch, task assignments, blockers, error fingerprints, next action. |
| `docs/ARCHITECTURE.md` | Master architecture, module boundaries, data flow, major system contracts. |
| `docs/SPECIFICATIONS.md` | Feature schemas, math definitions, data contracts, model assumptions. |
| `docs/decision_log/` | Permanent Architecture Decision Records. |
| `docs/RISK_REGISTER.md` | Persistent project risks, mitigations, owners, and review dates. |
| `docs/KNOWN_LIMITATIONS.md` | Known constraints that future agents should not rediscover repeatedly. |
| `docs/phase_logs/` | Completed phase handoff archive and concise phase summary. |
| `reviews/` | Manual review packets and responses for Matcha. |
| `PROJECT_CONTEXT.md` | Local-only project snapshot. Must not be sent wholesale to Matcha. Should be treated as local context only. |

---

## 4. Master Rules & Operational Protocol

| Rule # | Name | Description |
| :--- | :--- | :--- |
| Rule 1 | Active Operational Source of Truth | `HANDOFF.md` holds only active work status, task assignments, normalized error fingerprints, blockers, and next actions. Architecture, specifications, risks, decisions, and history belong in dedicated documents. |
| Rule 2 | Failure Cap & Escalation | PE may make at most two consecutive attempts with the same normalized error fingerprint before marking `BLOCKED` and escalating. |
| Rule 3 | Branch Isolation & Authority | All implementation work occurs on feature branches. `main` changes only after PM gate passes, required Matcha findings have recorded dispositions, and Sprite approves the merge. |
| Rule 4 | No Direct Code by PL | PL owns architecture and contracts, not production implementation. |
| Rule 5 | Session Flushing | Terminal sessions are terminated at the end of each phase to prevent context degradation. |
| Rule 6 | Cola Full Workspace Access | Cola may read, edit, create, refactor, and run project files through Claude Desktop MCP inside the project workspace. Cola must not access credentials, broker endpoints, live trading systems, or unrelated personal files. |
| Rule 7 | Strict PIT Compliance | No raw future lookups are allowed in feature matrices, labels, validation logic, or backtests. |
| Rule 8 | Context & Reproducibility | Every experiment must record commit hash, config version, random seeds, data snapshot/version, model version, dependency state, and execution timestamp. |
| Rule 9 | Evidence-Based Matcha Review | Matcha receives only redacted, task-specific evidence packets. No credentials, secrets, proprietary raw data, or unrestricted full-project context. |
| Rule 10 | Review Immutability | Matcha review responses and PM dispositions are stored in `reviews/completed/` and should not be silently overwritten. |
| Rule 11 | Research-Only Safety Boundary | Until Sprite approves a separately documented live-trading readiness decision, no agent, MCP tool, script, or environment may access broker credentials, submit orders, alter order limits, or connect to a live trading endpoint. |
| Rule 12 | Critical-Fault Exception | Architecture is normally frozen within a phase. Potential PIT leakage, invalid labels, data corruption, credential exposure, loss of reproducibility, or live-trading behavior bypasses the freeze and blocks the phase until Sprite and PL formally resolve it. |

---

## 5. Governance

### 5.1 Decision Authority Matrix

| Decision Type | Final Authority |
| :--- | :--- |
| Business objective | Sprite |
| Project scope | Sprite |
| System architecture | PL, unless material scope/risk changes require Sprite |
| Architecture Drift Proposal | PL or Sprite depending on impact |
| Implementation details | PE |
| Complex refactor strategy | Cola, with Sprite approval if high impact |
| Mathematical correctness | Cola |
| Backtesting risk / PIT leakage concerns | Matcha advises, Sprite decides |
| Test acceptance | PM via deterministic gate |
| Merge to `main` | Sprite |
| Live trading readiness | Sprite only |

### 5.2 Escalation Matrix

| Problem Type | Escalation Target |
| :--- | :--- |
| Syntax, import, typing, or ordinary unit-test failure | PE |
| Repeated identical failure fingerprint | Cola |
| Complex refactor | Cola |
| Mathematical / algorithmic uncertainty | Cola |
| Library limitation requiring architecture change | PL |
| Backtesting leakage or strategy-risk concern | Matcha |
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

- [x] PL: Generate system architecture document
- [x] PM: Initialize repository structure and test scaffolding
- [ ] PE: Implement PIT data fetcher
- [ ] PE: Write unit tests and pass local test target
- [ ] PM: Run candidate gate
- [ ] Sprite/Matcha: Conduct phase red-team audit if required
- [ ] Sprite: Approve merge

---

## Immediate Action Item for Next Agent

Target Agent: PE

Instruction:
Create `src/core/ingestion/sgx_feed.py` following the schema in `docs/ARCHITECTURE.md`.
Run the required unit test target.
If two consecutive failures share the same normalized error fingerprint, mark `BLOCKED` and escalate.

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
Decision Needed From: PL / Sprite  
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
- PL approves ordinary architecture changes.
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
PL / Sprite
```

---

## 8. Phase Gatekeeper

PM acts as a deterministic verifier, not as a second manual coding agent.

### 8.1 Candidate Gate

Run before commit.

The candidate gate should verify:

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

The release gate should verify:

```text
candidate checks pass against committed SHA
working tree is clean
branch is based on expected target
commit hash is recorded
phase documentation is updated
approved ADPs are resolved
Matcha findings have dispositions
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

1. PL creates or updates architecture and specification contracts.
2. PM creates a feature branch and initializes `HANDOFF.md`.
3. PE implements the task, writes tests, and runs local test targets.
4. If PE hits two identical error fingerprints or cycles without increasing pass count, PE marks `BLOCKED`.
5. Cola investigates escalated technical failures using full project workspace access.
6. PL or Sprite resolves any ADP.
7. PM runs the candidate gate and prepares the commit.
8. PM runs the release gate after commit.
9. Sprite prepares a redacted Matcha evidence packet if independent review is required.
10. Matcha performs manual red-team review.
11. PM records dispositions for Matcha findings.
12. Sprite approves or rejects merge to `main`.
13. PM archives `HANDOFF.md` to `docs/phase_logs/phase_N_handoff.md`.
14. PM writes `docs/phase_logs/phase_N_summary.md`.
15. Sprite flushes active LLM sessions before the next phase.

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

Matcha is an independent red-team reviewer, not a routine implementation agent and not the final approval authority.

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
- failure modes under stressed markets.

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

A confidence label without evidence is not sufficient.

---

## 12. Cola Operating Protocol

Cola is allowed full access inside the Sensilnet ATPE project workspace.

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
- approve its own work as final.

When Cola writes or modifies code, PM or PE must still run the deterministic gate afterward.

When Cola proposes an architecture change, PL or Sprite must approve it through the ADP process.

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
Owner: PL  
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
- accidental live-trading access.

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
Gemini PL:
Architecture, specifications, contracts, ordinary ADP approval.

Gemini PM:
Task board, deterministic gates, phase archives, ADR conversion, branch hygiene.

Gemini PE:
Routine implementation, tests, local debugging, initial fixes.

Claude Cola:
Full-access senior engineer inside the workspace for hard debugging, refactoring, math validation, and escalation support.

ChatGPT Matcha:
Manual independent red-team reviewer using redacted evidence packets only.

Sprite:
Final decision authority, merge approval, credential control, live-trading authority.
```

The operational philosophy is:

> Use Gemini for throughput, Claude for difficult technical depth, ChatGPT for independent challenge, deterministic tools for evidence, and Sprite for judgment.
```