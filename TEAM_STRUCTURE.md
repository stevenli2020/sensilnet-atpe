# Team Structure & Operational Blueprint: Sensilnet ATPE

Project Name: Sensilnet ATPE (Automated Trading & Prediction Engine)
Target Architecture: Multi-Modal Daily Batch Trading & Prediction Engine for SGX Equities
Environment: WSL Ubuntu Terminal / Python venv / Gemini CLI / Claude Desktop + MCP
Document Status: FROZEN (Version 1.0)

---

## 1. Executive Summary & Philosophy

To maximize accuracy, efficiency, and cost sustainability, project Sensilnet ATPE operates on a Flattened Multi-Agent Architecture. Rather than spawning individual persona instances for every phase, the system reuses 3 core Gemini Gem templates (PL, PM, PE) alongside specialized external agents (Claude and ChatGPT).

All 3 Gemini roles are implemented using a shared Gemini model with different system prompts and operational scopes. All state and communications between agents are stored in the local file system (HANDOFF.md, docs/ARCHITECTURE.md, and docs/decision_log/), allowing LLM chat sessions to be flushed cleanly between phases without loss of historical context.

---

## 2. Team Composition & Role Definitions

| Role | Agent / Platform | Primary Responsibility | Work Environment |
| :--- | :--- | :--- | :--- |
| Sprite | Project Owner (Human) | Final approvals, managing API credentials, running top-level orchestration scripts, deadlock resolution, and bridging Matcha/Cola when needed. | WSL Terminal / Browser |
| PL | Project Leader (Gemini Gem) | Context ingestion, maintaining docs/ARCHITECTURE.md, setting phase milestones, library architectural limitations, and defining task contracts. Writes zero code. | Gemini CLI / Web UI |
| PM | Project Manager (Gemini Gem Template) | Task decomposition inside HANDOFF.md, tracking daily progress, executing phase_gatekeeper.sh, archiving handoffs, and managing Git branches. | Gemini CLI (WSL Workspace) |
| PE | Primary Coding Engineer (Gemini Gem Template) | Writes ~90% of production Python code, builds features/models, resolves syntax/typing errors, writes unit tests, and executes scripts locally. | Gemini CLI in WSL (gemini -p) |
| Cola | Secondary Engineer (Claude Desktop + Local MCP) | Complex refactoring, deep technical architecture, mathematical logic validation, and resolving code blocks when PE hits an identical error failure cap. | Claude Desktop App (Windows / WSL bridge) |
| Matcha | Technology Advisor (ChatGPT Web UI) | Independent "Red Team" auditor, backtesting logic stress-testing, risk analysis, and edge-case detection. | ChatGPT Web UI (Isolated Sandbox) |

---

## 3. Directory Layout & File Communications

sensilnet-atpe/
├── .gemini/                    # Gemini CLI configuration & system prompts
├── docs/
│   ├── ARCHITECTURE.md          # Maintained by PL: Master system design & module contracts
│   ├── SPECIFICATIONS.md        # Feature schemas & math definitions
│   ├── RISK_REGISTER.md         # Financial, data, & backtesting risk tracking
│   ├── KNOWN_LIMITATIONS.md     # Preserved constraints & evaluated non-solutions
│   ├── decision_log/            # Permanent Architecture Decision Records (ADR-001.md, etc.)
│   └── phase_logs/              # PM's archived handoffs & narrative phase summaries
├── scripts/
│   └── phase_gatekeeper.sh      # Automated quality gate script
├── HANDOFF.md                   # SINGLE SOURCE OF TRUTH (Active Task Board)
├── TEAM_STRUCTURE.md            # THIS FILE: Master Operational Blueprint
├── mcp_server.py                # Local MCP server for Claude Desktop (Cola)
├── logs/                        # Verification and execution test outputs
│   └── test_runner.log
├── src/                         # Production Python Code
│   ├── core/                    # Ingestion & Point-In-Time (PIT) data handlers
│   ├── features/                # Technical indicators, SHAP selection
│   ├── models/                  # PyTorch Lightning TFT implementation
│   └── backtest/                # Strategy backtesting engine
└── tests/                       # Pytest unit & integration test suite

---

## 4. Master Rules & Governance

### Master Rules

| Rule # | Name | Description |
| :--- | :--- | :--- |
| Rule 1 | Single Source of Truth | All active work status, task assignments, and stack traces MUST be recorded in HANDOFF.md. No implicit memory between sessions. |
| Rule 2 | Failure Cap & Error Signatures | PE is escalated after 2 consecutive identical error signatures OR if PE cycles ("ping-pongs") between previously seen signatures without increasing test pass counts. Counter resets only on new error signatures accompanied by test progress. |
| Rule 3 | Branch Isolation | All work occurs on feature/phase-N branches. main is modified only after PM & Matcha pass final sign-off. |
| Rule 4 | No Direct Code by PL | PL focuses strictly on system architecture, specification schemas, and task decomposition. |
| Rule 5 | Session Flushing | Terminal sessions are terminated at the end of each phase to prevent LLM context windows from degrading. |
| Rule 6 | Manual Sandbox Boundary | Matcha (ChatGPT) is never connected to local CLI. Data flows to Matcha strictly via manual paste by Sprite. |
| Rule 7 | Strict PIT Compliance | Point-In-Time alignment: No raw future lookups allowed in feature matrices during backtesting. |
| Rule 8 | Architecture Freeze & Exceptions | System architecture is frozen during execution. Freeze can ONLY be bypassed for Critical Issues (security, data corruption, PIT leakage, incorrect labels, or loss of reproducibility). |
| Rule 9 | Reproducibility Metadata | Every model/backtest run must log: Git commit hash, Config version, Random seed(s), Dataset version/date, Model version, and Execution timestamp. |

### Decision Authority Matrix

| Decision Category | Final Authority |
| :--- | :--- |
| Business & Financial Objectives | Sprite |
| System Architecture & Contracts | PL (after technical review) |
| Implementation & Code Fixes | PE |
| Gatekeeper & Branch Acceptance | PM |
| Mathematical & Algorithmic Correctness | Cola |
| Strategy Risk & Red Team Audit | Matcha |
| Main Branch Merge | Sprite |

### Escalation Routing Matrix

| Problem / Issue Class | Primary Responsible Owner | Secondary Escalation |
| :--- | :--- | :--- |
| Syntax, typing, import, or local unit test errors | PE | Self-fix (Max 2 attempts) |
| Library limitation requiring architectural change | PL | Cola |
| Advanced math, algorithm optimization, deep refactor | Cola | Sprite |
| Backtesting leakage, survivorship bias, risk audit | Matcha | Sprite |
| Conflicting recommendations / Unresolved Deadlock | Sprite (Final Authority) | N/A |

---

## 5. Architecture Drift Proposals (ADP) & ADR Lifecycle

When PE or PM encounters a practical wall that requires deviating from ARCHITECTURE.md, the following lifecycle MUST be followed:

1. Log Proposal: PE logs an Architecture Drift Proposal (ADP) in HANDOFF.md with ID, Problem, Impact, and Proposed Solution.
2. Review & State: PL and Sprite review the proposal:
   - OPEN -> APPROVED -> IMPLEMENTED -> ARCHIVED (Converted to ADR)
   - OPEN -> REJECTED
3. ADR Conversion: Upon phase completion, PM converts all APPROVED ADPs into permanent, numbered files in docs/decision_log/ADR-xxx.md. ARCHITECTURE.md is updated accordingly.

---

## 6. Confidence Level & Evidence Reporting Standard

Whenever PL, PM, PE, Cola, or Matcha provides architectural or technical recommendations, the output MUST include explicit confidence ratings backed by evidence:

Example Format:
- Recommendation: Use PyTorch Lightning Temporal Fusion Transformer for multi-horizon forecast.
- Confidence: High
- Evidence: Verified experimentally in prototype tests / Documented in PyTorch Lightning official API specs.

Confidence Levels:
- High: Verified experimentally via code/test execution.
- Medium: Reasoned from official documentation; not yet experimentally verified.
- Low: Theoretical hypothesis or intuition only.

---

## 7. Active Task Board Template (HANDOFF.md)

When initializing or updating HANDOFF.md, PM and PE must maintain the following layout:

# Sensilnet ATPE - Active Phase Handoff Board

## Project Phase: [e.g., Phase 1 - Ingestion & PIT Data Infrastructure]
## Active Branch: feature/phase-1-ingestion
## Current Status: IN_PROGRESS
## Version Contract: Architecture v1.0 | Spec v1.0 | Handoff v1.0

---

### Phase Tasks Checklist
- [x] PL: Generate System Architecture Document (docs/ARCHITECTURE.md)
- [x] PM: Initialize repository structure and test suite scaffolding
- [ ] PE: Implement PIT Data Fetcher (src/core/ingestion/sgx_feed.py)
- [ ] PE: Write unit test (tests/test_sgx_feed.py) and pass pytest
- [ ] PM: Execute scripts/phase_gatekeeper.sh and merge branch to main
- [ ] Sprite/Matcha: Conduct Phase 1 Red Team Audit

---

### Immediate Action Item for Next Agent:
Target Agent: PE  
Instruction: Create src/core/ingestion/sgx_feed.py following the schema in docs/ARCHITECTURE.md. Run verification command pytest tests/test_sgx_feed.py.

---

### Architecture Drift Proposals (ADP):
- ADP ID: ADP-001 (Status: OPEN)
  - Problem: yfinance API missing corporate action split-adjustment flag.
  - Impact: Data ingestion pipeline.
  - Proposed Fix: Use custom adjustment parser in src/core/ingestion/adjustments.py.

---

### Failure & Error Signature Tracking:
- Current Attempt: 1
- Last Error Signature: NONE
- Escalation Status: GREEN

---

## 8. Definition of Done (DoD) & Phase Execution Lifecycle

### Definition of Done (DoD) for Phases
A project phase is formally COMPLETE only when all of the following criteria are met:
1. All planned tasks in HANDOFF.md are complete or explicitly deferred by Sprite.
2. The automated quality script scripts/phase_gatekeeper.sh passes 100% clean (Ruff, Black, Mypy, Pytest, Coverage, Pip Check, Git Diff Clean, No TODO/FIXME/print statements).
3. Documentation (ARCHITECTURE.md, SPECIFICATIONS.md, KNOWN_LIMITATIONS.md) reflects the implementation.
4. All approved ADPs are converted into permanent ADR files in docs/decision_log/.
5. Active HANDOFF.md is archived to docs/phase_logs/phase_N_handoff.md.
6. PM generates a narrative summary docs/phase_logs/phase_N_summary.md (Key Accomplishments, Tech Debt Incurred, Lessons Learned).
7. Sprite approves the phase and merges the feature branch to main.

### Phase Lifecycle Steps
1. Phase Initialization: PL breaks down the project proposal into specifications in docs/ARCHITECTURE.md.
2. Task Posting: PM creates a feature/phase-X branch and populates HANDOFF.md with tasks.
3. Execution & Testing: PE opens a Gemini CLI session, reads HANDOFF.md, writes code, and runs local tests.
4. Escalation (If Needed): On 2 identical error signatures or ping-pong debugging, PE sets status BLOCKED. Sprite routes the issue via the Escalation Matrix (e.g., to Cola or Matcha).
5. Gatekeeping & Audit: PM executes scripts/phase_gatekeeper.sh. Sprite shares the narrative summary with Matcha (ChatGPT) for Red Team audit.
6. Session Reset: Sprite approves merge to main, terminates the Gemini CLI session, converts ADPs to ADRs, archives handoff files, and launches a clean CLI session for Phase X+1.
